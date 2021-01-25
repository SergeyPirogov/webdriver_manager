import logging
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
                 "operasoftware/operachromiumdriver/releases/tags/{0}",
                 log_level=logging.INFO,
                 print_first_line=True,
                 cache_valid_range=1):
        super().__init__(path, log_level, print_first_line, cache_valid_range)

        self.driver = OperaDriver(name=name,
                                  version=version,
                                  os_type=os_type,
                                  url=url,
                                  latest_release_url=latest_release_url,
                                  opera_release_tag=opera_release_tag)

    def install(self):
        driver_path = self._get_driver_path(self.driver)
        if os.path.isfile(driver_path):
            os.chmod(driver_path, 0o755)
            return driver_path
        else:
            for name in os.listdir(driver_path):
                if 'sha512_sum' in name:
                    os.remove(os.path.join(driver_path, name))
                    break
            file_path = os.path.join(driver_path, os.listdir(driver_path)[0])
            os.chmod(file_path, 0o755)
            return file_path
