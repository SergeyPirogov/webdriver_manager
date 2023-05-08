import os

from .download_manager import WDMDownloadManager
from .driver import Driver
from .driver_cache import DriverCache
from .logger import log


def get_driver_site():
    drive_site = os.environ.get(
        'DRIVER_SITE',
        'https://huggingface.co/datasets/HansBug/browser_drivers_mirror/resolve/main'
    )
    if not drive_site.endswith('/'):
        drive_site = f'{drive_site}/'

    return drive_site


class DriverManager(object):
    def __init__(
            self,
            driver: Driver,
            root_dir=None,
            cache_valid_range=1,
            download_manager=None
    ):
        self.driver = driver
        self.driver_cache = DriverCache(root_dir, cache_valid_range)
        self._download_manager = download_manager
        if download_manager is None:
            self._download_manager = WDMDownloadManager()
        log("====== WebDriver manager ======")

    @property
    def http_client(self):
        return self._download_manager.http_client

    def install(self) -> str:
        raise NotImplementedError  # pragma: no cover

    def _get_driver_path(self, driver):
        binary_path = self.driver_cache.find_driver(driver)
        if binary_path:
            return binary_path

        url = driver.get_driver_download_url()
        file = self._download_manager.download_file(url)
        binary_path = self.driver_cache.save_file_to_cache(driver, file)
        return binary_path

    @property
    def latest_version(self):
        return self.driver.get_latest_release_version()

    @property
    def version_to_download(self):
        return self.driver.get_driver_version_to_download()

    @property
    def driver_url(self):
        return self.driver.get_driver_download_url()

    @property
    def browser_version(self):
        return self.driver.get_browser_version_from_os()

    @property
    def driver_executable(self):
        return self.install()
