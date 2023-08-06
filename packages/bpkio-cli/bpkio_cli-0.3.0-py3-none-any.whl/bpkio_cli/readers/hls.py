import re
from urllib.parse import urlparse

import m3u8
import requests
from colorama import Back, Fore, Style, init

from bpkio_cli.core.logger import get_child_logger
from bpkio_cli.readers import TextReader

init(autoreset=True)

logger = get_child_logger("readers.hls")


class HlsReader:
    _url: str
    _manifest: m3u8.model.M3U8  # type: ignore

    def __init__(self, url) -> None:
        self._url = url

    def fetch(self):
        logger.debug(f"Calling HLS URL {self._url}")
        self._manifest = m3u8.load(self._url)
        return self

    @staticmethod
    def is_hls(url: str) -> bool:
        res = requests.head(url)
        if res.headers.get("Content-Type") in [
            "application/x-mpegurl",
            "application/vnd.apple.mpegurl",
        ]:
            return True

        url_parts = urlparse(url)
        if url_parts.path.endswith(".m3u8"):
            return True

        # TODO - pull the whole content of the file and search for
        # BUT: then we can't cache it

        return False

    def summary(self):
        arr = []
        index = 0

        self.fetch()

        if self._manifest.is_variant:
            for playlist in self._manifest.playlists:
                index += 1

                si = playlist.stream_info
                res = (
                    "{}x{}".format(
                        si.resolution[0],
                        si.resolution[1],
                    )
                    if si.resolution
                    else ""
                )

                arr.append(
                    dict(
                        index=index,
                        type="variant",
                        manifest=playlist.uri,
                        bandwidth=playlist.stream_info.bandwidth,
                        codecs=playlist.stream_info.codecs,
                        resolution=res,
                        url=playlist.absolute_uri,
                    )
                )

            for media in self._manifest.media:
                index += 1
                arr.append(
                    dict(
                        index=index,
                        type="media",
                        manifest=media.uri,
                        language=media.language,
                        url=media.absolute_uri,
                    )
                )

        return arr

    @staticmethod
    def highlight_markers(content):
        """Highlights specific HLS elements of interest"""
        start_sequences = {
            "#EXT-X-DATERANGE": Fore.GREEN,
            "#EXT-OATCLS-SCTE35": Fore.GREEN,
            "#EXT-X-CUE": Fore.GREEN,
            "#EXT-X-PROGRAM-DATE-TIME": Fore.BLUE,
            "#EXT-X-DISCONTINUITY": Fore.MAGENTA,
            "#EXT-X-ENDLIST": Fore.YELLOW,
            "#EXT-X-DISCONTINUITY-SEQUENCE": Fore.RED,
        }

        # Just markers initially
        pattern = re.compile(r"^(#[A-Z0-9\-]*?)(\:|$)", re.MULTILINE)
        highlighted_content = pattern.sub(
            lambda match: Style.BRIGHT
            + match.group(1)
            + Style.NORMAL
            + Style.RESET_ALL
            + match.group(2),
            content,
        )

        # Overwrites for complete lines
        pattern = re.compile(
            # TODO - bug: rest of the line is not highlighted. Maybe the regex doesn't like control characters?
            r"(" + "|".join(start_sequences.keys()) + ").*$",
            re.MULTILINE,
        )
        highlighted_content = pattern.sub(
            lambda match: Style.BRIGHT
            + start_sequences[match.group(1)]
            + match.group(0)
            + Style.NORMAL
            + Style.RESET_ALL,
            highlighted_content,
        )

        # Highlight lines for BPKIO segments
        pattern = re.compile("^.*bpkio-jitt.*$", re.MULTILINE)
        highlighted_content = pattern.sub(
            lambda match: ""
            + Fore.CYAN
            + match.group(0)
            + Style.NORMAL
            + Style.RESET_ALL,
            highlighted_content,
        )

        return highlighted_content
