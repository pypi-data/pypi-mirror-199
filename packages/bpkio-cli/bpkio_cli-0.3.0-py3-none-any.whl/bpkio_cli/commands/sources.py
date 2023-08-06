from typing import Optional
from urllib.parse import urljoin

import click

import bpkio_cli.options as bic_options
from bpkio_cli.click_mods import RestResourceGroup
from bpkio_cli.core.app_settings import AppContext
from bpkio_cli.core.wrappers import treat_list_objects, treat_single_object
from bpkio_cli.readers.hls import HlsReader
from bpkio_cli.writers.content_display import display_url_content
from bpkio_cli.writers.breadcrumbs import display_resource_info

default_fields = ["id", "name", "type", "format"]


# Group: SOURCES
@click.group(cls=RestResourceGroup)
@click.argument("source_id")
@click.pass_obj
def sources(obj, source_id: str):
    """Commands for Source resources"""
    
    if source_id:
        source = obj.api.get_source(int(source_id))
        display_resource_info(source)


# Command: LIST
@sources.command()
@bic_options.list(default_fields=default_fields)
@click.pass_obj
def list(obj, json, select_fields):
    """Retrieves a list of all Sources"""
    sources = obj.api.list_sources()

    treat_list_objects(
        sources,
        select_fields=select_fields,
        json=json,
        search=None,
    )


# Command: SEARCH
@sources.command()
@bic_options.search
@bic_options.list(default_fields=default_fields)
@click.pass_obj
def search(obj, single_term, search_terms, search_fields, json, select_fields):
    """Retrieves a list of all Sources that match given terms in all or selected fields"""
    search_def = bic_options.validate_search(single_term, search_terms, search_fields)

    sources = obj.api.list_sources()

    treat_list_objects(
        sources,
        select_fields=select_fields,
        json=json,
        search=search_def,
    )


# Command: GET
@sources.command()
@click.pass_obj
def get(obj: AppContext):
    """Retrieves the JSON of a single Service, by its ID"""
    id = obj.resources.id
    source = obj.api.get_source(id)

    treat_single_object(source)


# Command: CHECK
@sources.command()
@bic_options.list
@click.pass_obj
def check(obj: AppContext, select_fields, json):
    """Checks the validity of an existing Source"""
    id = obj.resources.id
    results = obj.api.check_source(id)

    treat_list_objects(results, json=json, select_fields=select_fields)


# Command: READ
@sources.command()
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
    """Loads and displays the content of a Source, optionally highlighted for relevant information"""
    id = obj.resources.id
    source = obj.api.get_source(id)

    url = _compute_url(source, extra_url=url, subplaylist_index=sub)

    display_url_content(
        url=url,
        format=source.get("format"),
        object_info=dict(type=source["type"], name=source["name"], id=source["id"]),
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
@sources.command()
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
    """Similar to `read`, but regularly re-loads the Source's content"""
    id = obj.resources.id
    source = obj.api.get_source(id)

    url = _compute_url(source, extra_url=url, subplaylist_index=sub)

    display_url_content(
        url=url,
        format=source.get("format"),
        object_info=dict(type=source["type"], name=source["name"], id=source["id"]),
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
@sources.command()
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
def open(obj: AppContext, url: str, sub: int):
    """Opens the URL of the Source in the web browser"""
    id = obj.resources.id
    source = obj.api.get_source(id)

    url = _compute_url(source, extra_url=url, subplaylist_index=sub)

    click.launch(url)


# TODO - move to API helpers
def _compute_url(
    source, extra_url: Optional[str], subplaylist_index: Optional[int]
) -> str:
    url_to_read = source["url"]

    if source["type"] == "ad-server":
        # TODO - use correct URL builder
        url_to_read = url_to_read + "?" + source["queries"]

    if source["type"] == "asset-catalog":
        if extra_url:
            url_to_read = urljoin(url_to_read, extra_url)
        else:
            url_to_read = urljoin(url_to_read, source["assetSample"])

    if subplaylist_index:
        if not HlsReader.is_hls(url_to_read):
            raise click.UsageError("`--sub` can only be used with HLS sources")

        manifest_info = HlsReader(url_to_read).summary()
        url_to_read = manifest_info[subplaylist_index - 1]["url"]

    return url_to_read
