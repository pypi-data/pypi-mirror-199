import requests


class TextReader:
    def __init__(self, url) -> None:
        self._url = url

    def fetch(self):
        res = requests.get(self._url)
        return res.text
