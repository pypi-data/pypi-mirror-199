import click

from bpkio_cli.api.crudeApi import BroadpeakIoCrudeApi
from bpkio_cli.core.app_settings import AppContext
from bpkio_cli.utils.tenant_profile_provider import TenantProfileProvider


def initialize(tenant):
    if not tenant:
        try:
            with open(".tenant") as f:
                tenant = f.read().strip()
        except:
            pass

    config_provider = TenantProfileProvider()
    try:
        api_key = config_provider.get_api_key(tenant)
    except Exception as e:
        click.secho(e.args[0], fg="red")
        click.secho("You may want to try `bic init` first...\n", fg="yellow")
        raise click.Abort

    fqdn = config_provider.get_fqdn(tenant)

    api = BroadpeakIoCrudeApi(api_key, fqdn=fqdn)
    app_context = AppContext(
        api=api,
        tenant_provider=TenantProfileProvider(),
    )

    tenant = api.get_my_tenant()
    tenant["fqdn"] = fqdn
    app_context.tenant = tenant

    return app_context
