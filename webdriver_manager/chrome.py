import os

from webdriver_manager.archive import unpack
from webdriver_manager.driver import ChromeDriver
from webdriver_manager.manager import DriverManager
from webdriver_manager import utils


class ChromeDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_type()):
        # type: (str, str) -> None
        super(ChromeDriverManager, self).__init__()
        # there is no driver with 64 bit
        if os_type == "win64":
            os_type = "win32"
        self.driver = ChromeDriver(version=version,
                                   os_type=os_type)

    def install(self):
        # type: () -> str
        bin_file = self.get_driver_bin(self.driver).path

        os.chmod(bin_file, 0o755)
        return bin_file
