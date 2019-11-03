from webdriver_manager import utils
from webdriver_manager.driver import IEDriver
from webdriver_manager.manager import DriverManager


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
