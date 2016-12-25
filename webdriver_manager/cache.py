import os
import re

import requests

from webdriver_manager.utils import Archive


class CacheManager:
    def __init__(self, to_folder=".drivers"):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.to_folder = to_folder

    def get_cache_path(self):
        return os.path.join(self.root_dir, self.to_folder)

    def create_cache_dir(self, folder_name, version):
        cache_path = self.get_cache_path()
        driver_path = os.path.join(cache_path, folder_name, version)
        if not os.path.exists(driver_path):
            os.makedirs(driver_path)
        return driver_path

    def download_driver(self, driver):
        zip_file = self._download_file(driver)
        return Archive.unpack(zip_file, driver.name)

    def _download_file(self, driver):
        response = requests.get(driver.get_url(), stream=True)
        if response.status_code == 404:
            raise ValueError("There is no such driver {0} with version {1} by {2}".format(driver.name,
                                                                                          driver.get_version(),
                                                                                          driver.get_url()))

        filename = self._get_filename_from_response(response, driver)
        dir_path = self.create_cache_dir(driver.name, driver.get_version())
        file_path = os.path.join(dir_path, filename)

        return self._save_file_to_cache(response, file_path)

    def _save_file_to_cache(self, response, path):
        with open(path, "wb") as code:
            code.write(response.content)
            code.close()
        return file(path)

    def _get_filename_from_response(self, response, driver):
        try:
            return re.findall("filename=(.+)", response.headers["content-disposition"])[0]
        except KeyError:
            return "{}.zip".format(driver.name)
