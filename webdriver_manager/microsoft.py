import os
from typing import Optional

from .core import utils
from .core.download_manager import DownloadManager
from .core.manager import DriverManager, INDEX_SITE_ROOT
from .drivers.edge import EdgeChromiumDriver
from .drivers.ie import IEDriver


class IEDriverManager(DriverManager):
    def __init__(
            self,
            version: Optional[str] = None,
            os_type: Optional[str] = None,
            path: Optional[str] = None,
            name: str = "IEDriverServer",
            url: str = f"{INDEX_SITE_ROOT}/ie",
            latest_release_url: str = f"{INDEX_SITE_ROOT}/ie/LATEST_RELEASE",
            cache_valid_range: int = 1,
            download_manager: Optional[DownloadManager] = None,
    ):
        super().__init__(path, cache_valid_range, download_manager=download_manager)
        self.driver = IEDriver(
            version=version,
            os_type=os_type,
            name=name,
            url=url,
            latest_release_url=latest_release_url,
            http_client=self.http_client,
        )

    def install(self) -> str:
        return self._get_driver_path(self.driver)


class EdgeChromiumDriverManager(DriverManager):
    def __init__(
            self,
            version: Optional[str] = None,
            os_type: str = utils.os_type(),
            path: Optional[str] = None,
            name: str = "edgedriver",
            url: str = f"{INDEX_SITE_ROOT}/edge",
            latest_release_url: str = f"{INDEX_SITE_ROOT}/edge/LATEST_RELEASE",
            cache_valid_range: int = 1,
            download_manager: Optional[DownloadManager] = None,
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
