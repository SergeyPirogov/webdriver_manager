from webdriver_manager.driver import EdgeDriver, IEDriver
from webdriver_manager.manager import DriverManager
from webdriver_manager import utils


class EdgeDriverManager(DriverManager):
    def __init__(self, version=None,
                 os_type=utils.os_name()):
        super(EdgeDriverManager, self).__init__()
        self.driver = EdgeDriver(version=version,
                                 os_type=os_type)

    def install(self, path=None):
        # type: () -> str
        return self._file_manager.download_binary(self.driver, path).path


class IEDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_type()):
        super(IEDriverManager, self).__init__()
        self.driver = IEDriver(version=version, os_type=os_type)

    def install(self, path=None):
        # type: () -> str
        return self._file_manager.download_driver(self.driver, path).path
