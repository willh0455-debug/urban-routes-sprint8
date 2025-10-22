# pages.py
from dataclasses import dataclass
from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# —— Adjust selectors here if your app differs ——
# Tips from the sprint:
# - Supportive plan can be verified via "active" class on a tariff card
# - Phone confirm modal uses code field id="code" with class "card-input"
# - Payment "Link" may only enable after CVV field loses focus (send TAB or click outside)
# - Blanket/handkerchiefs: check the slider's 'checked' property
# - Ice cream: click plus button to increment and read the displayed count

@dataclass
class Locators:
    # Address
    FROM_INPUT: Tuple[str, str] = (By.ID, "from")
    TO_INPUT: Tuple[str, str] = (By.ID, "to")
    CALL_TAXI_BTN: Tuple[str, str] = (By.ID, "search")  # "Call a taxi" button

    # Tariffs (Supportive)
    SUPPORTIVE_TARIFF_CARD: Tuple[str, str] = (By.XPATH, "//div[contains(@class,'tcard')][.//div[contains(text(),'Supportive')]]")
    ACTIVE_TARIFF_CARD: Tuple[str, str] = (By.CSS_SELECTOR, "div.tcard.active")

    # Phone
    PHONE_FIELD: Tuple[str, str] = (By.ID, "phone")
    PHONE_REQUEST_CODE_BTN: Tuple[str, str] = (By.XPATH, "//button[.//span[contains(text(),'Confirm') or contains(text(),'Get code') or contains(text(),'Send')]]")
    CODE_INPUT: Tuple[str, str] = (By.ID, "code")  # used in both phone verify and card cvv per sprint hints
    PHONE_SUBMIT_BTN: Tuple[str, str] = (By.XPATH, "//button[contains(.,'Confirm') or contains(.,'Log in') or contains(.,'Verify')]")

    # Payment
    PAYMENT_METHOD_BTN: Tuple[str, str] = (By.XPATH, "//div[contains(@class,'payment-method') or .//span[contains(text(),'Payment')]]")
    ADD_CARD_BTN: Tuple[str, str] = (By.XPATH, "//button[contains(.,'Add card') or contains(.,'Add Card')]")
    CARD_NUMBER_INPUT: Tuple[str, str] = (By.XPATH, "//input[@name='cardNumber' or @id='number' or contains(@class,'card-number')]")
    CARD_CVV_INPUT: Tuple[str, str] = (By.XPATH, "//input[@name='cvv' or @id='code' or contains(@class,'card-input')]")
    LINK_CARD_BTN: Tuple[str, str] = (By.XPATH, "//button[contains(.,'Link') or contains(.,'Bind') or contains(.,'Save')]")
    PAYMENT_SELECTED_TEXT: Tuple[str, str] = (By.XPATH, "//div[contains(@class,'payment-method')]//span[contains(@class,'value') or contains(@class,'text') or self::span]")

    # Comment for driver
    DRIVER_COMMENT_INPUT: Tuple[str, str] = (By.XPATH, "//textarea[@id='comment' or @name='comment' or contains(@placeholder,'comment')]")

    # Blanket + handkerchiefs
    BLANKET_TOGGLE: Tuple[str, str] = (By.XPATH, "//input[@type='checkbox' and (contains(@id,'blanket') or contains(@name,'blanket'))]")  # slider input
    BLANKET_LABEL: Tuple[str, str] = (By.XPATH, "//label[contains(.,'Blanket') or contains(.,'handkerchief')]")

    # Ice cream
    ICECREAM_PLUS_BTN: Tuple[str, str] = (By.XPATH, "//button[contains(@aria-label,'Add ice cream') or contains(., '+')][1] | //div[contains(@class,'ice')]/following::button[1]")
    ICECREAM_COUNT_TEXT: Tuple[str, str] = (By.XPATH, "//div[contains(@class,'ice') or contains(.,'Ice cream')]/following::*[contains(@class,'count') or self::span][1]")

    # Order
    ORDER_BTN: Tuple[str, str] = (By.XPATH, "//button[contains(.,'Order') or contains(.,'Request')]")
    CAR_SEARCH_MODAL: Tuple[str, str] = (By.XPATH, "//*[contains(@class,'modal') and (contains(.,'search') or contains(.,'Car'))]")

    # Generic outside element to lose focus (e.g., header)
    OUTSIDE_CLICK: Tuple[str, str] = (By.XPATH, "//*[@id='root']")


class UrbanRoutesPage:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.loc = Locators()

    # ---- core helpers ----
    def type(self, locator, text):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.clear()
        el.send_keys(text)
        return el

    def click(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()
        return el

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text.strip()

    def get_value(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        return el.get_attribute("value")

    def is_displayed(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()

    # ---- flows ----
    def set_addresses(self, from_addr: str, to_addr: str):
        self.type(self.loc.FROM_INPUT, from_addr)
        self.type(self.loc.TO_INPUT, to_addr)
        # Optional: sometimes there’s a suggestion list; press Enter to accept
        self.wait.until(EC.presence_of_element_located(self.loc.FROM_INPUT)).send_keys(Keys.ENTER)
        self.wait.until(EC.presence_of_element_located(self.loc.TO_INPUT)).send_keys(Keys.ENTER)

    def call_taxi(self):
        self.click(self.loc.CALL_TAXI_BTN)

    def select_supportive_tariff_if_needed(self):
        # Only click Supportive if it’s not already active
        try:
            active = self.wait.until(EC.presence_of_element_located(self.loc.ACTIVE_TARIFF_CARD))
            if "Supportive" not in active.text:
                self.click(self.loc.SUPPORTIVE_TARIFF_CARD)
        except Exception:
            # No active found → select Supportive explicitly
            self.click(self.loc.SUPPORTIVE_TARIFF_CARD)
        # Assert selection is active
        active = self.wait.until(EC.presence_of_element_located(self.loc.ACTIVE_TARIFF_CARD))
        assert "Supportive" in active.text or "support" in active.get_attribute("class").lower()

    def enter_phone_and_confirm(self, phone: str, retrieve_code_callable):
        self.click(self.loc.PHONE_FIELD)
        self.type(self.loc.PHONE_FIELD, phone)
        # Some UIs ask to click a "Confirm/Send code" button:
        try:
            self.click(self.loc.PHONE_REQUEST_CODE_BTN)
        except Exception:
            pass  # if not present, the app might auto-send

        # Use provided helper to retrieve SMS code from performance logs:
        code = retrieve_code_callable(self.driver)
        code_input = self.wait.until(EC.element_to_be_clickable(self.loc.CODE_INPUT))
        code_input.clear()
        code_input.send_keys(code)

        # Submit phone verification if required:
        try:
            self.click(self.loc.PHONE_SUBMIT_BTN)
        except Exception:
            pass

        # Assert phone reflected (the field keeps phone value)
        assert phone.replace(" ", "") in self.wait.until(
            EC.visibility_of_element_located(self.loc.PHONE_FIELD)
        ).get_attribute("value").replace(" ", "")

    def add_card(self, number: str, cvv: str):
        self.click(self.loc.PAYMENT_METHOD_BTN)
        self.click(self.loc.ADD_CARD_BTN)
        self.type(self.loc.CARD_NUMBER_INPUT, number)
        cvv_el = self.type(self.loc.CARD_CVV_INPUT, cvv)

        # IMPORTANT: "Link" might stay disabled until CVV loses focus:
        # Option A: press TAB
        cvv_el.send_keys(Keys.TAB)
        # Option B (fallback): click somewhere outside
        try:
            self.click(self.loc.OUTSIDE_CLICK)
        except Exception:
            pass

        # Now "Link" should be clickable
        self.click(self.loc.LINK_CARD_BTN)

        # Assert payment method text shows "Card"
        txt = self.get_text(self.loc.PAYMENT_SELECTED_TEXT)
        assert "Card" in txt or "card" in txt

    def write_driver_comment(self, message: str):
        self.type(self.loc.DRIVER_COMMENT_INPUT, message)
        # Assert stored
        val = self.get_value(self.loc.DRIVER_COMMENT_INPUT)
        assert message in val

    def toggle_blanket_and_handkerchiefs(self):
        # Click label or input; then assert checked property
        try:
            self.click(self.loc.BLANKET_LABEL)
        except Exception:
            self.click(self.loc.BLANKET_TOGGLE)
        # verify checked
        checkbox = self.wait.until(EC.presence_of_element_located(self.loc.BLANKET_TOGGLE))
        is_checked = checkbox.get_property("checked")
        assert is_checked is True

    def add_ice_creams(self, count: int):
        for _ in range(count):
            self.click(self.loc.ICECREAM_PLUS_BTN)
        # Read the displayed count
        shown = self.get_text(self.loc.ICECREAM_COUNT_TEXT)
        # Normalize to digits
        digits = "".join(ch for ch in shown if ch.isdigit())
        assert str(count) == (digits or "0")

    def order_taxi(self):
        self.click(self.loc.ORDER_BTN)

    def car_search_modal_visible(self) -> bool:
        return self.is_displayed(self.loc.CAR_SEARCH_MODAL)
