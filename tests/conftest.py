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
    try:
        if os.path.exists(DEFAULT_USER_HOME_CACHE_PATH):
            log(f"Delete {DEFAULT_USER_HOME_CACHE_PATH} folder")
            shutil.rmtree(DEFAULT_USER_HOME_CACHE_PATH)
        if os.path.exists(DEFAULT_PROJECT_ROOT_CACHE_PATH):
            log(f"Delete {DEFAULT_PROJECT_ROOT_CACHE_PATH} folder")
            shutil.rmtree(DEFAULT_PROJECT_ROOT_CACHE_PATH)

        if os.path.exists(os.path.join(sys.path[0], 'custom-cache', ROOT_FOLDER_NAME)):
            log(f"Delete {os.path.join(sys.path[0], 'custom-cache')} folder")
            shutil.rmtree(os.path.join(sys.path[0], 'custom-cache'))
        if os.path.exists(os.path.join(sys.path[0], 'custom', ROOT_FOLDER_NAME)):
            log(f"Delete {os.path.join(sys.path[0], 'custom')} folder")
            shutil.rmtree(os.path.join(sys.path[0], 'custom'))
        if os.path.exists(os.path.join(sys.path[0], 'ssl_disabled', ROOT_FOLDER_NAME)):
            log(f"Delete {os.path.join(sys.path[0], 'ssl_disabled')} folder")
            shutil.rmtree(os.path.join(sys.path[0], 'ssl_disabled'))
        
        if os.path.exists(os.path.join(os.path.expanduser("~"), 'custom-cache', ROOT_FOLDER_NAME)):
            log(f"Delete {os.path.join(os.path.expanduser("~"), 'custom-cache')} folder")
            shutil.rmtree(os.path.join(os.path.expanduser("~"), 'custom-cache'))
        if os.path.exists(os.path.join(os.path.expanduser("~"), 'custom', ROOT_FOLDER_NAME)):
            log(f"Delete {os.path.join(os.path.expanduser("~"), 'custom')} folder")
            shutil.rmtree(os.path.join(os.path.expanduser("~"), 'custom'))
        if os.path.exists(os.path.join(os.path.expanduser("~"), 'ssl_disabled', ROOT_FOLDER_NAME)):
            log(f"Delete {os.path.join(os.path.expanduser("~"), 'ssl_disabled')} folder")
            shutil.rmtree(os.path.join(os.path.expanduser("~"), 'ssl_disabled'))

    except PermissionError as e:
        print(f"Can not delete folder {e}")


@pytest.fixture(scope='function')
def ssl_verify_enable():
    yield
    os.environ.pop('WDM_SSL_VERIFY', None)