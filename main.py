# main.py
# Minimal setup/teardown aligned with project requirements.
# Actual tests live in tests/test_e2e_urban_routes.py

import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities

import helpers
import data
from pages import UrbanRoutesPage  # reviewers expect pages.py at repo root


class TestUrbanRoutesSetup:
    @classmethod
    def setup_class(cls):
        # Performance logs required for helpers.retrieve_phone_code(driver)
        caps = DesiredCapabilities.CHROME.copy()
        caps["goog:loggingPrefs"] = {"performance": "ALL"}

        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")  # enable if needed on reviewer machine

        # Let Selenium Manager resolve chromedriver; pass caps via options.set_capability
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.driver, 10)

        base_url = getattr(data, "BASE_URL", getattr(data, "URBAN_ROUTES_URL", None))
        assert base_url, "BASE_URL (or URBAN_ROUTES_URL) missing in data.py"

        if not helpers.is_url_reachable(base_url):
            pytest.skip(f"BASE_URL not reachable: {base_url}")

        cls.driver.get(base_url)

    @classmethod
    def teardown_class(cls):
        try:
            cls.driver.quit()
        except Exception:
            pass

