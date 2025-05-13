import os

import pytest


@pytest.fixture()
def user_account(worker_id):
    """ use a different account in each xdist worker """
    os.environ.pop('WDM_SSL_VERIFY', None)
