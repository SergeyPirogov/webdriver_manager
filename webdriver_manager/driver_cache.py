import datetime
import json
import os
import sys

from webdriver_manager.logger import log
from webdriver_manager.utils import get_date_diff, File, save_file
from webdriver_manager.driver import Driver


class DriverCache(object):
    def __init__(self, root_dir=None, valid_range=1):
        self._root_dir = root_dir

        if self._root_dir is None and os.environ.get("WDM_LOCAL", "0") == "1":
            self._root_dir = os.path.join(sys.path[0], ".wdm")
        if self._root_dir is None:
            self._root_dir = os.path.join(os.path.expanduser("~"), ".wdm")
        self._drivers_root = "drivers"
        self._drivers_json_path = os.path.join(self._root_dir, "drivers.json")
        self._date_format = "%d/%m/%Y"
        self._drivers_directory = f"{self._root_dir}{os.sep}{self._drivers_root}"
        self.valid_range = valid_range

    def save_file_to_cache(self, driver, file: File):
        driver_name = driver.get_name()
        os_type = driver.get_os_type()
        driver_version = driver.get_version()
        browser_version = driver.browser_version

        path = os.path.join(
            self._drivers_directory, driver_name, os_type, driver_version
        )
        archive = save_file(file, path)
        files = archive.unpack(path)
        binary = self.__get_binary(files, driver_name)
        binary_path = os.path.join(path, binary)
        self.__save_metadata(
            browser_version, driver_name, os_type, driver_version, binary_path
        )
        log(f"Driver has been saved in cache [{path}]")
        return binary_path

    def __get_binary(self, files, driver_name):
        if len(files) == 1:
            return files[0]

        for f in files:
            if driver_name in f:
                return f

        raise Exception(f"Can't find binary for {driver_name} among {files}")

    def __save_metadata(
        self,
        browser_version,
        driver_name,
        os_type,
        driver_version,
        binary_path,
        date=None,
    ):
        if date is None:
            date = datetime.date.today()

        metadata = self.get_metadata()

        key = f"{os_type}_{driver_name}_{driver_version}_for_{browser_version}"

        data = {
            key: {
                "timestamp": date.strftime(self._date_format),
                "binary_path": binary_path,
            }
        }

        metadata.update(data)
        with open(self._drivers_json_path, "w+") as outfile:
            json.dump(metadata, outfile, indent=4)

    def find_latest_driver_in_cache(self, driver: Driver) -> str:
        """Find the latest cached driver for the current browser.

        Args:
            driver (Driver): The browser to find the latest driver for.

        Returns:
            str: The path to the latest driver.
            None: If no driver is found.
        """
        driver_name = driver.get_name()
        os_type = driver.get_os_type()
        browser_version = driver.browser_version

        metadata = self.get_metadata()

        latest = None
        for key, val in metadata.items():
            if not key.startswith(f"{os_type}_{driver_name}"):
                continue
            if not key.endswith(f"_for_{browser_version}"):
                continue

            dates_diff = get_date_diff(
                val["timestamp"], datetime.date.today(), self._date_format
            )

            if not latest or latest["age"] < dates_diff:
                latest = {"age": dates_diff, "path": val["binary_path"]}

        if not latest:
            log(
                f"There is no [{os_type}] {driver_name} for browser {browser_version} in cache"
            )
            return None

        path = val["binary_path"]
        log(f"Driver [{path}] found in cache")
        return path

    def find_driver(
        self,
        driver: Driver,
        timeout: int = 5,
        fallback_to_latest: bool = True,
    ) -> str:
        """Find driver by '{os_type}_{driver_name}_{driver_version}_{browser_version}'.

        Args:
            timeout (int): An amount in seconds to wait for a response in case the
                latest version has to be queried online. This is passed directly to
                the ``requests.get()`` call.

            fallback_to_latest (bool): In case the ``driver.get_version()`` call fails
                for any reason (such as a request for a latest version being blocked)
                then this will search through all the cached webdrivers to find the
                most recent one and returns it.

        Returns:
            str: The path to the webdriver file.
            None: If the file could not be found
        """

        # Attempt to find the correct driver version
        try:
            driver_version = driver.get_version(timeout=5)
        except Exception:
            log("No version found for driver")
            if fallback_to_latest:
                return self.find_latest_driver_in_cache(driver)
            else:
                return None

        os_type = driver.get_os_type()
        driver_name = driver.get_name()
        browser_version = driver.browser_version

        metadata = self.get_metadata()

        key = f"{os_type}_{driver_name}_{driver_version}_for_{browser_version}"
        if key not in metadata:
            log(
                f"There is no [{os_type}] {driver_name} for browser {browser_version} in cache"
            )
            return None

        path = os.path.join(
            self._drivers_directory, driver_name, os_type, driver_version
        )
        driver_binary_name = (
            "msedgedriver" if driver_name == "edgedriver" else driver_name
        )
        driver_binary_name = (
            f"{driver_binary_name}.exe" if "win" in os_type else driver_name
        )
        binary_path = os.path.join(path, driver_binary_name)
        if not os.path.exists(binary_path):
            return None

        driver_info = metadata[key]

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

    def get_metadata(self):
        if os.path.exists(self._drivers_json_path):
            with open(self._drivers_json_path, "r") as outfile:
                return json.load(outfile)
        return {}
