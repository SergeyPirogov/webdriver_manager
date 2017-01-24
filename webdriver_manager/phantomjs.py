import os

from webdriver_manager import archive
from webdriver_manager import utils
from webdriver_manager.binary import Binary
from webdriver_manager.driver import PhantomJsDriver
from webdriver_manager.manager import DriverManager
from shutil import copyfile


class PhantomJsDriverManager(DriverManager):
    def __init__(self, version=None, os_type=utils.os_name()):
        DriverManager.__init__(self)
        self.driver = PhantomJsDriver(version, os_type)

    def install(self):
        cached_binary = self._file_manager.get_cached_binary(self.driver)
        if cached_binary:
            return cached_binary.path
        zip_file = self._file_manager._download_file(self.driver)
        files = archive.unpack(zip_file)

        from_dest = os.path.join(os.path.dirname(zip_file.name), files[2])
        to_dest = os.path.join(os.path.dirname(zip_file.name), os.path.basename(files[2]))

        copyfile(from_dest, to_dest)
        bin_file_path = Binary(to_dest).path
        os.chmod(bin_file_path, 0o755)
        return bin_file_path
