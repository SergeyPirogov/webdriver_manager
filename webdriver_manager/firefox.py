import os
from typing import Optional
from urllib.parse import urljoin

from .core.download_manager import DownloadManager, WDMDownloadManager
from .core.manager import DriverManager, get_driver_site
from .drivers.firefox import GeckoDriver


class GeckoDriverManager(DriverManager):
    def __init__(
            self,
            version: Optional[str] = None,
            os_type: Optional[str] = None,
            path: Optional[str] = None,
            name: str = "geckodriver",
            url: str = f"firefox",
            latest_release_url: str = f"firefox/LATEST_RELEASE",
            cache_valid_range: int = 1,
            download_manager: Optional[DownloadManager] = None,
    ):
        download_manager = download_manager or WDMDownloadManager()

        driver = GeckoDriver(
            version=version,
            os_type=os_type,
            name=name,
            url=urljoin(get_driver_site(), url),
            latest_release_url=urljoin(get_driver_site(), latest_release_url),
            http_client=download_manager.http_client,
        )
        DriverManager.__init__(
            self, driver, path,
            cache_valid_range=cache_valid_range,
            download_manager=download_manager
        )

    def install(self) -> str:
        driver_path = self._get_driver_path(self.driver)
        os.chmod(driver_path, 0o755)
        return driver_path
