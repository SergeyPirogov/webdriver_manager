import os

from webdriver_manager.utils import FileManager, OSUtils


def test_can_download_chrome_driver():
    name = "chromedriver_mac64.zip"
    version = "2.26"
    url = "http://chromedriver.storage.googleapis.com"

    driver_url = "{url}/{version}/{name}".format(url=url, version=version, name=name)

    file_manager = FileManager()

    root_dir = os.path.dirname(os.path.abspath(__file__))
    folder = ".drivers"

    target_dir_path = os.path.join(root_dir, folder, version)

    file_manager.download_driver(driver_url, target_dir_path)

    assert os.path.exists(target_dir_path)

