# main.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import data
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code


@pytest.fixture(scope="function")
def driver():
    """Minimal Chrome setup per test; keep it simple per reviewer guidance."""
    opts = Options()
    # You can comment out the next line to watch the browser:
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,900")

    drv = webdriver.Chrome(options=opts)
    yield drv
    drv.quit()


def test_set_route(driver):
    driver.get(data.URBAN_ROUTES_URL)
    page = UrbanRoutesPage(driver)

    page.set_from(data.ADDRESS_FROM)
    page.set_to(data.ADDRESS_TO)

    assert page.get_from() == data.ADDRESS_FROM, f"Expected from '{data.ADDRESS_FROM}', got '{page.get_from()}'"
    assert page.get_to() == data.ADDRESS_TO, f"Expected to '{data.ADDRESS_TO}', got '{page.get_to()}'"


def test_select_plan(driver):
    driver.get(data.URBAN_ROUTES_URL)
    page = UrbanRoutesPage(driver)

    page.set_from(data.ADDRESS_FROM)
    page.set_to(data.ADDRESS_TO)
    page.click_call_a_taxi()
    page.select_supportive_plan()

    assert page.get_selected_plan() == "Supportive"


def test_fill_phone_number(driver):
    driver.get(data.URBAN_ROUTES_URL)
    page = UrbanRoutesPage(driver)

    page.set_from(data.ADDRESS_FROM)
    page.set_to(data.ADDRESS_TO)
    page.click_call_a_taxi()
    page.click_phone_number()
    page.enter_phone_number(data.PHONE_NUMBER)
    page.click_next()
    page.enter_sms(retrieve_phone_code(driver))
    page.click_confirm()

    actual_phone = page.get_phone_number()
    assert actual_phone == data.PHONE_NUMBER, f"Expected '{data.PHONE_NUMBER}', got '{actual_phone}'"

