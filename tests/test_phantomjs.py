from webdriver_manager.phantomjs import PhantomJsDriverManager
from selenium import webdriver


def test_can_phantom_with_selenium():
    driver = webdriver.PhantomJS(executable_path=PhantomJsDriverManager().install())
