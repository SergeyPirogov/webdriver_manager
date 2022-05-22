from abc import ABC

from webdriver_manager.core.http import WDMHttpClient
from webdriver_manager.core.logger import log
from webdriver_manager.core.utils import File


class DownloadManager(ABC):
    def __init__(self, http_client):
        self._http_client = http_client

    def download_file(self, url: str) -> File:
        raise NotImplementedError

    @property
    def http_client(self):
        return self._http_client


class WDMDownloadManager(DownloadManager):
    def __init__(self, http_client=None):
        if http_client is None:
            http_client = WDMHttpClient()
        super().__init__(http_client)

    def download_file(self, url: str) -> File:
        log(f"About to download new driver from {url}")
        response = self._http_client.get(url)
        return File(response)
