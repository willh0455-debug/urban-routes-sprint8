# pages.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RoutePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.base_url = base_url

    # ---------- Locators (REPLACE with your project’s exact selectors) ----------
    FROM_INPUT = (By.CSS_SELECTOR, "input[placeholder='From']")       # <-- update
    TO_INPUT = (By.CSS_SELECTOR, "input[placeholder='To']")           # <-- update
    CALL_TAXI_BUTTON = (By.CSS_SELECTOR, "button.call-taxi")          # <-- update
    PHONE_INPUT = (By.CSS_SELECTOR, "input[type='tel']")              # <-- update
    SUBMIT_PHONE = (By.CSS_SELECTOR, "button.submit-phone")           # <-- update
    CODE_INPUT = (By.CSS_SELECTOR, "input[name='code']")              # <-- update

    CARD_ADD_BUTTON = (By.CSS_SELECTOR, "button.add-card")            # <-- update
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "input[name='number']")     # <-- update
    CARD_HOLDER_INPUT = (By.CSS_SELECTOR, "input[name='holder']")     # <-- update
    CARD_MONTH_INPUT = (By.CSS_SELECTOR, "input[name='month']")       # <-- update
    CARD_YEAR_INPUT = (By.CSS_SELECTOR, "input[name='year']")         # <-- update
    CARD_CVC_INPUT = (By.CSS_SELECTOR, "input[name='cvc']")           # <-- update
    SAVE_CARD_BUTTON = (By.CSS_SELECTOR, "button.save-card")          # <-- update

    COMMENT_TEXTAREA = (By.CSS_SELECTOR, "textarea[name='comment']")  # <-- update

    BLANKET_PLUS = (By.CSS_SELECTOR, "button.blanket-plus")           # <-- update
    HANDKERCHIEF_PLUS = (By.CSS_SELECTOR, "button.handkerchief-plus") # <-- update

    ICE_CREAM_PLUS = (By.CSS_SELECTOR, "button.ice-cream-plus")       # <-- update
    ICE_CREAM_COUNTER = (By.CSS_SELECTOR, "span.ice-cream-count")     # <-- update

    CAR_SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='car-search']")  # <-- update
    CAR_MODEL_RESULT = (By.XPATH, "//div[contains(@class,'car-model') and contains(., '{model}')]")  # <-- update

    # ---------- Actions ----------
    def open(self):
        self.driver.get(self.base_url)

    def set_route(self, frm, to):
        self.wait.until(EC.element_to_be_clickable(self.FROM_INPUT)).clear()
        self.driver.find_element(*self.FROM_INPUT).send_keys(frm)
        self.driver.find_element(*self.TO_INPUT).clear()
        self.driver.find_element(*self.TO_INPUT).send_keys(to)
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def submit_phone_and_code(self, phone, code_fetcher):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_INPUT)).clear()
        self.driver.find_element(*self.PHONE_INPUT).send_keys(phone)
        self.driver.find_element(*self.SUBMIT_PHONE).click()
        code = code_fetcher()
        self.wait.until(EC.visibility_of_element_located(self.CODE_INPUT)).send_keys(code)

    def add_card(self, number, holder, month, year, cvc):
        self.wait.until(EC.element_to_be_clickable(self.CARD_ADD_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT)).send_keys(number)
        self.driver.find_element(*self.CARD_HOLDER_INPUT).send_keys(holder)
        self.driver.find_element(*self.CARD_MONTH_INPUT).send_keys(month)
        self.driver.find_element(*self.CARD_YEAR_INPUT).send_keys(year)
        self.driver.find_element(*self.CARD_CVC_INPUT).send_keys(cvc)
        self.driver.find_element(*self.SAVE_CARD_BUTTON).click()

    def add_comment_for_driver(self, text):
        self.wait.until(EC.visibility_of_element_located(self.COMMENT_TEXTAREA)).clear()
        self.driver.find_element(*self.COMMENT_TEXTAREA).send_keys(text)

    def order_blanket_and_handkerchiefs(self, blanket_count=1, handkerchief_count=1):
        for _ in range(blanket_count):
            self.wait.until(EC.element_to_be_clickable(self.BLANKET_PLUS)).click()
        for _ in range(handkerchief_count):
            self.wait.until(EC.element_to_be_clickable(self.HANDKERCHIEF_PLUS)).click()

    def add_ice_creams(self, count=2):
        for _ in range(count):
            self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS)).click()
        return self.driver.find_element(*self.ICE_CREAM_COUNTER).text

    def search_car_model(self, model):
        self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_INPUT)).clear()
        self.driver.find_element(*self.CAR_SEARCH_INPUT).send_keys(model)
        locator = (By.XPATH, self.CAR_MODEL_RESULT[1].format(model=model))
        self.wait.until(EC.visibility_of_element_located(locator))
        return True
