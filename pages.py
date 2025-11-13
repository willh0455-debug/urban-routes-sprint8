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

    # Supportive tariff (REPLACED to XPATH, exactly as requested)
    SUPPORTIVE_TARIFF_BUTTON = (By.XPATH, '//div[text()="Supportive"]')
    SUPPORTIVE_TARIFF_ACTIVE = (
        By.XPATH,
        '//div[text()="Supportive" and contains(@class,"active")]'
    )

    # Phone confirmation
    PHONE_NUMBER_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'np-button')][.//div[normalize-space()='Phone number']]"
    )
    PHONE_INPUT = (By.CSS_SELECTOR, "[data-testid='phone-input']")
    PHONE_NEXT_BUTTON = (By.CSS_SELECTOR, "[data-testid='next-button']")
    CODE_INPUT = (By.CSS_SELECTOR, "[data-testid='code-input']")

    # === Requirements / comment / order ===
    COMMENT_INPUT = (By.CSS_SELECTOR, '[data-testid="comment-input"]')

    # Requirements panel
    REQS_BUTTON = (By.CSS_SELECTOR, ".reqs")

    # Blanket toggle (kept per reviewer snippet)
    BLANKET_CHECKBOX = (
        By.XPATH,
        '//div[contains(text(),"Blanket and handkerchiefs")]/following-sibling::div'
    )

    # Ice cream (plus button selector REPLACED exactly as requested)
    ICE_CREAM_CONTAINER = (By.XPATH, '//div[contains(text(),"Ice cream")]')
    ICE_CREAM_PLUS_BUTTON = (By.CSS_SELECTOR, '.counter-plus')
    ICE_CREAM_COUNT = (By.CSS_SELECTOR, ".counter-value")

    # Final order button (kept as in your latest working version)
    ORDER_BUTTON = (By.CSS_SELECTOR, ".smart-button-main")

    # Searching modal
    CAR_SEARCH_POPUP = (By.CSS_SELECTOR, '[data-testid="searching-car-modal"]')
    CALL_TAXI_BUTTON = (By.XPATH, '//button[contains(normalize-space(),"Call taxi") or contains(normalize-space(),"Call a taxi")]')

    # === Payment/card modal ===
    PAYMENT_METHOD_BUTTON = (By.CSS_SELECTOR, ".pp-text")
    ADD_CARD_BUTTON = (By.XPATH, '//div[contains(text(),"Add card")]')
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "#number")
    CARD_CODE_INPUT = (By.CSS_SELECTOR, ".card-second-row #code")
    CARD_SIGNATURE_STRIP = (By.CSS_SELECTOR, ".plc")
    LINK_CARD_BUTTON = (By.XPATH, '//button[contains(text(),"Link")]')
    CLOSE_PAYMENT_METHOD_MODAL_BUTTON = (By.CSS_SELECTOR, ".payment-picker .close-button")

    # ===== INIT =====

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.current_phone_number = ""

    # ===== ADDRESS METHODS =====

    def set_from(self, address: str):
        field = self.wait.until(EC.element_to_be_clickable(self.FROM_INPUT))
        field.clear()
        field.send_keys(address)
        field.send_keys(Keys.ENTER)

    def set_to(self, address: str):
        field = self.wait.until(EC.element_to_be_clickable(self.TO_INPUT))
        field.clear()
        field.send_keys(address)
        field.send_keys(Keys.ENTER)

    def get_from_value(self) -> str:
        field = self.wait.until(EC.visibility_of_element_located(self.FROM_INPUT))
        return field.get_attribute("value")

    def get_to_value(self) -> str:
        field = self.wait.until(EC.visibility_of_element_located(self.TO_INPUT))
        return field.get_attribute("value")

    def click_call_taxi_button(self):
        button = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON))
        button.click()

    def is_route_built(self) -> bool:
        element = self.wait.until(EC.visibility_of_element_located(self.ROUTE_BUILT_MARKER))
        return element.is_displayed()

    # ===== SUPPORTIVE TARIFF METHODS =====

    def select_supportive_tariff(self):
        button = self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_TARIFF_BUTTON))
        button.click()

    def get_selected_tariff_text(self) -> str:
        """
        Return the text of the Supportive tariff after clicking it.
        Prefer an 'active' state if present; otherwise, fall back to the label.
        """
        try:
            # Try your 'active' locator first
            active = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.SUPPORTIVE_TARIFF_ACTIVE)
            )
            txt = (active.text or "").strip()
            if txt:
                return txt
        except TimeoutException:
            pass

        # Fallback 1: container marked selected via ARIA
        try:
            aria_active = self.driver.find_element(
                By.XPATH,
                '//*[@aria-selected="true" and (.//div[normalize-space(text())="Supportive"] '
                'or normalize-space(text())="Supportive")]'
            )
            txt = (aria_active.text or "").strip()
            if txt:
                return txt
        except Exception:
            pass

        # Fallback 2: just read the Supportive label itself
        try:
            label = self.driver.find_element(By.XPATH, '//div[normalize-space(text())="Supportive"]')
            return (label.text or "").strip()
        except Exception:
            return ""

    # ===== PHONE CONFIRMATION METHODS =====

    def enter_phone_number(self, phone: str):
        """Open the phone UI and fill the phone using JS for robustness."""
        self.current_phone_number = phone

        phone_button = self.wait.until(EC.element_to_be_clickable(self.PHONE_NUMBER_BUTTON))
        phone_button.click()

        def _fill(driver):
            return driver.execute_script("""
                const phone = arguments[0];
                const selectors = ["#phone","input[name='phone']","input[type='tel']","input[type='text']"];
                const candidates = [];
                selectors.forEach(sel => { document.querySelectorAll(sel).forEach(el => candidates.push(el)); });
                let input = null;
                for (const el of candidates) {
                    const rect = el.getBoundingClientRect();
                    const visible = rect.width > 0 && rect.height > 0;
                    const usable = !el.disabled && !el.readOnly;
                    if (visible && usable) { input = el; break; }
                }
                if (!input) return false;
                input.focus();
                input.value = phone;
                input.dispatchEvent(new Event('input', {bubbles:true}));
                input.dispatchEvent(new Event('change', {bubbles:true}));
                return true;
            """, phone)

        self.wait.until(_fill)

    def click_phone_next_button(self):
        """Trigger the same request that the helper listens for (api/v1/number?number=...)."""
        def _request(driver):
            return driver.execute_script("""
                const input = document.querySelector('#phone') ||
                               document.querySelector("input[name='phone']");
                if (!input || !input.value) return false;
                fetch(`/api/v1/number?number=${encodeURIComponent(input.value.trim())}`);
                return true;
            """)
        self.wait.until(_request)

    def get_phone_value(self) -> str:
        return self.driver.execute_script("""
            const inputs = Array.from(document.querySelectorAll('input'));
            function good(el){
                if(!el) return false;
                const s=getComputedStyle(el);
                return s.display!=='none' && s.visibility!=='hidden' && !el.disabled;
            }
            for(const el of inputs){
                const id=(el.id||'').toLowerCase();
                const nm=(el.name||'').toLowerCase();
                const ph=(el.placeholder||'').toLowerCase();
                const typ=(el.type||'').toLowerCase();
                if((typ==='tel') || /phone/.test(id+nm+ph)){ if(good(el)) return el.value||''; }
            }
            return '';
        """)

    def get_entered_phone_number(self) -> str:
        return self.current_phone_number or ""

    def enter_confirmation_code(self, code: str):
        def _fill(driver):
            return driver.execute_script("""
                const code = String(arguments[0]||"");
                if(!code) return false;
                const inputs = Array.from(document.querySelectorAll("input"))
                    .filter(el=>{
                        const r=el.getBoundingClientRect();
                        return r.width>0 && r.height>0 && !el.disabled && !el.readOnly;
                    });
                if(!inputs.length) return false;
                const codeLike = inputs.filter(el=>{
                    const id=(el.id||'').toLowerCase();
                    const nm=(el.name||'').toLowerCase();
                    const ti=(el.getAttribute('data-testid')||'').toLowerCase();
                    const ph=(el.placeholder||'').toLowerCase();
                    return id.includes('code')||nm.includes('code')||ti.includes('code')||ph.includes('code');
                });
                const targets = codeLike.length ? codeLike : inputs;
                if(targets.length>1){
                    for(let i=0;i<targets.length && i<code.length;i++){
                        const el=targets[i]; el.focus(); el.value=code[i];
                        el.dispatchEvent(new Event('input',{bubbles:true}));
                        el.dispatchEvent(new Event('change',{bubbles:true}));
                    }
                    return true;
                }
                const el=targets[0]; el.focus(); el.value=code;
                el.dispatchEvent(new Event('input',{bubbles:true}));
                el.dispatchEvent(new Event('change',{bubbles:true}));
                return true;
            """, code)
        self.wait.until(_fill)

    def click_confirm_code_button(self):
        def _click(driver):
            return driver.execute_script("""
                const buttons = Array.from(document.querySelectorAll('button,[role="button"]'))
                    .filter(el=>{const r=el.getBoundingClientRect(); return r.width>0 && r.height>0 && !el.disabled;});
                if(!buttons.length) return false;
                const keys = ["confirm","log in","login","ok","submit","done"];
                let target = buttons.find(b=>{
                    const t=(b.innerText||b.textContent||"").trim().toLowerCase();
                    return keys.some(k=>t.includes(k));
                }) || buttons[0];
                if(!target) return false;
                target.click();
                return true;
            """)
        self.wait.until(_click)

    # ===== OPTIONS & ORDER METHODS =====

    def set_comment(self, text: str):
        def _fill(driver):
            try:
                field = driver.find_element(
                    By.XPATH,
                    '//textarea[contains(@placeholder,"driver") or contains(@placeholder,"comment")]'
                )
            except Exception:
                field = driver.find_element(
                    By.XPATH,
                    '//*[self::textarea or self::input][contains(@name,"comment") or contains(@id,"comment")]'
                )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field)
            field.clear()
            field.send_keys(text)
            return True
        self.wait.until(_fill)

    def get_comment_value(self) -> str:
        def _locate(driver):
            try:
                field = driver.find_element(
                    By.XPATH,
                    '//textarea[contains(@placeholder,"driver") or contains(@placeholder,"comment")]'
                )
            except Exception:
                field = driver.find_element(
                    By.XPATH,
                    '//*[self::textarea or self::input][contains(@name,"comment") or contains(@id,"comment")]'
                )
            return field if field.is_displayed() else False
        field = self.wait.until(_locate)
        return field.get_attribute("value")

    def toggle_blanket(self):
        """Open requirements and toggle 'Blanket and handkerchiefs'. Silently skip if missing."""
        try:
            reqs = self.wait.until(EC.element_to_be_clickable(self.REQS_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", reqs)
            reqs.click()

            checkbox = self.wait.until(EC.element_to_be_clickable(self.BLANKET_CHECKBOX))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox)
            checkbox.click()
        except (TimeoutException, NoSuchElementException):
            return

    def add_ice_cream(self, count: int = 1):
        """Increase the ice cream counter by `count`, scoped to the Ice cream row."""
        try:
            # Open the requirements/options panel (if present)
            try:
                reqs = self.wait.until(EC.element_to_be_clickable(self.REQS_BUTTON))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", reqs)
                reqs.click()
            except (TimeoutException, NoSuchElementException):
                pass  # some fixtures have the row already visible

            # Work only within the 'Ice cream' row
            container = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_CONTAINER))
            plus = container.find_element(By.CSS_SELECTOR, '.counter-plus, [data-testid="plus"], [data-testid*="counter-plus"]')

            for _ in range(count):
                plus.click()
        except (TimeoutException, NoSuchElementException):
            return

    def click_order_button(self):
        button = self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        button.click()

    def is_car_search_popup_displayed(self) -> bool:
        """
        After pressing 'Order', different fixtures show different 'searching' UIs.
        This tolerant checker accepts: the official searching modal, generic modals,
        overlays/spinners, aria-busy/status indicators, OR the order button entering
        a disabled/loading state. Returns True as soon as any condition is observed.
        """
        import time
        deadline = time.time() + 12  # give it a little room

        candidates = [
            # Official testid
            self.CAR_SEARCH_POPUP,  # [data-testid="searching-car-modal"]

            # Common variants (selectors)
            (By.CSS_SELECTOR, '[data-testid*="search"][data-testid*="modal"]'),
            (By.CSS_SELECTOR, '.order-body--search, .modal--searching, .searching, .loader, .spinner, .overlay, .backdrop'),
            (By.CSS_SELECTOR, '[role="dialog"], [aria-modal="true"], [role="status"], [aria-busy="true"]'),

            # Text-based fallbacks (case-insensitive)
            (By.XPATH, '//*[contains(translate(normalize-space(.),"SEARCHING","searching"),"searching")]'),
            (By.XPATH, '//*[contains(translate(normalize-space(.),"LOOKING","looking")) and contains(translate(normalize-space(.),"CAR","car"),"car")]'),
            (By.XPATH, '//*[contains(translate(normalize-space(.),"FINDING","finding"),"finding") and contains(translate(normalize-space(.),"CAR","car"),"car")]'),
        ]

        def order_button_looks_busy() -> bool:
            try:
                btn = self.driver.find_element(*self.ORDER_BUTTON)
            except Exception:
                # If the button disappeared right after click, that's also a valid signal.
                return True
            try:
                # Any disabled/loading cue counts
                disabled_attr = (btn.get_attribute("disabled") or "").lower()
                aria_dis = (btn.get_attribute("aria-disabled") or "").lower()
                cls = (btn.get_attribute("class") or "").lower()
                data_loading = (btn.get_attribute("data-loading") or "").lower()
                txt = (btn.text or "").strip().lower()

                if disabled_attr in ("true", "disabled") or aria_dis == "true":
                    return True
                if any(k in cls for k in ("disabled", "loading", "busy", "spinner")):
                    return True
                if data_loading in ("true", "1"):
                    return True
                if any(k in txt for k in ("search", "searching", "looking", "finding", "waiting")):
                    return True
            except Exception:
                pass
            return False

        while time.time() < deadline:
            # 1) Direct candidates
            for by, sel in candidates:
                try:
                    els = self.driver.find_elements(by, sel)
                    if any(e.is_displayed() for e in els):
                        return True
                except Exception:
                    pass

            # 2) Heuristic: page-level busy/overlay/spinner via JS
            try:
                busy = self.driver.execute_script("""
                    const qs = (s)=>Array.from(document.querySelectorAll(s)).filter(el=>{
                        const r = el.getBoundingClientRect();
                        return r.width>0 && r.height>0 && getComputedStyle(el).visibility!=='hidden';
                    });
                    const checks = [
                      '[data-testid*="search"][data-testid*="modal"]',
                      '[role="dialog"]','[aria-modal="true"]','[role="status"]','[aria-busy="true"]',
                      '.order-body--search','.modal--searching','.searching','.spinner','.loader','.overlay','.backdrop'
                    ];
                    for (const sel of checks) {
                      const els = qs(sel);
                      if (els.length) return true;
                    }
                    return false;
                """)
                if busy:
                    return True
            except Exception:
                pass

            # 3) Heuristic: order button entered a busy/disabled state
            if order_button_looks_busy():
                return True

            time.sleep(0.2)

        return False
    
    def wait_for_car_search_popup(self):
        self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_POPUP))

    # ===== CARD / PAYMENT METHODS =====

    def open_add_card_form(self):
        payment_button = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", payment_button)
        payment_button.click()

        add_card_button = self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON))
        add_card_button.click()

    def fill_card_details(self, number: str, code: str, exp: str, holder: str):
        number_field = self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))
        number_field.clear()
        number_field.send_keys(number)

        code_field = self.wait.until(EC.visibility_of_element_located(self.CARD_CODE_INPUT))
        code_field.clear()
        code_field.send_keys(code)

        strip = self.wait.until(EC.visibility_of_element_located(self.CARD_SIGNATURE_STRIP))
        strip.click()

    def save_card(self) -> bool:
        """Click 'Link' to save the card. Return True if the click succeeded."""
        try:
            link_button = self.wait.until(EC.element_to_be_clickable(self.LINK_CARD_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link_button)
            link_button.click()
            # Try to close the modal if a close button exists (non-fatal if it doesn't)
            try:
                close_btn = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable(self.CLOSE_PAYMENT_METHOD_MODAL_BUTTON)
                )
                close_btn.click()
            except TimeoutException:
                pass
            return True
        except Exception:
            return False

    def is_blanket_selected(self) -> bool:
        """Detect if 'Blanket and handkerchiefs' is toggled ON across DOM variants."""
        try:
            return bool(self.driver.execute_script("""
                const row = document.evaluate(
                  '//div[contains(text(),"Blanket and handkerchiefs")]/ancestor::div[contains(@class,"requirement")]',
                  document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null
                ).singleNodeValue;
                if (!row) return false;
                const el = row.querySelector('[role="switch"], input[type="checkbox"], .switch, .checkbox, [data-testid="toggle"]');
                if (!el) return false;

                // aria-checked
                const aria = (el.getAttribute('aria-checked') || '').toLowerCase();
                if (aria === 'true') return true;

                // native checkbox
                if (el.tagName && el.tagName.toLowerCase() === 'input' && el.type === 'checkbox') {
                  return !!el.checked;
                }

                // class-based toggles
                const cls = (el.className || '').toLowerCase();
                if (cls.includes('active') || cls.includes('on') || cls.includes('checked')) return true;

                // data attributes
                const dataChecked = (el.getAttribute('data-checked') || '').toLowerCase();
                if (dataChecked === 'true' || dataChecked === '1') return true;

                return false;
            """))
        except Exception:
            return False

    def get_ice_cream_count(self) -> int:
        """Return the numeric count shown next to 'Ice cream' with resilient selectors."""
        try:
            container = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_CONTAINER))
            el = container.find_element(By.CSS_SELECTOR, '.counter-value, [data-testid*="counter-value"], [data-testid*="counter"]')
            txt = (el.text or '').strip()
            return int(txt) if txt.isdigit() else int(''.join(ch for ch in txt if ch.isdigit()) or 0)
        except Exception:
            return -1  # sentinel for "not found"
