import os

from configparser import ConfigParser

filename = 'config.ini'
folder = os.path.join(os.path.expanduser("~"), ".wdm")


class Configuration(object):
    def __init__(self, file_name,
                 config_folder, section=None):
        self._parser = ConfigParser()
        self.config_file_path = os.path.join(config_folder, file_name)
        self.section = section
        _default_config_path = os.path.join(
            os.path.dirname(__file__), 'default.ini')
        self._parser.read(_default_config_path)
        self._parser.read(self.config_file_path)

    def get(self, key):
        return self._parser.get(self.section, key)

    def set(self, key, value):
        if value is not None:
            self._parser.set(self.section, key, value)

    def __getattr__(self, item):
        return os.getenv(item.upper(), self.get(item))
