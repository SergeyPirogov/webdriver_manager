import requests

from webdriver_manager.logger import log
from webdriver_manager.utils import File


class DownloadManager:
    def __init__(self):
        pass

    def download_file(self, url: str, ssl_verify=True) -> File:
        raise NotImplementedError

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


class DefaultDownloadManager(DownloadManager):
    def download_file(self, url: str, ssl_verify=True) -> File:
        log(f"Trying to download new driver from {url}")
        response = requests.get(url, stream=True, verify=ssl_verify)
        self.validate_response(response)
        return File(response)
