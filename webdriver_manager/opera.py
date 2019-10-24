import os

from webdriver_manager import utils
from webdriver_manager.driver import OperaDriver
from webdriver_manager.manager import DriverManager


class OperaDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 path=None,
                 name="operadriver",
                 url="https://github.com/operasoftware/operachromiumdriver/"
                 "releases/",
                 latest_release_url="https://api.github.com/repos/"
                 "operasoftware/operachromiumdriver/releases/latest",
                 opera_release_tag="https://api.github.com/repos/"
                 "operasoftware/operachromiumdriver/releases/tags/{0}"):
        super(OperaDriverManager, self).__init__()

        self.driver = OperaDriver(name=name,
                                  version=version,
                                  os_type=os_type,
                                  url=url,
                                  latest_release_url=latest_release_url,
                                  opera_release_tag=opera_release_tag)

    def install(self):
        driver_path = self.download_driver(self.driver)
        if os.path.isfile(driver_path):
            os.chmod(driver_path, 0o755)
            return driver_path
        else:
            file_path = None
            for name in os.listdir(driver_path):
                abs_path = os.path.join(driver_path, name)
                if 'opera' in name:
                    os.chmod(abs_path, 0o755)
                    file_path = abs_path
                elif 'sha512_sum' in name:
                    os.remove(abs_path)
            return file_path
