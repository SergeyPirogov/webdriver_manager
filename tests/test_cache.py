import os
import shutil

import pytest

from webdriver_manager.cache import CacheManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.driver import ChromeDriver, FireFoxDriver

cache = CacheManager()


def test_can_create_cache_dir():
    path = cache.create_cache_dir("chrome", "2.2")
    assert os.path.exists(path)


@pytest.mark.parametrize("os_type", ["linux64",
                                     "linux32",
                                     "mac64",
                                     "win32"
                                     ])
def test_can_download_chrome_driver_for_os(os_type):
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
    assert cache.is_cached(manager.driver)


def test_should_be_false_for_new_driver():
    name = "chromedriver"
    version = "2.26"
    url = "http://chromedriver.storage.googleapis.com"
    driver = ChromeDriver(driver_url=url,
                          name=name,
                          version=version,
                          os="")
    cache.create_cache_dir(name, version)
    shutil.rmtree(cache.get_cache_path())
    assert cache.is_cached(driver) == False
