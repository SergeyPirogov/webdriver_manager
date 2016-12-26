from webdriver_manager import ff_config
from webdriver_manager.driver import FireFoxDriver
from webdriver_manager.manager import DriverManager
from webdriver_manager.utils import OSUtils


class GeckoDriverManager(DriverManager):
    def __init__(self, gh_token, version="latest",
                 name="geckodriver",
                 url="https://github.com/mozilla/geckodriver/releases/download",
                 os_type=OSUtils.os_name()):
        DriverManager.__init__(self)
        self.driver = FireFoxDriver(driver_url=url,
                                    name=name,
                                    version=version,
                                    os_type=os_type)
        self.set_token(gh_token)

    def install(self):
        return self._file_manager.download_driver(self.driver).path

    def set_token(self, token):
        ff_config.access_token = token
