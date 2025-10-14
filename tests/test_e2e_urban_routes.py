# tests/test_e2e_urban_routes.py
from pages.route_page import RoutePage
import data
import helpers

def test_urban_routes_e2e(driver):
    page = RoutePage(driver)

    # 1) Open app
    page.open()

    # 2) Enter addresses (matches your POM: set_from / set_to)
    page.set_from(data.FROM_ADDRESS)
    page.set_to(data.TO_ADDRESS)

    # 3) Choose tariff (matches your POM: choose_supportive)
    page.choose_supportive()

    # 4) Phone flow: enter phone, then read code from performance logs
    page.enter_phone(data.PHONE)
    code = helpers.retrieve_phone_code(driver)   # IMPORTANT: pass driver, not phone
    page.enter_sms_code(code)

    # 5) Card flow: your POM has open_payment() + add_card(number, cvv)
    page.open_payment()
    page.add_card(data.CARD_NUMBER, data.CARD_CVV)

    # 6) Order taxi and assert the "driver searching" modal appears
    page.click_order()
    assert page.is_car_search_modal_visible(), "Driver search modal not visible"

