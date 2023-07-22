import datetime
import json
import os

from webdriver_manager.core.config import wdm_local, get_xdist_worker_id
from webdriver_manager.core.constants import (
    DEFAULT_PROJECT_ROOT_CACHE_PATH,
    DEFAULT_USER_HOME_CACHE_PATH, ROOT_FOLDER_NAME,
)
from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log
from webdriver_manager.core.utils import get_date_diff, File, save_file


class DriverCache(object):
    def __init__(self, root_dir=None, valid_range=1):
        self._root_dir = DEFAULT_USER_HOME_CACHE_PATH
        is_wdm_local = wdm_local()
        xdist_worker_id = get_xdist_worker_id()
        if xdist_worker_id:
            log(f"xdist worker is: {xdist_worker_id}")
            self._root_dir = os.path.join(self._root_dir, xdist_worker_id)

        if root_dir is not None:
            self._root_dir = os.path.join(root_dir, ROOT_FOLDER_NAME, xdist_worker_id)
        if is_wdm_local:
            self._root_dir = os.path.join(DEFAULT_PROJECT_ROOT_CACHE_PATH, xdist_worker_id)

        self._drivers_root = "drivers"
        self._drivers_json_path = os.path.join(self._root_dir, "drivers.json")
        self._date_format = "%d/%m/%Y"
        self._drivers_directory = os.path.join(self._root_dir, self._drivers_root)
        self.valid_range = valid_range
        self._cache_key_driver_version = None
        self._metadata_key = None
        self._driver_binary_path = None

    def save_file_to_cache(self, driver: Driver, file: File):
        path = self.__get_path(driver)
        archive = save_file(file, path)
        files = archive.unpack(path)
        binary = self.__get_binary(files, driver.get_name())
        binary_path = os.path.join(path, binary)
        self.__save_metadata(driver, binary_path)
        log(f"Driver has been saved in cache [{path}]")
        return binary_path

    def __get_binary(self, files, driver_name):
        if not files:
            raise Exception(f"Can't find binary for {driver_name} among {files}")

        if len(files) == 1:
            return files[0]

        for f in files:
            if 'LICENSE' in f:
                continue
            if driver_name in f:
                return f

        raise Exception(f"Can't find binary for {driver_name} among {files}")

    def __save_metadata(self, driver: Driver, binary_path, date=None):
        if date is None:
            date = datetime.date.today()

        metadata = self.load_metadata_content()
        key = self.__get_metadata_key(driver)
        data = {
            key: {
                "timestamp": date.strftime(self._date_format),
                "binary_path": binary_path,
            }
        }

        metadata.update(data)
        with open(self._drivers_json_path, "w+") as outfile:
            json.dump(metadata, outfile, indent=4)

    def find_driver(self, driver: Driver):
        """Find driver by '{os_type}_{driver_name}_{driver_version}_{browser_version}'."""
        os_type = driver.get_os_type()
        driver_name = driver.get_name()
        browser_version = driver.get_browser_version_from_os()
        driver_version = self.get_cache_key_driver_version(driver)
        browser_type = driver.get_browser_type()
        metadata = self.load_metadata_content()

        key = self.__get_metadata_key(driver)
        if key not in metadata:
            log(f'There is no [{os_type}] {driver_name} "{driver_version}" for browser {browser_type} "{browser_version}" in cache')
            return None

        driver_info = metadata[key]
        path = driver_info["binary_path"]
        if not os.path.exists(path):
            return None

        if not self.__is_valid(driver_info):
            return None

        path = driver_info["binary_path"]
        log(f"Driver [{path}] found in cache")
        return path

    def __is_valid(self, driver_info):
        dates_diff = get_date_diff(
            driver_info["timestamp"], datetime.date.today(), self._date_format
        )
        return dates_diff < self.valid_range

    def load_metadata_content(self):
        if os.path.exists(self._drivers_json_path):
            with open(self._drivers_json_path, "r") as outfile:
                return json.load(outfile)
        return {}

    def __get_metadata_key(self, driver: Driver):
        if self._metadata_key is None:
            driver_version = self.get_cache_key_driver_version(driver)
            browser_version = driver.get_browser_version_from_os()
            browser_version = browser_version if browser_version else ""
            self._metadata_key = f"{driver.get_os_type()}_{driver.get_name()}_{driver_version}_for_{browser_version}"
        return self._metadata_key

    def get_cache_key_driver_version(self, driver: Driver):
        if self._cache_key_driver_version is None:
            self._cache_key_driver_version = "latest" if driver._version in (None, "latest") else driver._version
        return self._cache_key_driver_version

    def __get_path(self, driver: Driver):
        if self._driver_binary_path is None:
            self._driver_binary_path = os.path.join(
                self._drivers_directory,
                driver.get_name(),
                driver.get_os_type(),
                driver.get_driver_version_to_download(),
            )
        return self._driver_binary_path
