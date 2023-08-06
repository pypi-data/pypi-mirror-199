import re
import urllib.request
from urllib.parse import urlparse
from xml.sax.saxutils import escape

import requests
from colorama import Fore, Style, init
from lxml import etree

init()


class XmlReader:
    def __init__(self, url) -> None:
        self._url = url

        # Read the XML document from the URL
        with urllib.request.urlopen(url) as response:
            xml_string = response.read()

        # Parse the XML string into an Element object
        self._root = etree.fromstring(xml_string)  # type: ignore

    @staticmethod
    def is_xml(url: str) -> bool:
        res = requests.head(url)
        if res.headers.get("Content-Type") in ["application/xml", "text/xml"]:
            return True

        url_parts = urlparse(url)
        if url_parts.path.endswith(".xml"):
            return True

        # TODO - pull the whole content of the file and attempt to parse it
        # BUT: then we can't cache it

        return False

    # TODO - move to DashReader class
    @staticmethod
    def is_dash(url: str) -> bool:
        res = requests.head(url)
        if res.headers.get("Content-Type") in ["application/dash+xml"]:
            return True

        url_parts = urlparse(url)
        if url_parts.path.endswith(".mpd"):
            return True

        # TODO - pull the whole content of the file and attempt to parse it
        # BUT: then we can't cache it

        return False

    def raw(self):
        # Pretty-print the XML using the ElementTree's tostring() method
        return etree.tostring(self._root)

    # def pretty_print(self):
    #     return etree.tostring(self._root, pretty_print=True)

    # Pretty-print the XML with colored output
    # TODO - Fix. The closing tags are added twice for nodes with text content
    def pretty_print(self):
        # Parse the XML string into an Element object
        root = self._root

        # Get the namespaces in the root element
        namespaces = root.nsmap
        ns_mappings = dict((v, k + ":" if k else "") for k, v in namespaces.items())

        indent = "  "

        # Recursively pretty-print the XML with colored output and return as a string
        def _pretty_print(node, level=0):
            # Start the opening tag
            result = indent * level + "<"

            tag = node.tag

            # Resolve namespaces:
            if "{" in tag:
                tag = re.sub(
                    r"{(.*)}",
                    lambda m: ns_mappings.get(m.group(1), m.group(0)),
                    tag,
                )
            resolved_tag = tag

            # Color-code the element tag name
            tag = Fore.GREEN + Style.BRIGHT + tag + Style.RESET_ALL

            # Add the namespaces
            if level == 0:
                ns_strings = []
                for k, v in namespaces.items():
                    ns_string = Fore.RED
                    if k:
                        ns_string = ns_string + f'xmlns:{k}="{v}"'
                    else:
                        ns_string = ns_string + f'xmlns="{v}"'

                    ns_string = ns_string + Style.RESET_ALL
                    ns_strings.append(ns_string)
                n_str = " " + " ".join(ns_strings)
                tag += n_str

            # Add the namespace to the tag name, if necessary
            if node.prefix:
                tag = f"{Fore.YELLOW}{node.prefix}:{Fore.GREEN}{tag}"

            # Color-code the attributes
            if node.attrib:
                attr_strings = []
                for k, v in node.attrib.items():
                    # Replace namespace with prefix
                    if "{" in k:
                        k = re.sub(
                            r"{(.*)}",
                            lambda m: ns_mappings.get(m.group(1), m.group(0)) + ":",
                            k,
                        )

                    attr_value = escape(v, {'"': "&quot;"})
                    attr_string = '{yellow}{key}{reset}={cyan}"{value}"{reset}'.format(
                        yellow=Fore.MAGENTA,
                        cyan=Fore.CYAN,
                        reset=Fore.RESET,
                        key=k,
                        value=attr_value,
                    )
                    attr_strings.append(attr_string)
                attr_str = " " + " ".join(attr_strings)
                tag += attr_str

            # Add the tag
            result += tag

            # Close the tag
            if not node.text and not len(node):
                result += Style.RESET_ALL + "/>"
            else:
                result += Style.RESET_ALL + ">"

            # Add the text content, if any
            if node.text and node.text.strip():
                text = node.text.strip()
                if text.startswith("http"):
                    text = "<![CDATA[" + Fore.YELLOW + text + Style.RESET_ALL + "]]>"
                else:
                    text = escape(text)
                result += text

            # Recurse into child nodes
            if len(node):
                result += "\n"
                for child in node:
                    result += _pretty_print(child, level + 1)

            # Add the closing tag
            if len(node):
                result += indent * level

            result += (
                "</"
                + Fore.GREEN
                + Style.BRIGHT
                + resolved_tag
                + ">"
                + Style.RESET_ALL
                + "\n"
            )

            return result

        # Pretty-print the XML with colored output and include the XML declaration
        declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_string = _pretty_print(root)
        valid_xml = f"{declaration}{xml_string}\n"

        return valid_xml
