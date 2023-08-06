import json as j

import click

import bpkio_cli.options as bic_options
from bpkio_cli.click_mods import RestResourceGroup
from bpkio_cli.core.app_settings import AppContext
from bpkio_cli.core.wrappers import treat_list_objects, treat_single_object
from bpkio_cli.writers.breadcrumbs import display_resource_info


def _get_list_profiles(api, tenant_id):
    profiles = api.list_transcoding_profiles(tenant_id=tenant_id)

    for p in profiles:
        pj = j.loads(p["content"])
        p["#layers"] = len(pj["transcoding"]["jobs"])

    return profiles


default_fields = ["id", "name", "#layers"]


# Group: TRANSCODING PROFILES
@click.group(cls=RestResourceGroup)
@click.argument("profile_id")
@click.pass_obj
def profiles(obj, profile_id: str):
    """Commands for Transcoding Profile resources"""
    
    if profile_id:
        # TODO - find a way of passing the target tenant (admin mode)
        profile = obj.api.get_transcoding_profile(profile_id)
        display_resource_info(profile)


# Command: LIST
@profiles.command()
@bic_options.list(default_fields=None)
@bic_options.tenant
@click.pass_obj
def list(obj, json, select_fields, tenant):
    """Retrieves a list of all Transoding Profiles"""
    if not select_fields:
        # TODO - pass through the decorator
        select_fields = default_fields

    profiles = _get_list_profiles(obj.api, tenant)

    treat_list_objects(
        profiles,
        select_fields=select_fields,
        json=json,
    )


# Command: GET
@profiles.command()
@click.option(
    "--pretty",
    is_flag=True,
    default=False,
    help="Extracts the profile's JSON and pretty prints it",
)
@bic_options.tenant
@click.pass_obj
def get(obj: AppContext, tenant, pretty):
    """Retrieves the JSON of a single Transcoding Profile, by its ID"""
    id = obj.resources.id
    profile = obj.api.get_transcoding_profile(id, tenant)

    if pretty:
        pj = j.loads(profile["content"])
        treat_single_object(pj)
    else:
        treat_single_object(profile)


# Command: SEARCH
@profiles.command()
@bic_options.search
@bic_options.list(default_fields=None)
@bic_options.tenant
@click.pass_obj
def search(obj, tenant, single_term, search_terms, search_fields, json, select_fields):
    """Retrieves a list of all Transcoding Profiles that match given terms in all or selected fields"""
    search_def = bic_options.validate_search(single_term, search_terms, search_fields)

    if not select_fields:
        # TODO - pass through the decorator
        select_fields = default_fields

    profiles = _get_list_profiles(obj.api, tenant)

    treat_list_objects(
        profiles,
        select_fields=select_fields,
        json=json,
        search=search_def,
    )
