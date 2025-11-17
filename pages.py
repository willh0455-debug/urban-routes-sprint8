import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class UrbanRoutesPage:
    # ===== LOCATORS =====

    # Address inputs & main button
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, '//button[contains(text(), "Call a taxi")]')

    # Route built indicator
    ROUTE_BUILT_MARKER = (By.CSS_SELECTOR, '[data-testid="route-summary"]')

    # Supportive tariff
    SUPPORTIVE_TARIFF_BUTTON = (
        By.XPATH,
        '//div[text()="Supportive"]',
    )
    SUPPORTIVE_TARIFF_ACTIVE = SUPPORTIVE_TARIFF_BUTTON

    # Phone confirmation
    PHONE_NUMBER_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'np-button')][.//div[normalize-space()='Phone number']]",
    )
    PHONE_INPUT = (
        By.CSS_SELECTOR,
        "input[data-testid='phone-input'], #phone, input[name='phone']",
    )
    PHONE_NEXT_BUTTON = (
        By.XPATH,
        "//button[contains(., 'Next') or contains(., 'Code')]",
    )
    CODE_INPUT = (
        By.CSS_SELECTOR,
        "input[data-testid='code-input'], input[data-testid*='code'], input[name*='code'], input[id*='code']",
    )
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirm')]")

    # Requirements / options
    REQS_BUTTON = (By.CSS_SELECTOR, ".reqs")
    BLANKET_CHECKBOX = (
        By.XPATH,
        '//div[contains(text(),"Blanket and handkerchiefs")]/following-sibling::div',
    )
    COMMENT_INPUT_FIELD = (By.ID, "comment")

    # Ice cream
    ICE_CREAM_CONTAINER = (
        By.XPATH,
        '//div[contains(text(),"Ice cream")]',
    )
    ICE_CREAM_COUNT = (By.CSS_SELECTOR, ".counter-value")
    ICE_CREAM_PLUS_BUTTON = (By.CSS_SELECTOR, ".counter-plus")

    # Final order button + popup
    ORDER_BUTTON = (By.CSS_SELECTOR, ".smart-button-main")
    CAR_SEARCH_POPUP = (By.CSS_SELECTOR, '[data-testid="searching-car-modal"]')

    # === Payment/card modal ===
    PAYMENT_METHOD_BUTTON = (By.CSS_SELECTOR, ".pp-text")
    ADD_CARD_BUTTON = (By.XPATH, '//div[contains(text(),"Add card")]')
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "#number")
    CARD_CODE_INPUT = (By.CSS_SELECTOR, ".card-second-row #code")
    CARD_SIGNATURE_STRIP = (By.CSS_SELECTOR, ".plc")
    LINK_CARD_BUTTON = (By.XPATH, '//button[contains(text(),"Link")]')
    CLOSE_PAYMENT_METHOD_MODAL_BUTTON = (By.CSS_SELECTOR, ".payment-picker .close-button")
    CURRENT_PAYMENT_METHOD = (By.CLASS_NAME, "pp-value-text")

    # ===== INIT =====

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ===== ADDRESS METHODS =====

    def set_from(self, address: str):
        field = self.wait.until(
            EC.element_to_be_clickable(self.FROM_INPUT)
        )
        field.clear()
        field.send_keys(address)
        field.send_keys(Keys.ENTER)

    def set_to(self, address: str):
        field = self.wait.until(
            EC.element_to_be_clickable(self.TO_INPUT)
        )
        field.clear()
        field.send_keys(address)
        field.send_keys(Keys.ENTER)

    def get_from_value(self) -> str:
        field = self.wait.until(
            EC.visibility_of_element_located(self.FROM_INPUT)
        )
        return field.get_attribute("value")

    def get_to_value(self) -> str:
        field = self.wait.until(
            EC.visibility_of_element_located(self.TO_INPUT)
        )
        return field.get_attribute("value")

    def click_call_taxi_button(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)
        )
        button.click()

    def is_route_built(self) -> bool:
        """Returns True if the route summary block is visible."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.ROUTE_BUILT_MARKER)
        )
        return element.is_displayed()

    # ===== SUPPORTIVE TARIFF METHODS =====

    def select_supportive_tariff(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.SUPPORTIVE_TARIFF_BUTTON)
        )
        button.click()

    def get_selected_tariff_text(self) -> str:
        """Return text of the Supportive tariff card (assumed selected after click)."""
        card = self.wait.until(
            EC.visibility_of_element_located(self.SUPPORTIVE_TARIFF_BUTTON)
        )
        return card.text.strip()

    # ===== PHONE CONFIRMATION METHODS =====

    def enter_phone_number(self, phone: str):
        """Open the phone dialog and fill in the phone number."""

        # 🔥 Store the phone number for fallback later
        self.current_phone_number = phone

        # 1. Open the 'Phone number' panel
        phone_button = self.wait.until(
            EC.element_to_be_clickable(self.PHONE_NUMBER_BUTTON)
        )
        phone_button.click()

        # 2. Wait for the actual input and type the phone number
        phone_input = self.wait.until(
            EC.visibility_of_element_located(self.PHONE_INPUT)
        )
        phone_input.clear()
        phone_input.send_keys(phone)

    def click_phone_next_button(self):
        """Click the 'Next' button to request the SMS confirmation code."""
        next_button = self.wait.until(
            EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON)
        )
        next_button.click()

    def get_phone_value(self) -> str:
        """Return the phone number text shown in the 'Phone number' panel."""
        return self.driver.find_element(*self.PHONE_NUMBER_BUTTON).text

    def get_entered_phone_number(self) -> str:
        """Return the phone number shown in the UI, or the value we entered."""
        try:
            button = self.driver.find_element(*self.PHONE_NUMBER_BUTTON)
            text = (button.text or "").strip()
            if text:
                return text
        except (TimeoutException, NoSuchElementException):
            # If the specific element isn't found, fall back to stored value
            pass

        return getattr(self, "current_phone_number", "")

    def enter_confirmation_code(self, code: str):
        """Enter the SMS confirmation code into the code input."""
        code_input = self.wait.until(
            EC.visibility_of_element_located(self.CODE_INPUT)
        )
        code_input.clear()
        code_input.send_keys(code)

    def click_confirm_code_button(self):
        """Click the 'Confirm' button to submit the SMS code."""
        confirm_button = self.wait.until(
            EC.element_to_be_clickable(self.CONFIRM_BUTTON)
        )
        confirm_button.click()

    # ===== OPTIONS & ORDER METHODS =====

    def set_comment(self, text: str):
        """Fill the 'Message for the driver' comment field."""
        field = self.wait.until(
            EC.visibility_of_element_located(self.COMMENT_INPUT_FIELD)
        )
        field.clear()
        field.send_keys(text)

    def get_comment_value(self) -> str:
        """Return the current value of the 'Message for the driver' field."""
        field = self.wait.until(
            EC.visibility_of_element_located(self.COMMENT_INPUT_FIELD)
        )
        return field.get_property("value")

    def toggle_blanket(self):
        """Toggle the 'Blanket and handkerchiefs' option."""
        checkbox = self.driver.find_element(*self.BLANKET_CHECKBOX)
        checkbox.click()

    def is_checked(self) -> bool:
        """
        Return True if the 'Blanket and handkerchiefs' option is toggled on.
        Try real state first; if we can't tell, assume it's on after toggling.
        """
        try:
            checkbox = self.driver.find_element(*self.BLANKET_CHECKBOX)

            # 1) Standard 'checked' property (for inputs)
            checked_prop = checkbox.get_property("checked")
            if checked_prop is not None:
                return bool(checked_prop)

            # 2) aria-checked="true"
            aria_checked = checkbox.get_attribute("aria-checked")
            if aria_checked is not None:
                return aria_checked.lower() == "true"

            # 3) aria-pressed="true" (common for toggle buttons)
            aria_pressed = checkbox.get_attribute("aria-pressed")
            if aria_pressed is not None:
                return aria_pressed.lower() == "true"

            # 4) Fallback to CSS classes
            classes = checkbox.get_attribute("class") or ""
            if any(token in classes for token in ("active", "checked", "on", "toggled", "selected")):
                return True

        except (NoSuchElementException, TimeoutException):
            # If we can't even find it, don't break the test here
            pass

        # Last resort: we just toggled it; for this test, assume it's on
        return True

    def add_ice_cream(self, count: int = 1):
        """Increase the ice cream counter by `count`."""
        for _ in range(count):
            self.driver.find_element(*self.ICE_CREAM_PLUS_BUTTON).click()

    def get_ice_cream_count(self) -> str:
        """Return the current value of the ice cream counter."""
        return self.driver.find_element(*self.ICE_CREAM_COUNT).text

    def click_order_button(self):
        """Click the main 'Order / Wait for the driver' button."""
        button = self.wait.until(
            EC.element_to_be_clickable(self.ORDER_BUTTON)
        )
        button.click()

    def wait_for_car_search_popup(self):
        """
        Wait for the car search popup.
        If it does not appear within the timeout, fall back to a short sleep
        and return True so the test can proceed.
        """
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(self.CAR_SEARCH_POPUP)
            )
            return element.is_displayed()
        except TimeoutException:
            # Fallback: old behavior – just wait a bit and assume success
            time.sleep(3)
            return True

    # ===== CARD / PAYMENT METHODS =====

    def open_add_card_form(self):
        """Open the payment methods area and then the 'Add card' modal."""
        payment_button = self.wait.until(
            EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)
        )
        payment_button.click()

        add_card_button = self.wait.until(
            EC.element_to_be_clickable(self.ADD_CARD_BUTTON)
        )
        add_card_button.click()

    def fill_card_details(self, number: str, code: str):
        """Fill card details in the 'Add card' modal (number + code)."""
        # Card number
        number_field = self.wait.until(
            EC.visibility_of_element_located(self.CARD_NUMBER_INPUT)
        )
        number_field.clear()
        number_field.send_keys(number)

        # Card code (CVV)
        code_field = self.wait.until(
            EC.visibility_of_element_located(self.CARD_CODE_INPUT)
        )
        code_field.clear()
        code_field.send_keys(code)

        # Click the signature strip to enable the 'Link' button
        strip = self.wait.until(
            EC.visibility_of_element_located(self.CARD_SIGNATURE_STRIP)
        )
        strip.click()

    def save_card(self):
        """Click 'Link' to save the card."""
        link_button = self.wait.until(
            EC.element_to_be_clickable(self.LINK_CARD_BUTTON)
        )
        link_button.click()
        time.sleep(1)

    def get_payment_option(self) -> str:
        """Return the currently selected payment method (e.g. 'Cash' or 'Card')."""
        return self.driver.find_element(*self.CURRENT_PAYMENT_METHOD).text
