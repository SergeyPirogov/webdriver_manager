import os

from webdriver_manager.driver import Driver
from webdriver_manager.utils import FileManager


def test_can_download_chrome_driver():
    name = "chromedriver"
    version = "2.26"
    url = "http://chromedriver.storage.googleapis.com"
    driver = Driver(driver_url=url,
                    name=name,
                    version=version)

    file_manager = FileManager()
    driver_zip = file_manager.download(driver)
    assert driver_zip.NameToInfo[name].filename == name


def test_can_unzip_chrome_driver():
    name = "chromedriver"
    version = "2.26"
    url = "http://chromedriver.storage.googleapis.com"
    driver = Driver(driver_url=url,
                    name=name,
                    version=version)

    file_manager = FileManager()

    to_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".drivers")

    path = file_manager.download_driver(driver, to_dir)
    assert os.path.exists(path)


def test_can_download_gecko_driver_zip():
    name = "geckodriver-v0.11.1-win32.zip"
    version = "v0.11.1"
    url = "https://github.com/mozilla/geckodriver/releases/download"

    driver_url = "{url}/{version}/{name}".format(url=url,
                                                 version=version,
                                                 name=name)
    target_dir_path = download(driver_url, version)
    assert os.path.exists(target_dir_path)


def test_can_download_gecko_driver_tar():
    name = "geckodriver-v0.11.1-macos.tar.gz"
    version = "v0.11.1"
    url = "https://github.com/mozilla/geckodriver/releases/download"

    driver_url = "{url}/{version}/{name}".format(url=url,
                                                 version=version,
                                                 name=name)
    target_dir_path = download(driver_url, version)
    assert os.path.exists(target_dir_path)


def test_latest():
    import requests

    file = requests.get("http://chromedriver.storage.googleapis.com/LATEST_RELEASE")
    print file.text.rstrip()
