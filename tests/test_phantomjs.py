import os
import shutil

from tests.test_cache import delete_cache
from webdriver_manager.phantomjs import PhantomJsDriverManager

import pytest
from selenium import webdriver

PATH = '.'


def delete_old_install(path=None):
    if path is None:
        delete_cache()
    else:
        path = os.path.abspath(path)
        try:
            os.remove(os.path.join(path, 'phantomjs.exe'))
            for file in os.listdir(path):
                if 'phantomjs' in file and not os.path.isfile(file):
                    if 'phantomjs.exe' in os.listdir(os.path.join(path, file, 'bin')):
                        shutil.rmtree(os.path.join(path, file))
                elif 'phantomjs' in file and file.endswith('.zip'):
                        os.remove(os.path.join(path, file))
        except:
            pass


def test_can_phantom_with_selenium():
    delete_old_install()
    webdriver.PhantomJS(executable_path=PhantomJsDriverManager().install())


def test_can_download_phantom_for_windows():
    delete_old_install()
    path = PhantomJsDriverManager(os_type="win").install()
    assert path.endswith("phantomjs.exe")


def test_can_download_phantom_with_path():
    delete_old_install(PATH)
    path = PhantomJsDriverManager().install(PATH)
    assert path.endswith("phantomjs.exe")


def test_can_download_phantom_for_linux():
    delete_old_install()
    path = PhantomJsDriverManager(os_type="linux").install()
    assert path.endswith("phantomjs")


def test_can_user_phantom_driver_from_cache():
    delete_old_install()
    PhantomJsDriverManager(os_type="linux").install()
    path = PhantomJsDriverManager(os_type="linux").install()
    assert path.endswith("phantomjs")
