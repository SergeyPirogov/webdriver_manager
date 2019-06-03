import os
import shutil
from webdriver_manager.driver import OperaDriver
from webdriver_manager.manager import DriverManager
from webdriver_manager import utils

from webdriver_manager import config


class OperaDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_type()):
        # type: (str, str) -> GeckoDriverManager
        super(OperaDriverManager, self).__init__()
        if os_type.startswith("mac"):
            os_type = "mac64"

        self.driver = OperaDriver(version=version,
                                  os_type=os_type)

    def install(self, path=None):
        # type: () -> str
        bin_file = self._file_manager.download_driver(self.driver, path)
        os.chmod(bin_file.path, 0o755)
        source = os.path.dirname(bin_file.path)
        for fname in os.listdir(source):
            if fname == "sha512_sum":
                os.remove(os.path.join(source, fname))
        print(bin_file.path)
        return bin_file.path