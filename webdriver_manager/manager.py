import os

from webdriver_manager.utils import FileManager


class DriverManager:
    def __init__(self):
        self._file_manager = FileManager()
        self.root_dir = os.path.dirname(os.path.abspath(__file__))

    def install(self):
        raise NotImplementedError("Please Implement this method")
