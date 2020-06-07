import os

from tests.utils import driver_directory
from webdriver_manager.utils import download_file, save_file


def test_can_download_driver_as_file():
    file = download_file("http://chromedriver.storage.googleapis.com/2.26/chromedriver_win32.zip")
    assert file.filename == "driver.zip"
    archive_path = save_file(file, driver_directory)
    assert archive_path == f"{driver_directory}{os.sep}{file.filename}"
