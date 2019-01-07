import os

import pytest
from selenium import webdriver

from tests.test_cache import cache, delete_cache
from webdriver_manager.phantomjs import PhantomJsDriverManager

PATH = '.'


def delete_old_install(path=None):
    if path is None:
        delete_cache()
    else:
        path = os.path.abspath(path)
        for f in os.listdir(path):
            if f.startswith("phantomjs-"):
                try:
                    os.remove(os.path.join(path, f))
                except:
                    pass



def test_phantomjs_manager_with_specific_version():
    bin = PhantomJsDriverManager("2.0.0", os_type="win32").install()
    assert os.path.exists(bin)


@pytest.mark.parametrize('path', [PATH, None])
def test_phantomjs_manager_with_latest_version(path):
    bin = PhantomJsDriverManager().install(path)
    assert os.path.exists(bin)


def test_phantomjs_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        delete_old_install()
        PhantomJsDriverManager("0.2", os_type="win32").install()
    assert ex.value.args[0] == "There is no such driver phantomjs with version 0.2 " \
                               "by https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-0.2-windows.zip"


def test_phantomjs_manager_with_selenium():
    delete_old_install()
    driver_path = PhantomJsDriverManager().install()
    webdriver.PhantomJS(driver_path)


@pytest.mark.parametrize('path', [PATH, None])
def test_phantomjs_manager_cached_driver_with_selenium(path):
    PhantomJsDriverManager().install(path)
    webdriver.PhantomJS(PhantomJsDriverManager().install(path))


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_phantomjs_for_windows(os_type):
    delete_cache()
    path = PhantomJsDriverManager(os_type=os_type).install()
    assert os.path.exists(path)


@pytest.mark.parametrize('os_type', ['linux32', 'linux64'])
def test_can_get_phantomjs_for_linux(os_type):
    delete_cache()
    path = PhantomJsDriverManager(os_type=os_type).install()
    assert os.path.exists(path)