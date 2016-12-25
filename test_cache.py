from webdriver_manager.cache import CacheManager
import os

from webdriver_manager.driver import ChromeDriver

cache = CacheManager()


def test_can_create_cache_dir():
    path = cache.create_cache_dir()
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