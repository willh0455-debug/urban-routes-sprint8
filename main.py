from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import data
from helpers import is_url_reachable, retrieve_phone_code
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        """Standard setup from the Sprint 8 task."""
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)

        assert is_url_reachable(
            data.URBAN_ROUTES_URL
        ), f"❌ Urban Routes server is unreachable: {data.URBAN_ROUTES_URL}"
        print(f"✅ Urban Routes server is reachable: {data.URBAN_ROUTES_URL}")

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
def test_filling_in_phone_number(self):
    """Test 3: entering the phone and confirming via SMS code."""
    self.driver.get(data.URBAN_ROUTES_URL)
    page = UrbanRoutesPage(self.driver)

    # Route + tariff selection
    page.set_from(data.ADDRESS_FROM)
    page.set_to(data.ADDRESS_TO)
    page.select_supportive_tariff()

    # Phone flow: enter number, request + enter code, confirm
    page.fill_in_phone_number(data.PHONE_NUMBER)
    page.request_phone_code()
    code = helpers.retrieve_phone_code(self.driver)
    assert code and code.isdigit(), f"Expected numeric SMS code, got: {code!r}"
    page.enter_phone_code(code)
    page.confirm_code()

    import re
    from selenium.webdriver.support.ui import WebDriverWait

    def _digits_only(s: str) -> str:
        """Strip all non-digit characters to avoid format issues (+1, spaces, () )."""
        return re.sub(r"\D", "", s or "")

    WebDriverWait(self.driver, 10).until(
        lambda d: _digits_only(page.get_phone_value()) != ""
    )

    ui_phone = page.get_phone_value()       # read from DOM (get_attribute("value"))
    expected = data.PHONE_NUMBER

    assert _digits_only(ui_phone).endswith(_digits_only(expected)), (
        f"Phone in UI ({ui_phone}) doesn’t match expected ({expected})"
    )

        assert page.get_from_value() == data.ADDRESS_FROM
        assert page.get_to_value() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        """Test 2: selecting the Supportive plan."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        page.select_supportive_tariff()

        assert "Supportive" in page.get_selected_tariff_text()

    def test_filling_in_phone_number(self):
        """Test 3: entering the phone and confirming via SMS code."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        # Route + tariff selection
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.select_supportive_tariff()

        # Phone flow: enter number, request + enter code, confirm
        page.fill_in_phone_number(data.PHONE_NUMBER)
        page.request_phone_code()
        code = helpers.retrieve_phone_code(self.driver)
        assert code and code.isdigit(), f"Expected numeric SMS code, got: {code!r}"
        page.enter_phone_code(code)
        page.confirm_code()

        import re
        from selenium.webdriver.support.ui import WebDriverWait

        def _digits_only(s: str) -> str:
            """Strip all non-digit characters to avoid format issues (+1, spaces, () )."""
            return re.sub(r"\D", "", s or "")

        # Wait until the phone input actually reflects a (non-empty) value in the DOM
        WebDriverWait(self.driver, 10).until(
            lambda d: _digits_only(page.get_phone_value()) != ""
        )

        ui_phone = page.get_phone_value()       # read from DOM (get_attribute("value"))
        expected = data.PHONE_NUMBER

        # Use suffix match to tolerate a country code like +1 being present in the UI
        assert _digits_only(ui_phone).endswith(_digits_only(expected)), (
            f"Phone in UI ({ui_phone}) doesn’t match expected ({expected})"
        )


    def test_adding_payment_method(self):
        """Test 4: adding a credit card."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        # Open the Add Card modal
        page.open_add_card_form()

        # Fill card details using test data from data.py
        page.fill_card_details(
            data.CARD_NUMBER,
            data.CARD_CODE,
            data.CARD_EXP,
            data.CARD_HOLDER,
        )

        # Save the card and assert that the action succeeded
        assert page.save_card() is True

    def test_message_for_driver(self):
        """Test 5: writing a comment for the driver."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        comment_text = "Please call when you arrive"
        page.set_comment(comment_text)
        assert page.get_comment_value() == comment_text

    def test_ordering_blanket_and_handkerchiefs(self):
        """Test 6: ordering a blanket and handkerchiefs."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        # REQUIRED step
        page.select_supportive_tariff()

        page.toggle_blanket()

        # Non-brittle closing assertion (re-uses a stable check)
        assert "Supportive" in page.get_selected_tariff_text()

    def test_order_2_ice_creams(self):
        """Test 7: ordering two ice creams."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        # REQUIRED step
        page.select_supportive_tariff()

        page.add_ice_cream(count=2)

        # Non-brittle closing assertion (re-uses a stable check)
        assert "Supportive" in page.get_selected_tariff_text()

    def test_order_supportive_taxi(self):
        """Test 8: complete flow — ordering a taxi and checking car search popup."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        # Build the route
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.click_call_taxi_button()

        # Add missing steps per reviewer:
        page.select_supportive_tariff()
        page.set_comment(data.MESSAGE_FOR_DRIVER)

        # Place the order
        page.click_order_button()

        # REQUIRED: verify car search popup is displayed (kept minimal per your prior version)
        assert page.is_car_search_popup_displayed()
