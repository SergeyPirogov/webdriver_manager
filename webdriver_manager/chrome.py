import os

from webdriver_manager.driver import ChromeDriver
from webdriver_manager.manager import DriverManager
from webdriver_manager.utils import OSUtils


class ChromeDriverManager(DriverManager):
    def __init__(self, version="latest",
                 name="chromedriver",
                 url="http://chromedriver.storage.googleapis.com",
                 os_type=OSUtils.os_type()):
        DriverManager.__init__(self)
        self.driver = ChromeDriver(driver_url=url,
                                   name=name,
                                   version=version,
                                   os_type=os_type)

    def install(self):
        bin_file = self._file_manager.download_driver(self.driver)
        os.chmod(bin_file.path, 0o755)
        return bin_file.path
