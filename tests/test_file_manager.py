import os

from webdriver_manager.utils import FileManager


def download(driver_url, version):
    file_manager = FileManager()
    root_dir = os.path.dirname(os.path.abspath(__file__))
    folder = ".drivers"
    target_dir_path = os.path.join(root_dir, folder, version)
    file_manager.download_driver(driver_url, target_dir_path)
    return target_dir_path


def test_can_download_chrome_driver():
    name = "chromedriver_mac64.zip"
    version = "2.26"
    url = "http://chromedriver.storage.googleapis.com"
    driver_url = "{url}/{version}/{name}".format(url=url,
                                                 version=version,
                                                 name=name)
    target_dir_path = download(driver_url, version)
    assert os.path.exists(target_dir_path)


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
