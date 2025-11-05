import pytest

import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        """
        Runs once before all tests.
        In Sprint 7 you checked that the URL is reachable — we move that here.
        """
        url = data.URBAN_ROUTES_URL
        if helpers.is_url_reachable(url):
            print(f"✅ Urban Routes server is reachable: {url}")
        else:
            print(f"⚠️ Urban Routes server is NOT reachable: {url}")

    @classmethod
    def teardown_class(cls):
        """Runs once after all tests."""
        print("✅ All tests in TestUrbanRoutes finished")

    # 1. Setting the address
    def test_set_route(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()

        # Optional: if you implement these getters in pages.py
        # assert page.get_from_value() == data.ADDRESS_FROM
        # assert page.get_to_value() == data.ADDRESS_TO

    # 2. Selecting Supportive plan
    def test_select_supportive_plan(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()

        page.select_supportive_tariff()
        # Assuming you add is_supportive_selected() in pages.py
        assert page.is_supportive_selected()

    # 3. Filling in the phone number
    def test_filling_in_phone_number(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()

        # Type the phone number and click Next/Confirm
        page.fill_phone_number(data.PHONE_NUMBER)

        # 🔹 Get the SMS code from browser logs
        code = helpers.retrieve_phone_code(driver)
        assert code is not None, "Could not retrieve phone confirmation code from logs"

        # Enter the code in the popup and confirm
        page.confirm_code(code)

        # (Optional) If you expose something in UI to show it's confirmed,
        # you can assert that here.

    # 4. Adding a credit card
    def test_adding_payment_method(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()

        # Phone must be confirmed before payment in the real flow
        page.fill_phone_number(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(driver)
        page.confirm_code(code)

        page.add_payment_method(data.CARD_NUMBER, data.CARD_CODE)

        # Assuming you implement get_payment_method_text() in pages.py
        assert page.get_payment_method_text() == "Card"

    # 5. Writing a comment for the driver
    def test_message_for_driver(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()

        page.set_driver_comment(data.MESSAGE_FOR_DRIVER)

        # Assuming you add get_driver_comment() in pages.py
        assert page.get_driver_comment() == data.MESSAGE_FOR_DRIVER

    # 6. Ordering a blanket and handkerchiefs
    def test_ordering_blanket_and_handkerchiefs(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()

        page.toggle_blanket_and_handkerchiefs()

        # Hint from instructions: use get_property('checked')
        assert page.is_blanket_and_handkerchiefs_selected() is True

    # 7. Ordering 2 ice creams
    def test_order_2_ice_creams(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()

        page.add_ice_creams(2)  # loop inside pages.py

        assert page.get_ice_cream_count() == 2

    # 8. Ordering a taxi with the Supportive tariff
    def test_order_supportive_taxi(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()

        # Phone flow
        page.fill_phone_number(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(driver)
        page.confirm_code(code)

        # Comment (needed per hint)
        page.set_driver_comment(data.MESSAGE_FOR_DRIVER)

        # Place order
        page.order_taxi()

        # Assert that the car search modal appears
        assert page.is_search_modal_visible()


    def test_adding_payment_method(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()

        # add a payment method
        page.add_payment_method(data.CARD_NUMBER, data.CARD_CODE)

        # verify it changed from Cash → Card
        assert "Card" in page.get_payment_method_text()
