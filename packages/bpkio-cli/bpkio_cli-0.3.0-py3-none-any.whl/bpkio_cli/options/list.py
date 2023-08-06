import functools

import click

from bpkio_cli.utils import OptionEatAll


def list_options(default_fields=None):
    def decorator(fn):
        """Decorator to add multiple common decorators
        Idea from https://stackoverflow.com/questions/40182157/shared-options-and-flags-between-commands
        """

        @click.option(
            "-j",
            "--json",
            is_flag=True,
            default=False,
            help="Returns the results as a JSON payload",
        )
        @click.option(
            "-s",
            "--select",
            "select_fields",
            cls=OptionEatAll,
            type=tuple,
            default=default_fields,
            help="List of fields to return, separated by spaces",
        )
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper
    return decorator
