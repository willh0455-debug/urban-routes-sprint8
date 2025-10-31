✅ Resubmission (Seventh Submission Fix)

1. helpers.py unchanged from Sprint 7 (contains only retrieve_phone_code and is_url_reachable).
2. setup_class now matches lesson requirements (performance logs + reachability check).
3. Each test starts with:
   self.driver.get(data.URBAN_ROUTES_URL)
   page = UrbanRoutesPage(self.driver)
4. Assertions added (page.get_from_value() == data.ADDRESS_FROM).
5. All locators verified (#from, #to, Call Taxi, Supportive card).
6. Lesson-pattern methods in pages.py (direct find_element calls).
7. Booking flow enforced before plan selection (enter both addresses → Call Taxi).
8. Dedicated click_call_taxi() implemented.
9. select_supportive_plan() fixed with scroll + fallback click.
10. get_active_card() confirms Supportive plan.

Local result:
2 passed in <time>s
