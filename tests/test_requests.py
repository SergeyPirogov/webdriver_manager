import pytest
import requests

from webdriver_manager.chrome import ChromeDriverManager


def test_use_proxy():
    session = requests.Session()
    session.proxies = {
        "http": "http://127.0.0.1:1",  # it's a error proxy
        "https": "http://127.0.0.1:1",
    }

    with pytest.raises(requests.exceptions.ProxyError):
        # If an exception occurs, the proxy settings take effect
        ChromeDriverManager(session=session).install()


def test_disable_ssl_verify():
    session = requests.Session()
    session.verify = False

    ChromeDriverManager(session=session).install()
