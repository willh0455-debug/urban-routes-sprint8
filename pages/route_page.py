# pages/route_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import data

DEFAULT_TIMEOUT = 10


class RoutePage:
    # ===== Locators (replace with your real selectors if needed) =====
    FROM_INPUT = (By.ID, "from")                       # TODO confirm
    TO_INPUT = (By.ID, "to")                           # TODO confirm
    SUGGESTION_TOP = (By.CSS_SELECTOR, ".suggest-item")

    CALL_TAXI_BTN = (By.CSS_SELECTOR, "[data-test='call-taxi']")  # TODO

    PHONE_FIELD = (By.CSS_SELECTOR, "input[name='phone']")        # TODO
    SMS_CODE_INPUT = (By.CSS_SELECTOR, "input[name='code']")      # TODO

    PAYMENT_METHOD_BTN = (By.CSS_SELECTOR, "[data-test='payment-method']")  # TODO
    ADD_CARD_BTN = (By.CSS_SELECTOR, "[data-test='add-card']")              # TODO
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "input[name='cardNumber']")       # TODO
    CARD_CVV_INPUT = (By.CSS_SELECTOR, "input[name='cardCode']")            # TODO
    CARD_LINK_BTN = (By.CSS_SELECTOR, "[data-test='link-card']")            # TODO

    ORDER_BTN = (By.CSS_SELECTOR, "[data-test='order']")          # TODO
    CAR_SEARCH_MODAL = (By.CSS_SELECTOR, "#car-search-modal")     # TODO

    def __init__(self, driver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- internal helpers ----------
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

    # ---------- navigation / readiness ----------
    def open(self):
        url = getattr(data, "BASE_URL", getattr(data, "URBAN_ROUTES_URL", None))
        assert url, "BASE_URL (or URBAN_ROUTES_URL) missing in data.py"
        self.driver.get(url)
        return self

    def wait_route_built(self):
        # Use a stable element that indicates page is ready (adjust if needed)
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BTN))
        return self

    # ---------- addresses ----------
    def set_from(self, address: str):
        self._type(self.FROM_INPUT, address)
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

    # ---------- tariff (simple stub for Sprint 8) ----------
    def choose_supportive(self):
        # If you have real tariff buttons, click the right one here.
        # For now, no-op to keep the test flow moving.
        return self

    # ---------- phone ----------
    def enter_phone(self, phone: str):
        self._type(self.PHONE_FIELD, phone)
        # Your app should request the SMS code after entering the phone;
        # if it requires clicking a "request code" button, click it here.
        return self

    def enter_sms_code(self, code: str):
        self._type(self.SMS_CODE_INPUT, code)
        return self

    # ---------- payment ----------
    def open_payment(self):
        self._click(self.PAYMENT_METHOD_BTN)
        return self

    def add_card(self, card_number: str, cvv: str):
        self._click(self.ADD_CARD_BTN)
        self._type(self.CARD_NUMBER_INPUT, card_number)
        self._type(self.CARD_CVV_INPUT, cvv)
        # trigger validation then link/save
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.wait.until(EC.element_to_be_clickable(self.CARD_LINK_BTN)).click()
        return self

    # ---------- order & assert ----------
    def click_order(self):
        self._click(self.ORDER_BTN)
        return self

    def is_car_search_modal_visible(self) -> bool:
        return self._is_visible(self.CAR_SEARCH_MODAL)

def open(self):
    url = getattr(data, "BASE_URL", getattr(data, "URBAN_ROUTES_URL", None))
    assert url, "BASE_URL (or URBAN_ROUTES_URL) missing in data.py"
    self.driver.get(url)
    self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    return self

def wait_route_built(self):
    # safe readiness check (update to your real selector if you have a better one)
    self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BTN))
    return self
