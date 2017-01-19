import os
import shutil
from time import sleep

import pytest
from selenium import webdriver

from webdriver_manager.cache import CacheManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import OSUtils


def delete_cache():
    cache = CacheManager()
    cache_path = cache.get_cache_path()
    os.chmod(cache_path, 0o777)
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    sleep(5)


def test_chrome_manager_with_specific_version():
    bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin)


def test_chrome_manager_with_latest_version():
    bin = ChromeDriverManager().install()
    assert os.path.exists(bin)


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    assert ex.value.args[0] == "There is no such driver chromedriver with version 0.2 " \
                               "by http://chromedriver.storage.googleapis.com/0.2/chromedriver_{0}.zip".format(
        OSUtils.os_type())


def test_chrome_manager_with_selenium():
    delete_cache()
    driver_path = ChromeDriverManager().install()
    webdriver.Chrome(driver_path)


def test_chrome_manager_cached_driver_with_selenium():
    ChromeDriverManager().install()
    webdriver.Chrome(ChromeDriverManager().install())


def test_chrome_manager_with_win64_os():
    ChromeDriverManager(os_type="win64").install()
