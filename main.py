# main.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

import helpers
import data
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Enable Chrome logging so helpers.retrieve_phone_code() works
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        options = Options()
        options.add_argument("--window-size=1366,768")
        # If you prefer headless (no browser window), uncomment the next line:
        # options.add_argument("--headless=new")

        cls.driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)

        # Launch app URL
        app_url = os.environ.get(
            "URBAN_ROUTES_URL",
            "https://cnt-eb5b1fb8-a8a6-482d-813a-021c5e7712fc.containerhub.tripleten-services.com",
        )

        # Optional network-reachability check
        assert helpers.is_url_reachable(app_url), f"App not reachable: {app_url}"

        # Create page-object instance
        cls.page = UrbanRoutesPage(cls.driver, base_url=app_url)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # ---------- Helper to get to Supportive screen ----------
    def _reach_order_screen_supportive(self):
        self.page.open()
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.choose_supportive_if_needed()

    # --------------------- TESTS ---------------------

    def test_set_address(self):
        self.page.open()
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)

    def test_select_supportive_plan(self):
        self.page.open()
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        self.page.click_call_taxi()
        self.page.choose_supportive_if_needed()

    def test_fill_phone_number(self):
        self._reach_order_screen_supportive()
        self.page.enter_phone_and_confirm(data.PHONE_NUMBER, helpers.retrieve_phone_code)

    def test_add_credit_card(self):
        self._reach_order_screen_supportive()
        self.page.add_card(data.CARD_NUMBER, data.CARD_CVV)

    def test_comment_for_driver(self):
        self._reach_order_screen_supportive()
        self.page.write_comment(data.DRIVER_COMMENT)

    def test_blanket_and_handkerchiefs(self):
        self._reach_order_screen_supportive()
        self.page.toggle_blanket()

    def test_order_two_icecreams(self):
        self._reach_order_screen_supportive()
        self.page.add_icecreams(count=2)

    def test_order_taxi_supportive(self):
        self._reach_order_screen_supportive()
        self.page.enter_phone_and_confirm(data.PHONE_NUMBER, helpers.retrieve_phone_code)
        self.page.write_comment(data.DRIVER_COMMENT)
        self.page.click_order()
        assert self.page.is_car_search_modal_visible() is True, "Car search modal did not appear"
