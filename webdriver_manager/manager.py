from webdriver_manager.archive import unpack
from webdriver_manager.cache import CacheManager
from webdriver_manager import config


class DriverManager(object):
    def __init__(self):
        self._file_manager = CacheManager(to_folder=config.folder,
                                          dir_name=config.folder)

    def install(self):
        raise NotImplementedError("Please Implement this method")

    def get_driver_bin(self, driver):
        bin_file = self._file_manager.get_cached_binary(driver)

        if bin_file:
            return bin_file

        path = self._file_manager.download_driver(driver)

        unpack(path)

        return self._file_manager.get_cached_binary(driver)
