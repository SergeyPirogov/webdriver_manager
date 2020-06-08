import os
import shutil

import pytest

from tests.utils import driver_directory
from webdriver_manager.driver import ChromeDriver
from webdriver_manager.utils import download_file, save_file, ChromeType


@pytest.fixture()
def delete_drivers_dir():
    if os.path.exists(driver_directory):
        shutil.rmtree(driver_directory)


def test_can_download_driver_as_zip_file(delete_drivers_dir):
    file = download_file("http://chromedriver.storage.googleapis.com/2.26/chromedriver_win32.zip")
    assert file.filename == "driver.zip"
    archive = save_file(file, driver_directory)
    assert archive.file_path == f"{driver_directory}{os.sep}{file.filename}"
    assert archive.unpack(driver_directory) == ["chromedriver.exe"]


def test_can_download_driver_as_tar_gz(delete_drivers_dir):
    file = download_file(
        "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux32.tar.gz")
    assert file.filename == 'geckodriver-v0.26.0-linux32.tar.gz'
    archive = save_file(file, driver_directory)
    assert archive.file_path == f"{driver_directory}{os.sep}{file.filename}"
    assert archive.unpack(driver_directory) == ["geckodriver"]


@pytest.mark.parametrize('version', ["2.26", "latest"])
def test_can_download_chrome_driver(delete_drivers_dir, version):
    driver = ChromeDriver(name="chromedriver", version=version, os_type="win32",
                          url="http://chromedriver.storage.googleapis.com",
                          latest_release_url="http://chromedriver.storage.googleapis.com/LATEST_RELEASE",
                          chrome_type=ChromeType.GOOGLE)

    file = download_file(driver.get_url())
    assert file.filename == "driver.zip"
    archive = save_file(file, driver_directory)
    assert archive.unpack(driver_directory) == ["chromedriver.exe"]

