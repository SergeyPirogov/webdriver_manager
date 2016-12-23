import StringIO
import zipfile
import platform
import sys

import requests


class FileManager:
    def __init__(self):
        pass

    def _download_zip(self, url):
        r = requests.get(url, stream=True)
        return zipfile.ZipFile(StringIO.StringIO(r.content))

    def _extract_zip(self, zip_file, path):
        zip_file.extractall(path)

    def download_driver(self, url, path):
        try:
            zip_file = self._download_zip(url)
            self._extract_zip(zip_file, path)
        except zipfile.BadZipfile:
            raise ValueError("No such driver found by url {0}. Wrong url or driver version".format(url))


class OSUtils:
    @staticmethod
    def os_name():
        pl = sys.platform
        if pl == "linux" or pl == "linux2":
            return "linux"
        elif pl == "darwin":
            return "mac"
        elif pl == "win32":
            return "windows"

    @staticmethod
    def os_architecture():
        bits = platform.architecture()[0]
        if bits == "64bit":
            return 64
        return 32
