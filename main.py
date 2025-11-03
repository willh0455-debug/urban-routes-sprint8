import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from pages import UrbanRoutesPage
import helpers
import data


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        """Initialize a single WebDriver instance for all tests."""
        cls.driver = webdriver.Chrome()
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.base_url = data.URBAN_ROUTES_URL

    @classmethod
    def teardown_class(cls):
        """Quit the browser when all tests are finished."""
        cls.driver.quit()

    @property
    def driver(self):
        return self.__class__.driver

    def _page(self) -> UrbanRoutesPage:
        """Return a fresh page-object instance bound to the shared driver."""
        return UrbanRoutesPage(self.driver)

    # ----- Small flow helpers (not tests themselves) -----
    def _go_to_supportive_taxi(self) -> UrbanRoutesPage:
        """Open the site, build the route, and go to the Supportive tariff."""
        page = self._page()
        page.open(self.base_url)
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.choose_supportive()
        return page

    def _verify_phone(self, page: UrbanRoutesPage) -> None:
        """Run the full phone-confirmation flow for the current page."""
        page.fill_phone_number(data.PHONE_NUMBER)
        page.click_phone_next()
        code = helpers.retrieve_phone_code(self.driver)
        page.fill_phone_code(code)
        page.confirm_phone_code()

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
        page = self._go_to_supportive_taxi()
        page.check_supportive_selected()

    # 3. Fill in phone number and confirm
    def test_filling_in_phone_number(self):
        page = self._go_to_supportive_taxi()
        self._verify_phone(page)
        # If something is wrong with the flow, the helper will raise an error.

    # 4. Add payment method (card)
    def test_adding_payment_method(self):
        page = self._go_to_supportive_taxi()
        self._verify_phone(page)

        page.open_payment_form()
        page.add_card(data.CARD_NUMBER, data.CARD_CODE, data.CARD_EXP, data.CARD_NAME)
        page.save_card()
        page.check_card_saved()

    # 5. Add a message for the driver
    def test_message_for_driver(self):
        page = self._go_to_supportive_taxi()
        self._verify_phone(page)

        page.open_message_form()
        page.set_message_for_driver(data.MESSAGE_FOR_DRIVER)
        page.save_message()
        page.check_message_saved(data.MESSAGE_FOR_DRIVER)

    # 6. Turn on blanket & handkerchiefs
    def test_ordering_blanket_and_handkerchiefs(self):
        page = self._go_to_supportive_taxi()
        self._verify_phone(page)

        page.open_requirements()
        page.toggle_blanket_and_handkerchiefs(checked=True)
        page.save_requirements()
        page.check_blanket_and_handkerchiefs_selected()

    # 7. Order two ice creams
    def test_order_2_ice_creams(self):
        page = self._go_to_supportive_taxi()
        self._verify_phone(page)

        page.open_requirements()
        page.set_ice_cream_count(data.ICE_CREAM_COUNT)
        page.save_requirements()
        page.check_ice_cream_count(data.ICE_CREAM_COUNT)

    # 8. Final supportive taxi order
    def test_order_supportive_taxi(self):
        page = self._go_to_supportive_taxi()
        self._verify_phone(page)

        # Payment
        page.open_payment_form()
        page.add_card(data.CARD_NUMBER, data.CARD_CODE, data.CARD_EXP, data.CARD_NAME)
        page.save_card()

        # Message for driver
        page.open_message_form()
        page.set_message_for_driver(data.MESSAGE_FOR_DRIVER)
        page.save_message()

        # Requirements (blanket + ice cream)
        page.open_requirements()
        page.toggle_blanket_and_handkerchiefs(checked=True)
        page.set_ice_cream_count(data.ICE_CREAM_COUNT)
        page.save_requirements()

        # Final order
        page.order_taxi()
        page.check_taxi_ordered()
