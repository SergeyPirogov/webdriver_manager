import os
import shutil
from time import sleep

import pytest
from webdriver_manager import config

from webdriver_manager.cache import CacheManager
from webdriver_manager.config import Configuration
from webdriver_manager.driver import ChromeDriver, GeckoDriver

cache = CacheManager(to_folder=config.folder, dir_name=config.folder)


def delete_cache():
    cache_path = cache.get_cache_path()
    print("Delete cache folder {}".format(cache_path))
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
                                     "mac32",
                                     "win32"
                                     ])
def test_should_be_true_for_cached_driver(os_type):
    version = "2.10"
    driver = ChromeDriver(version=version,
                          os_type=os_type)
    cache.download_driver(driver)
    assert cache.get_cached_binary(driver)


def test_should_be_false_for_new_driver():
    version = "2.25"
    driver = ChromeDriver(version=version,
                          os_type="win")
    cache_path = cache.get_cache_path()
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    assert cache.get_cached_binary(driver) is None


def test_cache_driver_version():
    name = "chromedriver"
    version = "2.26"
    os_type = "mac64"
    driver = ChromeDriver(version=version,
                          os_type=os_type)
    cache.download_driver(driver)
    binary = cache.get_cached_binary(driver)
    assert binary
    assert os.path.join(cache.get_cache_path(), name, version, os_type, name) == binary.path


def test_cached_driver_manual_setup():
    config = Configuration(config_folder=os.path.dirname(__file__), file_name="wd_config.ini", section="ChromeDriver")
    version = "2.26"
    os_type = "linux"
    driver = ChromeDriver(version=version,
                          os_type=os_type)
    driver.config = config
    with pytest.raises(IOError) as ex:
        cache.get_cached_binary(driver)
    assert ex.value.args[1] == 'Is a directory'


def test_cached_driver_path():
    assert cache.get_driver_binary_path("chromedriver", "2.1.1", "linux64") == os.path.join(cache.get_cache_path(),
                                                                                            "chromedriver",
                                                                                            "2.1.1",
                                                                                            "linux64",
                                                                                            "chromedriver")
