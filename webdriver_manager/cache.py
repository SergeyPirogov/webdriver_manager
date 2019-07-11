import glob
import os

import requests

from webdriver_manager.binary import Binary
from webdriver_manager.driver import Driver
from webdriver_manager.utils import console, write_file, get_filename_from_response


class CacheManager:
    def __init__(
            self,
            sub_folder="drivers",
            root_dir=os.path.dirname(os.path.abspath(__file__))):
        self.root_dir = root_dir
        self.sub_folder = sub_folder

    def get_cache_path(self):
        # type: () -> str
        return os.path.join(self.root_dir, self.sub_folder)

    def create_cache_dir(self, driver_path):
        # type: (str) -> bool
        path = os.path.join(self.get_cache_path(), driver_path)

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return os.path.exists(path)

    def find_file_if_exists(self, name):
        if len(name) == 0:
            return None

        path = self.get_cache_path()
        paths = [f for f in glob.glob(path + "/**", recursive=True)]

        if len(paths) == 0:
            return None

        for path in paths:
            if os.path.isfile(path) and path.endswith(name):
                print("File path [{}]".format(path))
                return path

        return None

    def get_cached_binary(self, driver):
        cached_driver_path = driver.config.driver_path

        path = self.find_file_if_exists(cached_driver_path)
        if path is not None:
            return Binary(path)

        name = driver.name
        version = driver.get_version()
        os_type = driver.os_type

        console("")
        console(
            "Checking for {} {}:{} in cache {}".format(
                os_type,
                name,
                version,
                self.get_cache_path()),
            bold=True)

        if "win" in os_type:
            name += ".exe"

        path = self.find_file_if_exists(name)

        if path is not None:
            console("Driver found at {}".format(path))
            return Binary(path)

        return None

    def download_driver(self, driver):
        # type: (Driver) -> Binary
        return self._save_driver_to_cache(driver.get_url(), driver)

    # TODO merge download driver and this method
    def download_binary(self, driver, path=None):
        if path is not None:
            path = os.path.abspath(path)
        cached_binary = self.get_cached_binary(driver, path)
        if cached_binary:
            return cached_binary
        return Binary(self._save_driver_to_cache(driver).name)

    def _save_driver_to_cache(self, url, driver):
        console("Trying to download new driver from {}".format(url))

        driver_path = os.path.join(self.get_cache_path(), driver.name, driver.get_version(), driver.os_type)

        response = requests.get(url, stream=True)

        if response.status_code == 404:
            raise ValueError(
                "There is no such driver {} with version {} by {}".format(driver.name,driver.get_version(), url))

        filename = get_filename_from_response(response, driver.name)

        self.create_cache_dir(driver_path)

        file_path = os.path.join(driver_path, filename)

        return write_file(response.content, file_path)
