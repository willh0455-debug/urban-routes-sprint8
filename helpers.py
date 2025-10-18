

# helpers.py
# -----------------
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException




def wait_and_type(driver, locator, text, timeout=10, clear=True):
el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
if clear:
try:
el.clear()
except Exception:
pass
el.send_keys(text)
return el




def wait_and_click(driver, locator, timeout=10):
el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
el.click()
return el




def get_value(driver, locator, timeout=10):
el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
try:
return el.get_attribute("value") or el.text
except Exception:
return el.text




def retrieve_phone_code(driver, timeout=15, expected_len=None):
"""
Best-effort retrieval of the SMS/OTP code from the page.
This is intentionally generic since different cohorts use slightly different widgets.


Strategy:
1) Look for an input already split into boxes and just return once boxes are filled.
2) Look for any element that visibly contains a 4–6 digit code (notifications, dev panel, etc.).
3) If there's a specific data-testid or aria-label present, add it here.
"""
code_len = expected_len or globals().get("SMS_CODE_LEN", 4)


# 2) Scan common containers for a 4-6 digit sequence
patterns = [r"\b(\d{%d})\b" % code_len, r"\b(\d{4,6})\b"]
buckets = [
("//div[contains(@class,'notification') or contains(@class,'toast') or contains(@class,'modal')]",


),
raise TimeoutException("Could not automatically retrieve SMS code. If your app shows
