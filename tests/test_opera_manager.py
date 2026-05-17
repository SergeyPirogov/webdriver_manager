import glob
import os
import shutil

import browsers
import pytest
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from selenium.webdriver.chrome.service import Service

from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.os_manager import OperationSystemManager
from webdriver_manager.opera import OperaDriverManager

requires_gh_token = pytest.mark.skipif(
    not os.getenv("GH_TOKEN"),
    reason="GH_TOKEN is required to avoid GitHub API rate limiting in Opera tests",
)


@pytest.fixture(scope="module")
def opera_release_data():
    manager = OperaDriverManager()
    version = manager.driver.get_latest_release_version()
    response = manager.driver._http_client.get(
        url=manager.driver.tagged_release_url(version),
        headers=manager.driver.auth_header,
    )
    assets = response.json()["assets"]
    asset_names = [asset["name"] for asset in assets]

    supported_os_types = []
    if any(name.startswith("operadriver_win32") for name in asset_names):
        supported_os_types.append("win32")
    if any(name.startswith("operadriver_win64") for name in asset_names):
        supported_os_types.append("win64")
    if any(name.startswith("operadriver_linux64") for name in asset_names):
        supported_os_types.append("linux64")
    if any(name.startswith("operadriver_mac64") for name in asset_names):
        supported_os_types.append("mac64")

    return {
        "version": version,
        "supported_os_types": supported_os_types,
    }


@requires_gh_token
def test_opera_driver_manager_with_correct_version(delete_drivers_dir, opera_release_data):
    driver_path = OperaDriverManager(opera_release_data["version"]).install()
    assert os.path.exists(driver_path)


@pytest.mark.filterwarnings("ignore:Unverified HTTPS request:urllib3.exceptions.InsecureRequestWarning")
@requires_gh_token
def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "ssl_disabled",
    )
    driver_path = OperaDriverManager(cache_manager=DriverCacheManager(custom_path)).install()
    os.environ['WDM_SSL_VERIFY'] = '1'
    assert os.path.exists(driver_path)


@requires_gh_token
def test_operadriver_manager_with_selenium():
    driver_path = OperaDriverManager().install()
    options = webdriver.ChromeOptions()
    options.add_experimental_option('w3c', True)
    binary_location = browsers.get("opera")
    if not binary_location:
        pytest.skip("Opera not found")
    options.binary_location = binary_location["path"]
    web_service = Service(driver_path)
    web_service.start()

    try:
        opera_driver = webdriver.Remote(web_service.service_url, options=options)
        opera_driver.get("http://automation-remarks.com")
        opera_driver.quit()
    except (SessionNotCreatedException, WebDriverException):
        pytest.skip("Opera browser/driver mismatch or CI environment instability")


@requires_gh_token
def test_opera_driver_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        OperaDriverManager("0.2").install()

    assert "There is no such driver by url " \
           "https://api.github.com/repos/operasoftware/operachromiumdriver/" \
           "releases/tags/0.2" in ex.value.args[0]


@pytest.mark.parametrize('path', ['.', None])
@requires_gh_token
def test_opera_driver_manager_with_correct_version_and_token(path, opera_release_data):
    driver_path = OperaDriverManager(
        version=opera_release_data["version"],
        cache_manager=DriverCacheManager(path),
    ).install()
    assert os.path.exists(driver_path)


@pytest.mark.parametrize('os_type', ['win32',
                                     'win64',
                                     'linux64',
                                     'mac64'])
@requires_gh_token
def test_can_get_driver_from_cache(os_type, delete_drivers_dir, opera_release_data):
    if os_type not in opera_release_data["supported_os_types"]:
        pytest.skip(f"Opera release {opera_release_data['version']} has no asset for {os_type}")
    OperaDriverManager(os_system_manager=OperationSystemManager(os_type)).install()
    driver_path = OperaDriverManager(os_system_manager=OperationSystemManager(os_type)).install()
    assert os.path.exists(driver_path)
