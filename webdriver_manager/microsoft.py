import os

from webdriver_manager.core import utils
from webdriver_manager.core.download_manager import DownloadManager
from webdriver_manager.drivers.edge import EdgeChromiumDriver
from webdriver_manager.drivers.ie import IEDriver
from webdriver_manager.core.manager import DriverManager


class IEDriverManager(DriverManager):
    def __init__(
            self,
            version: str = "latest",
            os_type: str = None,
            path: str = None,
            name: str = "IEDriverServer",
            url: str = "https://github.com/seleniumhq/selenium/releases/download",
            latest_release_url: str = "https://api.github.com/repos/seleniumhq/selenium/releases",
            ie_release_tag: str = "https://api.github.com/repos/seleniumhq/selenium/releases/tags/selenium-{0}",
            cache_valid_range: int = 1,
            download_manager: DownloadManager = None,
    ):
        super().__init__(path, cache_valid_range, download_manager=download_manager)
        self.driver = IEDriver(
            version=version,
            os_type=os_type,
            name=name,
            url=url,
            latest_release_url=latest_release_url,
            ie_release_tag=ie_release_tag,
            http_client=self.http_client,
        )

    def install(self) -> str:
        return self._get_driver_path(self.driver)


class EdgeChromiumDriverManager(DriverManager):
    def __init__(
            self,
            version: str = "latest",
            os_type: str = utils.os_type(),
            path: str = None,
            name: str = "edgedriver",
            url: str = "https://msedgedriver.azureedge.net",
            latest_release_url: str = "https://msedgedriver.azureedge.net/LATEST_RELEASE",
            cache_valid_range: int = 1,
            download_manager: DownloadManager = None,
    ):
        super().__init__(path, cache_valid_range, download_manager=download_manager)
        self.driver = EdgeChromiumDriver(
            version=version,
            os_type=os_type,
            name=name,
            url=url,
            latest_release_url=latest_release_url,
            http_client=self.http_client,
        )

    def install(self) -> str:
        driver_path = self._get_driver_path(self.driver)
        os.chmod(driver_path, 0o755)
        return driver_path
