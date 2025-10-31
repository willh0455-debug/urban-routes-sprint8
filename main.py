# main.py
import pytest
from selenium import webdriver

import data
from pages import UrbanRoutesPage
from helpers import is_url_reachable  # keep helpers EXACTLY as provided in Sprint 7

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # === Must match the project requirements ===
        # Logging preferences for performance logs:
        # (Identical structure—do not deviate)
        options = webdriver.ChromeOptions()
        # “goog:loggingPrefs” is the canonical capability key ChromeDriver uses
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        # Instantiate driver
        cls.driver = webdriver.Chrome(options=options)

        # URL reachability check using the provided helper (unchanged)
        assert is_url_reachable(data.URBAN_ROUTES_URL), (
            f"URL not reachable: {data.URBAN_ROUTES_URL}. "
            f"Make sure your container is running and the URL in data.py is correct."
        )

        try:
            cls.driver.maximize_window()
        except Exception:
            # In some CI containers this may no-op; that’s fine
            pass

    @classmethod
    def teardown_class(cls):
        try:
            cls.driver.quit()
        except Exception:
            pass

    # === Test 1: Standardized init + clear assertion on From field ===
    def test_set_route(self):
        # Every test begins by opening the URL and instantiating the page
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        # Lesson-pattern setters
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)

        # Explicit assertion using a getter from the page object
        assert page.get_from_value() == data.ADDRESS_FROM

    # === Test 2: Enforce booking flow, then select Supportive plan, verify active ===
    def test_select_supportive_plan(self):
        # Standardized init
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        # Required booking flow: enter both addresses then Call a Taxi
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi()

        # Select Supportive using the same lesson-style method
        page.select_supportive_plan()

        # Verify the active card explicitly
        assert page.get_active_card() == "Supportive"
