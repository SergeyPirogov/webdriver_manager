from webdriver_manager.driver import GeckoDriver
from webdriver_manager.manager import DriverManager
from webdriver_manager import utils


class GeckoDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_name()):
        # type: (str, str) -> GeckoDriverManager
        super(GeckoDriverManager, self).__init__()
        self.driver = GeckoDriver(version=version,
                                  os_type=os_type)

    def install(self):
        # type: () -> str
        return self._file_manager.download_driver(self.driver).path
