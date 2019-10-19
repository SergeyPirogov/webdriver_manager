from webdriver_manager import utils
from webdriver_manager.driver import IEDriver
from webdriver_manager.manager import DriverManager


class IEDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_type()):
        super(IEDriverManager, self).__init__()
        self.driver = IEDriver(version=version, os_type=os_type)

    def install(self, path=None):
        return self.download_driver(self.driver)
