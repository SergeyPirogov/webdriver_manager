import os
import requests

from webdriver_manager.driver import ChromeDriver
from webdriver_manager.utils import FileManager, OSUtils


class DriverManager:
    def __init__(self):
        self._file_manager = FileManager()
        self.root_dir = os.path.dirname(os.path.abspath(__file__))

    def install(self):
        raise NotImplementedError("Please Implement this method")


class ChromeDriverManager(DriverManager):
    def __init__(self, version="latest",
                 name="chromedriver",
                 url="http://chromedriver.storage.googleapis.com"):
        DriverManager.__init__(self)
        self.driver = ChromeDriver(driver_url=url, name=name, version=version)

    def install(self, to_folder=".drivers"):
        to_directory = os.path.join(self.root_dir, to_folder)
        return self._file_manager.download_driver(self.driver, to_directory)


class GeckoDriverManager(DriverManager):
    def __init__(self, version="latest"):
        DriverManager.__init__(self)
        self.driver_url = "https://github.com/mozilla/geckodriver/releases/download"
        self.driver_name = "geckodriver"
        self.driver_version = version

    def install(self):
        if self.driver_version == "latest":
            self.driver_version = self.get_latest_release_version()
        return self.download_driver(self.get_url(), self.driver_name, self.driver_version)

    def get_latest_release_version(self):
        file = requests.get(self.driver_url + "/LATEST_RELEASE")
        return file.text.rstrip()
