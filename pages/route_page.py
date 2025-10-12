# pages.py
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

DEFAULT_TIMEOUT = 10


class UrbanRoutesPage:
    """
    Page Object for the Urban Routes app.
    - Locators live at the top (edit TODOs to match your DOM)
    - Methods wrap single user actions or small flows
    """

    # =========================
    # Locators (replace TODOs with real attributes from your app)
    # Prefer data-test=... if available for stability
    # =========================
    # Address fields
    FROM_INPUT = (By.ID, "from")  # TODO: confirm
    TO_INPUT = (By.ID, "to")      # TODO: confirm
    SUGGESTION_TOP = (By.CSS_SELECTOR, ".suggest-item")  # optional

    # Primary CTA
    CALL_TAXI_BTN = (By.CSS_SELECTOR, "[data-test='call-taxi']")  # TODO

    # Tariffs / Plans
    SUPPORTIVE_CARD = (By.CSS_SELECTOR, "[data-plan='supportive']")  # TODO
    ACTIVE_CARD = (By.CSS_SELECTOR, ".tcard.active")                 # used to verify active plan

    # Phone auth
    PHONE_FIELD = (By.CSS_SELECTOR, "input[name='phone']")    # TODO
    SMS_CODE_INPUT = (By.CSS_SELECTOR, "input[name='code']")  # TODO

    # Payment
    PAYMENT_METHOD_BTN = (By.CSS_SELECTOR, "[data-test='payment-method']")  # TODO
    ADD_CARD_BTN = (By.CSS_SELECTOR, "[data-test='add-card']")              # TODO
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "input[name='cardNumber']")       # TODO
    CARD_CVV_INPUT = (By.CSS_SELECTOR, "input[name='cardCode']")            # TODO
    CARD_LINK_BTN = (By.CSS_SELECTOR, "[data-test='link-card']")            # TODO
    PAYMENT_CHIP_TEXT = (By.CSS_SELECTOR, "[data-test='payment-chip']")     # shows Cash/Card

    # Comment
    COMMENT_INPUT = (By.CSS_SELECTOR, "textarea[name='comment']")  # TODO

    # Blanket & Handkerchiefs
    BLANKET_TOGGLE = (By.CSS_SELECTOR, "input[type='checkbox'][name='blanket']")  # TODO

    # Ice cream
    ICE_CREAM_PLUS_BTN = (By.CSS_SELECTOR, "[data-test='ice-cream-increment']")  # TODO
    ICE_CREAM_COUNT = (By.CSS_SELECTOR, "[data-test='ice-cream-count']")         # TODO

    # Order / Car search
    ORDER_BTN = (By.CSS_SELECTOR, "[data-test='order']")        # TODO
    CAR_SEARCH_MODAL = (By.CSS_SELECTOR, "#car-search-modal")   # TODO (id/class that appears)

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- tiny helpers ----------
    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def _type(self, locator, text: str, clear: bool = True, commit_with_enter: bool = False):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            el.clear()
        el.send_keys(text)
        if commit_with_enter:
            el.send_keys(Keys.ENTER)

    def _get_value(self, locator) -> str:
        el = self.wait.until(EC.presence_of_element_located(locator))
        return el.get_attribute("value") or el.text

    def _is_visible(self, locator) -> bool:
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False

    # ---------- address ----------
    def set_from(self, address: str):
        self._type(self.FROM_INPUT, address)
        # optional: pick top suggestion to normalize
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUGGESTION_TOP)).click()
        except Exception:
            pass
        return self

    def set_to(self, address: str):
        self._type(self.TO_INPUT, address)
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUGGESTION_TOP)).click()
        except Exception:
            pass
        return self

    def get_from_value(self) -> str:
        return self._get_value(self.FROM_INPUT)

    def get_to_value(self) -> str:
        return self._get_value(self.TO_INPUT)

    def click_call_taxi(self):
        self._click(self.CALL_TAXI_BTN)
        return self

    # ---------- supportive plan ----------
    def choose_supportive(self):
        self._click(self.SUPPORTIVE_CARD)
        return self

    def is_supportive_selected(self) -> bool:
        # Assert dynamic state via active class
        try:
            _ = self.wait.until(EC.presence_of_element_located(self.ACTIVE_CARD))
            return True
        except Exception:
            return False

    # ---------- phone ----------
    def enter_phone(self, phone: str):
        self._type(self.PHONE_FIELD, phone)
        return self

    def enter_sms_code(self, code: str):
        self._type(self.SMS_CODE_INPUT, code)
        return self

    def get_phone_value(self) -> str:
        return self._get_value(self.PHONE_FIELD)

    # ---------- payment ----------
    def open_payment(self):
        self._click(self.PAYMENT_METHOD_BTN)
        return self

    def add_card(self, card_number: str, cvv: str):
        self._click(self.ADD_CARD_BTN)
        self._type(self.CARD_NUMBER_INPUT, card_number)
        self._type(self.CARD_CVV_INPUT, cvv)
        # shift focus to trigger validation
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.wait.until(EC.element_to_be_clickable(self.CARD_LINK_BTN)).click()
        return self

    def is_payment_card_active(self) -> bool:
        text = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_CHIP_TEXT)).text.strip().lower()
        return text == "card"

    # ---------- comment ----------
    def leave_driver_comment(self, message: str):
        self._type(self.COMMENT_INPUT, message)
        return self

    def get_driver_comment_value(self) -> str:
        return self._get_value(self.COMMENT_INPUT)

    # ---------- blanket & handkerchiefs ----------
    def toggle_blanket_handkerchiefs(self):
        self._click(self.BLANKET_TOGGLE)
        return self

    def is_blanket_checked(self) -> bool:
        el = self.wait.until(EC.presence_of_element_located(self.BLANKET_TOGGLE))
        return bool(el.get_property("checked"))

    # ---------- ice cream (moved loop from test into POM) ----------
    def add_ice_creams(self, count: int = 2):
        for _ in range(count):
            self._click(self.ICE_CREAM_PLUS_BTN)
        return self

    def get_ice_cream_count(self) -> int:
        txt = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_COUNT)).text.strip()
        try:
            return int(txt)
        except ValueError:
            return 0

    # ---------- order ----------
    def click_order(self):
        self._click(self.ORDER_BTN)
        return self

    def is_car_search_modal_visible(self) -> bool:
        return self._is_visible(self.CAR_SEARCH_MODAL)
# wrapper class so tests can still import RoutePage
class RoutePage(UrbanRoutesPage):
    pass
# wrapper class so tests can still import RoutePage
class RoutePage(UrbanRoutesPage):
    pass
