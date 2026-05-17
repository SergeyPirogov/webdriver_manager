import os

import shutil

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from tests.helper import chrome_driver_for
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.os_manager import ChromeType, OperationSystemManager
from webdriver_manager.drivers.chrome import CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL, \
    CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL, CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL


@pytest.mark.filterwarnings("ignore:Unverified HTTPS request:urllib3.exceptions.InsecureRequestWarning")
def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        '.wdm',
        "ssl_disabled",
    )
    driver_path = ChromeDriverManager(
        driver_version="115.0.5763.0",
        cache_manager=DriverCacheManager(custom_path),
        chrome_type=ChromeType.BRAVE,
    ).install()

    assert os.path.exists(driver_path)


def test_brave_manager_with_specific_version():
    bin_path = ChromeDriverManager("115.0.5763.0", chrome_type=ChromeType.BRAVE).install()
    assert os.path.exists(bin_path)


def test_brave_manager_with_selenium():
    # ths works on linux
    brave_path = shutil.which("brave")
    if not brave_path:
        pytest.skip("Brave browser not found in PATH")
    
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    driver_path = ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("http://automation-remarks.com")
    driver.close()


def test_brave_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2", chrome_type=ChromeType.BRAVE).install()
    assert "There is no such driver by url" in ex.value.args[0]


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_brave_for_win(os_type):
    path = ChromeDriverManager(driver_version="115.0.5763.0",
                               os_system_manager=OperationSystemManager(os_type),
                               chrome_type=ChromeType.BRAVE).install()
    assert os.path.exists(path)


def test_brave_latest_release_version_falls_back_to_latest_milestone_when_build_is_missing():
    driver, http_client = chrome_driver_for(
        browser_version="120.0.6099.71",
        chrome_type=ChromeType.BRAVE,
        responses={
            CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL: {
                "builds": {},
            },
            CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL: {
                "milestones": {
                    "120": {
                        "version": "120.0.6099.109",
                    },
                },
            },
        },
    )

    assert driver.get_latest_release_version() == "120.0.6099.109"

    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
        CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL,
    ]


def test_brave_latest_release_version_raises_readable_error_when_no_build_and_no_milestone_exist():
    driver, http_client = chrome_driver_for(
        browser_version="120.0.9999.1",
        chrome_type=ChromeType.BRAVE,
        responses={
            CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL: {
                "builds": {},
            },
            CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL: {
                "milestones": {},
            },
        },
    )

    with pytest.raises(ValueError) as error:
        driver.get_latest_release_version()

    message = str(error.value)

    assert "Could not find a compatible chromedriver version" in message
    assert f"{ChromeType.BRAVE} 120.0.9999.1" in message
    assert CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL in message
    assert CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL in message

    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
        CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL,
    ]


@pytest.mark.parametrize(
    ("platform", "expected_url"),
    [
        (
            "mac-arm64",
            "https://storage.googleapis.com/chrome-for-testing-public/"
            "131.0.6778.264/mac-arm64/chromedriver-mac-arm64.zip",
        ),
        (
            "mac-x64",
            "https://storage.googleapis.com/chrome-for-testing-public/"
            "131.0.6778.264/mac-x64/chromedriver-mac-x64.zip",
        ),
    ],
)
def test_brave_115_plus_uses_chrome_for_testing_macos_download_url_after_milestone_fallback(
    platform,
    expected_url,
):
    driver, http_client = chrome_driver_for(
        browser_version="131.0.6778.1",
        chrome_type=ChromeType.BRAVE,
        responses={
            CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL: {
                "builds": {},
            },
            CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL: {
                "milestones": {
                    "131": {
                        "version": "131.0.6778.264",
                    },
                },
            },
            CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL: {
                "versions": [
                    {
                        "version": "131.0.6778.264",
                        "downloads": {
                            "chromedriver": [
                                {
                                    "platform": platform,
                                    "url": expected_url,
                                },
                            ],
                        },
                    },
                ],
            },
        },
    )

    driver_version = driver.get_latest_release_version()

    assert driver_version == "131.0.6778.264"
    assert driver.get_url_for_version_and_platform(driver_version, platform) == expected_url

    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
        CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL,
        CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL,
    ]
