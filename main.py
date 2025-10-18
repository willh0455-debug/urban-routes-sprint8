# main.py
from pages import UrbanRoutesPage
import helpers




@pytest.fixture(scope="function")
def driver():
options = Options()
# Add flags if your CI or container needs them
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
if os.getenv("HEADLESS", "1") == "1":
options.add_argument("--headless=new")
drv = webdriver.Chrome(options=options)
drv.set_window_size(1400, 900)
yield drv
drv.quit()




def open_app(drv):
url = os.getenv("URBAN_ROUTES_URL", data.URBAN_ROUTES_URL)
assert url and url.startswith("http"), "Set data.URBAN_ROUTES_URL or URBAN_ROUTES_URL env var"
drv.get(url)




class TestUrbanRoutes:
def test_set_route(self, driver):
open_app(driver)
page = UrbanRoutesPage(driver)


page.set_from(data.ADDRESS_FROM)
page.set_to(data.ADDRESS_TO)


assert data.ADDRESS_FROM == page.get_from(), f"Expected from '{data.ADDRESS_FROM}', got '{page.get_from()}'"
assert data.ADDRESS_TO == page.get_to(), f"Expected to '{data.ADDRESS_TO}', got '{page.get_to()}'"


def test_select_plan(self, driver):
open_app(driver)
page = UrbanRoutesPage(driver)


page.set_from(data.ADDRESS_FROM)
page.set_to(data.ADDRESS_TO)
page.click_call_a_taxi()
page.select_supportive_plan()


assert "Supportive" in page.get_selected_plan(), f"Expected 'Supportive' to be selected, got '{page.get_selected_plan()}'"


def test_fill_phone_number(self, driver):
open_app(driver)
page = UrbanRoutesPage(driver)


page.set_from(data.ADDRESS_FROM)
page.set_to(data.ADDRESS_TO)
page.click_call_a_taxi()


page.click_phone_number()
page.enter_phone_number(data.PHONE_NUMBER)
page.click_next()


sms_code = helpers.retrieve_phone_code(driver, expected_len=data.SMS_CODE_LEN)
page.enter_sms(sms_code)
page.click_confirm()


actual_phone = page.get_phone_number()
assert data.PHONE_NUMBER in actual_phone, f"Expected '{data.PHONE_NUMBER}', got '{actual_phone}'"
