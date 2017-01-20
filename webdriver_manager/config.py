import os
import ConfigParser

filename = 'config.ini'
folder = os.path.join(os.path.expanduser("~"), ".wdm")

_default_values = {
    'gh_token': '',
    'mozila_latest_release': 'https://api.github.com/repos/mozilla/geckodriver/releases/latest',
    'mozila_release_tag': 'https://api.github.com/repos/mozilla/geckodriver/releases/tags/{0}'
}


class Configuration(object):
    def __init__(self, file_name=filename,
                 config_folder=folder):
        self._parser = ConfigParser.SafeConfigParser(defaults=_default_values)
        self.config_file_path = os.path.join(config_folder, file_name)

    def get(self, key, default=None):
        self._parser.read(self.config_file_path)
        _defaults = self._parser.defaults()
        return _defaults.get(key, default)

    def __getattr__(self, item):
        return self.get(item)
