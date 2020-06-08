import logging
import os

from webdriver_manager import utils
from webdriver_manager.driver import ChromeDriver
from webdriver_manager.logger import log
from webdriver_manager.manager import DriverManager
from webdriver_manager.utils import ChromeType


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
        log(f"Current {self.driver.chrome_type} version is {self.driver.browser_version}", first_line=True)
        driver_path = self._get_driver_path(self.driver)

        os.chmod(driver_path, 0o755)
        return driver_path
