import os
import requests

from re import fullmatch
from typing import Optional

from webdriver_manager.core.download_manager import DownloadManager
from webdriver_manager.core.manager import DriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.drivers.chrome import ChromeDriver


class ChromeDriverManager(DriverManager):
    def __init__(
            self,
            version: Optional[str] = None,
            os_type: Optional[str] = None,
            path: Optional[str] = None,
            name: str = "chromedriver",
            url: str = "https://chromedriver.storage.googleapis.com",
            latest_release_url: str = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE",
            chrome_type: str = ChromeType.GOOGLE,
            get_version: bool = False,
            cache_valid_range: int = 1,
            download_manager: Optional[DownloadManager] = None,
    ):
        super().__init__(
            path,
            cache_valid_range=cache_valid_range,
            download_manager=download_manager)

        self.driver = ChromeDriver(
            name=name,
            version=get_chromedriver_version(version, get_version),
            os_type=os_type,
            url=url,
            latest_release_url=latest_release_url,
            chrome_type=chrome_type,
            http_client=self.http_client,
        )

    def install(self) -> str:
        driver_path = self._get_driver_path(self.driver)
        os.chmod(driver_path, 0o755)
        return driver_path

def get_chromedriver_version(browser_version, get_version):
    if (not get_version) or (browser_version is None):
        return browser_version
    elif fullmatch(r"\d+\.\d+\.\d+\.\d+", browser_version):
        browser_version = browser_version[:browser_version.rfind(".")]
    if fullmatch(r"\d+\.\d+\.\d+", browser_version) or fullmatch(
        r"\d+", browser_version
    ):
        version_response = requests.get(
            f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{browser_version}"
        )
        if version_response.status_code == 200:
            return version_response.text
        elif version_response.status_code == 404:
            raise ValueError(
                f"There is no such browser version number {browser_version}"
            )
        else:
            raise ValueError(
                f"response body:\n{version_response.text}\n"
                f"request url:\n{version_response.request.url}\n"
                f"response headers:\n{dict(version_response.headers)}\n"
            )
    else:
        raise ValueError(f"There is no such browser version number {browser_version}")
