# data.py
BASE_URL = "https://cnt-1674a75f-34eb-4ade-a853-f1d0a1b1337b.containerhub.tripleten-services.com"

# Addresses to use in tests
FROM_ADDRESS = "Tekstilor 5"      # adjust to any valid value in your app
TO_ADDRESS = "Telliskivi 60"      # adjust to any valid value in your app

# Phone (the app generates a code we’ll fetch via helpers.retrieve_phone_code)
PHONE_NUMBER = "+1 555 111 2233"

# Payment test data (dummy)
CARD_NUMBER = "4111111111111111"  # Visa test number
CARD_CVV = "123"

# Message for driver
DRIVER_COMMENT = "Please call when you arrive."

# For ice cream selection
ICE_CREAM_COUNT = 2
