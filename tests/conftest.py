import os
import shutil
from pprint import pprint
import sys

import pytest
import browsers
from webdriver_manager.core.constants import DEFAULT_PROJECT_ROOT_CACHE_PATH, DEFAULT_USER_HOME_CACHE_PATH, ROOT_FOLDER_NAME
from webdriver_manager.core.logger import log


@pytest.fixture(scope="session", autouse=True)
def list_browsers():
    pprint(list(browsers.browsers()))


@pytest.fixture()
def delete_drivers_dir():
    def remove_if_exists(path):
        if os.path.exists(path):
            log(f"Delete {path} folder")
            shutil.rmtree(path)

    project_cache_paths = [
        os.path.join(sys.path[0], "custom-cache"),
        os.path.join(sys.path[0], "custom"),
        os.path.join(sys.path[0], "ssl_disabled"),
    ]

    user_home_cache_paths = [
        os.path.join(os.path.expanduser("~"), "custom-cache"),
        os.path.join(os.path.expanduser("~"), "custom"),
        os.path.join(os.path.expanduser("~"), "ssl_disabled"),
    ]

    try:
        remove_if_exists(DEFAULT_USER_HOME_CACHE_PATH)
        remove_if_exists(DEFAULT_PROJECT_ROOT_CACHE_PATH)

        for cache_path in project_cache_paths + user_home_cache_paths:
            if os.path.exists(os.path.join(cache_path, ROOT_FOLDER_NAME)):
                remove_if_exists(cache_path)

    except PermissionError as e:
        print(f"Can not delete folder {e}")


@pytest.fixture(scope='function')
def ssl_verify_enable():
    yield
    os.environ.pop('WDM_SSL_VERIFY', None)