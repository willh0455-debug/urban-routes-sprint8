from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    # ===== Locators =====
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    PLAN_SUPPORTIVE_BUTTON = (By.XPATH, "//div[text()='Supportive']")
    PHONE_FIELD = (By.ID, "phone")
    PHONE_CODE_FIELD = (By.ID, "code")
    CARD_BUTTON = (By.CSS_SELECTOR, "button[data-testid='add-card']")
    CARD_NUMBER_FIELD = (By.NAME, "number")
    CARD_NAME_FIELD = (By.NAME, "name")
    CARD_EXP_FIELD = (By.NAME, "expiry")
    CARD_CVV_FIELD = (By.NAME, "code")
    MESSAGE_FIELD = (By.NAME, "comment")
    BLANKET_TOGGLE = (By.CSS_SELECTOR, "input[name='blanket']")
    ICE_CREAM_PLUS = (By.XPATH, "//button[contains(@class,'ice-cream-plus')]")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(),'Order')]")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)

    # ===== Basic actions =====
    def open(self, url):
        self.driver.get(url)

    def set_from(self, address):
        field = self.wait.until(EC.visibility_of_element_located(self.FROM_INPUT))
        field.clear()
        field.send_keys(address)

    def set_to(self, address):
        field = self.wait.until(EC.visibility_of_element_located(self.TO_INPUT))
        field.clear()
        field.send_keys(address)

    def select_plan(self, plan_name):
        button = self.wait.until(EC.element_to_be_clickable(self.PLAN_SUPPORTIVE_BUTTON))
        button.click()

    def fill_phone_number(self, phone):
        field = self.wait.until(EC.visibility_of_element_located(self.PHONE_FIELD))
        field.clear()
        field.send_keys(phone)

    def submit_phone_code(self, code):
        field = self.wait.until(EC.visibility_of_element_located(self.PHONE_CODE_FIELD))
        field.clear()
        field.send_keys(code)

    def add_payment_card(self, number, name, exp, cvv):
        self.wait.until(EC.element_to_be_clickable(self.CARD_BUTTON)).click()
        self.driver.find_element(*self.CARD_NUMBER_FIELD).send_keys(number)
        self.driver.find_element(*self.CARD_NAME_FIELD).send_keys(name)
        self.driver.find_element(*self.CARD_EXP_FIELD).send_keys(exp)
        self.driver.find_element(*self.CARD_CVV_FIELD).send_keys(cvv)

    def add_driver_message(self, message):
        field = self.wait.until(EC.visibility_of_element_located(self.MESSAGE_FIELD))
        field.clear()
        field.send_keys(message)

    def order_blanket_and_handkerchiefs(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.BLANKET_TOGGLE))
        toggle.click()

    def order_ice_creams(self, count):
        for _ in range(count):
            self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS)).click()

    def request_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()

    def check_order_successful(self):
        """
        Return True if the order success message appears.
        """
        return bool(self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE)))
