import os

from webdriver_manager.utils import FileManager


class DriverManager:
    def __init__(self):
        self._file_manager = FileManager()

    def install(self):
        raise NotImplementedError("Please Implement this method")
