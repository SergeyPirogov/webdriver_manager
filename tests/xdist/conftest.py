import os

import pytest
import logging

@pytest.fixture()
def user_account(worker_id):
    """ use a different account in each xdist worker """
    os.environ['WDM_LOCAL'] = '1'

    logging.info(f"worker id: {worker_id}")
