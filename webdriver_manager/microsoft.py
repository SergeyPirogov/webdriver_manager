import os
from typing import Optional

from .core.download_manager import DownloadManager, WDMDownloadManager
from .core.manager import DriverManager, INDEX_SITE_ROOT, NO_INDEX_SITE
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
            use_index=not NO_INDEX_SITE,
    ):
        download_manager = download_manager or WDMDownloadManager()
        driver = IEDriver(
            version=version,
            os_type=os_type,
            name=name,
            url=url,
            latest_release_url=latest_release_url,
            http_client=download_manager.http_client,
            use_index=use_index,
        )
        DriverManager.__init__(
            self, driver, path, cache_valid_range,
            download_manager=download_manager
        )

    def install(self) -> str:
        return self._get_driver_path(self.driver)


class EdgeChromiumDriverManager(DriverManager):
    def __init__(
            self,
            version: Optional[str] = None,
            os_type: str = None,
            path: Optional[str] = None,
            name: str = "edgedriver",
            url: str = f"{INDEX_SITE_ROOT}/edge",
            latest_release_url: str = f"{INDEX_SITE_ROOT}/edge/LATEST_RELEASE",
            cache_valid_range: int = 1,
            download_manager: Optional[DownloadManager] = None,
            use_index=not NO_INDEX_SITE,
    ):
        download_manager = download_manager or WDMDownloadManager()
        driver = EdgeChromiumDriver(
            version=version,
            os_type=os_type,
            name=name,
            url=url,
            latest_release_url=latest_release_url,
            http_client=download_manager.http_client,
            use_index=use_index,
        )
        DriverManager.__init__(
            self, driver, path, cache_valid_range,
            download_manager=download_manager
        )

    def install(self) -> str:
        driver_path = self._get_driver_path(self.driver)
        os.chmod(driver_path, 0o755)
        return driver_path
