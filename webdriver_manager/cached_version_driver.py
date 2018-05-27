import os
import time
from collections import namedtuple
from datetime import datetime

from webdriver_manager import config
from webdriver_manager.driver import Driver

CacheData = namedtuple("CacheData", ["version", "update_time"])


class CachedVersionDriver(Driver):
    def __init__(self, driver, cache_dir):
        # type: (Driver, str) -> None
        self.driver = driver

        self.config = driver.config
        # self._url = self.driver._url
        self.name = driver.name
        self._version = self.driver._version
        self.os_type = driver.os_type

        self.cache_dir = cache_dir
        file_name = "latest-{name}.cache".format(name=self.name)
        self.cache_file = os.path.join(cache_dir, file_name)

    def get_url(self):
        # type: () -> str
        return self.driver.get_url()

    def get_version(self, force_update_cache=False):
        # type: () -> str
        if self._version == "latest":
            return self.get_latest_release_version(force_update_cache)
        return self.driver.get_version()

    def get_latest_release_version(self, force_update_cache=False):
        # type: (bool) -> str
        version = None
        if not force_update_cache:
            try:
                cache = self.read_from_cache()
                delta = datetime.now() - cache.update_time
                if delta < config.cache_expired:
                    version = cache.version
            except:  # noqa
                pass
        if not version:
            version = self.driver.get_latest_release_version()
            self.write_to_cache(version)
        return version

    def read_from_cache(self):
        # type: () -> CacheData
        with open(self.cache_file) as f:
            _, _, version = f.readline().strip().partition("=")
            _, _, update_time_stamp = f.readline().strip().partition("=")
        update_time = datetime.fromtimestamp(float(update_time_stamp))
        return CacheData(version, update_time)

    def write_to_cache(self, version, update_time=None):
        # type: (str, datetime) -> None
        if update_time is None:
            update_time = datetime.today()
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        with open(self.cache_file, "w") as f:
            f.write("version={version}\n".format(version=version))
            timestamp = time.mktime(update_time.timetuple())
            f.write("update_time={timestamp}\n".format(timestamp=timestamp))
