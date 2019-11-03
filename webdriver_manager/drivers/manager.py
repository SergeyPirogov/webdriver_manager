from abc import abstractmethod

from webdriver_manager.utils.cache import CacheManager
from webdriver_manager import config


class DriverManager(object):
    def __init__(self):
        self._file_manager = CacheManager(
            to_folder=config.folder, dir_name=config.folder)

    @abstractmethod
    def install(self):
        """
        Method to install the webdriver binary
        :return:
        """
        raise NotImplementedError("Please Implement this method")
