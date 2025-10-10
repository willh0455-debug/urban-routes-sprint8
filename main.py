import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from pages import UrbanRoutesPage
import helpers
import data
import data  # We’ll use the constants from data.py in Project 8
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import helpers
import data
class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.wait = WebDriverWait(cls.driver, 10)

        # URL check moved from Sprint 7
        base_url = getattr(data, "BASE_URL", None)
        assert base_url, "BASE_URL missing in data.py"

        if not helpers.is_url_reachable(base_url):
            pytest.skip(f"BASE_URL not reachable: {base_url}")

        cls.driver.get(base_url)

class TestUrbanRoutes:
    def test_set_route(self):
        # Add in S8
        print("function created for set route")
        pass

    def test_select_plan(self):
        # Add in S8
        print("function created for select plan")
        pass

    def test_fill_phone_number(self):
        # Add in S8
        print("function created for fill phone number")
        pass

    def test_fill_card(self):
        # Add in S8
        print("function created for fill card")
        pass

    def test_comment_for_driver(self):
        # Add in S8
        print("function created for comment for driver")
        pass

    def test_order_blanket_and_handkerchiefs(self):
        # Add in S8
        print("function created for order blanket and handkerchiefs")
        pass

    def test_order_2_ice_creams(self):
        # Add in S8
        print("function created for order 2 ice creams")
        pass

    def test_car_search_model_appears(self):
        # Add in S8
        print("function created for car search model appears")
        pass


# Optional: quick local check so you can see the prints now.
# This block only runs if you do: python main.py
if __name__ == "__main__":
    t = TestUrbanRoutes()
    t.test_set_route()
    t.test_select_plan()
    t.test_fill_phone_number()
    t.test_fill_card()
    t.test_comment_for_driver()
    t.test_order_blanket_and_handkerchiefs()
    t.test_order_2_ice_creams()
    t.test_car_search_model_appears()
    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
