from abc import ABC

import requests
from requests import Response

from webdriver_manager.core.http import WDMHttpClient
from webdriver_manager.core.logger import log
from webdriver_manager.core.utils import File


class DownloadManager(ABC):
    def __init__(self, http_client):
        self._http_client = http_client

    def download_file(self, url: str, ssl_verify=True) -> File:
        raise NotImplementedError

    def get(self, url, **kwargs) -> Response:
        return self._http_client.get(url, **kwargs)

    @staticmethod
    def validate_response(resp: requests.Response):
        if resp.status_code == 404:
            raise ValueError("There is no such driver by url {}".format(resp.url))
        elif resp.status_code != 200:
            raise ValueError(
                f"response body:\n{resp.text}\n"
                f"request url:\n{resp.request.url}\n"
                f"response headers:\n{dict(resp.headers)}\n"
            )


class WDMDownloadManager(DownloadManager):

    def __init__(self, http_client=None):
        if http_client is None:
            http_client = WDMHttpClient()
        super().__init__(http_client)

    @property
    def http_client(self):
        return self._http_client

    def download_file(self, url: str, ssl_verify=True) -> File:
        log(f"Trying to download new driver from {url}")
        response = self.get(url, verify=ssl_verify)
        self.validate_response(response)
        return File(response)
