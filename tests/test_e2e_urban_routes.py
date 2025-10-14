from pages.route_page import RoutePage
import data
import helpers
def test_urban_routes_e2e(driver):
    page = RoutePage(driver)

    # 1) Open app
    page.open()

    # DEBUG: dump HTML so we can inspect if needed
    with open("/tmp/page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # 2) Enter addresses
    page.set_from(data.FROM_ADDRESS)
    page.set_to(data.TO_ADDRESS)

    # 3) Choose tariff
    page.choose_supportive()

    # 4) Phone flow
    page.enter_phone(data.PHONE)
    code = helpers.retrieve_phone_code(driver)
    page.enter_sms_code(code)

    # 5) Card flow
    page.open_payment()
    page.add_card(data.CARD_NUMBER, data.CARD_CVV)

    # 6) Order taxi and verify the search modal
    page.click_order()
    assert page.is_car_search_modal_visible(), "Driver search modal not visible"
