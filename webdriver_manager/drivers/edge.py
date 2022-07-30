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

    def get_stable_release_version(self):
        """Stable driver version when browser version was not determined."""
        stable_url = self._latest_release_url.replace(
            "LATEST_RELEASE", "LATEST_STABLE")
        resp = self._http_client.get(url=stable_url)
        return resp.text.rstrip()

    def get_latest_release_version(self) -> str:
        browser_version = self.get_browser_version()
        browser_version = (
            browser_version if browser_version else self.get_stable_release_version())
        log(f"Get LATEST {self._name} version for {browser_version} Edge")
        major_edge_version = browser_version.split(".")[0]
        latest_release_url = {
            OSType.WIN
            in self.get_os_type(): f"{self._latest_release_url}_{major_edge_version}_WINDOWS",
            OSType.MAC
            in self.get_os_type(): f"{self._latest_release_url}_{major_edge_version}_MACOS",
            OSType.LINUX
            in self.get_os_type(): f"{self._latest_release_url}_{major_edge_version}_LINUX",
        }[True]
        resp = self._http_client.get(url=latest_release_url)
        self._version = resp.text.rstrip()
        return self._version

    def get_browser_type(self):
        return ChromeType.MSEDGE
