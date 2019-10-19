from webdriver_manager.cache import CacheManager
from webdriver_manager import config
from webdriver_manager.driver_cache import DriverCache
from webdriver_manager.utils import download_driver


class DriverManager(object):
    def __init__(self):
        self._file_manager = CacheManager(
            to_folder=config.folder, dir_name=config.folder)
        self.driver_cache = DriverCache()

    def install(self):
        raise NotImplementedError("Please Implement this method")

    def download_driver(self, driver):
        driver_version = driver.get_version()

        if driver_version == "latest":
            latest_cached = self.driver_cache.get_latest_cached_driver_version(driver.name)
            if latest_cached is None:
                driver_version = driver.get_latest_release_version()
            else:
                driver_version = latest_cached

        cached_path = self.driver_cache.find_file_if_exists(driver.name, driver.os_type,
                                                            driver_version)
        if cached_path is not None:
            return cached_path

        response = download_driver(driver.get_url(driver_version))
        path = self.driver_cache.save_driver_to_cache(response, driver.name, driver_version,
                                                      driver.os_type)

        if driver.get_version() == "latest":
            self.driver_cache.save_latest_driver_version_number_to_cache(driver.name, driver_version)

        return path
