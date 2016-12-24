import os
import platform
import re
import sys
import tarfile
import zipfile

import requests


class FileManager:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))

    def download_file(self, driver, to_dir):
        response = requests.get(driver.get_url(), stream=True)
        if response.status_code == 404:
            raise ValueError("There is no such driver {0} with version {1} by {2}".format(driver.name,
                                                                                          driver.get_version(),
                                                                                          driver.get_url()))

        filename = self._get_filename(response)

        dir_path = os.path.join(self.root_dir, to_dir, driver.name, driver.get_version())
        file_path = os.path.join(dir_path, filename)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(file_path, "wb") as code:
            code.write(response.content)
            code.close()
        return file(file_path)

    def _get_filename(self, response):
        try:
            return re.findall("filename=(.+)", response.headers["content-disposition"])[0]
        except KeyError:
            return "driver.zip"

    def extract_zip(self, zip_file, to_directory):
        zipfile.ZipFile(zip_file).extractall(to_directory)

    def extract_tar_file(self, tar_file, to_dir):
        tar = tarfile.open(tar_file.name, mode="r:gz")
        tar.extractall(to_dir)
        tar.close()

    def download_driver(self, driver, to_dir):
        zip_file = self.download_file(driver, to_dir)
        to_directory = os.path.dirname(zip_file.name)
        if zip_file.name.endswith(".zip"):
            self.extract_zip(zip_file, to_directory)
        else:
            self.extract_tar_file(zip_file, to_directory)
        return os.path.join(os.path.dirname(zip_file.name), driver.name)


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
