import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from pages import UrbanRoutesPage
import helpers
import data


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        """
        Initialize the WebDriver once for all tests.
        This version avoids the deprecated 'desired_capabilities'
        argument so it works with newer Selenium versions too.
        """
        # basic Chrome driver; TripleTen runner will handle details
        cls.driver = webdriver.Chrome()
        cls.wait = WebDriverWait(cls.driver, 10)

        # Use the project URL from data.py
        base_url = getattr(data, "URBAN_ROUTES_URL", None) or getattr(data, "BASE_URL", None)
        assert base_url, "URBAN_ROUTES_URL or BASE_URL must be defined in data.py"

        cls.base_url = base_url

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def setup_method(self):
        """Start each test from the main page."""
        self.driver.get(self.base_url)

    @property
    def driver(self):
        return self.__class__.driver

    def _page(self):
        """Helper to get a fresh page object."""
        return UrbanRoutesPage(self.driver)

    # 1. Check setting route addresses
    def test_set_route(self):
        page = self._page()
        page.open(self.base_url)
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)

        assert page.get_from_value() == data.ADDRESS_FROM
        assert page.get_to_value() == data.ADDRESS_TO

    # 2. Select the Supportive plan
    def test_select_supportive_plan(self):
        page = self._page()
        page.open(self.base_url)
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.choose_supportive()

        assert page.is_supportive_selected()

    # 3. Fill in phone number and confirm
    def test_filling_in_phone_number(self):
        page = self._page()
        page.open(self.base_url)
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.choose_supportive()

        page.enter_phone(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.enter_sms_code(code)
        page.click_confirm_phone()
        # If something goes wrong, helpers or page methods should raise

    # 4. Add payment method (card)
    def test_adding_payment_method(self):
        page = self._page()
        page.open(self.base_url)
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.choose_supportive()

        page.enter_phone(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.enter_sms_code(code)
        page.click_confirm_phone()

        page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert page.is_payment_card_active()

    # 5. Add a message for the driver
    def test_message_for_driver(self):
        page = self._page()
        page.open(self.base_url)
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.choose_supportive()

        page.enter_phone(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.enter_sms_code(code)
        page.click_confirm_phone()

        page.leave_driver_comment(data.MESSAGE_FOR_DRIVER)
        assert page.get_driver_comment_value() == data.MESSAGE_FOR_DRIVER

    # 6. Turn on blanket & handkerchiefs
    def test_ordering_blanket_and_handkerchiefs(self):
        page = self._page()
        page.open(self.base_url)
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.choose_supportive()

        page.enter_phone(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.enter_sms_code(code)
        page.click_confirm_phone()

        page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        page.toggle_blanket_handkerchiefs()
        assert page.is_blanket_checked()

    # 7. Order two ice creams
    def test_order_2_ice_creams(self):
        page = self._page()
        page.open(self.base_url)
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.choose_supportive()

        page.enter_phone(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.enter_sms_code(code)
        page.click_confirm_phone()

        page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        page.add_ice_creams(count=2)
        assert page.get_ice_cream_count() == 2

    # 8. Final supportive taxi order
    def test_order_supportive_taxi(self):
        page = self._page()
        page.open(self.base_url)
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.choose_supportive()

        page.enter_phone(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.enter_sms_code(code)
        page.click_confirm_phone()

        page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        page.leave_driver_comment(data.MESSAGE_FOR_DRIVER)
        page.toggle_blanket_handkerchiefs()
        page.add_ice_creams(count=2)

        page.click_order()
        assert page.is_car_search_modal_visible()
