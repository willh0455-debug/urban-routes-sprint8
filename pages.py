# pages.py

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, data.DEFAULT_TIMEOUT)

    # ========== LOCATORS (simple & readable) ==========
    # Route fields (IDs are present on the demo)
    ADDRESS_FROM = (By.ID, "from")
    ADDRESS_TO = (By.ID, "to")

    # Call taxi button
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Call a taxi')]")

    # Tariff cards / selected plan
    SUPPORTIVE_PLAN = (By.XPATH, "//div[normalize-space(.)='Supportive']/..")

    # Phone flow
    PHONE_OPEN = (By.XPATH, "//div[contains(@class,'phone') or contains(.,'Phone')]/descendant-or-self::button[1] | //button[contains(.,'Phone')]")
    PHONE_INPUT = (By.XPATH, "//input[@type='tel' or @name='phone' or contains(@placeholder,'phone')]")
    NEXT_BTN = (By.XPATH, "//button[normalize-space(.)='Next' or contains(.,'Next')]")
    SMS_INPUT = (By.XPATH, "//input[@inputmode='numeric' or @type='tel' or contains(@placeholder,'code')]")
    CONFIRM_BTN = (By.XPATH, "//button[normalize-space(.)='Confirm' or contains(.,'Confirm')]")

    # Readback helpers
    SELECTED_TARIFF_TITLE = (
        By.XPATH,
        # typical “selected card” → get its visible title text
        "((//div[contains(@class,'active') or @aria-selected='true'])[1]//div"
        "[contains(@class,'tariff') and (contains(@class,'title') or contains(@class,'name'))]"
        ")[1]"
    )

    # ========== ACTIONS (POM) ==========
    def set_from(self, address: str):
        el = self.wait.until(EC.element_to_be_clickable(self.ADDRESS_FROM))
        el.clear()
        el.send_keys(address)
        el.send_keys(Keys.ENTER)

    def set_to(self, address: str):
        el = self.wait.until(EC.element_to_be_clickable(self.ADDRESS_TO))
        el.clear()
        el.send_keys(address)
        el.send_keys(Keys.ENTER)

    def get_from(self) -> str:
        el = self.wait.until(EC.presence_of_element_located(self.ADDRESS_FROM))
        return el.get_attribute("value") or ""

    def get_to(self) -> str:
        el = self.wait.until(EC.presence_of_element_located(self.ADDRESS_TO))
        return el.get_attribute("value") or ""

    def click_call_a_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_supportive_plan(self):
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN)).click()

    def get_selected_plan(self) -> str:
        # try a direct selected title; if not, fall back to reading “Supportive” card aria/state
        try:
            el = self.wait.until(EC.visibility_of_element_located(self.SELECTED_TARIFF_TITLE))
            text = (el.text or "").strip()
            if text:
                return text
        except Exception:
            pass
        # fallback: if Supportive card is selected it often gets an “active/selected” state
        card = self.wait.until(EC.presence_of_element_located(self.SUPPORTIVE_PLAN))
        classes = (card.get_attribute("class") or "").lower()
        aria = (card.get_attribute("aria-selected") or "").lower()
        if "active" in classes or aria == "true":
            return "Supportive"
        return ""

    # Phone flow
    def click_phone_number(self):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_OPEN)).click()

    def enter_phone_number(self, phone: str):
        el = self.wait.until(EC.element_to_be_clickable(self.PHONE_INPUT))
        el.clear()
        el.send_keys(phone)

    def click_next(self):
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BTN)).click()

    def enter_sms(self, code: str):
        el = self.wait.until(EC.element_to_be_clickable(self.SMS_INPUT))
        el.clear()
        el.send_keys(code)

    def click_confirm(self):
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BTN)).click()

    def get_phone_number(self) -> str:
        # After confirmation, most demos show the number back inside the phone widget.
        # Try to read it from the same input (value) or a nearby text.
        try:
            el = self.wait.until(EC.presence_of_element_located(self.PHONE_INPUT))
            val = (el.get_attribute("value") or "").strip()
            if val:
                return val
        except Exception:
            pass
        # Generic fallback: first tel-looking input
        try:
            el = self.driver.find_element(By.XPATH, "//input[@type='tel']")
            return (el.get_attribute("value") or "").strip()
        except Exception:
            return ""
