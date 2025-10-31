# Retrieves Phone code. Do not change
# File should be completely unchanged

def retrieve_phone_code(driver) -> str:
    """This code retrieves phone confirmation number and returns it as a string.
    Use it when application waits for the confirmation code to pass it into your tests.
    The phone confirmation code can only be obtained after it was requested in application."""
    import json
    import time
    from selenium.common import WebDriverException

    code = None
    for i in range(10):
        try:
            logs = [
                log["message"]
                for log in driver.get_log('performance')
                if log.get("message") and 'api/v1/number?number' in log.get("message")
            ]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd(
                    'Network.getResponseBody',
                    {'requestId': message_data["params"]["requestId"]}
                )
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if code:
            break

    if not code:
        raise Exception("No phone confirmation code found.")
    return code


def is_url_reachable(url: str) -> bool:
    """Checks if the provided URL is reachable."""
    import requests
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
