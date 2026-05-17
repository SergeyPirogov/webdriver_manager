import os
import gzip
import json
import zlib

import pytest

from tests.helper import chrome_driver_for
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.os_manager import ChromeType, OperationSystemManager
from webdriver_manager.drivers.chrome import (
    CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
    CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL,
    CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL,
)


@pytest.mark.filterwarnings("ignore:Unverified HTTPS request:urllib3.exceptions.InsecureRequestWarning")
def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "ssl_disabled",
    )
    driver_path = ChromeDriverManager(
        driver_version="115.0.5763.0",
        cache_manager=DriverCacheManager(custom_path),
        chrome_type=ChromeType.CHROMIUM,
    ).install()

    assert os.path.exists(driver_path)


def test_chromium_manager_with_specific_version():
    bin_path = ChromeDriverManager("115.0.5763.0", chrome_type=ChromeType.CHROMIUM).install()
    assert os.path.exists(bin_path)


def test_driver_can_be_saved_to_custom_path():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom")

    path = ChromeDriverManager(driver_version="115.0.5763.0", cache_manager=DriverCacheManager(custom_path),
                               chrome_type=ChromeType.CHROMIUM).install()
    assert os.path.exists(path)
    assert custom_path in path


def test_chromium_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2", chrome_type=ChromeType.CHROMIUM).install()
    assert "There is no such driver by url" in ex.value.args[0]


def test_chromium_latest_release_version_uses_latest_patch_version_per_build():
    driver, http_client = chrome_driver_for(
        browser_version="120.0.6099.71",
        responses={
            CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL: {
                "builds": {
                    "120.0.6099": {
                        "version": "120.0.6099.109",
                    },
                },
            },
        },
    )

    assert driver.get_latest_release_version() == "120.0.6099.109"
    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
    ]


def test_chromium_latest_release_version_falls_back_to_latest_milestone_when_build_is_missing():
    driver, http_client = chrome_driver_for(
        browser_version="120.0.6099.71",
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


def test_chromium_latest_release_version_raises_readable_error_when_build_has_no_version():
    driver, http_client = chrome_driver_for(
        browser_version="120.0.6099.71",
        responses={
            CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL: {
                "builds": {
                    "120.0.6099": {},
                },
            },
        },
    )

    with pytest.raises(ValueError) as error:
        driver.get_latest_release_version()

    message = str(error.value)

    assert "Could not find a compatible chromedriver version" in message
    assert "chromium 120.0.6099.71" in message
    assert CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL in message
    assert "entry for build 120.0.6099" in message
    assert "does not contain a driver version" in message
    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
    ]


def test_chromium_latest_release_version_raises_readable_error_when_no_build_and_no_milestone_exist():
    driver, http_client = chrome_driver_for(
        browser_version="120.0.9999.1",
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
    assert "chromium 120.0.9999.1" in message
    assert CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL in message
    assert CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL in message
    assert "No entry for build 120.0.9999" in message
    assert "no entry for milestone 120" in message
    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
        CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL,
    ]


def test_chromium_latest_release_version_raises_readable_error_when_milestone_has_no_version():
    driver, http_client = chrome_driver_for(
        browser_version="120.0.9999.1",
        responses={
            CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL: {
                "builds": {},
            },
            CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL: {
                "milestones": {
                    "120": {},
                },
            },
        },
    )

    with pytest.raises(ValueError) as error:
        driver.get_latest_release_version()

    message = str(error.value)

    assert "Could not find a compatible chromedriver version" in message
    assert "chromium 120.0.9999.1" in message
    assert CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL in message
    assert CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL in message
    assert "entry for milestone 120" in message
    assert "does not contain a driver version" in message
    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
        CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL,
    ]


def test_chromium_latest_release_version_raises_readable_error_when_cft_metadata_is_not_json():
    driver, http_client = chrome_driver_for(
        browser_version="120.0.6099.71",
        responses={
            CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL: "not json",
        },
    )

    with pytest.raises(ValueError) as error:
        driver.get_latest_release_version()

    message = str(error.value)

    assert "Could not parse Chrome for Testing metadata" in message
    assert CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL in message
    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
    ]


def test_chrome_115_plus_uses_chrome_for_testing_download_url_after_milestone_fallback():
    driver, http_client = chrome_driver_for(
        browser_version="131.0.6778.1",
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
                                    "platform": "win64",
                                    "url": (
                                        "https://storage.googleapis.com/"
                                        "chrome-for-testing-public/"
                                        "131.0.6778.264/"
                                        "win64/"
                                        "chromedriver-win64.zip"
                                    ),
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

    assert (
        driver.get_url_for_version_and_platform(driver_version, "win64")
        == "https://storage.googleapis.com/"
           "chrome-for-testing-public/"
           "131.0.6778.264/"
           "win64/"
           "chromedriver-win64.zip"
    )

    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
        CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL,
        CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL,
    ]


def test_os_manager_uses_chromium_command_for_chromium_type(monkeypatch):
    captured = {}

    def fake_read_version_from_cmd(cmd, _pattern):
        captured["cmd"] = cmd
        return "125.0.6422"

    monkeypatch.setattr("webdriver_manager.core.os_manager.read_version_from_cmd", fake_read_version_from_cmd)

    version = OperationSystemManager(os_type="linux64").get_browser_version_from_os(ChromeType.CHROMIUM)

    assert version == "125.0.6422"
    assert "chromium" in captured["cmd"]
    assert "google-chrome" not in captured["cmd"]


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_chromium_for_win(os_type):
    path = ChromeDriverManager(driver_version="115.0.5763.0",
                               os_system_manager=OperationSystemManager(os_type=os_type),
                               chrome_type=ChromeType.CHROMIUM).install()
    assert os.path.exists(path)


def test_chromium_latest_release_version_does_not_request_milestone_when_build_exists():
    driver, http_client = chrome_driver_for(
        browser_version="120.0.6099.71",
        responses={
            CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL: {
                "builds": {
                    "120.0.6099": {
                        "version": "120.0.6099.109",
                    },
                },
            },
        },
    )

    assert driver.get_latest_release_version() == "120.0.6099.109"

    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
    ]


def test_chromium_115_plus_resolves_driver_version_from_milestone_when_build_metadata_is_missing():
    driver, http_client = chrome_driver_for(
        browser_version="115.0.5790.99",
        responses={
            CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL: {
                "builds": {},
            },
            CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL: {
                "milestones": {
                    "115": {
                        "version": "115.0.5790.170",
                    },
                },
            },
        },
    )

    assert driver.get_latest_release_version() == "115.0.5790.170"

    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
        CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL,
    ]


def test_chrome_115_plus_uses_chrome_for_testing_macos_download_url_after_milestone_fallback():
    driver, http_client = chrome_driver_for(
        browser_version="131.0.6778.1",
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
                                    "platform": "mac-arm64",
                                    "url": (
                                        "https://storage.googleapis.com/"
                                        "chrome-for-testing-public/"
                                        "131.0.6778.264/"
                                        "mac-arm64/"
                                        "chromedriver-mac-arm64.zip"
                                    ),
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

    assert (
        driver.get_url_for_version_and_platform(driver_version, "mac-arm64")
        == "https://storage.googleapis.com/"
           "chrome-for-testing-public/"
           "131.0.6778.264/"
           "mac-arm64/"
           "chromedriver-mac-arm64.zip"
    )

    assert http_client.requested_urls == [
        CHROME_FOR_TESTING_LATEST_PATCH_VERSIONS_PER_BUILD_URL,
        CHROME_FOR_TESTING_LATEST_VERSIONS_PER_MILESTONE_URL,
        CHROME_FOR_TESTING_KNOWN_GOOD_VERSIONS_URL,
    ]


def test_chromium_cft_json_parser_handles_gzip_compressed_response():
    class Response:
        headers = {"Content-Encoding": "gzip"}
        text = ""
        content = gzip.compress(
            json.dumps({"builds": {"120.0.6099": {"version": "120.0.6099.109"}}}).encode("utf-8")
        )

        @staticmethod
        def json():
            raise ValueError("broken json parser")

    driver, _ = chrome_driver_for(browser_version="120.0.6099.71", responses={})
    parsed = driver._parse_json_response(Response())

    assert parsed["builds"]["120.0.6099"]["version"] == "120.0.6099.109"


def test_chromium_cft_json_parser_handles_deflate_compressed_response():
    class Response:
        headers = {"Content-Encoding": "deflate"}
        text = ""
        content = zlib.compress(
            json.dumps({"versions": [{"version": "120.0.6099.109"}]}).encode("utf-8")
        )

        @staticmethod
        def json():
            raise ValueError("broken json parser")

    driver, _ = chrome_driver_for(browser_version="120.0.6099.71", responses={})
    parsed = driver._parse_json_response(Response())

    assert parsed["versions"][0]["version"] == "120.0.6099.109"
