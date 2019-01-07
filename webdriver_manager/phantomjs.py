import os
from webdriver_manager.driver import PhantomJsDriver
from webdriver_manager.manager import DriverManager
from webdriver_manager import utils


class PhantomJsDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_type()):
        # type: (str, str) -> None
        super(PhantomJsDriverManager, self).__init__()
        self.driver = PhantomJsDriver(version=version,
                                      os_type=os_type)

    def install(self, path=None):
        # type: () -> str

        filename = self.driver.get_url().split('/')[-1].split('.zip')[0].split('.tar')[0]
        subpath = os.path.join(filename, 'bin', 'phantomjs')
        if self.driver.os_type.startswith("win"):
            subpath += ".exe"

        bin_file = self._file_manager.download_driver(self.driver, path, subpath)
        os.chmod(bin_file.path, 0o755)
        return bin_file.path
