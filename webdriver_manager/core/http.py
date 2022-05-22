import requests
from requests import Response

from webdriver_manager.core.constants import WDM_SSL_VERIFY


class HttpClient:
    def get(self, url, params=None, **kwargs) -> Response:
        raise NotImplementedError


class WDMHttpClient(HttpClient):
    def __init__(self):
        self._ssl_verify = WDM_SSL_VERIFY
        if WDM_SSL_VERIFY == "0":
            self._ssl_verify = False

    def get(self, url, **kwargs) -> Response:
        return requests.get(url=url, verify=self._ssl_verify, **kwargs)
