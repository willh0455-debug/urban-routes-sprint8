from pages.route_page import RoutePage
import data

def test_can_find_and_type_addresses(driver):
    page = RoutePage(driver).open()
    page.set_from(data.FROM_ADDRESS)
    page.set_to(data.TO_ADDRESS)
