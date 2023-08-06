from typing import Optional
from urllib.parse import urljoin

import click
from InquirerPy import inquirer

import bpkio_cli.options as bic_options
from bpkio_cli.click_mods.group_rest_resource import RestResourceGroup
from bpkio_cli.core.app_settings import AppContext
from bpkio_cli.core.wrappers import treat_list_objects, treat_single_object
from bpkio_cli.readers.hls import HlsReader
from bpkio_cli.utils.urls import add_query_parameters
from bpkio_cli.writers.breadcrumbs import display_resource_info
from bpkio_cli.writers.content_display import display_url_content
from bpkio_cli.api.crudeApi import BroadpeakIoCrudeApi

default_fields = ["id", "name", "type", "#serviceId"]


# TODO - move to the API helpers
def _get_list_services(api):
    services = api.list_services()

    for s in services:
        s["#serviceId"] = BroadpeakIoCrudeApi.extract_service_id(s["url"])

    return services


# Group: SERVICES
@click.group(cls=RestResourceGroup)
@click.argument("service_id")
@click.pass_obj
def services(obj, service_id: str):
    """Commands for Service objects"""

    if service_id:
        service = obj.api.get_service(int(service_id))
        display_resource_info(service)


# Command: LIST
@services.command()
@bic_options.list(default_fields=default_fields)
@click.pass_obj
def list(obj, json, select_fields):
    """Retrieves a list of all Services"""

    services = _get_list_services(obj.api)

    treat_list_objects(
        services,
        select_fields=select_fields,
        json=json,
    )


# Command: SEARCH
@services.command()
@bic_options.search
@bic_options.list(default_fields=default_fields)
@click.pass_obj
def search(obj, single_term, search_terms, search_fields, json, select_fields):
    """Retrieves a list of all Services that match given terms in all or selected fields"""
    search_def = bic_options.validate_search(single_term, search_terms, search_fields)

    services = _get_list_services(obj.api)

    treat_list_objects(
        services,
        select_fields=select_fields,
        json=json,
        search=search_def,
    )


# Command: GET
@services.command()
@click.pass_obj
def get(obj: AppContext):
    """Retrieves the JSON of a single Service, by its ID"""
    id = obj.resources.id
    source = obj.api.get_service(id)

    treat_single_object(source)


# Command: READ
@services.command()
@bic_options.read
@click.option(
    "-t",
    "--table",
    is_flag=True,
    type=bool,
    default=False,
    help="For supported formats, extracts key information about the content and show it as a table",
)
@click.pass_obj
def read(
    obj: AppContext,
    sub: int,
    url: str,
    table: bool,
    raw: bool,
    highlight: bool,
    tail: bool,
):
    """Loads and displays the content of a Service, optionally highlighted for relevant information"""
    id = obj.resources.id
    service = obj.api.get_service(id)

    full_url = _compute_url(service, obj.api, extra_url=url, subplaylist_index=sub)

    display_url_content(
        url=full_url,
        format=service.get("format"),
        object_info=dict(type=service["type"], name=service["name"], id=service["id"]),
        max=1,
        interval=0,
        table=table,
        raw=raw,
        highlight=highlight,
        diff=False,
        tail=tail,
        clear=False,
    )


# Command: POLL
@services.command()
@bic_options.read
@bic_options.poll
@click.pass_obj
def poll(
    obj: AppContext,
    sub: int,
    url: str,
    max: int,
    interval: int,
    raw: bool,
    highlight: bool,
    diff: bool,
    tail: bool,
    clear: bool,
):
    """Similar to `read`, but regularly re-loads the Service's content"""
    id = obj.resources.id
    service = obj.api.get_service(id)

    full_url = _compute_url(service, obj.api, extra_url=url, subplaylist_index=sub)

    display_url_content(
        url=full_url,
        format=service.get("format"),
        object_info=dict(type=service["type"], name=service["name"], id=service["id"]),
        max=max,
        interval=interval,
        table=False,
        raw=raw,
        highlight=highlight,
        diff=diff,
        tail=tail,
        clear=clear,
    )


# Command: OPEN
@services.command()
@click.option(
    "-u",
    "--url",
    type=str,
    default=None,
    help="Full URL of URL sub-path (for asset catalogs) to fetch",
)
@click.option(
    "-s",
    "--sub",
    type=int,
    default=None,
    help="For HLS, reads a sub-playlist (by index - as given by the `read ID --table` option with the main playlist)",
)
@click.pass_obj
def open(obj: AppContext, url, sub):
    """Opens the URL of the Source in the web browser"""
    id = obj.resources.id
    service = obj.api.get_service(id)

    full_url = _compute_url(service, obj.api, extra_url=url, subplaylist_index=sub)

    click.launch(full_url)


# TODO - move to API helpers
def _compute_url(
    service, api, extra_url: Optional[str], subplaylist_index: Optional[int]
) -> str:
    """Calculates the URL to call for a Service, based on its type and Source"""
    url_to_read = service["url"]

    source_type = service["source"]["type"]
    source_id = service["source"]["id"]

    if source_type == "asset-catalog":
        if extra_url:
            # extra URL supplied, let's take it
            url_to_read = urljoin(url_to_read, extra_url)
        else:
            # otherwise, let's ask
            source = api.get_source(source_id)
            extra_url = source["assetSample"]

            extra_url = inquirer.text(message="Sub-path", default=extra_url).execute()

            url_to_read = urljoin(url_to_read, extra_url)

    # Then ask query params
    def get_first_matching_key_value(dictionary: dict, possible_keys: list):
        for key in possible_keys:
            if key in dictionary:
                return dictionary[key]
        return None

    # In case it's an ad insertion service, and the ad server has query params,
    # prompt for values for the ones expected to be passed through
    ad_config = get_first_matching_key_value(
        service, ["vodAdInsertion", "liveAdPreRoll", "liveAdReplacement"]
    )
    if ad_config and ad_config.get("adServer"):
        filled_params = dict()
        params = ad_config.get("adServer")["queries"]
        if params:
            params = params.split("&")
            for p in params:
                (k, val) = p.split("=")
                if val.startswith("$arg_"):
                    input_param = val.replace("$arg_", "")
                    input_val = inquirer.text(
                        message=f"Parameter '{input_param}'"
                    ).execute()
                    filled_params[input_param] = input_val

        url_to_read = add_query_parameters(url_to_read, filled_params)

    if subplaylist_index:
        if not HlsReader.is_hls(url_to_read):
            raise click.UsageError("`--sub` can only be used with HLS sources")

        manifest_info = HlsReader(url_to_read).summary()
        url_to_read = manifest_info[subplaylist_index - 1]["url"]

    return url_to_read
