from tests.test_cache import delete_cache
from webdriver_manager.phantomjs import PhantomJsDriverManager

import pytest
from selenium import webdriver

PATH = '.'

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_can_phantom_with_selenium(path, with_path):
    delete_cache()
    webdriver.PhantomJS(executable_path=PhantomJsDriverManager().install())

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_can_download_phantom_for_windows(path, with_path):
    delete_cache()
    path = PhantomJsDriverManager(os_type="win").install()
    assert path.endswith("phantomjs.exe")

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_can_download_phantom_for_linux(path, with_path):
    delete_cache()
    path = PhantomJsDriverManager(os_type="linux").install()
    assert path.endswith("phantomjs")

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_can_user_phantom_driver_from_cache(path, with_path):
    delete_cache()
    if with_path:
        PhantomJsDriverManager(os_type="linux").install(path)
        path = PhantomJsDriverManager(os_type="linux").install(path)
    else:
        PhantomJsDriverManager(os_type="linux").install()
        path = PhantomJsDriverManager(os_type="linux").install()
    assert path.endswith("phantomjs")
