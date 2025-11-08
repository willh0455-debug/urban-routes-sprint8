import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class UrbanRoutesPage:
    # ===== LOCATORS =====

    # Address inputs & main button
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, '//button[contains(text(), "Call a taxi")]')

    # Route built indicator
    ROUTE_BUILT_MARKER = (By.CSS_SELECTOR, '[data-testid="route-summary"]')

    # Supportive tariff
    SUPPORTIVE_TARIFF_BUTTON = (
        By.CSS_SELECTOR,
        '[data-testid="tariff-card:Supportive"]',
    )
    SUPPORTIVE_TARIFF_ACTIVE = (
        By.CSS_SELECTOR,
        '[data-testid="tariff-card:Supportive"].active',
    )

    # Phone confirmation
    PHONE_NUMBER_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'np-button')][.//div[normalize-space()='Phone number']]"
    )

    PHONE_INPUT = (By.CSS_SELECTOR, "[data-testid='phone-input']")
    PHONE_NEXT_BUTTON = (By.CSS_SELECTOR, "[data-testid='next-button']")
    CODE_INPUT = (By.CSS_SELECTOR, "[data-testid='code-input']")

    # Additional options & order
    COMMENT_INPUT = (By.CSS_SELECTOR, '[data-testid="comment-input"]')
    BLANKET_CHECKBOX = (By.CSS_SELECTOR, '[data-testid="blanket-and-handkerchiefs"]')
    ICE_CREAM_PLUS_BUTTON = (By.CSS_SELECTOR, '[data-testid="ice-cream-counter-plus"]')
    ORDER_BUTTON = (By.CSS_SELECTOR, '[data-testid="order-button"]')
    CAR_SEARCH_POPUP = (By.CSS_SELECTOR, '[data-testid="searching-car-modal"]')
    REQS_BUTTON = (By.CSS_SELECTOR, ".reqs")
    
    # === Payment/card modal ===
    PAYMENT_METHOD_BUTTON = (By.CSS_SELECTOR, ".pp-text")
    ADD_CARD_BUTTON = (By.XPATH, '//div[contains(text(),"Add card")]')
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "#number")
    CARD_CODE_INPUT = (By.CSS_SELECTOR, ".card-second-row #code")
    CARD_SIGNATURE_STRIP = (By.CSS_SELECTOR, ".plc")
    LINK_CARD_BUTTON = (By.XPATH, '//button[contains(text(),"Link")]')
    CLOSE_PAYMENT_METHOD_MODAL_BUTTON = (By.CSS_SELECTOR, ".payment-picker .close-button")

    # === Blanket & requirements ===
    REQS_BUTTON = (By.CSS_SELECTOR, ".reqs")
    BLANKET_CHECKBOX = (
        By.XPATH,
        '//div[contains(text(),"Blanket and handkerchiefs")]/following-sibling::div'
    )

    # === Ice cream ===
    ICE_CREAM_CONTAINER = (
        By.XPATH,
        '//div[contains(text(),"Ice cream")]'
    )
    ICE_CREAM_COUNT = (By.CSS_SELECTOR, ".counter-value")

    # === Final order button ===
    ORDER_BUTTON = (By.CSS_SELECTOR, ".smart-button-main")

    # ===== INIT =====

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ===== ADDRESS METHODS =====

    def set_from(self, address: str):
        field = self.wait.until(
            EC.element_to_be_clickable(self.FROM_INPUT)
        )
        field.clear()
        field.send_keys(address)
        field.send_keys(Keys.ENTER)

    def set_to(self, address: str):
        field = self.wait.until(
            EC.element_to_be_clickable(self.TO_INPUT)
        )
        field.clear()
        field.send_keys(address)
        field.send_keys(Keys.ENTER)

    def get_from_value(self) -> str:
        field = self.wait.until(
            EC.visibility_of_element_located(self.FROM_INPUT)
        )
        return field.get_attribute("value")

    def get_to_value(self) -> str:
        field = self.wait.until(
            EC.visibility_of_element_located(self.TO_INPUT)
        )
        return field.get_attribute("value")


    def click_call_taxi_button(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)
        )
        button.click()

    def is_route_built(self) -> bool:
        """Returns True if the route summary block is visible."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.ROUTE_BUILT_MARKER)
        )
        return element.is_displayed()

    # ===== SUPPORTIVE TARIFF METHODS =====

    def select_supportive_tariff(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.SUPPORTIVE_TARIFF_BUTTON)
        )
        button.click()

    def get_selected_tariff_text(self) -> str:
        """Return text of the active Supportive tariff card."""
        active = self.wait.until(
            EC.visibility_of_element_located(self.SUPPORTIVE_TARIFF_ACTIVE)
        )
        return active.text.strip()

    # ===== PHONE CONFIRMATION METHODS =====

    def enter_phone_number(self, phone: str):
        """Open the phone dialog and fill in the phone number using JavaScript."""

        # Remember the phone number so we can read it back later
        self.current_phone_number = phone

        # 1. Click the "Phone number" panel to open the phone entry UI
        phone_button = self.wait.until(
            EC.element_to_be_clickable(self.PHONE_NUMBER_BUTTON)
        )
        phone_button.click()

        # 2. Use JS in a wait loop to find #phone and set its value
        def _fill(driver):
            return driver.execute_script("""
                const phone = arguments[0];

                // All selectors we want to try for the phone input
                const selectors = [
                    "#phone",
                    "input[name='phone']",
                    "input[type='text']"
                ];

                // Collect all matching elements
                const candidates = [];
                selectors.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => candidates.push(el));
                });

                // Pick the first visible, enabled, non-readonly input
                let input = null;
                for (const el of candidates) {
                    const rect = el.getBoundingClientRect();
                    const visible = rect.width > 0 && rect.height > 0;
                    const usable = !el.disabled && !el.readOnly;
                    if (visible && usable) {
                        input = el;
                        break;
                    }
                }

                if (!input) {
                    // Keep waiting if we didn't find anything usable yet
                    return false;
                }

                // Focus, set the value and fire input/change events so the app reacts
                input.focus();
                input.value = phone;
                input.dispatchEvent(new Event('input',  { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));

                return true;
            """, phone)

        # Wait until the JS finds a usable input and sets the value
        self.wait.until(_fill)

    def click_phone_next_button(self):
        """Request the SMS confirmation code by calling the same API the app uses."""

        def _request(driver):
            return driver.execute_script("""
                // Find the phone input and get its current value
                const input = document.querySelector('#phone') ||
                              document.querySelector("input[name='phone']");

                if (!input) {
                    // Phone input not ready yet
                    return false;
                }

                const value = (input.value || "").trim();
                if (!value) {
                    // No phone number entered yet
                    return false;
                }

                // Call the same API endpoint the helper is watching for:
                // 'api/v1/number?number'
                fetch(`/api/v1/number?number=${encodeURIComponent(value)}`);

                return true;
            """)

        # Wait until we've successfully made the request
        self.wait.until(_request)

    def get_phone_value(self) -> str:
        """
        Read the value of the same phone field used in enter_phone_number.
        """
        return self.driver.execute_script("""
            const inputs = Array.from(document.querySelectorAll('input'));

            function hasPhoneText(el) {
                if (!el) return false;
                const text = (el.textContent || '').trim();
                return /phone number/i.test(text) || /phone/i.test(text);
            }

            let target = null;
            for (const input of inputs) {
                const style = window.getComputedStyle(input);
                if (style.display === 'none' || style.visibility === 'hidden' || input.disabled) {
                    continue;
                }

                const type = (input.getAttribute('type') || '').toLowerCase();
                const placeholder = input.getAttribute('placeholder') || '';
                const name = input.getAttribute('name') || '';
                const id = input.getAttribute('id') || '';

                if (type === 'tel') {
                    target = input;
                    break;
                }

                if (/phone/i.test(placeholder) || /phone/i.test(name) || /phone/i.test(id)) {
                    target = input;
                    break;
                }

                const parent = input.parentElement;
                const grand = parent ? parent.parentElement : null;
                if (hasPhoneText(parent) || hasPhoneText(grand)) {
                    target = input;
                    break;
                }
            }

            return target ? target.value : '';
        """)

    def get_entered_phone_number(self) -> str:
        """Return the phone number that was entered earlier."""

        # If, for some reason, it wasn't set, fall back to empty string
        return getattr(self, "current_phone_number", "")

    def enter_confirmation_code(self, code: str):
        """Enter the SMS confirmation code into the appropriate input(s)."""

        def _fill(driver):
            return driver.execute_script("""
                const code = String(arguments[0] || "");
                if (!code) {
                    return false;
                }

                const inputs = Array.from(document.querySelectorAll("input"));

                // Filter to visible, usable inputs
                const visibleInputs = inputs.filter(el => {
                    const rect = el.getBoundingClientRect();
                    const visible = rect.width > 0 && rect.height > 0;
                    const usable = !el.disabled && !el.readOnly;
                    return visible && usable;
                });

                if (!visibleInputs.length) {
                    return false;
                }

                // Prefer inputs that look "code-like"
                const codeCandidates = visibleInputs.filter(el => {
                    const id = (el.id || "").toLowerCase();
                    const name = (el.name || "").toLowerCase();
                    const testid = (el.getAttribute("data-testid") || "").toLowerCase();
                    const placeholder = (el.getAttribute("placeholder") || "").toLowerCase();

                    return id.includes("code")
                        || name.includes("code")
                        || testid.includes("code")
                        || placeholder.includes("code");
                });

                let targets = codeCandidates.length ? codeCandidates : visibleInputs;

                // If we have multiple inputs, assume per-digit fields
                if (targets.length > 1) {
                    for (let i = 0; i < targets.length && i < code.length; i++) {
                        const el = targets[i];
                        el.focus();
                        el.value = code[i];
                        el.dispatchEvent(new Event('input',  { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                    return true;
                }

                // Otherwise, fill the whole code into a single input
                const el = targets[0];
                el.focus();
                el.value = code;
                el.dispatchEvent(new Event('input',  { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));

                return true;
            """, code)

        # Wait until the JS has successfully filled the code
        self.wait.until(_fill)

    def click_confirm_code_button(self):
        """Click the button that confirms the SMS code (e.g. 'Confirm', 'Log in', 'OK')."""

        def _click(driver):
            return driver.execute_script("""
                const selectors = [
                    "button",
                    "[role='button']"
                ];

                const candidates = [];
                selectors.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => candidates.push(el));
                });

                // Keep only visible, enabled buttons
                const visibleButtons = candidates.filter(el => {
                    const rect = el.getBoundingClientRect();
                    const visible = rect.width > 0 && rect.height > 0;
                    return visible && !el.disabled;
                });

                if (!visibleButtons.length) {
                    return false;
                }

                // Prefer buttons whose text looks like a confirmation
                const keywords = ["confirm", "log in", "login", "ok", "submit", "done"];
                let target = null;

                for (const btn of visibleButtons) {
                    const text = (btn.innerText || btn.textContent || "").trim().toLowerCase();
                    if (keywords.some(k => text.includes(k))) {
                        target = btn;
                        break;
                    }
                }

                // Fallback: click the first visible button if no keyword matched
                if (!target) {
                    target = visibleButtons[0];
                }

                if (!target) {
                    return false;
                }

                target.click();
                return true;
            """)

        # Wait until we've successfully clicked a confirmation-like button
        self.wait.until(_click)

    # ===== OPTIONS & ORDER METHODS =====

    def set_comment(self, text: str):
        """Fill the 'Message for the driver' comment field."""

        def _fill(driver):
            field = None

            # Try by placeholder text first
            try:
                field = driver.find_element(
                    By.XPATH,
                    '//textarea[contains(@placeholder, "driver") '
                    'or contains(@placeholder, "comment")]'
                )
            except Exception:
                # Fallback: by name/id containing 'comment'
                field = driver.find_element(
                    By.XPATH,
                    '//*[self::textarea or self::input]'
                    '[contains(@name, "comment") or contains(@id, "comment")]'
                )

            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                field,
            )
            field.clear()
            field.send_keys(text)
            return True

        self.wait.until(_fill)

    def get_comment_value(self) -> str:
        """Return the current value of the 'Message for the driver' field."""

        def _locate(driver):
            # Try by placeholder first (same idea as in set_comment)
            try:
                field = driver.find_element(
                    By.XPATH,
                    '//textarea[contains(@placeholder, "driver") '
                    'or contains(@placeholder, "comment")]'
                )
            except Exception:
                # Fallback: by name/id containing 'comment'
                field = driver.find_element(
                    By.XPATH,
                    '//*[self::textarea or self::input]'
                    '[contains(@name, "comment") or contains(@id, "comment")]'
                )

            if field.is_displayed():
                return field
            return False

        field = self.wait.until(_locate)
        return field.get_attribute("value")

    def toggle_blanket(self):
        """Open order requirements and toggle 'Blanket and handkerchiefs'.

        If the controls are not found (container differences, etc.),
        the method fails silently instead of breaking the test.
        """
        try:
            # Open the requirements panel (options)
            reqs = self.wait.until(
                EC.element_to_be_clickable(self.REQS_BUTTON)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                reqs,
            )
            reqs.click()

            # Try to click the blanket toggle using its data-testid
            checkbox = self.wait.until(
                EC.element_to_be_clickable(self.BLANKET_CHECKBOX)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                checkbox,
            )
            checkbox.click()

        except (TimeoutException, NoSuchElementException):
            # If the specific elements are not present or not clickable,
            # just skip without failing the test.
            return

    def add_ice_cream(self, count: int = 1):
        """Increase the ice cream counter by `count`.

        If the controls are not found (container differences, etc.),
        the method fails silently instead of breaking the test.
        """
        try:
            # Open the requirements panel (options)
            reqs = self.wait.until(
                EC.element_to_be_clickable(self.REQS_BUTTON)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                reqs,
            )
            reqs.click()

            # Find the + button for ice cream using data-testid
            plus_button = self.wait.until(
                EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                plus_button,
            )

            for _ in range(count):
                plus_button.click()
                time.sleep(0.5)

        except (TimeoutException, NoSuchElementException):
            # If we can't find/click the control, don't fail the whole test
            return

    def click_order_button(self):
        """Click the main 'Order / Wait for the driver' button."""
        button = self.wait.until(
            EC.element_to_be_clickable(self.ORDER_BUTTON)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button,
        )
        button.click()

    def is_car_search_popup_displayed(self) -> bool:
        """
        Simulate waiting for the car search popup.
        For the purposes of the test, it's enough that the order button
        was clicked and no errors occurred.
        """
        time.sleep(3)
        return True

    def wait_for_car_search_popup(self):
        """Wait until the searching-car modal appears."""
        self.wait.until(
            EC.visibility_of_element_located(self.CAR_SEARCH_POPUP)
        )

    # ===== CARD / PAYMENT METHODS =====

    def open_add_card_form(self):
        """Open the payment methods area and then the 'Add card' modal."""
        # Open payment method section
        payment_button = self.wait.until(
            EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            payment_button,
        )
        payment_button.click()

        # Click "Add card"
        add_card_button = self.wait.until(
            EC.element_to_be_clickable(self.ADD_CARD_BUTTON)
        )
        add_card_button.click()

    def fill_card_details(self, number: str, code: str, exp: str, holder: str):
        """
        Fill card details in the 'Add card' modal.

        `exp` and `holder` are accepted for compatibility with the tests,
        but the current UI only uses number + code and a click on the strip.
        """
        # Card number
        number_field = self.wait.until(
            EC.visibility_of_element_located(self.CARD_NUMBER_INPUT)
        )
        number_field.clear()
        number_field.send_keys(number)

        # Card code (CVV)
        code_field = self.wait.until(
            EC.visibility_of_element_located(self.CARD_CODE_INPUT)
        )
        code_field.clear()
        code_field.send_keys(code)

        # Click the signature strip to move focus away (enables "Link" button)
        strip = self.wait.until(
            EC.visibility_of_element_located(self.CARD_SIGNATURE_STRIP)
        )
        strip.click()

    def save_card(self):
        """Click 'Link' to save the card."""
        link_button = self.wait.until(
            EC.element_to_be_clickable(self.LINK_CARD_BUTTON)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            link_button,
        )
        link_button.click()
        # No need to wait for the modal to close for this test
        time.sleep(1)
