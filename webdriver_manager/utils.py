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

    def download(self, driver):
        response = requests.get(driver.get_url(), stream=True)
        if response.status_code == 404:
            raise ValueError("There is no such driver {0} with version {1} by {2}".format(driver.name,
                                                                                          driver.get_version(),
                                                                                          driver.get_url()))
        try:
            return zipfile.ZipFile(StringIO.StringIO(response.content))
        except zipfile.BadZipfile:
            return gzip.GzipFile(fileobj=StringIO.StringIO(response.content), filename=driver.name)

    def extract_zip(self, zip_file, to_directory):
        if isinstance(zip_file, zipfile.ZipFile):
            zip_file.extractall(to_directory)
        elif isinstance(zip_file, gzip.GzipFile):
            self.extract_tar_file(zip_file, to_directory)
        else:
            raise ValueError("Bad zip file")

    def extract_tar_file(self, tar, to_directory):
        out_file_path = os.path.join(to_directory, tar.filename)
        if not os.path.exists(to_directory):
            os.makedirs(to_directory)
        with open(out_file_path, 'w') as outfile:
            outfile.write(tar.read())

    def download_driver(self, driver, to_dir):
        zip_file = self.download(driver)
        driver_path = os.path.join(to_dir, driver.name, driver.get_version())
        self.extract_zip(zip_file, driver_path)
        return os.path.join(driver_path, driver.name)


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
