from webdriver_manager.cache import CacheManager
from webdriver_manager import config


class DriverManager(object):
    def __init__(self):
        self._file_manager = CacheManager(root_dir=config.folder)

    def install(self):
        raise NotImplementedError("Please Implement this method")
