import os
from typing import Optional
from urllib.parse import urljoin

from .core.download_manager import DownloadManager, WDMDownloadManager
from .core.manager import DriverManager, get_driver_site
from .core.utils import ChromeType
from .drivers.chrome import ChromeDriver


class ChromeDriverManager(DriverManager):
    def __init__(
            self,
            version: Optional[str] = None,
            os_type: Optional[str] = None,
            path: Optional[str] = None,
            name: str = "chromedriver",
            url: str = f'google',
            latest_release_url: str = f'google/LATEST_RELEASE',
            chrome_type: str = ChromeType.GOOGLE,
            cache_valid_range: int = 1,
            download_manager: Optional[DownloadManager] = None,
    ):
        download_manager = download_manager or WDMDownloadManager()
        driver = ChromeDriver(
            name=name,
            version=version,
            os_type=os_type,
            url=urljoin(get_driver_site(), url),
            latest_release_url=urljoin(get_driver_site(), latest_release_url),
            chrome_type=chrome_type,
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
