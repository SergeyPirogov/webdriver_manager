import os

from webdriver_manager.utils import FileManager, OSUtils


class DriverManager:
    def __init__(self):
        self._file_manager = FileManager()
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder = ".drivers"

    def install(self):
        raise NotImplementedError("Please Implement this method")


class ChromeDriverManager(DriverManager):
    def __init__(self, version="latest"):
        DriverManager.__init__(self)
        self.driver_url = "http://chromedriver.storage.googleapis.com"
        self.driver_name = "chromedriver"
        self.driver_version = version

    def install(self):
        target_dir_path = os.path.join(self.root_dir, self.folder, self.driver_version)
        self._file_manager.download_driver(self.get_driver_url(), target_dir_path)
        driver_path = os.path.join(target_dir_path, self.driver_name)
        os.chmod(driver_path, 0755)
        return driver_path

    def get_driver_url(self):
        url = "{url}/{ver}/{name}_{os}.zip"
        return url.format(url=self.driver_url,
                          ver=self.driver_version,
                          name=self.driver_name,
                          os=OSUtils.os_name() + str(OSUtils.os_architecture()))
