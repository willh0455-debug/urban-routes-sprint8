

# pages.py
# -----------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import data
import helpers




class UrbanRoutesPage:
def __init__(self, driver):
self.driver = driver
self.wait = WebDriverWait(driver, data.EXPLICIT_WAIT_SECONDS)


# --- Locators ---
ADDRESS_FROM = (By.ID, "from")
ADDRESS_TO = (By.ID, "to")


CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Call a taxi')]")


# Tariff cards
SUPPORTIVE_PLAN = (By.XPATH, "//div[normalize-space(text())='Supportive']/.. | //div[contains(@class,'tcard')][.//div[normalize-space(text())='Supportive']]")
ACTIVE_TARIFF_TITLE = (By.XPATH, "//div[contains(@class,'tcard') and (contains(@class,'active') or contains(@class,'selected'))]//*[self::div or self::span][1]")


# Phone / verification flow (generic selectors that work in many cohorts)
PHONE_OPEN = (By.XPATH, "//button[.//span[contains(normalize-space(.), 'Phone')]] | //button[contains(normalize-space(.), 'Phone')]")
PHONE_INPUT = (By.XPATH, "//input[@type='tel' or @name='phone' or contains(@aria-label,'phone')]")
NEXT_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Next') or contains(normalize-space(.), 'Send')]")
SMS_INPUTS = (By.XPATH, "//input[@inputmode='numeric' or @name='code' or contains(@aria-label,'code')]")
CONFIRM_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Confirm') or contains(normalize-space(.), 'Verify')]")


# --- Basic actions ---
def set_from(self, address: str):
helpers.wait_and_type(self.driver, self.ADDRESS_FROM, address, timeout=data.EXPLICIT_WAIT_SECONDS)


def set_to(self, address: str):
helpers.wait_and_type(self.driver, self.ADDRESS_TO, address, timeout=data.EXPLICIT_WAIT_SECONDS)


def get_from(self) -> str:
return helpers.get_value(self.driver, self.ADDRESS_FROM, timeout=data.EXPLICIT_WAIT_SECONDS)


def get_to(self) -> str:
return helpers.get_value(self.driver, self.ADDRESS_TO, timeout=data.EXPLICIT_WAIT_SECONDS)


def click_call_a_taxi(self):
helpers.wait_and_click(self.driver, self.CALL_TAXI_BUTTON, timeout=data.EXPLICIT_WAIT_SECONDS)


# Tariff actions
def click_supportive(self):
helpers.wait_and_click(self.driver, self.SUPPORTIVE_PLAN, timeout=data.EXPLICIT_WAIT_SECONDS)


self.click_supportive()


def get_selected_plan(self) -> str:
try:
el = self.wait.until(EC.presence_of_element_located(self.ACTIVE_TARIFF_TITLE))
return (el.text or el.get_attribute('textContent') or '').strip()
except Exception:
return ""


# Phone / verification actions
def click_phone_number(self):
try:
helpers.wait_and_click(self.driver, self.PHONE_OPEN, timeout=data.EXPLICIT_WAIT_SECONDS)
except Exception:
# Some variants open phone field automatically; that's OK.
pass


def enter_phone_number(self, phone: str):
helpers.wait_and_type(self.driver, self.PHONE_INPUT, phone, timeout=data.EXPLICIT_WAIT_SECONDS)


def click_next(self):
helpers.wait_and_click(self.driver, self.NEXT_BUTTON, timeout=data.EXPLICIT_WAIT_SECONDS)


def enter_sms(self, code: str):
# If there are split inputs, type digit-by-digit; otherwise type into a single field.
inputs = self.driver.find_elements(*self.SMS_INPUTS)
if inputs and len(inputs) > 1:
for i, ch in enumerate(code):
if i < len(inputs):
inputs[i].send_keys(ch)
else:
# fallback: try any focused element
from selenium.webdriver.common.keys import Keys
self.driver.switch_to.active_element.send_keys(code)


def click_confirm(self):
helpers.wait_and_click(self.driver, self.CONFIRM_BUTTON, timeout=data.EXPLICIT_WAIT_SECONDS)


def get_phone_number(self) -> str:
return helpers.get_value(self.driver, self.PHONE_INPUT, timeout=data.EXPLICIT_WAIT_SECONDS)
