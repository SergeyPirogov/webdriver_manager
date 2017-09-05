import os
import shutil
from time import sleep

import pytest
from selenium import webdriver

from webdriver_manager.cache import CacheManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager import utils
from webdriver_manager import config

PATH = '.'


def delete_cache():
    cache = CacheManager()
    cache_path = cache.get_cache_path()
    if os.path.exists(cache_path):
        os.chmod(cache_path, 0o777)
        shutil.rmtree(cache_path)
    sleep(5)


def delete_old_install(path=None):
    if path is None:
        delete_cache()
    else:
        path = os.path.abspath(path)
        try:
            os.remove(os.path.join(path, 'chromedriver.exe'))
            os.remove(os.path.join(path, 'chromedriver.zip'))
        except:
            pass


def test_chrome_manager_with_specific_version():
    bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin)


@pytest.mark.parametrize('path', [PATH, None])
def test_chrome_manager_with_latest_version(path):
    bin = ChromeDriverManager().install(path)
    assert os.path.exists(bin)


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        delete_old_install()
        ChromeDriverManager("0.2").install()
    assert ex.value.args[0] == "There is no such driver chromedriver with version 0.2 " \
                               "by http://chromedriver.storage.googleapis.com/0.2/chromedriver_{0}.zip".format(
        utils.os_type())



def test_chrome_manager_with_selenium():
    delete_old_install()
    driver_path = ChromeDriverManager().install()
    webdriver.Chrome(driver_path)


@pytest.mark.parametrize('path', [PATH, None])
def test_chrome_manager_cached_driver_with_selenium(path):
    ChromeDriverManager().install(path)
    webdriver.Chrome(ChromeDriverManager().install(path))


@pytest.mark.parametrize('path', [PATH, None])
def test_chrome_manager_with_win64_os(path):
    ChromeDriverManager(os_type="win64").install(path)
