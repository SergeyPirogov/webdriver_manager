import StringIO
import gzip
import os
import platform
import sys
import zipfile

import requests


class FileManager:
    def __init__(self):
        pass

    def _download_zip(self, url):
        response = requests.get(url, stream=True)
        try:
            return zipfile.ZipFile(StringIO.StringIO(response.content))
        except zipfile.BadZipfile:
            return gzip.GzipFile(fileobj=StringIO.StringIO(response.content))

    def _extract_zip(self, zip_file, path):
        try:
            zip_file.extractall(path)
        except Exception:
            self.extract_tar_file(zip_file, path, "geckodriver")

    def extract_tar_file(self, tar, to_directory, filename):
        out_file_path = os.path.join(to_directory, filename)
        with open(out_file_path, 'w') as outfile:
            outfile.write(tar.read())

    def download_driver(self, url, path):
        zip_file = self._download_zip(url)
        self._extract_zip(zip_file, path)


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
