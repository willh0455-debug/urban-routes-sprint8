# pages/route_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import data

DEFAULT_TIMEOUT = 25  # a bit more generous for headless Chromium


# Candidate locators for From/To inputs (we'll try them in order)
FROM_INPUT_CANDIDATES = [
    (By.ID, "from"),
    (By.NAME, "from"),
    (By.CSS_SELECTOR, "input#from"),
    (By.CSS_SELECTOR, "input[name='from']"),
    (By.CSS_SELECTOR, "input[placeholder*='From']"),
    (By.CSS_SELECTOR, "input[aria-label*='From']"),
    (By.CSS_SELECTOR, "input[type='text']"),
]

TO_INPUT_CANDIDATES = [
    (By.ID, "to"),
    (By.NAME, "to"),
    (By.CSS_SELECTOR, "input#to"),
    (By.CSS_SELECTOR, "input[name='to']"),
    (By.CSS_SELECTOR, "input[placeholder*='To']"),
    (By.CSS_SELECTOR, "input[aria-label*='To']"),
    (By.CSS_SELECTOR, "input[type='text']"),
]


class RoutePage:
    # Keep your original selectors (update later if needed)
    SUGGESTION_TOP = (By.CSS_SELECTOR, ".suggest-item")

    CALL_TAXI_BTN = (By.CSS_SELECTOR, "[data-test='call-taxi']")  # TODO set to real selector

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

    def _find_first_visible(self, locators):
        last_exc = None
        for loc in locators:
            try:
                el = self.wait.until(EC.visibility_of_element_located(loc))
                return el
            except Exception as e:
                last_exc = e
                continue
        if last_exc:
            raise last_exc

    def _maybe_switch_into_app_iframe(self):
        # Many TripleTen sandboxes render the app inside an iframe.
        # Try switching to the first iframe that actually contains inputs.
        self.driver.switch_to.default_content()
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for f in iframes:
            try:
                self.driver.switch_to.frame(f)
                # if we can see any input, assume we're in the app frame
                inputs = self.driver.find_elements(By.CSS_SELECTOR, "input")
                if inputs:
                    return
                self.driver.switch_to.default_content()
            except Exception:
                self.driver.switch_to.default_content()
        # If no iframe contains inputs, we stay on default content.

    # ---------- navigation / readiness ----------
    def open(self):
        url = getattr(data, "BASE_URL", getattr(data, "URBAN_ROUTES_URL", None))
        assert url, "BASE_URL (or URBAN_ROUTES_URL) missing in data.py"
        self.driver.get(url)
        # ensure body exists, then switch into app frame if needed
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self._maybe_switch_into_app_iframe()
        return self

    def wait_route_built(self):
        # If you have a more specific 'route ready' element, replace this
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        try:
            self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BTN))
        except Exception:
            # fall back to presence of any input field
            self._find_first_visible(FROM_INPUT_CANDIDATES)
        return self

    # ---------- addresses ----------
    def set_from(self, address: str):
        self._maybe_switch_into_app_iframe()
        el = self._find_first_visible(FROM_INPUT_CANDIDATES)
        el.clear()
        el.send_keys(address)
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUGGESTION_TOP)).click()
        except Exception:
            pass
        return self

    def set_to(self, address: str):
        self._maybe_switch_into_app_iframe()
        el = self._find_first_visible(TO_INPUT_CANDIDATES)
        el.clear()
        el.send_keys(address)
        try:
            self.wait.until(EC.visibility_of_element_located(self.SUGGESTION_TOP)).click()
        except Exception:
            pass
        return self

    # ---------- tariff (simple stub for Sprint 8) ----------
    def choose_supportive(self):
        # Click a real tariff button here if available
        return self

    # ---------- phone ----------
    def enter_phone(self, phone: str):
        self._maybe_switch_into_app_iframe()
        self._type(self.PHONE_FIELD, phone)
        # If your app requires clicking a 'request code' button, click it here.
        return self

    def enter_sms_code(self, code: str):
        self._maybe_switch_into_app_iframe()
        self._type(self.SMS_CODE_INPUT, code)
        return self

    # ---------- payment ----------
    def open_payment(self):
        self._maybe_switch_into_app_iframe()
        self._click(self.PAYMENT_METHOD_BTN)
        return self

    def add_card(self, card_number: str, cvv: str):
        self._maybe_switch_into_app_iframe()
        self._click(self.ADD_CARD_BTN)
        self._type(self.CARD_NUMBER_INPUT, card_number)
        self._type(self.CARD_CVV_INPUT, cvv)
        # trigger validation then link/save
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        self.wait.until(EC.element_to_be_clickable(self.CARD_LINK_BTN)).click()
        return self

    # ---------- order & assert ----------
    def click_order(self):
        self._maybe_switch_into_app_iframe()
        self._click(self.ORDER_BTN)
        return self

    def is_car_search_modal_visible(self) -> bool:
        self._maybe_switch_into_app_iframe()
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
