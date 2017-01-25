from tests.test_cache import delete_cache
from webdriver_manager.phantomjs import PhantomJsDriverManager
from selenium import webdriver


def test_can_phantom_with_selenium():
    delete_cache()
    webdriver.PhantomJS(executable_path=PhantomJsDriverManager().install())


def test_can_download_phantom_for_windows():
    delete_cache()
    path = PhantomJsDriverManager(os_type="win").install()
    assert path.endswith("phantomjs.exe")


def test_can_download_phantom_for_linux():
    delete_cache()
    path = PhantomJsDriverManager(os_type="linux").install()
    assert path.endswith("phantomjs")


def test_can_user_phantom_driver_from_cache():
    delete_cache()
    PhantomJsDriverManager(os_type="linux").install()
    path = PhantomJsDriverManager(os_type="linux").install()
    assert path.endswith("phantomjs")
