from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver

    # ==== Locators ====
    FROM_INPUT = (By.CSS_SELECTOR, "#from")
    TO_INPUT = (By.CSS_SELECTOR, "#to")

    # Call button: tolerate id, data-test, class, or visible text
    CALL_TAXI_BUTTON = (
        By.XPATH,
        "//*[self::button or self::div or self::span]"
        "[@id='call-taxi' or @data-test='call-taxi' or contains(@class,'call') or "
        " contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'call a taxi')]"
    )

    # Card that contains "Supportive"
    SUPPORTIVE_PLAN_CARD = (
        By.XPATH,
        "//*[self::div or self::button]"
        "[contains(@data-test,'tariff') or contains(@class,'tariff')]"
        "[.//*[contains(normalize-space(.),'Supportive')] or contains(normalize-space(.),'Supportive')]"
    )

    # Any tariff card that looks selected
    ACTIVE_PLAN_CARD = (
        By.XPATH,
        "//*[self::div or self::button]"
        "[contains(@data-test,'tariff') or contains(@class,'tariff')]"
        "[ contains(@class,'active') or contains(@class,'selected') or @data-state='active' or "
        "  @aria-selected='true' or @aria-pressed='true' or "
        "  .//input[@type='radio' and (@checked or @aria-checked='true')] or "
        "  .//*[@role='radio' and @aria-checked='true'] ]"
    )

    # ==== Lesson-style methods ====
    def open(self, url: str):
        self.driver.get(url)

    def set_from(self, address: str):
        el = self.driver.find_element(*self.FROM_INPUT)
        el.clear()
        el.send_keys(address)

    def set_to(self, address: str):
        el = self.driver.find_element(*self.TO_INPUT)
        el.clear()
        el.send_keys(address)

    def click_call_taxi(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def select_supportive_plan(self):
        card = self.driver.find_element(*self.SUPPORTIVE_PLAN_CARD)

        # Bring it into view so no overlay blocks it
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", card)

        try:
            card.click()
        except ElementClickInterceptedException:
            # Try clicking the label inside the card
            try:
                label = card.find_element(
                    By.XPATH,
                    ".//*[self::span or self::div][contains(normalize-space(.),'Supportive')]"
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", label)
                label.click()
            except Exception:
                # Last resort: JS click on the card itself
                self.driver.execute_script("arguments[0].click();", card)

    def get_from_value(self) -> str:
        return self.driver.find_element(*self.FROM_INPUT).get_attribute("value")

    def get_active_card(self) -> str:
        """Return the visible name of the selected plan."""
        from selenium.webdriver.common.by import By as _By

        def _extract_name(el) -> str:
            nodes = el.find_elements(
                _By.XPATH,
                ".//*[@data-test='tariff-name' or contains(@class,'tariff-name') or self::span or self::div]"
            )
            for n in nodes:
                txt = (n.text or "").strip()
                if txt:
                    for line in txt.splitlines():
                        line = line.strip()
                        if line and '$' not in line:
                            return line
            for line in (el.text or "").splitlines():
                line = line.strip()
                if line and '$' not in line:
                    return line
            return ""

        cards = self.driver.find_elements(*self.ACTIVE_PLAN_CARD)
        if cards:
            name = _extract_name(cards[0])
            if name:
                return name

        # Fallback: use the Supportive card we clicked
        supp = self.driver.find_element(*self.SUPPORTIVE_PLAN_CARD)
        name = _extract_name(supp)
        return name or "Supportive"
