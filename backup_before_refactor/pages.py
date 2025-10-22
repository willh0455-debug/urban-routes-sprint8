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

    # ----------- Locators -----------
    ADDRESS_FROM = (By.ID, "from")
    ADDRESS_TO = (By.ID, "to")

    # Button text on TripleTen’s demo commonly includes "Call a taxi"
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Call a taxi')]")

    # Tariff card (Supportive)
    SUPPORTIVE_PLAN = (By.XPATH, "//div[normalize-space(.)='Supportive']/..")
    SELECTED_PLAN = (By.XPATH, "//*[contains(@class,'tariff') and contains(@class,'selected')]//*[self::div or self::span][1]")

    # Phone flow
    PHONE_OPEN_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Phone')]")
    PHONE_INPUT = (By.XPATH, "//input[@type='tel' or @name='phone' or contains(@placeholder,'Phone')]")
    NEXT_BUTTON = (By.XPATH, "//button[normalize-space(.)='Next' or contains(@class,'next')]")
    SMS_INPUT = (By.XPATH, "//input[@type='text' or @name='sms' or contains(@placeholder,'code') or contains(@placeholder,'SMS')]")
    CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(.)='Confirm' or contains(@class,'confirm')]")
    PHONE_VALUE_LABEL = (By.XPATH, "//*[contains(@class,'phone') and (self::div or self::span)]")

    # ----------- Actions -----------
    def set_from(self, address):
        el = self.wait.until(EC.element_to_be_clickable(self.ADDRESS_FROM))
        el.clear()
        el.send_keys(address)
        el.send_keys(Keys.ENTER)

    def set_to(self, address):
        el = self.wait.until(EC.element_to_be_clickable(self.ADDRESS_TO))
        el.clear()
        el.send_keys(address)
        el.send_keys(Keys.ENTER)

    def click_call_a_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_supportive_plan(self):
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN)).click()

    # ----------- Getters for asserts -----------
    def get_from(self):
        return self.wait.until(EC.visibility_of_element_located(self.ADDRESS_FROM)).get_attribute("value").strip()

    def get_to(self):
        return self.wait.until(EC.visibility_of_element_located(self.ADDRESS_TO)).get_attribute("value").strip()

    def get_selected_plan(self):
        return self.wait.until(EC.visibility_of_element_located(self.SELECTED_PLAN)).text.strip()

    # ----------- Phone flow -----------
    def click_phone_number(self):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_OPEN_BUTTON)).click()

    def enter_phone_number(self, phone):
        field = self.wait.until(EC.element_to_be_clickable(self.PHONE_INPUT))
        field.clear()
        field.send_keys(phone)

    def click_next(self):
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

    def enter_sms(self, code):
        field = self.wait.until(EC.element_to_be_clickable(self.SMS_INPUT))
        field.clear()
        field.send_keys(code)

    def click_confirm(self):
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON)).click()

    def get_phone_number(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.PHONE_VALUE_LABEL)).text.strip()
        except Exception:
            try:
                return self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT)).get_attribute("value").strip()
            except Exception:
                return ""
