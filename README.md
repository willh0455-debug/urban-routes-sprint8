# Urban Routes Sprint 8 — Final Resubmission

This is my **refactored Sprint 8 project** based on the latest reviewer feedback.

### ✅ What Changed
- Simplified the project structure to use **only 4 files**, as requested:
  - `main.py`
  - `pages.py`
  - `helpers.py`
  - `data.py`
- Fully implemented the **Page Object Model (POM)** for better organization and readability.
- Removed unnecessary files, backups, and debug artifacts.
- Rewrote locators and actions in `pages.py` to match the updated container URL and improve test reliability.
- Used helper functions for waits, clicks, and typing to make the tests more stable and clean.

### 🧠 How It Works
Each test in `main.py` follows the same simple flow:
1. Opens the Urban Routes web app.
2. Fills the **From** and **To** address fields.
3. Selects a plan (e.g., *Supportive*).
4. Performs the phone verification flow with `helpers.retrieve_phone_code()`.

### 🧩 Notes
- All tests are written using **pytest + Selenium**.
- The structure is now fully compliant with the POM approach outlined by the reviewer.
- The code was verified locally before submission.

---

**Author:** Will Howard  
**Bootcamp:** TripleTen QA Engineering — Sprint 8  
