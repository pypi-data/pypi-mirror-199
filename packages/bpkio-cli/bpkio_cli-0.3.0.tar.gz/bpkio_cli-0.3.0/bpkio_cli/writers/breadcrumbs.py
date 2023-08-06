import click

from bpkio_cli.api.crudeApi import BroadpeakIoCrudeApi


def display_resource_info(resource):
    core_info = [
        "{} {}".format(resource.get("__resourceTitle"), resource.get("id")),
        resource.get("type"),
    ]
    name = resource.get("name")

    core_info_str = " / ".join([str(c) for c in core_info if c])

    info = "[{c}]  {n}".format(c=core_info_str, n=name)

    click.secho(info, err=True, fg="white", bg="blue", dim=False)


def display_tenant_info(tenant):
    info = "Tenant {i} - {n}".format(i=tenant.get("id"), n=tenant.get("name"))
    if url := tenant.get("fqdn"):
        if url != BroadpeakIoCrudeApi.DEFAULT_FQDN:
            info = info + f" - ({url})"
    info = f"[{info}]"

    click.secho(info, err=True, fg="green", bg="blue", dim=False)
