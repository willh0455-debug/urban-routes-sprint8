import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Uncomment if your reviewer needs headless
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
# tests/test_e2e_urban_routes.py
from pages.route_page import RoutePage
import data
import helpers

def test_urban_routes_e2e(driver):
    page = RoutePage(driver)

    # 1. Open the app
    page.open()

    # 2. Enter route addresses
    page.set_from_address(data.FROM_ADDRESS)
    page.set_to_address(data.TO_ADDRESS)
    page.wait_route_built()

    # 3. Select tariff
    page.choose_tariff("Comfort")

    # 4. Add phone number and confirm
    page.enter_phone(data.PHONE)
    code = helpers.retrieve_phone_code(data.PHONE)
    page.enter_code(code)
    page.confirm_phone()

    # 5. Add card
    page.enter_card_details(data.CARD_NUMBER, data.CARD_EXP, data.CARD_CVV, data.CARD_NAME)
    page.save_card()

    # 6. Request ride
    page.order_taxi()
    page.wait_for_driver()
    page.assert_driver_searching()
