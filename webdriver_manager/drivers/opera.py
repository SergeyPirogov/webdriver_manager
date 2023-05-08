from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log


class OperaDriver(Driver):
    def __init__(
            self,
            name,
            version,
            os_type,
            url,
            latest_release_url,
            http_client,
    ):
        super(OperaDriver, self).__init__(
            name, version, os_type, url, latest_release_url, http_client,
        )

    def get_latest_release_version(self) -> str:
        resp = self._http_client.get(url=self.latest_release_url)
        return resp.text.strip()

    def get_driver_download_url(self) -> str:
        """Like https://github.com/operasoftware/operachromiumdriver/releases/download/v.2.45/operadriver_linux64.zip"""
        driver_version_to_download = self.get_driver_version_to_download()
        log(f"Getting latest opera release info for {driver_version_to_download}")
        name = "{0}_{1}.zip".format(self.get_name(), self.get_os_type())
        url = f'{self._url}/{driver_version_to_download}/{name}'
        return self._url_postprocess(url)

    @property
    def latest_release_url(self):
        return self._latest_release_url

    def get_browser_type(self):
        return "opera"
