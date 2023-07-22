from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


def test_chrome_manager_with_selenium():
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(service=ChromeService(driver_path))
    driver.get("http://automation-remarks.com")
    driver.close()
