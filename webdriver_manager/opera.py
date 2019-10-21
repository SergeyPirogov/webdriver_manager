import os

from webdriver_manager import utils
from webdriver_manager.driver import OperaDriver
from webdriver_manager.manager import DriverManager


class OperaDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_type()):
        # type: (str, str) -> OperaDriverManager
        super(OperaDriverManager, self).__init__()
        if os_type.startswith("mac"):
            os_type = "mac64"

        self.driver = OperaDriver(version=version,
                                  os_type=os_type)

    def install(self, path=None):
        driver_path = self.download_driver(self.driver)
        os.chmod(driver_path, 0o755)
        return driver_path
