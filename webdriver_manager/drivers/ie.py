import requests

from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log


class IEDriver(Driver):
    def __init__(
            self,
            name,
            version,
            os_type,
            url,
            latest_release_url,
            http_client,
    ):
        super(IEDriver, self).__init__(
            name, version, os_type, url, latest_release_url, http_client
        )
        self.os_type = "x64" if self._os_type == "win64" else "Win32"
        # todo: for 'browser_version' implement installed IE version detection
        #       like chrome or firefox

    def get_latest_release_version(self) -> str:
        log(f"Get LATEST driver version for Internet Explorer")
        resp = self._http_client.get(url=self.latest_release_url)
        return resp.text.strip().replace("selenium-", "")

    def _get_version_to_fulfill(self, version):
        response = requests.get(f'{self._latest_release_url}_{version}')
        if response.status_code != 404:
            response.raise_for_status()
            return response.text.strip().replace("selenium-", "")
        else:
            raise ValueError(f'Unknown version of ie webdriver - {version!r}.')

    def get_driver_version_to_download(self):
        if not self._driver_to_download_version:
            self._driver_to_download_version = self._get_version_to_fulfill(self._version) \
                if self._version not in (None, "latest") else self.get_latest_release_version()
        return self._driver_to_download_version

    def get_driver_download_url(self):
        """Like https://github.com/seleniumhq/selenium/releases/download/3.141.59/IEDriverServer_Win32_3.141.59.zip"""
        driver_version_to_download = self.get_driver_version_to_download()
        log(f"Getting latest ie release info for {driver_version_to_download}")
        filename = f"{self._name}_{self.os_type}_{driver_version_to_download}.zip"
        url = f'{self._url}/selenium-{driver_version_to_download}/{filename}'
        return self._url_postprocess(url)

    @property
    def latest_release_url(self):
        return self._latest_release_url

    def get_browser_type(self):
        return "msie"
