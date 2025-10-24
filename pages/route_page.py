# pages.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.base_url = base_url

    # --------------------------------
    # LOCATORS (identifiers for elements)
    # --------------------------------
    FROM_INPUT = (By.CSS_SELECTOR, "input#from")      # TODO: check exact ID
    TO_INPUT = (By.CSS_SELECTOR, "input#to")          # TODO: check exact ID
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(.,'Call a taxi')]")

    SUPPORTIVE_CARD = (By.XPATH, "//div[contains(.,'Supportive') and contains(@class,'tcard')]")
    ACTIVE_TARIFF_CARD = (By.CSS_SELECTOR, ".tcard.active")

    PHONE_FIELD = (By.CSS_SELECTOR, "input[name='phone']")
    NEXT_BUTTON = (By.XPATH, "//button[contains(.,'Next')]")
    CODE_FIELD = (By.CSS_SELECTOR, "input[name='code']")

    PAYMENT_BUTTON = (By.XPATH, "//button[contains(.,'Payment')]")
    ADD_CARD_BUTTON = (By.XPATH, "//button[contains(.,'Add card')]")
    CARD_NUMBER_FIELD = (By.CSS_SELECTOR, "input[name='number']")
    CARD_CVV_FIELD = (By.CSS_SELECTOR, "input[name='code'].card-input, input[name='cvv']")
    LINK_CARD_BUTTON = (By.XPATH, "//button[contains(.,'Link')]")
    PAYMENT_VALUE = (By.XPATH, "//button[contains(.,'Payment')]//span[contains(@class,'value')]")

    COMMENT_FIELD = (By.CSS_SELECTOR, "textarea[name='comment']")

    BLANKET_SWITCH = (By.CSS_SELECTOR, "input[type='checkbox'][name*='blanket']")
    BLANKET_LABEL = (By.XPATH, "//label[contains(.,'Blanket')]")

    ICECREAM_PLUS = (By.XPATH, "//button[contains(.,'+')]")
    ICECREAM_COUNT = (By.XPATH, "//*[contains(@class,'counter') or contains(@class,'count')]")

    ORDER_BUTTON = (By.XPATH, "//button[contains(.,'Order')]")
    CAR_SEARCH_MODAL = (By.XPATH, "//*[contains(@class,'modal') and contains(.,'search')]")

    # --------------------------------
    # PAGE METHODS (actions)
    # --------------------------------
    def open(self):
        """Open the Urban Routes app"""
        self.driver.get(self.base_url)
        self.wait.until(EC.visibility_of_element_located(self.FROM_INPUT))

    def set_addresses(self, from_addr, to_addr):
        """Type in the pickup and destination addresses"""
        from_field = self.wait.until(EC.element_to_be_clickable(self.FROM_INPUT))
        from_field.clear()
        from_field.send_keys(from_addr)
        from_field.send_keys(Keys.TAB)

        to_field = self.wait.until(EC.element_to_be_clickable(self.TO_INPUT))
        to_field.clear()
        to_field.send_keys(to_addr)
        to_field.send_keys(Keys.TAB)

        # Check that text stayed in the boxes
        assert from_field.get_attribute("value") == from_addr
        assert to_field.get_attribute("value") == to_addr

    def click_call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def choose_supportive_if_needed(self):
        """Only click Supportive plan if it isn't already active"""
        try:
            active = self.driver.find_element(*self.ACTIVE_TARIFF_CARD)
            if "Supportive" in active.text:
                return
        except:
            pass
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_CARD)).click()
        # Verify selection
        active = self.wait.until(EC.presence_of_element_located(self.ACTIVE_TARIFF_CARD))
        assert "Supportive" in active.text

    def enter_phone_and_confirm(self, phone, retrieve_code):
        """Enter phone number and confirm with retrieved code"""
        phone_box = self.wait.until(EC.element_to_be_clickable(self.PHONE_FIELD))
        phone_box.clear()
        phone_box.send_keys(phone)
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

        code = retrieve_code(self.driver)
        code_box = self.wait.until(EC.element_to_be_clickable(self.CODE_FIELD))
        code_box.clear()
        code_box.send_keys(code)

        # Wait until phone number appears confirmed
        self.wait.until(lambda d: phone in d.find_element(*self.PHONE_FIELD).get_attribute("value"))

    def add_card(self, number, cvv):
        """Add a credit card and confirm"""
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.CARD_NUMBER_FIELD)).send_keys(number)

        cvv_box = self.wait.until(EC.element_to_be_clickable(self.CARD_CVV_FIELD))
        cvv_box.send_keys(cvv)
        cvv_box.send_keys(Keys.TAB)  # Lose focus to enable Link button

        self.wait.until(EC.element_to_be_clickable(self.LINK_CARD_BUTTON)).click()
        payment_text = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_VALUE)).text
        assert "Card" in payment_text

    def write_comment(self, text):
        """Type a message for the driver"""
        comment_box = self.wait.until(EC.element_to_be_clickable(self.COMMENT_FIELD))
        comment_box.clear()
        comment_box.send_keys(text)
        assert comment_box.get_attribute("value") == text

    def toggle_blanket(self):
        """Turn on blanket option"""
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_LABEL)).click()
        assert self.driver.find_element(*self.BLANKET_SWITCH).get_property("checked") is True

    def add_icecreams(self, count=2):
        """Add multiple ice creams"""
        plus_button = self.wait.until(EC.element_to_be_clickable(self.ICECREAM_PLUS))
        for _ in range(count):
            plus_button.click()

        count_el = self.wait.until(EC.visibility_of_element_located(self.ICECREAM_COUNT))
        displayed = "".join([c for c in count_el.text if c.isdigit()]) or "0"
        assert int(displayed) == count

    def click_order(self):
        """Click Order button"""
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()

    def is_car_search_modal_visible(self):
        """Check if car search modal pops up"""
        try:
            modal = self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))
            return modal.is_displayed()
        except:
            return False
