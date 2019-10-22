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
                 mozila_release_tag="https://api.github.com/repos/mozilla/geckodriver/releases/tags/{0}"):
        super(GeckoDriverManager, self).__init__(path)

        self.driver = GeckoDriver(version=version,
                                  os_type=os_type,
                                  name=name,
                                  url=url,
                                  latest_release_url=latest_release_url,
                                  mozila_release_tag=mozila_release_tag)

    def install(self):
        return self.download_driver(self.driver)
