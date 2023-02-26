from packaging import version

from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log
from webdriver_manager.core.utils import ChromeType, is_arch, is_mac_os


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
        self._browser_type = chrome_type
        self._os_type = self.get_os_type()

    def get_os_type(self):
        os_type = super().get_os_type()
        if "win" in os_type:
            return "win32"

        if not is_mac_os(os_type):
            return os_type

        if is_arch(os_type):
            return "mac_arm64"

        return os_type

    def get_driver_download_url(self):
        driver_version_to_download = self.get_driver_version_to_download()
        os_type = self._os_type
        # For Mac ARM CPUs after version 106.0.5249.61 the format of OS type changed
        # to more unified "mac_arm64". For newer versions, it'll be "mac_arm64"
        # by default, for lower versions we replace "mac_arm64" to old format - "mac64_m1".
        if version.parse(driver_version_to_download) < version.parse("106.0.5249.61"):
            os_type = os_type.replace("mac_arm64", "mac64_m1")

        return f"{self._url}/{driver_version_to_download}/{self.get_name()}_{os_type}.zip"

    def get_browser_type(self):
        return self._browser_type

    def get_latest_release_version(self):
        determined_browser_version = self.get_browser_version_from_os()

        log(f"Get LATEST {self._name} version for {self._browser_type}")
        latest_release_url = (
            self._latest_release_url
            if (self._version == "latest" or determined_browser_version is None)
            else f"{self._latest_release_url}_{determined_browser_version}"
        )
        resp = self._http_client.get(url=latest_release_url)
        return resp.text.rstrip()
