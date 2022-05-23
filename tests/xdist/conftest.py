import pytest


@pytest.fixture()
def user_account(worker_id):
    """ use a different account in each xdist worker """
    print(f"worker id: {worker_id}")
