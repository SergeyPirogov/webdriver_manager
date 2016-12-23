import os
import requests

from webdriver_manager.utils import FileManager, OSUtils


class DriverManager:
    def __init__(self):
        self._file_manager = FileManager()
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder = ".drivers"

    def download_driver(self, url, name, version):
        target_dir_path = os.path.join(self.root_dir, self.folder, version)
        self._file_manager.download_driver(url, target_dir_path)
        driver_path = os.path.join(target_dir_path, name)
        os.chmod(driver_path, 0755)
        return driver_path

    def install(self):
        raise NotImplementedError("Please Implement this method")

    def get_driver_url(self):
        raise NotImplementedError("Please Implement this method")


class ChromeDriverManager(DriverManager):
    def __init__(self, version="latest"):
        DriverManager.__init__(self)
        self.driver_url = "http://chromedriver.storage.googleapis.com"
        self.driver_name = "chromedriver"
        self.driver_version = version

    def install(self):
        if self.driver_version == "latest":
            self.driver_version = self.get_latest_release_version()
        return self.download_driver(self.get_driver_url(), self.driver_name, self.driver_version)

    def get_driver_url(self):
        url = "{url}/{ver}/{name}_{os}.zip"
        return url.format(url=self.driver_url,
                          ver=self.driver_version,
                          name=self.driver_name,
                          os=OSUtils.os_name() + str(OSUtils.os_architecture()))

    def get_latest_release_version(self):
        file = requests.get(self.driver_url + "/LATEST_RELEASE")
        return file.text.rstrip()
