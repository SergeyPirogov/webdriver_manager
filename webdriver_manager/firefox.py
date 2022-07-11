import os

from webdriver_manager.core.download_manager import DownloadManager
from webdriver_manager.core.manager import DriverManager
from webdriver_manager.drivers.firefox import GeckoDriver


class GeckoDriverManager(DriverManager):
    def __init__(
            self,
            version: str = None,
            os_type: str = None,
            path: str = None,
            name: str = "geckodriver",
            url: str = "https://github.com/mozilla/geckodriver/releases/download",
            latest_release_url: str = "https://api.github.com/repos/mozilla/geckodriver/releases/latest",
            mozila_release_tag: str = "https://api.github.com/repos/mozilla/geckodriver/releases/tags/{0}",
            cache_valid_range: int = 1,
            download_manager: DownloadManager = None,
    ):
        super(GeckoDriverManager, self).__init__(
            path, cache_valid_range, download_manager=download_manager
        )

        self.driver = GeckoDriver(
            version=version,
            os_type=os_type,
            name=name,
            url=url,
            latest_release_url=latest_release_url,
            mozila_release_tag=mozila_release_tag,
            http_client=self.http_client,
        )

    def install(self) -> str:
        driver_path = self._get_driver_path(self.driver)
        os.chmod(driver_path, 0o755)
        return driver_path
