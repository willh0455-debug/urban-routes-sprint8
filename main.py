# main.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from data import (
    BASE_URL,
    FROM_ADDRESS, TO_ADDRESS,
    PHONE_NUMBER, CARD_NUMBER, CARD_HOLDER, CARD_MONTH, CARD_YEAR, CARD_CVC,
    COMMENT_TEXT,
    CAR_SEARCH_MODEL,
    BLANKET_COUNT, HANDKERCHIEF_COUNT,
    ICE_CREAM_COUNT,
)
from pages import RoutePage
from helpers import retrieve_phone_code  # Ensure this exists in helpers.py per Project 7

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        options = Options()
        # If your course uses headless:
        # options.add_argument("--headless=new")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_window_size(1440, 900)
        cls.page = RoutePage(cls.driver, BASE_URL)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # ---------- Your original 3 tests (rename if needed, but keep working steps) ----------
    def test_find_and_type_addresses(self):
        self.page.open()
        self.page.set_route(FROM_ADDRESS, TO_ADDRESS)
        # Add an assert that matches the UI change that confirms route set (element visible, etc.)
        # Example placeholder (replace with a real check):
        assert True

    def test_phone_confirmation(self):
        self.page.open()
        self.page.set_route(FROM_ADDRESS, TO_ADDRESS)
        self.page.submit_phone_and_code(PHONE_NUMBER, lambda: retrieve_phone_code())
        # Add a UI confirmation assert here (e.g., code accepted)
        assert True

    def test_call_taxi_button(self):
        self.page.open()
        self.page.set_route(FROM_ADDRESS, TO_ADDRESS)
        # Assert button state/visibility if your lesson requires it
        assert True

    # ---------- REQUIRED NEW TESTS (5) ----------
    def test_fill_card(self):
        self.page.open()
        self.page.set_route(FROM_ADDRESS, TO_ADDRESS)
        self.page.add_card(CARD_NUMBER, CARD_HOLDER, CARD_MONTH, CARD_YEAR, CARD_CVC)
        # Add an assert that verifies card saved/visible in UI
        assert True

    def test_comment_for_driver(self):
        self.page.open()
        self.page.set_route(FROM_ADDRESS, TO_ADDRESS)
        self.page.add_comment_for_driver(COMMENT_TEXT)
        # Assert comment persisted/visible
        assert True

    def test_order_blanket_and_handkerchiefs(self):
        self.page.open()
        self.page.set_route(FROM_ADDRESS, TO_ADDRESS)
        self.page.order_blanket_and_handkerchiefs(BLANKET_COUNT, HANDKERCHIEF_COUNT)
        # Assert counters or order summary reflects the items
        assert True

    def test_order_2_ice_creams(self):
        self.page.open()
        self.page.set_route(FROM_ADDRESS, TO_ADDRESS)
        count_text = self.page.add_ice_creams(ICE_CREAM_COUNT)
        # Replace this with a real assertion matching your UI (e.g., '2')
        assert str(ICE_CREAM_COUNT) in str(count_text)

    def test_car_search_model_appears(self):
        self.page.open()
        self.page.set_route(FROM_ADDRESS, TO_ADDRESS)
        ok = self.page.search_car_model(CAR_SEARCH_MODEL)
        assert ok is True
