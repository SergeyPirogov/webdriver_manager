from webdriver_manager.driver import FireFoxDriver
from webdriver_manager.manager import DriverManager


class GeckoDriverManager(DriverManager):

    def __init__(self, version="latest",
                 name="geckodriver",
                 url="https://github.com/mozilla/geckodriver/releases/download"):
        DriverManager.__init__(self)
        self.driver = FireFoxDriver(driver_url=url, name=name, version=version)

    def install(self):
        return self._file_manager.download_driver(self.driver)

