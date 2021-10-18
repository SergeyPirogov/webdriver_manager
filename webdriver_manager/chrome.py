import os

from webdriver_manager import utils
from webdriver_manager.driver import ChromeDriver
from webdriver_manager.logger import logger
from webdriver_manager.manager import DriverManager
from webdriver_manager.utils import ChromeType


class ChromeDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 path=None,
                 name="chromedriver",
                 url="https://chromedriver.storage.googleapis.com",
                 latest_release_url="https://chromedriver.storage.googleapis.com/LATEST_RELEASE",
                 chrome_type=ChromeType.GOOGLE,
                 print_first_line=True,
                 cache_valid_range=1):
        super().__init__(path, print_first_line=print_first_line,
                         cache_valid_range=cache_valid_range)

        self.driver = ChromeDriver(name=name,
                                   version=version,
                                   os_type=os_type,
                                   url=url,
                                   latest_release_url=latest_release_url,
                                   chrome_type=chrome_type)

    def install(self):
        logger.info(f"Current {self.driver.chrome_type} version is {self.driver.browser_version}")
        driver_path = self._get_driver_path(self.driver)

        os.chmod(driver_path, 0o755)
        return driver_path
