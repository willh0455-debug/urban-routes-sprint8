import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


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

    # Card/payment (locators may need small tweaks if UI differs)
    ADD_CARD_BUTTON = (By.CSS_SELECTOR, '[data-testid="add-card"]')
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.ID, "code")
    CARD_EXP_INPUT = (By.ID, "expiry")
    CARD_HOLDER_INPUT = (By.ID, "name")
    SAVE_CARD_BUTTON = (By.CSS_SELECTOR, '[data-testid="save-card"]')

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
        comment_field = self.wait.until(
            EC.visibility_of_element_located(self.COMMENT_INPUT)
        )
        return comment_field.get_attribute("value")

    def toggle_blanket(self):
        """Toggle the 'Blanket and handkerchiefs' option."""

        def _toggle(driver):
            # Click any element whose text mentions Blanket + handkerchief
            el = driver.find_element(
                By.XPATH,
                '//*[contains(text(), "Blanket") '
                'and contains(text(), "handkerchief")]'
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            driver.execute_script("arguments[0].click();", el)
            return True

        self.wait.until(_toggle)

    def add_ice_cream(self, count: int = 1):
        """Increase the ice cream counter by `count`."""

        def _locate_plus(driver):
            # Find the container that mentions 'Ice cream'
            container = driver.find_element(
                By.XPATH,
                '//*[contains(text(), "Ice cream")]'
                '/ancestor-or-self::*[self::div or self::li][1]'
            )
            # Inside that container, find a + button
            plus = container.find_element(
                By.XPATH,
                './/button[contains(@class, "plus") '
                'or contains(@class, "increment") '
                'or normalize-space(text()) = "+"]'
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                plus,
            )
            return plus

        plus_button = self.wait.until(lambda d: _locate_plus(d))

        for _ in range(count):
            plus_button.click()
            time.sleep(0.2)

    def click_order_button(self):
        """Click the main 'Order' button to place the request."""

        def _click(driver):
            button = driver.find_element(
                By.XPATH,
                '//button[contains(@class, "order") '
                'or contains(normalize-space(.), "Order")]'
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                button,
            )
            button.click()
            return True

        self.wait.until(_click)

    def is_car_search_popup_displayed(self) -> bool:
        """Return True when the searching-car modal is visible."""
        popup = self.wait.until(
            EC.visibility_of_element_located(self.CAR_SEARCH_POPUP)
        )
        return popup.is_displayed()

    def wait_for_car_search_popup(self):
        """Wait until the searching-car modal appears."""
        self.wait.until(
            EC.visibility_of_element_located(self.CAR_SEARCH_POPUP)
        )

    # ===== CARD / PAYMENT METHODS =====

    def open_add_card_form(self):
        """Open the 'Add card' form in the payment section."""

        def _click(driver):
            try:
                # Any button/div whose visible text contains 'Add card'
                button = driver.find_element(
                    By.XPATH,
                    '//*[self::button or self::div]'
                    '[contains(normalize-space(.), "Add card")]'
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    button,
                )
                button.click()
                return True
            except Exception:
                return False

        self.wait.until(_click)

    def fill_card_details(self, number: str, code: str, exp: str, holder: str):
        number_field = self.wait.until(
            EC.visibility_of_element_located(self.CARD_NUMBER_INPUT)
        )
        code_field = self.wait.until(
            EC.visibility_of_element_located(self.CARD_CODE_INPUT)
        )
        exp_field = self.wait.until(
            EC.visibility_of_element_located(self.CARD_EXP_INPUT)
        )
        holder_field = self.wait.until(
            EC.visibility_of_element_located(self.CARD_HOLDER_INPUT)
        )

        number_field.clear()
        number_field.send_keys(number)

        code_field.clear()
        code_field.send_keys(code)

        exp_field.clear()
        exp_field.send_keys(exp)

        holder_field.clear()
        holder_field.send_keys(holder)

        # Move focus away from CVV to enable the link/save button if needed
        holder_field.send_keys(Keys.TAB)

    def save_card(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.SAVE_CARD_BUTTON)
        )
        button.click()
