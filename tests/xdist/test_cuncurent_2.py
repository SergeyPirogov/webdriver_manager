import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager


def test_chrome_manager_with_selenium():
    logging.info(os.environ.get("PYTEST_XDIST_WORKER"))

    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(service=Service(driver_path))
    driver.get("http://automation-remarks.com")
    driver.close()
