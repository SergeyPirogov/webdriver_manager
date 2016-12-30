from webdriver_manager.driver import EdgeDriver
from webdriver_manager.manager import DriverManager
from webdriver_manager.utils import OSUtils


class EdgeDriverManager(DriverManager):
    def __init__(self, version="latest",
                 name="MicrosoftWebDriver",
                 url="https://download.microsoft.com/download/3/2/D/32D3E464-F2EF-490F-841B-05D53C848D15/",
                 os_type=OSUtils.os_name()):
        DriverManager.__init__(self)
        self.driver = EdgeDriver(driver_url=url,
                                 name=name,
                                 version=version,
                                 os_type=os_type)

    def install(self):
        return self._file_manager.download_binary(self.driver).path
