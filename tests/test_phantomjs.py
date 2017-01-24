from webdriver_manager.phantomjs import PhantomJsDriverManager
from selenium import webdriver


def test_can_phantom_with_selenium():
    webdriver.PhantomJS(executable_path=PhantomJsDriverManager().install())


def test_can_download_phantom_for_windows():
    path = PhantomJsDriverManager(os_type="win").install()
    assert path.endswith("phantomjs.exe")
