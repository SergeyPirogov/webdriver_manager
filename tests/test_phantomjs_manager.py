import os

import pytest
from selenium import webdriver

from tests.test_cache import cache, delete_cache
from webdriver_manager.phantomjs import PhantomJsDriverManager

# PATH = '.'
#
#
# def test_phantomjs_manager_with_specific_version():
#     bin = PhantomJsDriverManager("2.0.0", os_type="win32").install()
#     assert os.path.exists(bin)
#
#
# @pytest.mark.parametrize('path', [PATH, None])
# def test_phantomjs_manager_with_latest_version(path):
#     bin = PhantomJsDriverManager(version="2.1.1").install(path)
#     assert os.path.exists(bin)
#
#
# @pytest.mark.parametrize('os_type', ['win32', 'win64'])
# def test_can_get_phantomjs_for_windows(os_type):
#     delete_cache()
#     path = PhantomJsDriverManager(os_type=os_type).install()
#     assert os.path.exists(path)


@pytest.mark.parametrize('os_type', ['linux32', 'linux64'])
def test_can_get_phantomjs_for_linux(os_type):
    delete_cache()
    path = PhantomJsDriverManager(os_type=os_type).install()
    assert os.path.exists(path)
