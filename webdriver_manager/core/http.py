import requests
from requests import Response


class HttpClient:

    def get(self, url, params=None, **kwargs) -> Response:
        raise NotImplementedError


class WDMHttpClient(HttpClient):

    def get(self, url, params=None, **kwargs) -> Response:
        return requests.get(url=url, headers=params, **kwargs)
