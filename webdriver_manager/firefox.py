import requests

from webdriver_manager.manager import DriverManager


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
