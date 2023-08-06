import click

from bpkio_cli.core.resources import ResourcesContext


class RestResourceGroup(click.Group):
    """A click.Group sub-class that enables the use of command lines that
    1.  mirror REST endpoint structure that use resource identifiers
        (eg. `mycli sources 123 slots 456` -> http://myapi/sources/:source_id/slots/:slot_id)
    2.  allow for implicit commands for `list` and `get` when no sub-commands are provided
        on parent groups that support it.
        (eg. `mycli sources` -> `mycli sources list`)
        (eg. `mycli sources 123` -> `mycli sources 123 get`)
    3.  save automatically the ID to the context (for use deeper in the chain)

    Inspired by https://stackoverflow.com/a/44056564/2215413"""

    def parse_args(self, ctx, args):
        commands_without_resource_id = ["list", "search"]

        # No sub-command?  Then it's an implicit `list`
        if len(args) == 0 and "list" in self.commands:
            args.append("list")

        # Some commands does not take an ID argument,
        # so inject an empty one to prevent parse failure
        if args[0] in commands_without_resource_id:
            args.insert(0, "")

        # Single argument, which is not a command?
        # It must be an ID, and we treat it as an implicit `get`
        if args[0] not in self.commands:
            if (len(args) == 1) or (len(args) == 2 and args[1] in ["-h", "--help"]):
                args.insert(1, "get")

        # If there is a resource-based command preceded by a non-empty string, that's an error
        if args[0] != "" and args[1] in commands_without_resource_id:
            raise click.BadArgumentUsage(
                f"The `{self.name}` command cannot be preceded by an object identifier"
            )

        # actual (non-empty) argument before command?  It's an ID,
        # and we save it automatically to the context object
        if args[0] != "" and args[0] not in self.commands and args[1] in self.commands:
            resources: ResourcesContext = ctx.obj.resources
            resources.record_resource_id(self.name, args[0])

            # arg_name = self.params[0].name
            # ctx.obj[arg_name] = args[0]

        super(RestResourceGroup, self).parse_args(ctx, args)
