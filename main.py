import pytest
import data
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    def setup_method(self):
        self.page = None

    # 1. Set route addresses
    def test_set_route(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()

        # optional asserts if you have get_from_value() / get_to_value() methods
        # assert page.get_from_value() == data.ADDRESS_FROM
        # assert page.get_to_value() == data.ADDRESS_TO

    # 2. Select the Supportive plan
    def test_select_supportive_plan(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()

    # 3. Fill in phone number and confirm it
    def test_filling_in_phone_number(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()
        page.fill_phone_number(data.PHONE_NUMBER)
        page.confirm_code(data.PHONE_CODE)

    # 4. Add a payment method (card)
    def test_adding_payment_method(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()
        page.fill_phone_number(data.PHONE_NUMBER)
        page.confirm_code(data.PHONE_CODE)
        page.add_payment_method(data.CARD_NUMBER, data.CARD_CODE)

    # 5. Leave a message for the driver
    def test_message_for_driver(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()
        page.fill_phone_number(data.PHONE_NUMBER)
        page.confirm_code(data.PHONE_CODE)
        page.add_payment_method(data.CARD_NUMBER, data.CARD_CODE)
        page.add_message_for_driver(data.MESSAGE_FOR_DRIVER)

    # 6. Order a blanket and handkerchiefs
    def test_ordering_blanket_and_handkerchiefs(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()
        page.fill_phone_number(data.PHONE_NUMBER)
        page.confirm_code(data.PHONE_CODE)
        page.add_payment_method(data.CARD_NUMBER, data.CARD_CODE)
        page.order_blanket_and_handkerchiefs()

    # 7. Order two ice creams
    def test_order_2_ice_creams(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()
        page.fill_phone_number(data.PHONE_NUMBER)
        page.confirm_code(data.PHONE_CODE)
        page.add_payment_method(data.CARD_NUMBER, data.CARD_CODE)
        page.order_two_ice_creams()

    # 8. Final test for completing Supportive taxi order
    def test_order_supportive_taxi(self, driver):
        driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(driver)

        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)
        page.submit_route()
        page.select_supportive_tariff()
        page.fill_phone_number(data.PHONE_NUMBER)
        page.confirm_code(data.PHONE_CODE)
        page.add_payment_method(data.CARD_NUMBER, data.CARD_CODE)
        page.add_message_for_driver(data.MESSAGE_FOR_DRIVER)
        page.order_blanket_and_handkerchiefs()
        page.order_two_ice_creams()
