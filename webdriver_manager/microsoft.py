import logging
import os

from webdriver_manager import utils
from webdriver_manager.driver import EdgeChromiumDriver
from webdriver_manager.driver import IEDriver
from webdriver_manager.manager import DriverManager


class IEDriverManager(DriverManager):
    def __init__(
        self,
        version="latest",
        os_type=utils.os_type(),
        path=None,
        name="IEDriverServer",
        url="https://github.com/seleniumhq/selenium/releases/download",
        latest_release_url="https://api.github.com/repos/seleniumhq/selenium/releases",
        ie_release_tag="https://api.github.com/repos/seleniumhq/selenium/releases/tags/selenium-{0}",
        log_level=logging.INFO,
        print_first_line=True,
        cache_valid_range=1,
    ):
        super().__init__(path, log_level, print_first_line, cache_valid_range)
        self.driver = IEDriver(
            version=version,
            os_type=os_type,
            name=name,
            url=url,
            latest_release_url=latest_release_url,
            ie_release_tag=ie_release_tag,
        )

    def install(self):
        return self._get_driver_path(self.driver)


class EdgeChromiumDriverManager(DriverManager):
    def __init__(
        self,
        version="latest",
        os_type=utils.os_type(),
        path=None,
        name="edgedriver",
        url="https://msedgedriver.azureedge.net",
        latest_release_url="https://msedgedriver.azureedge.net/LATEST_RELEASE",
        log_level=logging.INFO,
        print_first_line=None,
        cache_valid_range=1,
    ):
        super().__init__(path, log_level, print_first_line, cache_valid_range)
        self.driver = EdgeChromiumDriver(
            version=version,
            os_type=os_type,
            name=name,
            url=url,
            latest_release_url=latest_release_url,
        )

    def install(self):
        driver_path = self._get_driver_path(self.driver)

        os.chmod(driver_path, 0o755)
        return driver_path
