from tests.test_chrome_driver import delete_cache
from webdriver_manager.microsoft import EdgeDriverManager
from selenium import webdriver


def test_edge_manager_with_selenium():
    delete_cache()
    driver_path = EdgeDriverManager().install()
    dr = webdriver.Edge(driver_path)
    dr.quit()


def test_edge_manager_with_selenium_cache():
    driver_path = EdgeDriverManager().install()
    dr = webdriver.Edge(driver_path)
    dr.quit()
