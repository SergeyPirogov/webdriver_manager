import json
import os

import pytest
import browsers
from selenium import webdriver
from mock import patch
from tests.helper import chrome_driver_for

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.constants import ROOT_FOLDER_NAME
from selenium.webdriver.chrome.service import Service
from webdriver_manager.core.driver import Driver

from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.os_manager import OperationSystemManager, ChromeType
from webdriver_manager.drivers.chrome import (
    CHROMEDRIVER_STORAGE_LATEST_RELEASE_URL,
    CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
    CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL,
)

os.environ.setdefault("WDM_LOCAL", "false")


def test_chrome_manager_with_cache(delete_drivers_dir):
    ChromeDriverManager().install()
    driver_binary = ChromeDriverManager().install()
    assert os.path.exists(driver_binary)


def test_chrome_manager_with_specific_version(delete_drivers_dir):
    driver_binary = ChromeDriverManager("115.0.5763.0").install()
    assert os.path.exists(driver_binary)


@pytest.mark.skip(reason='I dont think this works any more')
@patch.object(Driver, 'get_browser_version_from_os', return_value="112.0.5615.165")
def test_chrome_manager_with_old_detected_version(mock_version, delete_drivers_dir):
        driver_binary = ChromeDriverManager().install()
        assert os.path.exists(driver_binary)


@pytest.mark.skip(reason='I dont think this works any more')
def test_106_0_5249_61_chrome_version(delete_drivers_dir):
    driver_binary = ChromeDriverManager("106.0.5249.61").install()
    assert os.path.exists(driver_binary)


def test_chrome_manager_with_project_root_local_folder(delete_drivers_dir):
    os.environ['WDM_LOCAL'] = "1"
    driver_binary = ChromeDriverManager("115.0.5763.0").install()
    os.environ['WDM_LOCAL'] = "0"
    assert os.path.exists(driver_binary)


def test_driver_can_be_saved_to_custom_path():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom")
    path = ChromeDriverManager(driver_version="115.0.5763.0", cache_manager=DriverCacheManager(custom_path)).install()
    assert os.path.exists(path)
    assert custom_path in path


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    assert "There is no such driver by url" in ex.value.args[0]


def test_chrome_manager_with_selenium():
    options = webdriver.ChromeOptions()
    options.binary_location = browsers.get("chrome")["path"]
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver.get("http://automation-remarks.com")
    driver.close()


@pytest.mark.filterwarnings("ignore:Unverified HTTPS request:urllib3.exceptions.InsecureRequestWarning")
def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)),
        "ssl_disabled",
    )
    driver_path = ChromeDriverManager(cache_manager=DriverCacheManager(custom_path)).install()
    os.environ['WDM_SSL_VERIFY'] = '1'
    assert os.path.exists(driver_path)


def test_chrome_manager_cached_driver_with_selenium():
    options = webdriver.ChromeOptions()
    options.binary_location = browsers.get("chrome")["path"]
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom-cache")
    manager = ChromeDriverManager(cache_manager=DriverCacheManager(custom_path))
    driver = webdriver.Chrome(service=Service(manager.install()), options=options)
    driver.get("http://automation-remarks.com")

    metadata_file = os.path.join(custom_path, ROOT_FOLDER_NAME, 'drivers.json')

    with open(metadata_file) as json_file:
        data = json.load(json_file)

    for k in data.keys():
        data[k]['timestamp'] = "08/06/2019"

    with open(metadata_file, 'w') as outfile:
        json.dump(data, outfile)

    ChromeDriverManager(cache_manager=DriverCacheManager(custom_path)).install()
    driver.close()


@pytest.mark.parametrize('os_type', ['win32', 'win64', 'mac64', 'mac64_m1'])
def test_can_get_chrome_for_os(os_type):
    path = ChromeDriverManager(os_system_manager=OperationSystemManager(os_type=os_type)).install()
    assert os.path.exists(path)


def test_chrome_118_resolves_cft_driver_version_and_download_url():
    expected_url = (
        "https://storage.googleapis.com/chrome-for-testing-public/"
        "118.0.5993.90/win32/chromedriver-win32.zip"
    )
    driver, http_client = chrome_driver_for(
        browser_version="118.0.5993.88",
        chrome_type=ChromeType.GOOGLE,
        responses={
            CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL: {
                "builds": {
                    "118.0.5993": {
                        "version": "118.0.5993.90",
                    },
                },
            },
            CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL: {
                "versions": [
                    {
                        "version": "118.0.5993.90",
                        "downloads": {
                            "chromedriver": [
                                {
                                    "platform": "win32",
                                    "url": expected_url,
                                }
                            ],
                        },
                    },
                ],
            },
        },
    )

    resolved_version = driver.get_latest_release_version()
    assert resolved_version == "118.0.5993.90"
    assert driver.get_driver_download_url("win32") == expected_url
    assert "chromedriver.storage.googleapis.com" not in driver.get_driver_download_url("win32")
    assert CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL in http_client.requested_urls
    assert CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL in http_client.requested_urls


def test_chrome_102_uses_legacy_storage_url_and_win32_archive_for_win64():
    driver, http_client = chrome_driver_for(
        browser_version="102.0.5005.63",
        driver_version="102.0.5005.61",
        chrome_type=ChromeType.GOOGLE,
        responses={},
    )

    assert driver.get_driver_download_url("win64") == (
        "https://chromedriver.storage.googleapis.com/"
        "102.0.5005.61/chromedriver_win32.zip"
    )
    assert http_client.requested_urls == []


def test_chrome_102_detected_version_uses_legacy_latest_release_url():
    expected_url = f"{CHROMEDRIVER_STORAGE_LATEST_RELEASE_URL}_102.0.5005"
    driver, http_client = chrome_driver_for(
        browser_version="102.0.5005.63",
        chrome_type=ChromeType.GOOGLE,
        responses={
            expected_url: "102.0.5005.61",
        },
    )

    assert driver.get_latest_release_version() == "102.0.5005.61"
    assert http_client.requested_urls == [expected_url]


def test_chrome_download_url_boundary_switches_from_legacy_to_cft():
    legacy_driver, legacy_http_client = chrome_driver_for(
        browser_version="114.0.5735.199",
        driver_version="114.0.5735.90",
        chrome_type=ChromeType.GOOGLE,
        responses={},
    )
    cft_url = (
        "https://storage.googleapis.com/chrome-for-testing-public/"
        "115.0.5790.170/win64/chromedriver-win64.zip"
    )
    cft_driver, cft_http_client = chrome_driver_for(
        browser_version="115.0.5790.99",
        driver_version="115.0.5790.170",
        chrome_type=ChromeType.GOOGLE,
        responses={
            CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL: {
                "versions": [
                    {
                        "version": "115.0.5790.170",
                        "downloads": {
                            "chromedriver": [
                                {"platform": "win64", "url": cft_url},
                            ],
                        },
                    },
                ],
            },
        },
    )

    assert legacy_driver.get_driver_download_url("win64") == (
        "https://chromedriver.storage.googleapis.com/"
        "114.0.5735.90/chromedriver_win32.zip"
    )
    assert legacy_http_client.requested_urls == []
    assert cft_driver.get_driver_download_url("win64") == cft_url
    assert cft_http_client.requested_urls == [
        CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL,
    ]


def test_chrome_manager_downloads_legacy_chrome_102_url_for_win64(tmp_path):
    class CacheManagerMock:
        def find_driver(self, _driver):
            return None

        def get_driver_lock_path(self, _driver_name, _os_type):
            return str(tmp_path / ".wdm-lock")

        def save_file_to_cache(self, _driver, _file):
            driver_path = tmp_path / "chromedriver.exe"
            driver_path.write_text("")
            return str(driver_path)

    class DownloadManagerMock:
        http_client = None

        def __init__(self):
            self.requested_urls = []

        def download_file(self, url):
            self.requested_urls.append(url)
            return object()

    class Windows64OSManagerMock:
        def get_os_type(self):
            return "win64"

        def get_os_architecture(self):
            return 64

        def is_mac_os(self, _os_type):
            return False

        def get_browser_version_from_os(self, _browser_type=None):
            return "102.0.5005.63"

    download_manager = DownloadManagerMock()
    manager = ChromeDriverManager(
        driver_version="102.0.5005.61",
        download_manager=download_manager,
        cache_manager=CacheManagerMock(),
        os_system_manager=Windows64OSManagerMock(),
    )

    driver_path = manager.install()

    assert os.path.exists(driver_path)
    assert download_manager.requested_urls == [
        "https://chromedriver.storage.googleapis.com/"
        "102.0.5005.61/chromedriver_win32.zip"
    ]


def test_chrome_115_plus_prefers_win64_download_when_available():
    expected_url = (
        "https://storage.googleapis.com/chrome-for-testing-public/"
        "131.0.6778.264/win64/chromedriver-win64.zip"
    )
    driver, _ = chrome_driver_for(
        browser_version="131.0.6778.70",
        chrome_type=ChromeType.GOOGLE,
        responses={
            CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL: {
                "versions": [
                    {
                        "version": "131.0.6778.264",
                        "downloads": {
                            "chromedriver": [
                                {"platform": "win32", "url": "https://example/win32.zip"},
                                {"platform": "win64", "url": expected_url},
                            ],
                        },
                    },
                ],
            },
        },
    )

    assert driver.get_url_for_version_and_platform("131.0.6778.264", "win64") == expected_url


def test_chrome_115_plus_falls_back_to_win32_when_win64_is_unavailable():
    expected_url = (
        "https://storage.googleapis.com/chrome-for-testing-public/"
        "131.0.6778.264/win32/chromedriver-win32.zip"
    )
    driver, _ = chrome_driver_for(
        browser_version="131.0.6778.70",
        chrome_type=ChromeType.GOOGLE,
        responses={
            CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL: {
                "versions": [
                    {
                        "version": "131.0.6778.264",
                        "downloads": {
                            "chromedriver": [
                                {"platform": "win32", "url": expected_url},
                            ],
                        },
                    },
                ],
            },
        },
    )

    assert driver.get_url_for_version_and_platform("131.0.6778.264", "win64") == expected_url
