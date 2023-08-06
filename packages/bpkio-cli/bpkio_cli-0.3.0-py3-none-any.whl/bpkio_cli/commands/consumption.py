from datetime import datetime

import click

import bpkio_cli.options as bic_options
from bpkio_cli.click_mods.option_eat_all import OptionEatAll
from bpkio_cli.core.wrappers import treat_list_objects, treat_single_object
from bpkio_cli.utils import get_utc_date_ranges, parse_date_string


@click.command()
@click.option(
    "-s",
    "--start",
    type=tuple,
    cls=OptionEatAll,
    default=("5 months ago",),
    help="Start time",
)
@click.option(
    "-e", "--end", type=tuple, cls=OptionEatAll, default=("now",), help="End time"
)
@click.option(
    "--by",
    type=click.Choice(["day", "week", "month"]),
    required=False,
    default="month",
    help="Splits the data in ranges of dates",
)
@click.option(
    "--tenant",
    type=int,
    required=False,
    help="[ADMIN] ID of the tenant",
)
@click.pass_obj
def consumption(obj, start, end, by, tenant):
    """Extract consumption/billing info"""

    # TODO - can this not be done in click.option somehow?
    if isinstance(start, tuple):
        start = " ".join(start)
    start = parse_date_string(start)
    start = datetime.utcfromtimestamp(start)

    if isinstance(end, tuple):
        end = " ".join(end)
    end = parse_date_string(end)
    end = datetime.utcfromtimestamp(end)

    if not by:
        cons = obj.api.get_consumption(start, end, tenant)
        treat_single_object(cons)
        return

    else:
        ranges = get_utc_date_ranges(from_time=start, to_time=end, unit=by)
        data = []
        for start, end in ranges:
            data.append(obj.api.get_consumption(start, end, tenant))

        treat_list_objects(data)
    return
