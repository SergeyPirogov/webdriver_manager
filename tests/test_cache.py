import os
import shutil
from time import sleep

import pytest

from webdriver_manager.cache import CacheManager
from webdriver_manager.driver import ChromeDriver, GeckoDriver

cache = CacheManager()


def delete_cache():
    cache_path = cache.get_cache_path()
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    sleep(5)


@pytest.mark.parametrize("os_type", ["linux64",
                                     "linux32",
                                     "mac64",
                                     "win32"
                                     ])
def test_can_download_chrome_driver_for_os(os_type):
    delete_cache()
    driver = ChromeDriver(version="2.26",
                          os_type=os_type)

    binary = cache.download_driver(driver)
    assert binary.name == "chromedriver"


@pytest.mark.parametrize("os_type", ["linux64",
                                     "linux32",
                                     "macos",
                                     "win32",
                                     "win64",
                                     ])
def test_can_download_firefox_driver(os_type):
    delete_cache()
    name = "geckodriver"
    version = "v0.11.1"
    driver = GeckoDriver(version=version,
                         os_type=os_type)

    binary = cache.download_driver(driver)
    assert binary.name == name


@pytest.mark.parametrize("os_type", ["linux64",
                                     "linux32",
                                     "macos",
                                     "win32",
                                     "win64",
                                     ])
def test_should_be_true_for_cached_driver(os_type):
    version = "2.26"
    driver = ChromeDriver(version=version,
                          os_type=os_type)
    cache.download_driver(driver)
    assert cache.get_cached_binary(driver.name, driver.get_version(), os_type)


def test_should_be_false_for_new_driver():
    version = "2.26"
    driver = ChromeDriver(version=version,
                          os_type="")
    cache_path = cache.get_cache_path()
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    assert cache.get_cached_binary(driver.name, driver.get_version(), os_type="win") is None


def test_cache_driver_version():
    name = "chromedriver"
    version = "2.26"
    os_type = "mac64"
    driver = ChromeDriver(version=version,
                          os_type=os_type)
    cache.download_driver(driver)
    binary = cache.get_cached_binary(driver.name, driver.get_version(), os_type)
    assert binary
    assert os.path.join(cache.get_cache_path(), name, version, name) == binary.path
