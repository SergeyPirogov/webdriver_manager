import datetime
import json
import os
import sys

from webdriver_manager.logger import log
from webdriver_manager.utils import get_date_diff, File, save_file


class DriverCache(object):

    def __init__(self, root_dir=None):
        self._root_dir = root_dir

        if self._root_dir is None and os.environ.get("WDM_LOCAL", '0') == '1':
            self._root_dir = os.path.join(sys.path[0], ".wdm")
        if self._root_dir is None:
            self._root_dir = os.path.join(os.path.expanduser("~"), ".wdm")
        self._drivers_root = "drivers"
        self._drivers_json_path = os.path.join(self._root_dir, "drivers.json")
        self._date_format = "%d/%m/%Y"
        self._drivers_directory = f"{self._root_dir}{os.sep}{self._drivers_root}"

    def save_file_to_cache(self, file: File, browser_version, driver_name, os_type, driver_version):
        path = os.path.join(self._drivers_directory, driver_name, os_type, driver_version)
        archive = save_file(file, path)
        files = archive.unpack(path)
        binary = self.__get_binary(files, driver_name)
        binary_path = os.path.join(path, binary)
        self.__save_metadata(browser_version, driver_name, os_type, driver_version, binary_path)
        log(f"Driver has been saved in cache [{path}]")
        return binary_path

    def __get_binary(self, files, driver_name):
        if len(files) == 1:
            return files[0]

        for f in files:
            if driver_name in f:
                return f

        raise Exception(f"Can't find binary for {driver_name} among {files}")

    def __save_metadata(self, browser_version, driver_name, os_type, driver_version, binary_path,
                        date=None):
        if date is None:
            date = datetime.date.today()

        metadata = self.get_metadata()

        key = f"{os_type}_{driver_name}_{driver_version}_for_{browser_version}"

        data = {
            key: {
                "timestamp": date.strftime(self._date_format),
                "binary_path": binary_path
            }
        }

        metadata.update(data)
        with open(self._drivers_json_path, 'w+') as outfile:
            json.dump(metadata, outfile, indent=4)

    def find_driver(self, browser_version, driver_name, os_type, driver_version):
        metadata = self.get_metadata()

        key = f"{os_type}_{driver_name}_{driver_version}_for_{browser_version}"
        if key not in metadata:
            log(f"There is no [{os_type}] {driver_name} for browser {browser_version} in cache")
            return None

        driver_info = metadata[key]

        if not self.__is_valid(driver_info):
            return None

        path = driver_info['binary_path']
        log(f"Driver [{path}] found in cache")
        return path

    def __is_valid(self, driver_info):
        dates_diff = get_date_diff(driver_info['timestamp'],
                                   datetime.date.today(),
                                   self._date_format)
        return dates_diff < 1

    def get_metadata(self):
        if os.path.exists(self._drivers_json_path):
            with open(self._drivers_json_path, 'r') as outfile:
                return json.load(outfile)
        return {}
