# pages.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    # ===== LOCATORS (only here, nowhere else) =====
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    SUBMIT_ROUTE_BUTTON = (By.CSS_SELECTOR, '[data-testid="submit-route-button"]')
    ROUTE_BUILT_MARKER = (By.CSS_SELECTOR, '[data-testid="route-summary"]')  # adjust to real one if different

    SUPPORTIVE_TARIFF_BUTTON = (By.CSS_SELECTOR, '[data-testid="tariff-card:Supportive"]')
    SUPPORTIVE_SELECTED = (By.CSS_SELECTOR, '[data-testid="tariff-card:Supportive"].active')

    PHONE_INPUT = (By.CSS_SELECTOR, '[data-testid="phone-input"]')
    PHONE_NEXT_BUTTON = (By.CSS_SELECTOR, '[data-testid="next-button"]')
    CODE_INPUT = (By.CSS_SELECTOR, '[data-testid="code-input"]')
    CONFIRM_CODE_BUTTON = (By.CSS_SELECTOR, '[data-testid="confirm-button"]')

    PAYMENT_METHOD_BUTTON = (By.CSS_SELECTOR, '[data-testid="open-payment-method"]')
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, '[data-testid="card-number"]')
    CARD_CODE_INPUT = (By.CSS_SELECTOR, '[data-testid="card-code"]')
    CARD_EXPIRATION_INPUT = (By.CSS_SELECTOR, '[data-testid="card-expiration"]')
    CARDHOLDER_NAME_INPUT = (By.CSS_SELECTOR, '[data-testid="card-name"]')
    SAVE_CARD_BUTTON = (By.CSS_SELECTOR, '[data-testid="save-card"]')
    CARD_ADDED_CHECK = (By.CSS_SELECTOR, '[data-testid="card-saved"]')

    MESSAGE_BUTTON = (By.CSS_SELECTOR, '[data-testid="open-message"]')
    MESSAGE_INPUT = (By.CSS_SELECTOR, '[data-testid="message-input"]')
    MESSAGE_SAVE_BUTTON = (By.CSS_SELECTOR, '[data-testid="save-message"]')
    MESSAGE_SAVED_LABEL = (By.CSS_SELECTOR, '[data-testid="message-saved"]')

    REQUIREMENTS_BUTTON = (By.CSS_SELECTOR, '[data-testid="open-requirements"]')
    BLANKET_CHECKBOX = (By.CSS_SELECTOR, '[data-testid="checkbox:blanket-and-handkerchiefs"]')
    ICE_CREAM_PLUS_BUTTON = (By.CSS_SELECTOR, '[data-testid="counter-plus:icecream"]')
    ICE_CREAM_COUNT_LABEL = (By.CSS_SELECTOR, '[data-testid="counter-value:icecream"]')
    REQUIREMENTS_SAVE_BUTTON = (By.CSS_SELECTOR, '[data-testid="save-requirements"]')

    ORDER_BUTTON = (By.CSS_SELECTOR, '[data-testid="order-button"]')
    ORDER_CONFIRMED_LABEL = (By.CSS_SELECTOR, '[data-testid="order-confirmed"]')
    CALL_TAXI_BUTTON = (By.CSS_SELECTOR, "button.button.round")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ===== BASIC NAVIGATION =====
    def open(self, url: str):
        self.driver.get(url)

    # ===== ROUTE =====
    def set_from(self, addr: str):
        field = self.wait.until(EC.visibility_of_element_located(self.FROM_INPUT))
        field.clear()
        field.send_keys(addr)

    def set_to(self, addr: str):
        field = self.wait.until(EC.visibility_of_element_located(self.TO_INPUT))
        field.clear()
        field.send_keys(addr)

    def submit_route(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_ROUTE_BUTTON))
        btn.click()

    def wait_route_built(self):
        # wait for some element that appears after route is calculated
        self.wait.until(EC.visibility_of_element_located(self.ROUTE_BUILT_MARKER))

    # ===== TARIFF =====
    def select_supportive_tariff(self):
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_TARIFF_BUTTON)).click()

    def check_supportive_selected(self):
        self.wait.until(EC.visibility_of_element_located(self.SUPPORTIVE_SELECTED))

    # ===== PHONE =====
    def fill_phone_number(self, phone: str):
        field = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))
        field.clear()
        field.send_keys(phone)

    def click_phone_next(self):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON)).click()

    def fill_phone_code(self, code: str):
        field = self.wait.until(EC.visibility_of_element_located(self.CODE_INPUT))
        field.clear()
        field.send_keys(code)

    def confirm_phone_code(self):
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_CODE_BUTTON)).click()

    # ===== PAYMENT =====
    def open_payment_form(self):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)).click()

    def add_card(self, number: str, code: str, expiration: str, name: str):
        num = self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))
        num.clear()
        num.send_keys(number)

        cvc = self.wait.until(EC.visibility_of_element_located(self.CARD_CODE_INPUT))
        cvc.clear()
        cvc.send_keys(code)

        exp = self.wait.until(EC.visibility_of_element_located(self.CARD_EXPIRATION_INPUT))
        exp.clear()
        exp.send_keys(expiration)

        holder = self.wait.until(EC.visibility_of_element_located(self.CARDHOLDER_NAME_INPUT))
        holder.clear()
        holder.send_keys(name)

    def save_card(self):
        self.wait.until(EC.element_to_be_clickable(self.SAVE_CARD_BUTTON)).click()

    def check_card_saved(self):
        self.wait.until(EC.visibility_of_element_located(self.CARD_ADDED_CHECK))

    # ===== MESSAGE =====
    def open_message_form(self):
        self.wait.until(EC.element_to_be_clickable(self.MESSAGE_BUTTON)).click()

    def set_message_for_driver(self, message: str):
        field = self.wait.until(EC.visibility_of_element_located(self.MESSAGE_INPUT))
        field.clear()
        field.send_keys(message)

    def save_message(self):
        self.wait.until(EC.element_to_be_clickable(self.MESSAGE_SAVE_BUTTON)).click()

    def check_message_saved(self, expected: str):
        label = self.wait.until(EC.visibility_of_element_located(self.MESSAGE_SAVED_LABEL))
        # you can assert text if you want, but wait alone is usually enough
        assert expected in label.text

    # ===== REQUIREMENTS / EXTRAS =====
    def open_requirements(self):
        self.wait.until(EC.element_to_be_clickable(self.REQUIREMENTS_BUTTON)).click()

    def toggle_blanket_and_handkerchiefs(self, checked: bool):
        checkbox = self.wait.until(EC.element_to_be_clickable(self.BLANKET_CHECKBOX))
        # if you want to ensure state:
        if checkbox.is_selected() != checked:
            checkbox.click()

    def set_ice_cream_count(self, count: int):
        # assumes starting from zero, click + until desired
        while True:
            current = int(
                self.wait.until(
                    EC.visibility_of_element_located(self.ICE_CREAM_COUNT_LABEL)
                ).text
            )
            if current >= count:
                break
            self.wait.until(
                EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON)
            ).click()

    def save_requirements(self):
        self.wait.until(EC.element_to_be_clickable(self.REQUIREMENTS_SAVE_BUTTON)).click()

    def check_blanket_and_handkerchiefs_selected(self):
        checkbox = self.wait.until(EC.visibility_of_element_located(self.BLANKET_CHECKBOX))
        assert checkbox.is_selected()

    def check_ice_cream_count(self, expected: int):
        current = int(
            self.wait.until(
                EC.visibility_of_element_located(self.ICE_CREAM_COUNT_LABEL)
            ).text
        )
        assert current == expected

    # ===== ORDER =====
    def order_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()

    def check_taxi_ordered(self):
        self.wait.until(EC.visibility_of_element_located(self.ORDER_CONFIRMED_LABEL))

    def get_from_value(self):
        """Return the current value of the 'From' field."""
        field = self.wait.until(EC.visibility_of_element_located(self.FROM_INPUT))
        return field.get_attribute("value")

    def get_to_value(self):
        """Return the current value of the 'To' field."""
        field = self.wait.until(EC.visibility_of_element_located(self.TO_INPUT))
        return field.get_attribute("value")

    def click_call_taxi(self):
        """Click the main 'Call taxi' button on the route page."""
        button = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON))
        button.click()

    def choose_supportive(self):
        """Select the 'Supportive' tariff card."""
        card = self.wait.until(
            EC.element_to_be_clickable(self.SUPPORTIVE_TARIFF_BUTTON)
        )
        card.click()

