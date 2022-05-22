import os
import shutil

import pytest

project_root = os.path.dirname(os.path.dirname(__file__))
DEFAULT_DRIVER_DIR = f"{project_root}{os.sep}.drivers"


@pytest.fixture()
def delete_drivers_dir():
    if os.path.exists(DEFAULT_DRIVER_DIR):
        shutil.rmtree(DEFAULT_DRIVER_DIR)


@pytest.fixture(scope='function')
def ssl_verify_enable():
    yield
    os.environ['WDM_SSL_VERIFY'] = ''
