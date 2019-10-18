import os

from webdriver_manager.driver_cache import DriverCache
from webdriver_manager.utils import download_driver

project_root = os.path.dirname(os.path.dirname(__file__))
cache_root_dir = ".wdm"
name = "chromedriver"
version = "77"
os_type = "linux"

driver_cache = DriverCache(os.path.join(project_root, cache_root_dir))


def create_file(name, version, os_type):
    path = os.path.join(project_root, cache_root_dir, name, version, os_type)

    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, "chromedriver")

    open(file_path, "w+")
    return file_path


def test_driver_cash_can_create_folder_on_init():
    driver_cache.create_cache_dir_for_driver(os.path.join(project_root, cache_root_dir, name, version, os_type))
    assert os.path.exists(driver_cache._root_dir)


def test_driver_cache_can_find_file():
    file_path = create_file(name, version, os_type)
    path = driver_cache.find_file_if_exists(version, name)
    assert path == file_path


def test_can_save_driver_to_cache():
    response = download_driver("http://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip")
    path = driver_cache.save_driver_to_cache(response, name, version, os_type)
    assert path == os.path.join(driver_cache._root_dir, name, version, os_type, name)
