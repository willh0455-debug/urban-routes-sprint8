# main.py

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import data
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code


@pytest.fixture(scope="function")
def driver():
    """Minimal Chrome setup per test; no conftest.py."""
    chrome_opts = Options()
    chrome_opts.add_argument("--headless=new")   # comment out to watch it run
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--window-size=1280,900")

    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    os.environ.setdefault("SELENIUM_MANAGER_DIAGNOSTIC", "1")

    drv = webdriver.Chrome(options=chrome_opts)
    yield drv
    drv.quit()


def test_set_route(driver):
    driver.get(data.URBAN_ROUTES_URL)
    page = UrbanRoutesPage(driver)

    page.set_from(data.ADDRESS_FROM)
    page.set_to(data.ADDRESS_TO)

    assert data.ADDRESS_FROM == page.get_from(), f"Expected from '{data.ADDRESS_FROM}', got '{page.get_from()}'"
    assert data.ADDRESS_TO == page.get_to(), f"Expected to '{data.ADDRESS_TO}', got '{page.get_to()}'"


def test_select_plan(driver):
    driver.get(data.URBAN_ROUTES_URL)
    page = UrbanRoutesPage(driver)

    page.set_from(data.ADDRESS_FROM)
    page.set_to(data.ADDRESS_TO)
    page.click_call_a_taxi()
    page.select_supportive_plan()   # name matches reviewer’s example

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
    assert data.PHONE_NUMBER == actual_phone, f"Expected '{data.PHONE_NUMBER}', got '{actual_phone}'"
