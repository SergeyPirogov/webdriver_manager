from webdriver_manager.cache import CacheManager
import os

from webdriver_manager.driver import ChromeDriver, FireFoxDriver

cache = CacheManager()


def test_can_create_cache_dir():
    path = cache.create_cache_dir("chrome", "2.2")
    assert os.path.exists(path)


def test_can_download_chrome_driver():
    name = "chromedriver"
    version = "2.26"
    url = "http://chromedriver.storage.googleapis.com"
    driver = ChromeDriver(driver_url=url,
                          name=name,
                          version=version)

    binary = cache.download_driver(driver)
    assert binary.name == name


def test_can_download_firefox_driver():
    name = "geckodriver"
    version = "v0.11.1"
    url = "https://github.com/mozilla/geckodriver/releases/download"

    driver = FireFoxDriver(driver_url=url,
                           name=name,
                           version=version)

    binary = cache.download_driver(driver)
    assert binary.name == name