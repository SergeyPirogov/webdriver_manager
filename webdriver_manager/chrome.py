import os
from typing import Optional

from .core.download_manager import DownloadManager, WDMDownloadManager
from .core.manager import DriverManager, INDEX_SITE_ROOT, NO_INDEX_SITE
from .core.utils import ChromeType
from .drivers.chrome import ChromeDriver


class ChromeDriverManager(DriverManager):
    def __init__(
            self,
            version: Optional[str] = None,
            os_type: Optional[str] = None,
            path: Optional[str] = None,
            name: str = "chromedriver",
            url: str = f'{INDEX_SITE_ROOT}/google',
            latest_release_url: str = f'{INDEX_SITE_ROOT}/google/LATEST_RELEASE',
            chrome_type: str = ChromeType.GOOGLE,
            cache_valid_range: int = 1,
            download_manager: Optional[DownloadManager] = None,
            use_index=not NO_INDEX_SITE,
    ):
        download_manager = download_manager or WDMDownloadManager()
        driver = ChromeDriver(
            name=name,
            version=version,
            os_type=os_type,
            url=url,
            latest_release_url=latest_release_url,
            chrome_type=chrome_type,
            http_client=download_manager.http_client,
            use_index=use_index,
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
