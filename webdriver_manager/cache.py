import os
import re
import requests
from webdriver_manager import archive
from webdriver_manager.binary import Binary
from webdriver_manager.driver import Driver
from webdriver_manager.utils import console
import glob


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

        path = self.find_file_if_exists(self.get_cache_path(), name)

        if path is not None:
            console("Driver found at {}".format(path))
            return Binary(path)

        return None

    def download_driver(self, driver, path=None, subpath=None):
        # type: (Driver) -> Binary
        if path is not None:
            path = os.path.abspath(path)

        zip_file = self._download_file(driver, path)
        files = archive.unpack(zip_file)
        if subpath is None:
            subpath = files[0]
        return Binary(os.path.join(os.path.dirname(zip_file.name), subpath))

    # TODO merge download driver and this method
    def download_binary(self, driver, path=None):
        if path is not None:
            path = os.path.abspath(path)
        cached_binary = self.get_cached_binary(driver, path)
        if cached_binary:
            return cached_binary
        return Binary(self._download_file(driver).name)

    def _download_file(self, url, name):
        console("Trying to download new driver from {}".format(url))

        driver_path = self.get_cache_path()

        response = requests.get(url, stream=True)
        if response.status_code == 404:
            raise ValueError(
                "There is no such driver by {}".format(url))
        filename = self._get_filename_from_response(response, name)
        if '"' in filename:
            filename = filename.replace('"', "")

        self.create_cache_dir(driver_path)
        file_path = os.path.join(driver_path, filename)

        return self._save_file_to_cache(response, file_path)

    def _save_file_to_cache(self, response, path):
        with open(path, "wb") as code:
            code.write(response.content)
            code.close()
        return path

    def _get_filename_from_response(self, response, name):
        try:
            return re.findall("filename=(.+)",
                              response.headers["content-disposition"])[0]
        except KeyError:
            return "{}.zip".format(name)
        except IndexError:
            return name + ".exe"

    def _get_driver_path(self, name, version, os_type):
        cache_path = self.get_cache_path()
        return os.path.join(cache_path, name, version, os_type)

    def get_driver_binary_path(self, name, version, os_type):
        # type: (str, str) -> str
        directory = self._get_driver_path(name, version, os_type)
        return os.path.join(directory, name)
