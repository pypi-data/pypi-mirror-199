import functools

import click


# Common parameters for READ and POLL
def read_options(fn):
    @click.option(
        "-s",
        "--sub",
        type=int,
        default=None,
        help="For HLS, reads a sub-playlist (by index - as given by the `read ID --table` option with the main playlist)",
    )
    @click.option(
        "-u",
        "--url",
        type=str,
        default=None,
        help="Full URL of URL sub-path (for asset catalogs) to fetch",
    )
    @click.option(
        "--raw",
        is_flag=True,
        type=bool,
        default=False,
        help="Gets the raw content, unchanged",
    )
    @click.option(
        "-h",
        "--highlight",
        is_flag=True,
        type=bool,
        default=True,
        help="Add highlights (such as SCTE) in the content",
    )
    @click.option(
        "--tail", type=int, default=None, help="Only displays the last N lines"
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper
