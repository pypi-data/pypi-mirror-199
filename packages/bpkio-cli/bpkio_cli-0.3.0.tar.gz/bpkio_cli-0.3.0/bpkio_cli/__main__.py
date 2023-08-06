# from __future__ import absolute_import

import click

import bpkio_cli.commands as commands
from bpkio_cli.commands.configure import init
from bpkio_cli.core.initialize import initialize
from bpkio_cli.core.logger import (
    get_child_logger,
    get_level_names,
    set_console_logging_level,
)
from bpkio_cli.writers.breadcrumbs import display_tenant_info

logger = get_child_logger("cli")


@click.group()
@click.option(
    "-t",
    "--tenant",
)
@click.option("-l", "--log-level", type=click.Choice(get_level_names()), required=False)
@click.option("--log-sdk", type=bool, is_flag=True, required=False, default=False)
@click.pass_context
def cli(ctx, tenant, log_level, log_sdk):
    if log_level:
        set_console_logging_level(log_level, include_sdk=log_sdk)

    # Bypass initialisation if there is an explicit call to initialise the configuration
    if ctx.invoked_subcommand not in ["init", "config"]:
        app_context = initialize(tenant)

        display_tenant_info(app_context.tenant)

        # TODO - validate the token in the initialisation of BroadpeakApi
        ctx.obj = app_context


cli.add_command(commands.hello)
cli.add_command(init)
cli.add_command(commands.config)
cli.add_command(commands.sources)
cli.add_command(commands.services)
cli.add_command(commands.profiles)
cli.add_command(commands.tenants)
cli.add_command(commands.consumption)


if __name__ == "__main__":
    cli()
