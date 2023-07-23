import os
from typing import Optional
from webdriver_manager.core.logger import log
from packaging import version

from webdriver_manager.core.download_manager import DownloadManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.manager import DriverManager
from webdriver_manager.core.os_manager import OperationSystemManager, ChromeType
from webdriver_manager.drivers.chrome import ChromeDriver


class ChromeDriverManager(DriverManager):
    def __init__(
            self,
            driver_version: Optional[str] = None,
            name: str = "chromedriver",
            url: str = "https://chromedriver.storage.googleapis.com",
            latest_release_url: str = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE",
            chrome_type: str = ChromeType.GOOGLE,
            download_manager: Optional[DownloadManager] = None,
            cache_manager: Optional[DriverCacheManager] = None,
            os_system_manager: Optional[OperationSystemManager] = None
    ):
        super().__init__(
            download_manager=download_manager,
            cache_manager=cache_manager,
            os_system_manager=os_system_manager
        )

        self._url = url
        self._browser_type = chrome_type
        self._browser_version = self.get_browser_version_from_os()

        self.driver = ChromeDriver(
            name=name,
            driver_version=driver_version,
            url=url,
            latest_release_url=latest_release_url,
            chrome_type=chrome_type,
            http_client=self.http_client,
            os_system_manager=os_system_manager
        )

    def install(self) -> str:
        driver_path = self._get_driver_binary_path(self.driver)
        if all(test_os not in driver_path for test_os in ["mac_arm64", "mac_x64"]):
            os.chmod(driver_path, 0o755)
        return driver_path

    def get_os_type(self):
        os_type = super().get_os_type()
        if "win" in os_type:
            return "win32"

        if not self._os_system_manager.is_mac_os(os_type):
            return os_type

        if self._os_system_manager.is_arch(os_type):
            return "mac_arm64"

        return os_type

    def get_browser_version_from_os(self):
        """
        Use-cases:
        - for key in metadata;
        - for printing nice logs;
        - for fallback if version was not set at all.
        Note: the fallback may have collisions in user cases when previous browser was not uninstalled properly.
        """
        return self._os_system_manager.get_browser_version_from_os(self._browser_type)

    def get_driver_download_url(self, os_type):
        driver_version_to_download = self.get_browser_version_from_os()
        # For Mac ARM CPUs after version 106.0.5249.61 the format of OS type changed
        # to more unified "mac_arm64". For newer versions, it'll be "mac_arm64"
        # by default, for lower versions we replace "mac_arm64" to old format - "mac64_m1".
        if version.parse(driver_version_to_download) < version.parse("106.0.5249.61"):
            os_type = os_type.replace("mac_arm64", "mac64_m1")

        if version.parse(driver_version_to_download) >= version.parse("115"):
            if os_type == "mac64":
                os_type = "mac-x64"
            if os_type in ["mac_64", "mac64_m1", "mac_arm64"]:
                os_type = "mac-arm64"

            modern_version_url = self.get_url_for_version_and_platform(driver_version_to_download, os_type)
            log(f"Modern chrome version {modern_version_url}")
            return modern_version_url

        return f"{self._url}/{driver_version_to_download}/{self.driver.get_name()}_{os_type}.zip"

    def get_url_for_version_and_platform(self, browser_version, platform):
        url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
        response = self._download_manager._http_client.get(url)
        data = response.json()
        versions = data["versions"]
        for v in versions:
            if v["version"] == browser_version:
                downloads = v["downloads"]["chromedriver"]
                for d in downloads:
                    if d["platform"] == platform:
                        return d["url"]

        raise Exception(f"No such driver version {browser_version} for {platform}")
