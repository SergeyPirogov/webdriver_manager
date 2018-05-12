import os
import re
import requests
from webdriver_manager import archive
from webdriver_manager.binary import Binary
from webdriver_manager.driver import Driver
from webdriver_manager.utils import console


class CacheManager:
    def __init__(
            self,
            to_folder=".drivers",
            dir_name=os.path.dirname(
                os.path.abspath(__file__))):
        self.root_dir = dir_name
        self.to_folder = to_folder

    def get_cache_path(self):
        # type: () -> str
        return os.path.join(self.root_dir, self.to_folder)

    def create_cache_dir(self, driver_path):
        # type: (str) -> None
        if not os.path.exists(driver_path):
            os.makedirs(driver_path)

    def get_cached_binary(self, driver, path=None):
        if path is not None:
            self.root_dir = path
        cached_driver = driver.config.driver_path
        is_offline = driver.config.offline
        if cached_driver and is_offline == 'True':
            console("Using driver from cache {}".format(cached_driver))
            return Binary(cached_driver)

        name = driver.name
        version = driver.get_version()
        os_type = driver.os_type
        console("")
        console(
            "Checking for {} {}:{} in cache".format(
                os_type,
                name,
                version),
            bold=True)
        if "win" in os_type:
            name += ".exe"
        if path is None:
            for dirName, subdirList, fileList in \
                    os.walk(self.get_cache_path()):
                for fname in fileList:
                    target_file = os.path.join(version, os_type, name)
                    driver_file = os.path.join(dirName, fname)

                    if driver_file.endswith(target_file):
                        console("Driver found in {}/{}".format(dirName, fname))
                        return Binary(os.path.join(dirName, fname))
        else:
            if os.path.isfile(os.path.join(path, name)):
                console("Driver found in {}".format(os.path.join(path, name)))
                return Binary(os.path.join(path, name))
        console("There is no cached driver. Downloading new one...")
        return None

    def download_driver(self, driver, path=None):
        # type: (Driver) -> Binary
        if path is not None:
            path = os.path.abspath(path)
        cached_binary = self.get_cached_binary(driver, path)
        if cached_binary:
            return cached_binary
        zip_file = self._download_file(driver, path)
        files = archive.unpack(zip_file)
        return Binary(os.path.join(os.path.dirname(zip_file.name), files[0]))

    # TODO merge download driver and this method
    def download_binary(self, driver, path=None):
        if path is not None:
            path = os.path.abspath(path)
        cached_binary = self.get_cached_binary(driver, path)
        if cached_binary:
            return cached_binary
        return Binary(self._download_file(driver).name)

    def _download_file(self, driver, path=None):
        # type: (Driver) -> file
        url = driver.get_url()
        console("Trying to download new driver from {}".format(url))

        response = requests.get(url, stream=True)
        if response.status_code == 404:
            raise ValueError(
                "There is no such driver {0} with version {1} by {2}".format(
                    driver.name, driver.get_version(), driver.get_url()))
        filename = self._get_filename_from_response(response, driver)
        if '"' in filename:
            filename = filename.replace('"', "")
        if path is None:
            driver_path = self._get_driver_path(driver.name,
                                                driver.get_version(),
                                                driver.os_type)
        else:
            driver_path = path
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
            return re.findall("filename=(.+)",
                              response.headers["content-disposition"])[0]
        except KeyError:
            return "{}.zip".format(driver.name)
        except IndexError:
            return driver.name + ".exe"

    def _get_driver_path(self, name, version, os_type):
        cache_path = self.get_cache_path()
        return os.path.join(cache_path, name, version, os_type)

    def get_driver_binary_path(self, name, version, os_type):
        # type: (str, str) -> str
        directory = self._get_driver_path(name, version, os_type)
        return os.path.join(directory, name)
