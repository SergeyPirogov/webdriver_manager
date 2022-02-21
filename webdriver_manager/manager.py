import os

from webdriver_manager.driver_cache import DriverCache
from webdriver_manager.logger import log
from webdriver_manager.utils import download_file


class DriverManager(object):
    def __init__(self, root_dir=None, log_level=None, print_first_line=None, cache_valid_range=1):
        self.driver_cache = DriverCache(root_dir, cache_valid_range)
        if os.environ.get('WDM_PRINT_FIRST_LINE', str(print_first_line)) == 'True':
            log("\n", formatter='%(message)s', level=log_level)
        log("====== WebDriver manager ======", level=log_level)

    def install(self):
        raise NotImplementedError("Please Implement this method")

    def _get_driver_path(self, driver):
        binary_path = self.driver_cache.find_driver(driver)
        if binary_path:
            return binary_path

        file = download_file(driver.get_url(), driver.ssl_verify)
        binary_path = self.driver_cache.save_file_to_cache(driver, file)
        return binary_path
