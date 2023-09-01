from concurrent.futures import ProcessPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def _run(_):
    chromedriver_path = ChromeDriverManager().install()
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
    url = 'https://www.google.com'
    driver.set_page_load_timeout(10)
    driver.get(url)
    driver.quit()


def test_install_driver_in_multi_processes(delete_drivers_dir):
    pool = ProcessPoolExecutor(max_workers=5)
    assert list(pool.map(_run, range(5)))
