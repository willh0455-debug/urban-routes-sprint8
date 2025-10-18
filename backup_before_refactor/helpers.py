# helpers.py

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def retrieve_phone_code(driver, timeout=10):
    """
    Reads the SMS verification code from the page. If your DOM is different,
    adjust ONE of the locators below—keep the function this simple.
    """
    wait = WebDriverWait(driver, timeout)

    candidates = [
        (By.XPATH, "//*[contains(normalize-space(.), 'SMS') and contains(normalize-space(.), 'code')]"),
        (By.CSS_SELECTOR, "[data-testid='sms-code'], .sms-code, #sms-code"),
    ]

    text_blob = ""
    for by_, selector in candidates:
        try:
            el = wait.until(EC.visibility_of_element_located((by_, selector)))
            text_blob = el.text.strip()
            if text_blob:
                break
        except Exception:
            continue

    m = re.search(r"\b(\d{4,6})\b", text_blob) or re.search(r"\b(\d{4,6})\b", driver.page_source)
    if not m:
        raise RuntimeError("SMS code not found. Update the locator in helpers.retrieve_phone_code().")
    return m.group(1)
