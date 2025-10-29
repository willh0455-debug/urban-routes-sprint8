# helpers.py
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import Optional
import json
import time

from selenium.common import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver


def is_url_reachable(url: str, timeout: int = 5) -> bool:
    """
    Return True if a quick request to the URL succeeds (HTTP 2xx/3xx).
    Uses a lightweight GET with a short timeout to avoid HEAD restrictions.
    """
    try:
        req = Request(url, method="GET")
        with urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400
    except (HTTPError, URLError, TimeoutError):
        return False


def retrieve_phone_code(driver: WebDriver, attempts: int = 10, sleep_sec: float = 1.0) -> str:
    """
    Retrieve the phone confirmation code from Chrome performance logs.

    The application emits a request like .../api/v1/number?number=...
    We scan recent performance logs, pull the matching response body,
    and extract all digits as the confirmation code.

    Raises:
        Exception if no confirmation code is found after retries.
    """
    code: Optional[str] = None

    for _ in range(attempts):
        try:
            logs = [
                entry["message"]
                for entry in driver.get_log("performance")
                if entry.get("message") and "api/v1/number?number" in entry.get("message", "")
            ]

            for raw in reversed(logs):
                message_data = json.loads(raw)["message"]
                request_id = message_data.get("params", {}).get("requestId")
                if not request_id:
                    continue

                body = driver.execute_cdp_cmd(
                    "Network.getResponseBody",
                    {"requestId": request_id}
                )
                # Extract digits only (e.g., "Your code is 1234" -> "1234")
                digits = "".join(ch for ch in body.get("body", "") if ch.isdigit())
                if digits:
                    code = digits
                    break

            if code:
                return code

        except WebDriverException:
            time.sleep(sleep_sec)
            continue

        time.sleep(sleep_sec)

    raise Exception("No phone confirmation code found. Make sure the app requested a code first.")


def clear_and_type(element, text: str) -> None:
    """
    Convenience helper to reliably clear an input and type text.
    """
    element.clear()
    element.send_keys(text)
