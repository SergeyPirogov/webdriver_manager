from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log
from webdriver_manager.core.utils import OSType, ChromeType


class EdgeChromiumDriver(Driver):

    def __init__(
            self,
            name,
            version,
            os_type,
            url,
            latest_release_url,
            http_client
    ):
        super(EdgeChromiumDriver, self).__init__(
            name,
            version,
            os_type,
            url,
            latest_release_url,
            http_client
        )
        self._os_type = self.get_os_type()

    def get_stable_release_version(self):
        """Stable driver version when browser version was not determined."""
        stable_url = self._latest_release_url.replace("LATEST_RELEASE", "LATEST_STABLE")
        resp = self._http_client.get(url=stable_url)
        return resp.text.rstrip()

    def get_latest_release_version(self) -> str:
        determined_browser_version = self.get_browser_version_from_os()
        log(f"Get LATEST {self._name} version for Edge {determined_browser_version}")

        edge_driver_version_to_download = (
            self.get_stable_release_version()
            if (self._version == "latest" or determined_browser_version is None)
            else determined_browser_version
        )
        major_edge_version = edge_driver_version_to_download.split(".")[0]
        latest_release_url = {
            OSType.WIN
            in self._os_type: f"{self._latest_release_url}_{major_edge_version}_WINDOWS",
            OSType.MAC
            in self._os_type: f"{self._latest_release_url}_{major_edge_version}_MACOS",
            OSType.LINUX
            in self._os_type: f"{self._latest_release_url}_{major_edge_version}_LINUX",
        }[True]
        resp = self._http_client.get(url=latest_release_url)
        return resp.text.rstrip()

    def get_browser_type(self):
        return ChromeType.MSEDGE
