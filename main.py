from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        """
        Initialize Chrome WebDriver and connect to the Urban Routes server.
        """
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check that the server is running.")

    def test_set_route(self):
        """
        Step 1: Set pickup and drop-off locations.
        """
        page = UrbanRoutesPage(self.driver)
        page.open(data.URBAN_ROUTES_URL)
        page.set_from(data.ADDRESS_FROM)
        page.set_to(data.ADDRESS_TO)

    def test_select_supportive_plan(self):
        """
        Step 2: Choose the supportive ride plan.
        """
        page = UrbanRoutesPage(self.driver)
        # Optional: validate the label exists in TARIFFS
        assert data.PLAN_SUPPORTIVE in data.TARIFFS
        page.select_plan(data.PLAN_SUPPORTIVE)

    def test_filling_in_phone_number(self):
        """
        Step 3: Fill in and confirm phone number.
        """
        page = UrbanRoutesPage(self.driver)
        page.fill_phone_number(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.submit_phone_code(code)

    def test_adding_payment_method(self):
        """
        Step 4: Add a payment card.
        """
        page = UrbanRoutesPage(self.driver)
        page.add_payment_card(
            data.CARD_NUMBER,
            data.CARD_NAME,
            data.CARD_EXP,
            data.CARD_CODE
        )

    def test_message_for_driver(self):
        """
        Step 5: Send a short message for the driver.
        """
        page = UrbanRoutesPage(self.driver)
        page.add_driver_message(data.MESSAGE_FOR_DRIVER)

    def test_ordering_blanket_and_handkerchiefs(self):
        """
        Step 6: Order blanket and handkerchiefs (optional items).
        """
        page = UrbanRoutesPage(self.driver)
        page.order_blanket_and_handkerchiefs()

    def test_order_2_ice_creams(self):
        """
        Step 7: Add ice creams to the order.
        """
        page = UrbanRoutesPage(self.driver)
        page.order_ice_creams(data.ICE_CREAM_COUNT)

    def test_order_supportive_taxi(self):
        """
        Step 8: Complete order and verify the supportive taxi is requested.
        """
        page = UrbanRoutesPage(self.driver)
        page.request_taxi()
        assert page.check_order_successful()

    @classmethod
    def teardown_class(cls):
        """
        Quit the browser when tests are done.
        """
        cls.driver.quit()
