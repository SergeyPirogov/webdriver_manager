import logging
import os

from webdriver_manager import utils
from webdriver_manager.driver import ChromeDriver
from webdriver_manager.logger import log
from webdriver_manager.manager import DriverManager
from webdriver_manager.utils import ChromeType, download_file


class ChromeDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 path=None,
                 name="chromedriver",
                 url="http://chromedriver.storage.googleapis.com",
                 latest_release_url="http://chromedriver.storage.googleapis.com/LATEST_RELEASE",
                 chrome_type=ChromeType.GOOGLE,
                 log_level=logging.INFO):
        super().__init__(path, log_level=log_level)

        self.driver = ChromeDriver(name=name,
                                   version=version,
                                   os_type=os_type,
                                   url=url,
                                   latest_release_url=latest_release_url,
                                   chrome_type=chrome_type)

    def install(self):
        driver_path = self.__get_driver_path(self.driver)

        os.chmod(driver_path, 0o755)
        return driver_path

    def __get_driver_path(self, driver):
        chrome_browser_version = driver.chrome_version
        log(f"Current {self.driver.chrome_type} version is {chrome_browser_version}", first_line=True)

        driver_name = driver.get_name()
        os_type = driver.get_os_type()
        driver_version = driver.get_version()

        binary_path = self.driver_cache.find_driver_in_cache(chrome_browser_version, driver_name, os_type,
                                                             driver_version)
        if binary_path:
            return binary_path

        file = download_file(driver.get_url())
        binary_path = self.driver_cache.save_file_to_cache(file, chrome_browser_version,
                                                           driver_name, os_type, driver_version)
        return binary_path
