import glob
import os

from webdriver_manager import archive
from webdriver_manager.archive import extract_zip, extract_tar_file
from webdriver_manager.utils import write_file, get_filename_from_response, console


class DriverCache(object):

    def __init__(self, root_dir):
        self._root_dir = root_dir

    def create_cache_dir_for_driver(self, driver_path):
        path = os.path.join(self._root_dir, driver_path)

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return os.path.exists(path)

    def find_file_if_exists(self, version, name):
        if len(name) == 0 or len(version) == 0:
            return None

        paths = [f for f in glob.glob(os.path.join(self._root_dir, name, version) + "/**", recursive=True)]

        if len(paths) == 0:
            return None

        for path in paths:
            if os.path.isfile(path) and path.endswith(name):
                print("File path [{}]".format(path))
                return path

        return None

    def save_driver_to_cache(self, response, driver_name, version, os_type):
        driver_path = os.path.join(self._root_dir, driver_name, version, os_type)
        filename = get_filename_from_response(response, driver_name)
        self.create_cache_dir_for_driver(driver_path)

        file_path = os.path.join(driver_path, filename)

        write_file(response.content, file_path)

        files = self.__unpack(file_path)
        return os.path.join(driver_path, files[0])

    def __unpack(self, path, to_directory=None):
        console("Unpack archive {}".format(path))
        if not to_directory:
            to_directory = os.path.dirname(path)
        if path.endswith(".zip"):
            return extract_zip(path, to_directory)
        else:
            file_list = extract_tar_file(path, to_directory)
            return [x.name for x in file_list]
