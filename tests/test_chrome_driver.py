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

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_chrome_manager_with_specific_version(path, with_path):
    if with_path:
        bin = ChromeDriverManager("2.26").install(path)
    else:
        bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin)

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_chrome_manager_with_latest_version(path, with_path):
    if with_path:
        bin = ChromeDriverManager().install(path)
    else:
        bin = ChromeDriverManager().install()
    assert os.path.exists(bin)

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_chrome_manager_with_wrong_version(path, with_path):
    with pytest.raises(ValueError) as ex:
        if with_path:
            ChromeDriverManager("0.2").install(path)
        else:
            ChromeDriverManager("0.2").install()
    assert ex.value.args[0] == "There is no such driver chromedriver with version 0.2 " \
                               "by http://chromedriver.storage.googleapis.com/0.2/chromedriver_{0}.zip".format(
        utils.os_type())


@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_chrome_manager_with_selenium(path, with_path):
    delete_cache()
    if with_path:
        driver_path = ChromeDriverManager().install(path)
    else:
        driver_path = ChromeDriverManager().install()
    webdriver.Chrome(driver_path)


def test_chrome_manager_with_selenium_path_param():
    driver_path = ChromeDriverManager().install(PATH)
    webdriver.Chrome(driver_path)

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_chrome_manager_cached_driver_with_selenium(path, with_path):
    if with_path:
        ChromeDriverManager().install()
        webdriver.Chrome(ChromeDriverManager().install())
    else:
        ChromeDriverManager().install(path)
        webdriver.Chrome(ChromeDriverManager().install(path))



def test_chrome_manager_cached_driver_with_selenium_with_path_param():
    ChromeDriverManager().install(PATH)
    webdriver.Chrome(ChromeDriverManager().install(PATH))

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_chrome_manager_with_win64_os(path, with_path):
    if with_path:
        ChromeDriverManager(os_type="win64").install(PATH)
    else:
        ChromeDriverManager(os_type="win64").install()
