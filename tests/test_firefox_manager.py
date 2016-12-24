import os

from selenium import webdriver

from webdriver_manager.driver import FireFoxDriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.utils import FileManager

name = "geckodriver"
version = "v0.11.1"
url = "https://github.com/mozilla/geckodriver/releases/download"

driver_folder = ".drivers"

driver = FireFoxDriver(driver_url=url,
                       name=name,
                       version=version)

file_manager = FileManager()


def test_can_download_gecko_driver():
    driver_zip = file_manager.download_file(driver, driver_folder)
    assert os.path.exists(driver_zip.name)


def test_can_unzip_chrome_driver():
    to_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".drivers")
    path = file_manager.download_driver(driver, to_dir)
    assert os.path.exists(path)


def test_firefox_driver_version():
    url = ""
    name = ""
    version = ""

    version = FireFoxDriver(url, name=name, version=version).get_latest_release_version()
    print "FF version", version
    assert version != ""


def test_firefox_driver_url():
    driver_url = FireFoxDriver(url, name=name, version=version).get_url()
    assert driver_url != ""


def test_gecko_manager_with_selenium():
    driver_path = GeckoDriverManager().install()
    webdriver.Firefox(executable_path=
                      driver_path)
