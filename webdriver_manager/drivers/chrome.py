from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log
from webdriver_manager.core.utils import ChromeType, get_browser_version_from_os, is_arch, OSType, is_mac_os


class ChromeDriver(Driver):
    def __init__(
            self,
            name,
            version,
            os_type,
            url,
            latest_release_url,
            http_client,
            chrome_type=ChromeType.GOOGLE,
    ):
        super(ChromeDriver, self).__init__(
            name, version, os_type, url, latest_release_url, http_client
        )
        self.chrome_type = chrome_type
        self.browser_version = ""

    def get_os_type(self):
        os_type = super().get_os_type()
        if "win" in os_type:
            return "win32"

        if not is_mac_os(os_type):
            return os_type

        if is_arch(os_type):
            return f"{os_type.replace('_m1', '')}_m1"

        return os_type

    def get_latest_release_version(self):
        self.browser_version = get_browser_version_from_os(self.chrome_type)
        log(f"Get LATEST {self._name} version for {self.browser_version} {self.chrome_type}")
        latest_release_url = (
            f"{self._latest_release_url}_{self.browser_version}"
            if self.browser_version
            else self._latest_release_url
        )
        resp = self._http_client.get(url=latest_release_url)
        self._version = resp.text.rstrip()
        return self._version
