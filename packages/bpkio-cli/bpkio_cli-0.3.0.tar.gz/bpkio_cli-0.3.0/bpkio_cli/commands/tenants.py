import click

import bpkio_cli.options as bic_options
from bpkio_cli.click_mods.group_rest_resource import RestResourceGroup
from bpkio_cli.core.app_settings import AppContext
from bpkio_cli.core.wrappers import treat_list_objects, treat_single_object
from bpkio_cli.writers.breadcrumbs import display_resource_info

default_fields = ["id", "name", "email"]


# Group: TENANTS
@click.group(cls=RestResourceGroup)
@click.argument("tenant_id")
@click.pass_obj
def tenants(obj, tenant_id):
    """Commands for Tenant resources"""
    
    if tenant_id:
        tenant = obj.api.get_tenant(str(tenant_id))
        display_resource_info(tenant)


# Command: LIST
@tenants.command()
@bic_options.list(default_fields=default_fields)
@click.pass_obj
def list(obj, json, select_fields):
    """Retrieves a list of all Tenants"""
    tenants = obj.api.list_tenants()

    treat_list_objects(
        tenants,
        select_fields=select_fields,
        json=json,
    )

    return


# Command: SEARCH
@tenants.command()
@bic_options.search
@bic_options.list(default_fields=default_fields)
@click.pass_obj
def search(obj, single_term, search_terms, search_fields, json, select_fields):
    """Retrieves a list of all Tenants that match given terms in all or selected fields"""
    search_def = bic_options.validate_search(single_term, search_terms, search_fields)

    tenants = obj.api.list_tenants()

    treat_list_objects(
        tenants,
        select_fields=select_fields,
        json=json,
        search=search_def,
    )


# Command: GET
@tenants.command()
@click.pass_obj
def get(obj: AppContext):
    """Retrieves the JSON of a single Service, by its ID"""
    id = obj.resources.id
    source = obj.api.get_tenant(id)

    treat_single_object(source)
