import os

from webdriver_manager.driver import ChromeDriver
from webdriver_manager.manager import DriverManager


class ChromeDriverManager(DriverManager):
    def __init__(self, version="latest",
                 name="chromedriver",
                 url="http://chromedriver.storage.googleapis.com"):
        DriverManager.__init__(self)
        self.driver = ChromeDriver(driver_url=url, name=name, version=version)

    def install(self, to_folder=".drivers"):
        to_directory = os.path.join(self.root_dir, to_folder)
        path = self._file_manager.download_driver(self.driver, to_directory)
        os.chmod(path, 0755)
        return path
