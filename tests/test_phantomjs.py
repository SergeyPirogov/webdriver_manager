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
            os.remove(os.path.join(path, 'phantomjs.zip'))
            for file in os.listdir(path):
                if 'phantomjs' in file and not os.path.isfile(file):
                    if 'phantomjs.exe' in os.listdir(os.path.join(path, file, 'bin')):
                        shutil.rmtree(os.path.join(path, file))
        except:
            pass


@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_can_phantom_with_selenium(path, with_path):
    if with_path:
        delete_old_install(path)
        webdriver.PhantomJS(executable_path=PhantomJsDriverManager().install(path))
    else:
        delete_old_install(path)
        webdriver.PhantomJS(executable_path=PhantomJsDriverManager().install())

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_can_download_phantom_for_windows(path, with_path):
    if with_path:
        delete_old_install(path)
        path = PhantomJsDriverManager(os_type="win").install(path)
    else:
        delete_old_install()
        path = PhantomJsDriverManager(os_type="win").install()
    assert path.endswith("phantomjs.exe")

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_can_download_phantom_for_linux(path, with_path):
    if with_path:
        delete_old_install(path)
        path = PhantomJsDriverManager(os_type="linux").install(path)
    else:
        delete_old_install()
        path = PhantomJsDriverManager(os_type="linux").install()
    assert path.endswith("phantomjs")

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_can_user_phantom_driver_from_cache(path, with_path):
    if with_path:
        delete_old_install(path)
        PhantomJsDriverManager(os_type="linux").install(path)
        path = PhantomJsDriverManager(os_type="linux").install(path)
    else:
        delete_old_install()
        PhantomJsDriverManager(os_type="linux").install()
        path = PhantomJsDriverManager(os_type="linux").install()
    assert path.endswith("phantomjs")
