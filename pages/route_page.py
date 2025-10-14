import os
try:
    import data
except Exception:
    data = None

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class RoutePage:
    def __init__(self, driver, wait=None):
        from selenium.webdriver.support.ui import WebDriverWait
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, 10)

    # ---------- URL resolution ----------
    def _resolve_base_url(self) -> str:
        """Priority: env var -> data.py -> error."""
        env_url = os.getenv("URBAN_ROUTES_BASE_URL")
        if env_url:
            return env_url
        if data:
            for name in ["MAIN_PAGE", "BASE_URL", "URL", "APP_URL", "SERVICE_URL"]:
                if hasattr(data, name):
                    val = getattr(data, name)
                    if isinstance(val, str) and val.startswith("http"):
                        return val
        raise RuntimeError("Set URBAN_ROUTES_BASE_URL or define MAIN_PAGE/BASE_URL in data.py")

    # ---------- Navigation ----------
    def open(self):
        url = self._resolve_base_url()
        print(f"[POM] open: {url}")
        self.driver.get(url)
        # ensure DOM is ready
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        # land inside app frame if needed
        self._ensure_app_frame()
        return self

    # ---------- Debug helpers ----------
    def _debug_dump(self, html: str | None = None, label: str = "page"):
        try:
            if html is None:
                html = self.driver.page_source
            path = f"/tmp/{label}.html"
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"[POM] dumped {path}")
        except Exception as e:
            print("[POM] dump failed:", e)
            self._debug_dump_all_frames()

    def _debug_dump_all_frames(self):
        try:
            self.driver.switch_to.default_content()
            frames = self.driver.find_elements(By.CSS_SELECTOR, "iframe, frame")
            for idx, fr in enumerate(frames):
                try:
                    self.driver.switch_to.default_content()
                    self.driver.switch_to.frame(fr)
                    html = self.driver.page_source
                    with open(f"/tmp/frame-{idx}.html", "w", encoding="utf-8") as f:
                        f.write(html)
                    print(f"[POM] dumped /tmp/frame-{idx}.html")
                except Exception as inner:
                    print(f"[POM] frame dump {idx} failed:", inner)
            self.driver.switch_to.default_content()
        except Exception as outer:
            print("[POM] _debug_dump_all_frames failed:", outer)

    # ---------- Frame helpers ----------
    def _ensure_app_frame(self):
        """Switch into the first iframe that contains any <input>."""
        self.driver.switch_to.default_content()
        frames = self.driver.find_elements(By.CSS_SELECTOR, "iframe, frame")
        for fr in frames:
            try:
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(fr)
                if self.driver.find_elements(By.CSS_SELECTOR, "input"):
                    print("[POM] switched into app iframe")
                    return
            except Exception:
                pass
        self.driver.switch_to.default_content()

    # ---------- Element search helpers ----------
    def _visible_text_inputs(self):
        inputs = self.driver.find_elements(
            By.CSS_SELECTOR,
            "input[type='text'], input[type='search'], input[role='combobox'], input[aria-autocomplete]"
        )
        return [el for el in inputs if el.is_displayed() and el.is_enabled()]

    def _any_text_input_exists_in_any_frame(self) -> bool:
        sel = "input[type='text'], input[type='search'], input[role='combobox'], input[aria-autocomplete]"
        try:
            self.driver.switch_to.default_content()
            if self.driver.find_elements(By.CSS_SELECTOR, sel):
                return True
        except Exception:
            pass
        try:
            frames = self.driver.find_elements(By.CSS_SELECTOR, "iframe, frame")
            for fr in frames:
                try:
                    self.driver.switch_to.default_content()
                    self.driver.switch_to.frame(fr)
                    if self.driver.find_elements(By.CSS_SELECTOR, sel):
                        return True
                except Exception:
                    pass
        finally:
            self.driver.switch_to.default_content()
        return False

    def _js_find_visible_inputs(self):
        script = r"""
        const SEL = "input[type='text'], input[type='search'], input[role='combobox'], input[aria-autocomplete]";
        function isVisible(el) {
          const style = window.getComputedStyle(el);
          const rect = el.getBoundingClientRect();
          return !!(el.offsetParent !== null || (rect.width && rect.height)) &&
                 style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
        }
        function walk(root) {
          const out = [];
          try {
            root.querySelectorAll(SEL).forEach(el => { if (isVisible(el)) out.push(el); });
            root.querySelectorAll('*').forEach(node => {
              if (node.shadowRoot) out.push(...walk(node.shadowRoot));
            });
          } catch (e) {}
          return out;
        }
        return walk(document);
        """
        return self.driver.execute_script(script)

    def _find_from_field_anywhere(self):
        candidates = [
            "input#from",
            "input[name='from']",
            "[data-test='from'] input",
            "input[aria-label='From']",
            "input[placeholder*='From' i]",
            "input[placeholder*='Pickup' i]",
            "input[aria-label*='Pickup' i]",
        ]
        # default content
        self.driver.switch_to.default_content()
        for sel in candidates:
            for el in self.driver.find_elements(By.CSS_SELECTOR, sel):
                if el.is_displayed() and el.is_enabled():
                    return el
        # shadow in default
        for el in self._js_find_visible_inputs():
            try:
                text = " ".join([
                    (el.get_attribute("placeholder") or ""),
                    (el.get_attribute("aria-label") or ""),
                    (el.get_attribute("name") or ""),
                    (el.get_attribute("id") or ""),
                ]).lower()
                if any(k in text for k in ["from", "pickup", "pick up"]):
                    return el
            except Exception:
                pass
        # frames
        frames = self.driver.find_elements(By.CSS_SELECTOR, "iframe, frame")
        for fr in frames:
            try:
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(fr)
                for sel in candidates:
                    for el in self.driver.find_elements(By.CSS_SELECTOR, sel):
                        if el.is_displayed() and el.is_enabled():
                            return el
                for el in self._js_find_visible_inputs():
                    try:
                        text = " ".join([
                            (el.get_attribute("placeholder") or ""),
                            (el.get_attribute("aria-label") or ""),
                            (el.get_attribute("name") or ""),
                            (el.get_attribute("id") or ""),
                        ]).lower()
                        if any(k in text for k in ["from", "pickup", "pick up"]):
                            return el
                    except Exception:
                        pass
            except Exception:
                pass
        self.driver.switch_to.default_content()
        return None

    # ---------- Actions ----------
    def set_from(self, value: str):
        print("[POM] set_from start")
        # wait until any input exists in page or frames
        self._ensure_app_frame()
        self.wait.until(lambda d: self._any_text_input_exists_in_any_frame())
        field = self._find_from_field_anywhere()
        if not field:
            self._debug_dump(label="page")
            self._debug_dump_all_frames()
            raise TimeoutException("Could not locate the 'From' field.")
        try:
            field.click()
            field.clear()
        except Exception:
            pass
        field.send_keys(value)
        field.send_keys(Keys.TAB)
        self._from_element = field
        print("[POM] set_from done")

    def set_to(self, value: str):
        print("[POM] set_to start")
        candidates = [
            "input#to",
            "input[name='to']",
            "[data-test='to'] input",
            "input[aria-label='To']",
            "input[placeholder*='To' i]",
            "input[placeholder*='Dropoff' i]",
            "input[placeholder*='Destination' i]",
            "input[aria-label*='Dropoff' i]",
            "input[aria-label*='Destination' i]",
        ]
        field = None
        # try specific selectors in default + frames
        self._ensure_app_frame()
        for sel in candidates:
            field = self._find_in_all_frames(By.CSS_SELECTOR, sel) if hasattr(self, "_find_in_all_frames") else None
            if field:
                break
            # default content quick check (helps if _find_in_all_frames not defined)
            for el in self.driver.find_elements(By.CSS_SELECTOR, sel):
                if el.is_displayed() and el.is_enabled():
                    field = el
                    break
            if field:
                break

        # fallback: a different visible input than 'from'
        if not field:
            self.wait.until(lambda d: self._any_text_input_exists_in_any_frame())
            inputs = self._visible_text_inputs()
            if inputs:
                if hasattr(self, "_from_element") and self._from_element in inputs:
                    for el in inputs:
                        if el != self._from_element:
                            field = el
                            break
                if not field:
                    field = inputs[1] if len(inputs) >= 2 else inputs[0]

        if not field:
            self._debug_dump(label="page")
            self._debug_dump_all_frames()
            raise TimeoutException("Could not locate the 'To' field.")

        try:
            field.click()
            field.clear()
        except Exception:
            pass
        field.send_keys(value)
        field.send_keys(Keys.TAB)
        print("[POM] set_to done")
