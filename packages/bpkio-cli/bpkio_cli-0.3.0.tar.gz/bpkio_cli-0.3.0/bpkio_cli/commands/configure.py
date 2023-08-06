import re

import click
from InquirerPy import inquirer

from bpkio_cli.api.crudeApi import BroadpeakIoCrudeApi
from bpkio_cli.commands.hello import hello
from bpkio_cli.core.initialize import initialize
from bpkio_cli.core.wrappers import treat_list_objects
from bpkio_cli.utils.tenant_profile_provider import TenantProfileProvider


# Command: INIT
# To be attached to the root group
@click.command()
@click.pass_context
def init(ctx):
    """Initialize the tool, and create a first tenant profile"""
    cp = TenantProfileProvider()

    if not cp.has_default_tenant():
        ctx.invoke(add)

    click.secho("All done!  You're ready to go now", fg="yellow")


# Group: CONFIG
@click.group()
@click.pass_obj
def config(obj):
    """Configure how the CLI works"""
    print(obj)
    pass


# Group: TENANTS
@config.group()
@click.pass_obj
def tenants(obj):
    """Define CLI profiles to be able to easily switc h tenant"""
    print(obj)
    pass


# Command: LIST
@tenants.command()
def list():
    "Lists the tenants previously configured"
    cp = TenantProfileProvider()
    tenants = cp.list_tenants()
    treat_list_objects(tenants)


# Command: SWITCH
@tenants.command()
@click.argument("tenant", required=False)
@click.pass_context
def switch(ctx, tenant):
    """Switch the tenant being used for subsequent invocations"""
    if not tenant:
        cp = TenantProfileProvider()
        tenant_list = cp.list_tenants()
        choices = [
            dict(value=t["tenant"], name=f"{t['tenant']} ({t['id']})")
            for t in tenant_list
        ]

        tenant = inquirer.fuzzy(message="Select a tenant", choices=choices).execute()

    # Write it to the .tenant file
    with open(".tenant", "w") as f:
        f.write(tenant)

    # Reinitialize the app context, before showing tenant info to the user for validation
    ctx.obj = initialize(tenant)
    ctx.invoke(hello)


# Command: ADD
@tenants.command()
def add():
    """Stores credentials in a tenant profile"""
    cp = TenantProfileProvider()

    api_key = inquirer.secret(
        message="Your API Key",
        validate=lambda candidate: BroadpeakIoCrudeApi.is_valid_api_key_format(
            candidate
        ),
        invalid_message="Invalid API Key",
    ).execute()
    fqdn = inquirer.text(
        message="Application domain name",
        default=BroadpeakIoCrudeApi.DEFAULT_FQDN,
        validate=lambda url: BroadpeakIoCrudeApi.is_correct_entrypoint(url, api_key),
        invalid_message="This URL does not appear to be a broadpeak.io application, or your API key does not give you access to it",
    ).execute()

    # Test the API key by initialising the API with it
    bpk_api = BroadpeakIoCrudeApi(api_key, fqdn=fqdn)

    # Parse the API
    tenant = bpk_api.get_my_tenant()
    tenant_id = tenant["id"]

    default_name = tenant["name"]
    default_name = re.sub(r"[^a-zA-Z0-9-_]", "_", default_name)
    # If there is no default profile yet, suggest that one instead
    if not cp.has_default_tenant():
        default_name = "default"

    # key = click.prompt("Profile name", type=str, default=default_name)
    key = inquirer.text(
        message="Profile name",
        default=default_name,
        validate=lambda s: bool(re.match(r"^[a-zA-Z0-9_-]*$", s)),
        invalid_message="Please only use alphanumerical characters",
    ).execute()

    # Create a dict
    config = {"api_key": api_key, "id": tenant["id"]}

    if fqdn != BroadpeakIoCrudeApi.DEFAULT_FQDN:
        config["fqdn"] = fqdn

    cp.add_tenant(key, config)

    click.echo(
        f'A profile named "{key}" for tenant {tenant_id} has been added to {cp.inifile}'
    )
    if key != "default":
        click.echo(
            f"You can now simply use `bic --tenant {key} COMMAND` to work within that tenant's account"
        )
    else:
        click.echo(
            f"You can now simply use `bic COMMAND` to work within that tenant's account"
        )


# Command: EDIT
@tenants.command()
def edit():
    "Edit the tenants file manually"
    cp = TenantProfileProvider()
    click.launch(str(cp.inifile))
