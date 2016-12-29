import logging
import os
import re

import requests

from webdriver_manager.binary import Binary
from webdriver_manager.utils import Archive


class CacheManager:
    def __init__(self, to_folder=".drivers"):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.to_folder = to_folder

    def get_cache_path(self):
        return os.path.join(self.root_dir, self.to_folder)

    def create_cache_dir(self, driver_path):
        if not os.path.exists(driver_path):
            os.makedirs(driver_path)

    def get_cached_binary(self, name, version, os_type):
        logging.warning("Checking for {} {}:{} in cache".
                        format(os_type, name, version))
        if "win" in os_type:
            name += ".exe"
        for dirName, subdirList, fileList in os.walk(self.get_cache_path()):
            for fname in fileList:
                if os.path.join(dirName, fname).endswith(os.path.join(version, name)):
                    logging.warning("Driver found in cache {}/{}".format(dirName, fname))
                    return Binary(os.path.join(dirName, fname))
        logging.warning("There is no cached driver. Downloading new one...")
        return None

    def download_driver(self, driver):
        cached_binary = self.get_cached_binary(driver.name, driver.get_version(), driver.os_type)
        if cached_binary:
            return cached_binary
        zip_file = self._download_file(driver)
        files = Archive.unpack(zip_file)
        return Binary(os.path.join(os.path.dirname(zip_file.name), files[0]))

    def _download_file(self, driver):
        response = requests.get(driver.get_url(), stream=True)
        if response.status_code == 404:
            raise ValueError("There is no such driver {0} with version {1} by {2}".format(driver.name,
                                                                                          driver.get_version(),
                                                                                          driver.get_url()))

        filename = self._get_filename_from_response(response, driver)
        driver_path = self._get_driver_path(driver.name, driver.get_version())
        self.create_cache_dir(driver_path)
        file_path = os.path.join(driver_path, filename)

        return self._save_file_to_cache(response, file_path)

    def _save_file_to_cache(self, response, path):
        with open(path, "wb") as code:
            code.write(response.content)
            code.close()
        return open(path, "rb")

    def _get_filename_from_response(self, response, driver):
        try:
            return re.findall("filename=(.+)", response.headers["content-disposition"])[0]
        except KeyError:
            return "{}.zip".format(driver.name)

    def _get_driver_path(self, name, version):
        cache_path = self.get_cache_path()
        return os.path.join(cache_path, name, version)

    def get_driver_binary_path(self, name, version):
        return os.path.join(self._get_driver_path(name, version), name)
