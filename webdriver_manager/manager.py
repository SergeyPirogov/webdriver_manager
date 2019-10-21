from webdriver_manager.driver_cache import DriverCache
from webdriver_manager.utils import download_driver


class DriverManager(object):
    def __init__(self, root_dir=None):
        self.driver_cache = DriverCache(root_dir)

    def install(self):
        raise NotImplementedError("Please Implement this method")

    def __get_latest_driver_version(self, driver):
        latest_cached = self.driver_cache.get_latest_cached_driver_version(driver.get_name())
        if latest_cached is not None:
            return latest_cached

        return driver.get_latest_release_version()

    def __get_version_to_download(self, driver):
        driver_version = driver.get_version()

        if driver_version == "latest":
            return self.__get_latest_driver_version(driver), True
        return driver_version, False

    def __download_and_save_driver_to_cache(self, driver, driver_version):
        response = download_driver(driver.get_url(driver_version))
        return self.driver_cache.save_driver_to_cache(response, driver.get_name(), driver_version,
                                                      driver.get_os_type())

    def download_driver(self, driver):
        driver_version, is_latest = self.__get_version_to_download(driver)

        cached_path = self.driver_cache.find_file_if_exists(driver.get_name(), driver.get_os_type(),
                                                            driver_version, is_latest)
        if cached_path is not None:
            return cached_path

        path = self.__download_and_save_driver_to_cache(driver, driver_version)

        if is_latest:
            self.driver_cache.save_latest_driver_version_number_to_cache(driver.get_name(), driver_version)

        return path
