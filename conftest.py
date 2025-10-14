import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture
def driver():
    chrome_options = Options()

    # Run Chrome in headless mode (needed for CI reviewers)
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1366,768")

    # Create the driver
    drv = webdriver.Chrome(options=chrome_options)
    drv.set_page_load_timeout(30)
    drv.implicitly_wait(0)  # use explicit waits instead of implicit

    yield drv
    drv.quit()

@pytest.fixture
def wait(driver):
    """Provide a 10-second explicit WebDriverWait to all tests."""
    return WebDriverWait(driver, 10)
