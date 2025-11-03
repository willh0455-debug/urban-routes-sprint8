import pytest
from selenium import webdriver

from pages import UrbanRoutesPage
import data
import helpers


class TestUrbanRoutes:
    def setup_method(self):
        """
        Called before each test.
        Create (or reuse) a single shared driver and page object,
        and open the Urban Routes URL.
        """
        cls = self.__class__

        # Create the driver once and reuse it across tests
        if not hasattr(cls, "driver"):
            cls.driver = webdriver.Chrome()

        self.driver = cls.driver
        self.page = UrbanRoutesPage(self.driver)
        self.page.open(data.URBAN_ROUTES_URL)

    @classmethod
    def teardown_class(cls):
        """
        Called once after all tests in this class finish.
        Close the browser.
        """
        cls.driver.quit()

    # ---- Small helpers for common flows ----
    def _build_route_to_supportive(self):
        """Set the route and switch to the Supportive tariff."""
        self.page.set_from(data.ADDRESS_FROM)
        self.page.set_to(data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.choose_supportive()

    def _confirm_phone(self):
        """Complete the phone confirmation flow using helpers.retrieve_phone_code."""
        self.page.fill_phone_number(data.PHONE_NUMBER)
        self.page.click_phone_next()
        code = helpers.retrieve_phone_code(self.driver)
        self.page.fill_phone_code(code)
        self.page.confirm_phone_code()

    # 1. Set route addresses
    def test_set_route(self):
        self.page.set_from(data.ADDRESS_FROM)
        self.page.set_to(data.ADDRESS_TO)

        assert self.page.get_from_value() == data.ADDRESS_FROM
        assert self.page.get_to_value() == data.ADDRESS_TO

    # 2. Select the Supportive plan
    def test_select_supportive_plan(self):
        self._build_route_to_supportive()
        self.page.check_supportive_selected()

    # 3. Fill in phone number and confirm it
    def test_filling_in_phone_number(self):
        self._build_route_to_supportive()
        self._confirm_phone()

    # 4. Add a payment method (card)
    def test_adding_payment_method(self):
        self._build_route_to_supportive()
        self._confirm_phone()

        self.page.open_payment_form()
        self.page.add_card(
            data.CARD_NUMBER,
            data.CARD_CODE,
            data.CARD_EXP,
            data.CARD_NAME,
        )
        self.page.save_card()
        self.page.check_card_saved()

    # 5. Add a message for the driver
    def test_message_for_driver(self):
        self._build_route_to_supportive()
        self._confirm_phone()

        self.page.open_message_form()
        self.page.set_message_for_driver(data.MESSAGE_FOR_DRIVER)
        self.page.save_message()
        self.page.check_message_saved(data.MESSAGE_FOR_DRIVER)

    # 6. Turn on blanket & handkerchiefs
    def test_ordering_blanket_and_handkerchiefs(self):
        self._build_route_to_supportive()
        self._confirm_phone()

        self.page.open_requirements()
        self.page.toggle_blanket_and_handkerchiefs(checked=True)
        self.page.save_requirements()
        self.page.check_blanket_and_handkerchiefs_selected()

    # 7. Order two ice creams
    def test_order_2_ice_creams(self):
        self._build_route_to_supportive()
        self._confirm_phone()

        self.page.open_requirements()
        self.page.set_ice_cream_count(data.ICE_CREAM_COUNT)
        self.page.save_requirements()
        self.page.check_ice_cream_count(data.ICE_CREAM_COUNT)

    # 8. Full supportive taxi order
    def test_order_supportive_taxi(self):
        self._build_route_to_supportive()
        self._confirm_phone()

        # Payment
        self.page.open_payment_form()
        self.page.add_card(
            data.CARD_NUMBER,
            data.CARD_CODE,
            data.CARD_EXP,
            data.CARD_NAME,
        )
        self.page.save_card()

        # Message for driver
        self.page.open_message_form()
        self.page.set_message_for_driver(data.MESSAGE_FOR_DRIVER)
        self.page.save_message()

        # Requirements
        self.page.open_requirements()
        self.page.toggle_blanket_and_handkerchiefs(checked=True)
        self.page.set_ice_cream_count(data.ICE_CREAM_COUNT)
        self.page.save_requirements()

        # Final order
        self.page.order_taxi()
        self.page.check_taxi_ordered()
