from webdriver_manager.driver import EdgeDriver, IEDriver
from webdriver_manager.manager import DriverManager
from webdriver_manager import utils


class EdgeDriverManager(DriverManager):
    def __init__(self, version=None,
                 os_type=utils.os_name()):
        DriverManager.__init__(self)
        self.driver = EdgeDriver(version=version,
                                 os_type=os_type)

    def install(self):
        return self._file_manager.download_binary(self.driver).path


class IEDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_type()):
        DriverManager.__init__(self)
        self.driver = IEDriver(version=version, os_type=os_type)

    def install(self):
        return self._file_manager.download_driver(self.driver).path
