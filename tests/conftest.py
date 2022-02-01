import os

import pytest


@pytest.fixture(scope='function')
def ssl_verify_enable():
    yield
    os.environ['WDM_SSL_VERIFY'] = ''
