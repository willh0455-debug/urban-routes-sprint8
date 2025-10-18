# helpers.py

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def retrieve_phone_code(driver, timeout=10) -> str:
    """
    Very simple helper that looks for a visible place on the page where the
    demo shows an SMS code, then extracts 4–6 consecutive digits.
    Update just one of the locators below if your DOM is different.
    """
    wait = WebDriverWait(driver, timeout)

    candidates = [
        # any element whose text includes “SMS” and “code”
        (By.XPATH, "//*[contains(translate(., 'SMSCODE', 'smscode'), 'sms') and contains(translate(., 'SMSCODE', 'smscode'), 'code')]"),
        # common test hooks
        (By.CSS_SELECTOR, "[data-testid='sms-code'], .sms-code, #sms-code"),
    ]

    blob = ""
    for by_, sel in candidates:
        try:
            el = wait.until(EC.visibility_of_element_located((by_, sel)))
            blob = (el.text or "").strip()
            if blob:
                break
        except Exception:
            continue

    m = re.search(r"\b(\d{4,6})\b", blob) or re.search(r"\b(\d{4,6})\b", driver.page_source)
    if not m:
        raise RuntimeError("SMS code not found. Update helpers.retrieve_phone_code() locator.")
    return m.group(1)
