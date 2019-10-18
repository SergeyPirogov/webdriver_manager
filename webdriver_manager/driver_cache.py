import glob
import os

from webdriver_manager.utils import write_file, get_filename_from_response


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

        return write_file(response.content, file_path)
