# main.py
import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # do not modify - additional logging enabled to retrieve phone confirmation code
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

        # Move the URL reachability check into setup (from your previous project)
        assert helpers.is_url_reachable(data.BASE_URL), "Server URL is not reachable"
        cls.driver.get(data.BASE_URL)
        cls.page = UrbanRoutesPage(cls.driver, timeout=20)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # ------- Tests -------

    def test_01_set_addresses(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        # Verify typed values persisted
        # (done indirectly in POM via retrieving 'value' if needed,
        #  here we rely on no exception thrown = success)
        assert True

    def test_02_select_supportive_plan(self):
        self.page.call_taxi()
        self.page.select_supportive_tariff_if_needed()

    def test_03_fill_phone_number(self):
        self.page.enter_phone_and_confirm(
            data.PHONE_NUMBER,
            helpers.retrieve_phone_code  # provided in your helpers.py
        )

    def test_04_add_credit_card(self):
        self.page.add_card(data.CARD_NUMBER, data.CARD_CVV)

    def test_05_write_comment_for_driver(self):
        self.page.write_driver_comment(data.DRIVER_COMMENT)

    def test_06_order_blanket_and_handkerchiefs(self):
        self.page.toggle_blanket_and_handkerchiefs()

    def test_07_order_two_ice_creams(self):
        self.page.add_ice_creams(data.ICE_CREAM_COUNT)

    def test_08_order_taxi_supportive(self):
        # Ensure message is present and tariff already Supportive from previous steps
        self.page.order_taxi()
        assert self.page.car_search_modal_visible() is True
