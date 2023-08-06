# Command: HELLO
import click

from bpkio_cli.core.app_settings import AppContext


@click.command()
@click.pass_obj
def hello(obj: AppContext):
    """Validates access to the API and displays tenant information"""

    tenant = obj.api.get_my_tenant()
    user = obj.api.retrieve_user_by(field="tenantId", value=tenant["id"])

    click.echo(
        f"You are working with tenant \"{tenant['name']}\"  [id: {tenant['id']}]"
    )
    click.echo(
        f"The associated user is \"{user['firstName']}\"  [email: {user['email']}]"
    )
    if not obj.api.uses_default_fqdn():
        base_url = obj.api.base_url
        click.echo(f"This tenant is using a non-default API entrypoint at {base_url}")