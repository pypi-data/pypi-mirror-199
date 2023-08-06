import os
import time
from datetime import datetime
from typing import Optional

import click

from bpkio_cli.core.wrappers import treat_list_objects
from bpkio_cli.readers import HlsReader, TextReader, XmlReader
from bpkio_cli.utils.diff import generate_diff


# ---- Shared Functions ----
def display_url_content(
    url: str,
    format: str,
    object_info: dict,
    max: int,
    interval: int,
    table: bool,
    raw: bool,
    highlight: bool,
    diff: bool,
    tail: bool,
    clear: bool,
):
    """Fetches the content of the URL associated with ID"""
    previous_content = None

    # TODO - move all this to a separate module

    counter = max
    inc_counter = 0

    try:
        while True:
            content = None
            stamp = datetime.utcnow()

            if clear:
                _clear_screen()

            header = _make_header(stamp=stamp, url=url, counter=counter)
            click.secho(header, err=True, fg="blue", bg="white")

            if not raw:
                # HLS content
                if format == "HLS" or HlsReader.is_hls(url):
                    if table:
                        # Table output of summary
                        manifest = HlsReader(url)
                        treat_list_objects(manifest.summary())
                        return

                # DASH / VAST / VMAP content
                if (
                    object_info.get("type") == "ad-server"
                    or format == "DASH"
                    or XmlReader.is_dash(url)
                ):
                    content = XmlReader(url).pretty_print()
                    _display_content(
                        content,
                        previous_content,
                        highlight=highlight,
                        diff=diff,
                    )
                    return

            # for other formats
            content = TextReader(url).fetch()
            content = _trim_content(content, tail)
            _display_content(
                content,
                previous_content,
                highlight=highlight,
                diff=diff,
            )

            previous_content = content

            if counter == 1:
                break

            time.sleep(int(interval))
            counter = counter - 1
            inc_counter = inc_counter + 1

    except KeyboardInterrupt:
        print("Stopped!")


def _clear_screen():
    cls = lambda: os.system("cls" if os.name == "nt" else "clear")
    cls()


def _trim_content(content, tail):
    if tail:
        lines = content.splitlines()
        prev = f"(... {len(lines)} previous lines ...)\n"
        return prev + "\n".join(lines[-tail:])
    return content


def _make_header(stamp: datetime, url: str, counter: Optional[int]):
    lines = []

    if url:
        lines.append(url)

    lines.append(
        "[request{} @ {}]".format(
            " " + str(counter) if counter else "", stamp.isoformat()
        )
    )

    header = "\n".join(lines)

    return header


def _display_content(
    content,
    previous_content,
    highlight: bool = False,
    diff: bool = False,
):
    if highlight:
        # TODO - Make more generic than just for HLS
        print(HlsReader.highlight_markers(content))
        return

    if previous_content and diff:
        print(generate_diff(previous_content, content))
        return

    print(content)
