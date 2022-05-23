import os
import re

import pytest
from selenium import webdriver

from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.core.utils import PATTERN, ChromeType


def test_edge_manager_with_selenium():
    driver_path = EdgeChromiumDriverManager().install()
    driver = webdriver.Edge(executable_path=driver_path, capabilities={})
    driver.get("http://automation-remarks.com")
    driver.quit()


def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "ssl_disabled",
    )
    driver_path = EdgeChromiumDriverManager(path=custom_path).install()
    os.environ['WDM_SSL_VERIFY'] = '1'
    assert os.path.exists(driver_path)


def test_edge_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        EdgeChromiumDriverManager(
            version="0.2",
            os_type='win64',
        ).install()

    assert (
               "There is no such driver by url "
               "https://msedgedriver.azureedge.net/0.2/edgedriver_win64.zip"
           ) in ex.value.args[0]


@pytest.mark.parametrize('os_type', ['win32', 'win64', 'mac64', 'linux64'])
@pytest.mark.parametrize('specific_version', ['86.0.600.0'])
def test_edge_with_specific_version(os_type, specific_version):
    bin_path = EdgeChromiumDriverManager(
        version=specific_version,
        os_type=os_type,
    ).install()
    assert os.path.exists(bin_path)


@pytest.mark.parametrize('os_type', ['win32', 'win64', 'mac64', 'linux64'])
@pytest.mark.parametrize('specific_version', ['87.0.637.0'])
def test_can_get_edge_driver_from_cache(os_type, specific_version):
    EdgeChromiumDriverManager(
        version=specific_version,
        os_type=os_type,
    ).install()
    driver_path = EdgeChromiumDriverManager(
        version=specific_version,
        os_type=os_type
    ).install()
    assert os.path.exists(driver_path)


def test_get_stable_release_version():
    pattern = PATTERN[ChromeType.MSEDGE]
    edge_driver = EdgeChromiumDriverManager(
    ).driver

    version = edge_driver.get_stable_release_version()
    version = re.search(pattern, version).group(0)

    assert len(version.split('.')) == 3, (
        f"version '{version}' doesn't match version's count parts"
    )
