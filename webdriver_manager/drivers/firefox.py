from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log
from webdriver_manager.core.utils import is_arch, is_mac_os


class GeckoDriver(Driver):
    def __init__(
            self,
            name,
            version,
            os_type,
            url,
            latest_release_url,
            http_client,
    ):
        super(GeckoDriver, self).__init__(
            name, version, os_type, url, latest_release_url, http_client
        )
        self._os_type = self.get_os_type()

    def get_latest_release_version(self) -> str:
        determined_browser_version = self.get_browser_version_from_os()
        log(f"Get LATEST {self._name} version for {determined_browser_version} firefox")
        resp = self._http_client.get(url=self.latest_release_url)
        return resp.text.strip()

    def get_driver_download_url(self):
        """Like https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz"""
        driver_version_to_download = self.get_driver_version_to_download()
        log(f"Getting latest firefox release info for {driver_version_to_download}")
        _exts = ['tar.gz', 'zip', 'gz']
        for ext in _exts:
            name = f"{self.get_name()}-{driver_version_to_download}-{self._os_type}.{ext}"
            url = f'{self._url}/{driver_version_to_download}/{name}'
            try:
                return self._url_postprocess(url)
            except (ValueError, IOError):
                continue
        else:
            # noinspection PyUnboundLocalVariable
            raise ValueError(f'There is no such driver by url {url}.')

    def get_os_type(self):
        os_type = super().get_os_type()
        if not is_mac_os(os_type):
            return os_type

        macos = 'macos'
        if is_arch(os_type):
            return f"{macos}-aarch64"
        return macos

    @property
    def latest_release_url(self):
        return self._latest_release_url

    def get_browser_type(self):
        return "firefox"
