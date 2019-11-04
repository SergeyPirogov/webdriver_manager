from webdriver_manager.utils import utils
from webdriver_manager.drivers.driver import IEDriver
from webdriver_manager.drivers.manager import DriverManager

from webdriver_manager.drivers.driver import EdgeChromiumDriver


class IEDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 name="IEDriverServer",
                 url="http://selenium-release.storage.googleapis.com",
                 latest_release_url=None):
        super(IEDriverManager, self).__init__()
        self.driver = IEDriver(version=version,
                               os_type=os_type,
                               name=name,
                               url=url,
                               latest_release_url=latest_release_url)

    def install(self):
        return self.download_driver(self.driver)


class EdgeChromiumDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 name="edgedriver",
                 url="https://msedgedriver.azureedge.net",
                 latest_release_url="https://msedgedriver.azureedge.net/LATEST_CANARY",
                 latest_version="80.0.320.0"):
        super(EdgeChromiumDriverManager, self).__init__()
        self.driver = EdgeChromiumDriver(version=version,
                                         os_type=os_type,
                                         name=name,
                                         url=url,
                                         latest_release_url=latest_release_url,
                                         latest_version=latest_version)

    def install(self):
        return self.download_driver(self.driver)
