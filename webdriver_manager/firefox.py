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

    def install(self, path=None):
        return self.download_driver(self.driver)
