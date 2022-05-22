import os

import requests
from requests import Response


class HttpClient:
    def get(self, url, params=None, **kwargs) -> Response:
        raise NotImplementedError

    @staticmethod
    def validate_response(resp: requests.Response):
        if resp.status_code == 404:
            raise ValueError(
                "There is no such driver by url {}".format(resp.url))
        elif resp.status_code != 200:
            raise ValueError(
                f"response body:\n{resp.text}\n"
                f"request url:\n{resp.request.url}\n"
                f"response headers:\n{dict(resp.headers)}\n"
            )


class WDMHttpClient(HttpClient):
    def __init__(self):
        wdm_ssl_verify = os.getenv("WDM_SSL_VERIFY", "1")
        self._ssl_verify = True
        if wdm_ssl_verify == "0":
            self._ssl_verify = False

    def get(self, url, **kwargs) -> Response:
        resp = requests.get(url=url, verify=self._ssl_verify, **kwargs)
        self.validate_response(resp)
        return resp
