from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    # ===== LOCATORS =====
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    SUBMIT_ROUTE_BUTTON = (By.CSS_SELECTOR, "button.button.round")  # <-- Correct locator
    ROUTE_BUILT_MARKER = (By.CSS_SELECTOR, '[data-testid="route-summary"]')

    SUPPORTIVE_TARIFF_BUTTON = (By.CSS_SELECTOR, '[data-testid="tariff-card:Supportive"]')
    SUPPORTIVE_SELECTED = (By.CSS_SELECTOR, '[data-testid="tariff-card:Supportive"].active')

    PHONE_INPUT = (By.CSS_SELECTOR, '[data-testid="phone-input"]')
    PHONE_NEXT_BUTTON = (By.CSS_SELECTOR, '[data-testid="next-button"]')
    CODE_INPUT = (By.CSS_SELECTOR, '[data-testid="code-input"]')
    CONFIRM_CODE_BUTTON = (By.CSS_SELECTOR, '[data-testid="confirm-button"]')

    PAYMENT_METHOD_BUTTON = (By.CSS_SELECTOR, '[data-testid="open-payment-method"]')
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, '[data-testid="card-number"]')
    CARD_CODE_INPUT = (By.CSS_SELECTOR, '[data-testid="code"]')
    SAVE_PAYMENT_BUTTON = (By.CSS_SELECTOR, '[data-testid="save-payment"]')

    MESSAGE_INPUT = (By.CSS_SELECTOR, '[data-testid="comment"]')
    BLANKET_SWITCH = (By.CSS_SELECTOR, '[data-testid="blanket"]')
    HANDKERCHIEF_SWITCH = (By.CSS_SELECTOR, '[data-testid="handkerchief"]')
    ICE_CREAM_PLUS_BUTTON = (By.CSS_SELECTOR, '[data-testid="plus"]')

    # ===== METHODS =====
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    def set_from(self, address):
        from_field = self.wait.until(EC.visibility_of_element_located(self.FROM_INPUT))
        from_field.clear()
        from_field.send_keys(address)

    def set_to(self, address):
        to_field = self.wait.until(EC.visibility_of_element_located(self.TO_INPUT))
        to_field.clear()
        to_field.send_keys(address)

    def submit_route(self):
        button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_ROUTE_BUTTON))
        button.click()
        # Wait until the route summary appears (confirm route built)
        self.wait.until(EC.visibility_of_element_located(self.ROUTE_BUILT_MARKER))

    def select_supportive_tariff(self):
        button = self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_TARIFF_BUTTON))
        button.click()
        self.wait.until(EC.visibility_of_element_located(self.SUPPORTIVE_SELECTED))

    def fill_phone_number(self, phone):
        self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT)).send_keys(phone)
        self.wait.until(EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON)).click()

    def confirm_code(self, code):
        self.wait.until(EC.visibility_of_element_located(self.CODE_INPUT)).send_keys(code)
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_CODE_BUTTON)).click()

    def add_payment_method(self, number, code):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT)).send_keys(number)
        self.wait.until(EC.visibility_of_element_located(self.CARD_CODE_INPUT)).send_keys(code)
        self.wait.until(EC.element_to_be_clickable(self.SAVE_PAYMENT_BUTTON)).click()

    def add_message_for_driver(self, message):
        self.wait.until(EC.visibility_of_element_located(self.MESSAGE_INPUT)).send_keys(message)

    def order_blanket_and_handkerchiefs(self):
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_SWITCH)).click()
        self.wait.until(EC.element_to_be_clickable(self.HANDKERCHIEF_SWITCH)).click()

    def order_two_ice_creams(self):
        plus = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON))
        plus.click()
        plus.click()
