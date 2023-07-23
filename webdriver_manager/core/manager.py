from webdriver_manager.core.download_manager import WDMDownloadManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.logger import log


class DriverManager(object):
    def __init__(
            self,
            download_manager=None,
            cache_manager=None
    ):
        self._cache_manager = cache_manager
        if not self._cache_manager:
            self._cache_manager = DriverCacheManager()

        self._download_manager = download_manager
        if self._download_manager is None:
            self._download_manager = WDMDownloadManager()
        log("====== WebDriver manager ======")

    @property
    def http_client(self):
        return self._download_manager.http_client

    def install(self) -> str:
        raise NotImplementedError("Please Implement this method")

    def _get_driver_binary_path(self, driver):
        binary_path = self._cache_manager.find_driver(driver)
        if binary_path:
            return binary_path

        file = self._download_manager.download_file(driver.get_driver_download_url())
        binary_path = self._cache_manager.save_file_to_cache(driver, file)
        return binary_path
