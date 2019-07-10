from webdriver_manager.cache import CacheManager
from webdriver_manager import config


class DriverManager(object):
    def __init__(self):
        self._file_manager = CacheManager(dir_name=config.folder)

    def install(self):
        raise NotImplementedError("Please Implement this method")
