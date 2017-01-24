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
        path = self.__extract_phantomjs_bin(zip_file)
        bin_file = Binary(path)
        os.chmod(bin_file.path, 0o755)
        return bin_file.path

    def __get_phantom_bin(self, files):
        for index, name in enumerate(files):
            if "/bin/phantomjs" in name:
                return files[index]

    def __extract_phantomjs_bin(self, zip_file):
        files = archive.unpack(zip_file)

        phantom_js = self.__get_phantom_bin(files)

        from_dest = os.path.join(os.path.dirname(zip_file.name), phantom_js)
        to_dest = os.path.join(os.path.dirname(zip_file.name), os.path.basename(phantom_js))

        copyfile(from_dest, to_dest)
        return to_dest
