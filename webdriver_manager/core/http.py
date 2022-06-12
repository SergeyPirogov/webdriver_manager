import requests
from requests import Response

from tqdm import tqdm

from webdriver_manager.core.config import ssl_verify


class HttpClient:
    def get(self, url, params=None, **kwargs) -> Response:
        raise NotImplementedError

    @staticmethod
    def validate_response(resp: requests.Response):
        status_code = resp.status_code
        if status_code == 404:
            raise ValueError(f"There is no such driver by url {resp.url}")
        elif status_code == 401:
            raise ValueError(f"API Rate limit exceeded. You have to add GH_TOKEN!!!")
        elif resp.status_code != 200:
            raise ValueError(
                f"response body:\n{resp.text}\n"
                f"request url:\n{resp.request.url}\n"
                f"response headers:\n{dict(resp.headers)}\n"
            )



class WDMHttpClient(HttpClient):
    def __init__(self):
        self._ssl_verify = ssl_verify()

    def get(self, url, **kwargs) -> Response:
        resp = requests.get(url=url, verify=self._ssl_verify, stream=True, **kwargs)
        self.validate_response(resp)

        total = int(resp.headers['Content-Length'])
        if total > 100:
            content = bytearray()
            pbar = tqdm(total=total)
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    pbar.update(len(chunk))
                    content.extend(chunk)
            resp._content = content  # To allow content to be "consumed" again

        return resp
