from webdriver_manager.core.download_manager import WDMDownloadManager
from webdriver_manager.core.driver_cache import DriverCache
from webdriver_manager.core.logger import log


class DriverManager(object):
    def __init__(
            self,
            root_dir=None,
            cache_valid_range=1,
            download_manager=None):
        self.driver_cache = DriverCache(root_dir, cache_valid_range)
        self._download_manager = download_manager
        if download_manager is None:
            self._download_manager = WDMDownloadManager()
        print('', flush=True)  # this is just to make log output a better
        log("====== WebDriver manager ======")

    @property
    def http_client(self):
        return self._download_manager.http_client

    def install(self) -> str:
        raise NotImplementedError("Please Implement this method")

    def _get_driver_path(self, driver):
        binary_path = self.driver_cache.find_driver(driver)
        if binary_path:
            return binary_path

        file = self._download_manager.download_file(driver.get_url())
        binary_path = self.driver_cache.save_file_to_cache(driver, file)
        return binary_path
