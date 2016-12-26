import os
import shutil
from time import sleep

import pytest

from webdriver_manager.cache import CacheManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.driver import ChromeDriver, FireFoxDriver
from webdriver_manager.utils import OSUtils

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
    name = "chromedriver"
    version = "2.26"
    url = "http://chromedriver.storage.googleapis.com"
    driver = ChromeDriver(driver_url=url,
                          name=name,
                          version=version,
                          os=os_type)

    binary = cache.download_driver(driver)
    assert binary.name == name


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
    url = "https://github.com/mozilla/geckodriver/releases/download"
    driver = FireFoxDriver(driver_url=url,
                           name=name,
                           version=version,
                           os=os_type)

    binary = cache.download_driver(driver)
    assert binary.name == name


def test_should_be_true_for_cached_driver():
    manager = ChromeDriverManager()
    manager.install()
    assert cache.is_cached(manager.driver.name, manager.driver.get_version(), OSUtils.os_type())


def test_should_be_true_for_cached_driver_for_win():
    manager = ChromeDriverManager(os_type="win32")
    manager.install()
    assert cache.is_cached(manager.driver.name, manager.driver.get_version(), os_type="win32")


def test_should_be_false_for_new_driver():
    name = "chromedriver"
    version = "2.26"
    url = "http://chromedriver.storage.googleapis.com"
    driver = ChromeDriver(driver_url=url,
                          name=name,
                          version=version,
                          os="")
    cache_path = cache.get_cache_path()
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    assert cache.is_cached(driver.name, driver.get_version()) == False
