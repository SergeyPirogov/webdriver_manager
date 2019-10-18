from webdriver_manager.driver import GeckoDriver
from webdriver_manager.driver_cache import DriverCache
from webdriver_manager.manager import DriverManager
from webdriver_manager import utils
from webdriver_manager.utils import download_driver


class GeckoDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_type()):
        # type: (str, str) -> GeckoDriverManager
        super(GeckoDriverManager, self).__init__()
        if os_type.startswith("mac"):
            os_type = "macos"

        self.driver = GeckoDriver(version=version,
                                  os_type=os_type)
        self.driver_cache = DriverCache()

    def install(self, path=None):
        cached_path = self.driver_cache.find_file_if_exists(self.driver.os_type, self.driver.name,
                                                            self.driver.get_version())
        if cached_path is not None:
            return cached_path

        response = download_driver(self.driver.get_url())
        path = self.driver_cache.save_driver_to_cache(response, self.driver.name, self.driver.get_version(),
                                                      self.driver.os_type)

        if self.driver._version == "latest":
            latest_version = self.driver.get_latest_release_version()
            self.driver_cache.save_latest_driver_version_number_to_cache(self.driver.name, latest_version)

        return path
