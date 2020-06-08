import os

from webdriver_manager.driver_cache import DriverCache
from webdriver_manager.utils import download_file


class DriverManager(object):
    def __init__(self, root_dir=None, log_level=None):
        self.driver_cache = DriverCache(root_dir)
        global_log_level = os.getenv('WDM_LOG_LEVEL')
        if not global_log_level and log_level:
            os.environ['WDM_LOG_LEVEL'] = str(log_level)

    def install(self):
        raise NotImplementedError("Please Implement this method")

    def _get_driver_path(self, driver):
        browser_version = driver.browser_version

        driver_name = driver.get_name()
        os_type = driver.get_os_type()
        driver_version = driver.get_version()

        binary_path = self.driver_cache.find_driver(browser_version, driver_name, os_type,
                                                    driver_version)
        if binary_path:
            return binary_path

        file = download_file(driver.get_url())
        binary_path = self.driver_cache.save_file_to_cache(file, browser_version,
                                                           driver_name, os_type, driver_version)
        return binary_path
