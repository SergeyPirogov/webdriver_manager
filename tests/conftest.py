import os
import shutil
from pprint import pprint

import pytest
import browsers
from webdriver_manager.core.constants import DEFAULT_PROJECT_ROOT_CACHE_PATH, DEFAULT_USER_HOME_CACHE_PATH
from webdriver_manager.core.logger import log


@pytest.fixture(scope="session", autouse=True)
def list_browsers():
    pprint(list(browsers.browsers()))


@pytest.fixture()
def delete_drivers_dir():
    try:
        if os.path.exists(DEFAULT_USER_HOME_CACHE_PATH):
            log(f"Delete {DEFAULT_USER_HOME_CACHE_PATH} folder")
            shutil.rmtree(DEFAULT_USER_HOME_CACHE_PATH)
        if os.path.exists(DEFAULT_PROJECT_ROOT_CACHE_PATH):
            log(f"Delete {DEFAULT_PROJECT_ROOT_CACHE_PATH} folder")
            shutil.rmtree(DEFAULT_PROJECT_ROOT_CACHE_PATH)
    except PermissionError as e:
        print(f"Can not delete folder {e}")


@pytest.fixture(scope='function')
def ssl_verify_enable():
    yield
    os.environ['WDM_SSL_VERIFY'] = ''
