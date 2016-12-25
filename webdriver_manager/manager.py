from webdriver_manager.cache import CacheManager


class DriverManager:
    def __init__(self):
        self._file_manager = CacheManager()

    def install(self):
        raise NotImplementedError("Please Implement this method")
