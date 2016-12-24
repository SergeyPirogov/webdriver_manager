import os

from webdriver_manager.driver import ChromeDriver
from webdriver_manager.utils import FileManager

name = "chromedriver"
version = "2.26"
url = "http://chromedriver.storage.googleapis.com"
driver = ChromeDriver(driver_url=url,
                      name=name,
                      version=version)

file_manager = FileManager()


def test_can_download_chrome_driver():
    driver_zip = file_manager.download(driver)
    assert driver_zip.NameToInfo[name].filename == name


def test_can_unzip_chrome_driver():
    to_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".drivers")
    path = file_manager.download_driver(driver, to_dir)
    assert os.path.exists(path)


import os
from selenium import webdriver
import pytest

from webdriver_manager.manager import ChromeDriverManager


def test_chrome_manager_with_specific_version():
    path = ChromeDriverManager("2.27").install()
    assert os.path.exists(path)


def test_chrome_manager_with_latest_version():
    path = ChromeDriverManager().install()
    assert os.path.exists(path)


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    assert ex.value.message == "There is no such driver chromedriver with version 0.2 " \
                               "by http://chromedriver.storage.googleapis.com/0.2/chromedriver_linux64.zip"


def test_chrome_manager_with_selenium():
    driver_path = ChromeDriverManager().install()
    webdriver.Chrome(driver_path)
