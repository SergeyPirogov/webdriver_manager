import logging

from webdriver_manager import utils
from webdriver_manager.driver import GeckoDriver
from webdriver_manager.manager import DriverManager


class GeckoDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 path=None,
                 name="geckodriver",
                 url="https://github.com/mozilla/geckodriver/releases/download",
                 latest_release_url="https://api.github.com/repos/mozilla/geckodriver/releases/latest",
                 mozila_release_tag="https://api.github.com/repos/mozilla/geckodriver/releases/tags/{0}",
                 log_level=logging.INFO,
                 print_first_line=None,
                 cache_valid_range=1):
        super(GeckoDriverManager, self).__init__(path, log_level, print_first_line, cache_valid_range)

        self.driver = GeckoDriver(version=version,
                                  os_type=os_type,
                                  name=name,
                                  url=url,
                                  latest_release_url=latest_release_url,
                                  mozila_release_tag=mozila_release_tag)

    def install(self):
        return self._get_driver_path(self.driver)
