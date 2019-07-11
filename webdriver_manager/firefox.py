from webdriver_manager.archive import unpack
from webdriver_manager.driver import GeckoDriver
from webdriver_manager.manager import DriverManager
from webdriver_manager import utils


class GeckoDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_type()):
        # type: (str, str) -> GeckoDriverManager
        super(GeckoDriverManager, self).__init__()
        if os_type.startswith("mac"):
            os_type = "macos"

        self.driver = GeckoDriver(version=version,
                                  os_type=os_type)

    def install(self, path=None):
        # type: () -> str
        bin_file = self._file_manager.get_cached_binary(self.driver)

        if bin_file:
            return bin_file.path

        path = self._file_manager.download_driver(self.driver)

        unpack(path)

        bin_file = self._file_manager.get_cached_binary(self.driver)

        return bin_file.path
