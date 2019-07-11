import os
import shutil
from os.path import expanduser
from time import sleep

import pytest
from webdriver_manager import config, archive
from webdriver_manager.archive import unpack

from webdriver_manager.cache import CacheManager
from webdriver_manager.config import Configuration
from webdriver_manager.driver import ChromeDriver, GeckoDriver

cache = CacheManager(root_dir=config.folder)


def create_file(path):
    with open(path, "w") as f:
        f.write("Demo")
        f.close()


def delete_cache():
    cache_path = cache.get_cache_path()
    print("Delete cache folder {}".format(cache_path))
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    sleep(5)


def test_correct_cache_path():
    assert cache.get_cache_path() == expanduser("~") + "/.wdm/drivers"


def test_can_create_cache_dir():
    assert cache.create_cache_dir("folder")
    assert cache.create_cache_dir("folder")  # check even for exists


def test_can_check_for_driver_in_cache():
    delete_cache()

    file_path = cache.get_cache_path() + "/folder/demo.txt"

    cache.create_cache_dir("folder")

    create_file(file_path)

    result = cache.find_file_if_exists("demo.txt")

    assert result == file_path


@pytest.mark.parametrize("os_type", ["linux64",
                                     "linux32",
                                     "mac64",
                                     "win32"
                                     ])
def test_can_download_chrome_driver_for_os(os_type):
    delete_cache()
    driver = ChromeDriver(version="2.26",
                          os_type=os_type)

    zip_file_path = cache.download_driver(driver)
    assert zip_file_path == os.path.join(cache.get_cache_path(), "chromedriver", "2.26", os_type, "chromedriver.zip")


def test_can_unzip_chrome_driver():
    delete_cache()
    driver = ChromeDriver(version="2.26",
                          os_type="linux64")

    zip_file_path = cache.download_driver(driver)
    assert unpack(zip_file_path) == ["chromedriver"]


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

    zip_file_path = cache.download_driver(driver)

    if os_type.startswith("win"):
        assert unpack(zip_file_path) == [name + ".exe"]
    else:
        assert unpack(zip_file_path) == [name]


def test_can_get_cached_binary_by_custom_path():
    delete_cache()

    cfg = Configuration(config_folder=os.path.dirname(__file__), file_name="wd_config.ini", section="GeckoDriver")

    driver = GeckoDriver("v0.11.1", "macos")

    path = cache.download_driver(driver)

    cfg.set("driver_path", path)

    driver.config = cfg

    cached_binary = cache.get_cached_binary(driver)

    assert path == cached_binary.path


@pytest.mark.parametrize("os_type", ["linux64",
                                     "linux32",
                                     "mac32",
                                     "win32"
                                     ])
def test_should_be_true_for_cached_driver(os_type):
    delete_cache()
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
