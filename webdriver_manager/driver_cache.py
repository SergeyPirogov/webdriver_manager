import datetime
import glob
import json
import os

from webdriver_manager.archive import extract_zip, extract_tar_file
from webdriver_manager.logger import log
from webdriver_manager.utils import write_file, get_filename_from_response, get_date_diff, File, save_file


class DriverCache(object):

    def __init__(self, root_dir=None):
        self._root_dir = root_dir
        if root_dir is None:
            self._root_dir = os.path.join(os.path.expanduser("~"), ".wdm")
        self._drivers_root = "drivers"
        self._drivers_json_path = os.path.join(self._root_dir, "drivers.json")
        self._date_format = "%d/%m/%Y"
        self._drivers_directory = f"{self._root_dir}{os.sep}{self._drivers_root}"

    def save_file_to_cache(self, file: File, browser_version, driver_name, os_type, driver_version):
        path = os.path.join(self._drivers_directory, driver_name, os_type, driver_version)
        archive = save_file(file, path)
        files = archive.unpack(path)
        binary_path = os.path.join(path, files[0])
        self.save_metadata(browser_version, driver_name, os_type, driver_version, binary_path)
        log(f"Driver has been saved in cache [{path}]")
        return binary_path

    def save_metadata(self, browser_version, driver_name, os_type, driver_version, binary_path,
                      date=None):
        if date is None:
            date = datetime.date.today()

        metadata = self.read_metadata()

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

    def find_driver_in_cache(self, browser_version, driver_name, os_type, driver_version):
        metadata = self.read_metadata()

        key = f"{os_type}_{driver_name}_{driver_version}_for_{browser_version}"
        if key not in metadata:
            log(f"There is no [{os_type}] {driver_name} for browser {browser_version} in cache")
            return None

        driver_info = metadata[key]
        path = driver_info['binary_path']
        log(f"Driver [{path}] found in cache")
        return path

    def create_cache_dir_for_driver(self, driver_path):
        path = os.path.join(self._root_dir, driver_path)

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return os.path.exists(path)

    def __get_path(self, name, version, os_type):
        return [f for f in glob.glob(os.path.join(self._root_dir,
                                                  self._drivers_root, name,
                                                  version, os_type) + "/**",
                                     recursive=True)]

    def __find_file(self, paths, name, version, os_type):
        log(f"Looking for [{name} {version} {os_type}] driver in cache ")
        if len(name) == 0 or len(version) == 0:
            return None

        if "win" in os_type:
            name += ".exe"

        for path in paths:
            if os.path.isfile(path) and path.endswith(name):
                log(f"Driver found in cache [{path}]")
                return path
        return None

    def find_file_if_exists(self, name, os_type, version, is_latest):
        if is_latest and not self.is_valid_cache(name):
            return None

        paths = self.__get_path(name, version, os_type)

        return self.__find_file(paths, name, version, os_type)

    def save_driver_to_cache(self, response, driver_name, version, os_type):
        driver_path = os.path.join(self._root_dir, self._drivers_root,
                                   driver_name, version, os_type)
        filename = get_filename_from_response(response, driver_name)
        self.create_cache_dir_for_driver(driver_path)
        file_path = os.path.join(driver_path, filename)
        write_file(response.content, file_path)
        files = self.__unpack(file_path)

        binary_file = None
        if "win" in os_type:
            for item in files:
                if item.endswith('.exe'):
                    binary_file = item
        else:
            binary_file = files[0]
        return os.path.join(driver_path, binary_file)

    def save_latest_driver_version_number_to_cache(self, name, version,
                                                   date=None):
        if date is None:
            date = datetime.date.today()

        metadata = self.read_metadata()
        new = {name: {"latest_version": version,
                      "timestamp": date.strftime(self._date_format)}}
        metadata.update(new)
        with open(self._drivers_json_path, 'w+') as outfile:
            json.dump(metadata, outfile, indent=4)

    def is_valid_cache(self, driver_name):
        metadata = self.read_metadata()
        if driver_name in metadata:
            driver_data = metadata[driver_name]
            dates_diff = get_date_diff(driver_data['timestamp'],
                                       datetime.date.today(),
                                       self._date_format)
            return dates_diff < 1

        return False

    def get_latest_cached_driver_version(self, driver_name):
        if not self.is_valid_cache(driver_name):
            return None

        metadata = self.read_metadata()[driver_name]
        log(f"Cache is valid for [{metadata['timestamp']}]", first_line=True)
        return metadata["latest_version"]

    def read_metadata(self):
        if os.path.exists(self._drivers_json_path):
            with open(self._drivers_json_path, 'r') as outfile:
                return json.load(outfile)
        return {}

    def __unpack(self, path, to_directory=None):
        log(f"Unpack archive {path}")
        if not to_directory:
            to_directory = os.path.dirname(path)
        if path.endswith(".zip"):
            return extract_zip(path, to_directory)
        else:
            file_list = extract_tar_file(path, to_directory)
            return [x.name for x in file_list]
