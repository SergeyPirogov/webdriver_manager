from webdriver_manager.core.driver_cache import DriverCacheManager


class OSMock:
    def get_os_type(self):
        return "linux64"

    def get_browser_version_from_os(self, _browser_type=None):
        return "120.0.6099.71"


class DriverMock:
    def __init__(self):
        self.version_calls = 0

    def get_name(self):
        return "chromedriver"

    def get_browser_type(self):
        return "google-chrome"

    def get_browser_version_from_os(self):
        return "120.0.6099.71"

    def get_driver_version_to_download(self):
        self.version_calls += 1
        return "120.0.6099.109"


def test_driver_version_lookup_is_cached_within_cache_manager(tmp_path):
    cache = DriverCacheManager(root_dir=str(tmp_path), os_system_manager=OSMock())
    driver = DriverMock()

    cache.get_cache_key_driver_version(driver)
    cache.get_cache_key_driver_version(driver)
    cache._DriverCacheManager__get_path(driver)
    cache._DriverCacheManager__get_metadata_key(driver)

    assert driver.version_calls == 1
