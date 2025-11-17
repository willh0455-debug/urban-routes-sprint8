from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import data
import helpers  # so we can call helpers.is_url_reachable
from helpers import retrieve_phone_code
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        """Standard setup from the Sprint 8 task."""
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        cls.driver = webdriver.Chrome(options=options)

        # URL reachability check (informational, not a test assertion)
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print(
                "Cannot connect to Urban Routes. "
                "Check that the server is still on and running."
            )

        cls.driver.maximize_window()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_set_route(self):
        """Test 1: setting FROM and TO addresses."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        # REQUIRED assertions: verify addresses in the inputs
        assert page.get_from_value() == data.ADDRESS_FROM
        assert page.get_to_value() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        """Test 2: selecting the Supportive plan."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        # Select the Supportive tariff explicitly
        page.select_supportive_tariff()

        # Assert that the active tariff is indeed "Supportive"
        assert "Supportive" in page.get_selected_tariff_text()

    def test_filling_in_phone_number(self):
        """Test 3: entering the phone and confirming via SMS code."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        # Enter phone and request code
        page.enter_phone_number(data.PHONE_NUMBER)
        page.click_phone_next_button()

        # Get SMS code from browser logs
        code = retrieve_phone_code(self.driver)
        assert code is not None, "Could not retrieve phone confirmation code from logs."

        # Enter the code in the popup and confirm
        page.enter_confirmation_code(code)
        page.click_confirm_code_button()

        # REQUIRED assertion: phone on page equals data.PHONE_NUMBER
        assert page.get_entered_phone_number() == data.PHONE_NUMBER

    def test_adding_payment_method(self):
        """Test 4: adding a credit card."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        page.open_add_card_form()
        page.fill_card_details(
            data.CARD_NUMBER,
            data.CARD_CODE,
        )
        page.save_card()

        # ASSERTION: payment method changed from "Cash" to "Card"
        assert page.get_payment_option() == "Card"

    def test_message_for_driver(self):
        """Test 5: writing a comment for the driver."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        page.set_comment(data.MESSAGE_FOR_DRIVER)
        assert page.get_comment_value() == data.MESSAGE_FOR_DRIVER

    def test_ordering_blanket_and_handkerchiefs(self):
        """Test 6: ordering a blanket and handkerchiefs."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        page.select_supportive_tariff()
        page.toggle_blanket()

        # ASSERTION: blanket & handkerchiefs option is toggled on
        assert page.is_checked()

    def test_order_2_ice_creams(self):
        """Test 7: ordering two ice creams."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        page.select_supportive_tariff()
        page.add_ice_cream(count=2)

        # ASSERTION: ice cream counter shows 2
        assert page.get_ice_cream_count() == "2"

    def test_order_supportive_taxi(self):
        """Test 8: complete flow — ordering a taxi and checking car search popup."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        # Build the route
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        # Select the Supportive tariff and set the driver message
        page.select_supportive_tariff()
        page.set_comment(data.MESSAGE_FOR_DRIVER)

        # Place the order
        page.click_order_button()

        # REQUIRED: verify car search popup is displayed
        assert page.wait_for_car_search_popup()
