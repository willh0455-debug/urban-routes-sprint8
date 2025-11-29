# Urban Routes – Sprint 8
### End-to-End Web UI Testing Project (TripleTen QA Engineering Program)

This project is part of TripleTen’s QA Engineering program, Sprint 8.  
It demonstrates end-to-end UI test automation of the Urban Routes web application using Python, Selenium WebDriver, Pytest, and the Page Object Model (POM).

This repository contains the cleaned and finalized version of the Sprint 8 project, following all reviewer feedback and industry best practices.

---

## Project Overview

Urban Routes is an on-demand taxi service web application.

In Sprint 8, the focus was to:

- Test the "Order Supportive Taxi" flow
- Validate the "About Customer" form
- Verify name and phone number validation
- Interact with UI elements including fields, buttons, modals, and dropdowns
- Use explicit waits instead of time.sleep
- Apply the Page Object Model for clean test architecture

This project reflects real-world QA responsibilities including test design, automation, refactoring, and debugging.

---

## Technologies Used

- Python 3.11
- Selenium WebDriver
- Pytest
- Page Object Model (POM)
- Explicit Waits (WebDriverWait + Expected Conditions)
- Virtual Environment (.venv)

---

## Project Structure

urban-routes-sprint8/
│
├── conftest.py               # WebDriver setup + reusable fixtures
├── data.py                   # Test data and constants
├── helpers.py                # Shared helper functions
├── pages.py                  # Page Object Model classes
├── main.py                   # Automated test suite for Sprint 8
├── .gitignore                # Ignored system/cache/env files
└── README.md                 # Project documentation

All backup/debug files and older versions were removed to maintain a clean, professional repository.

---

## Test Coverage

### Positive Scenarios
- Successful supportive taxi order
- Valid customer data submission
- Proper behavior of UI elements

### Negative Scenarios
- Invalid phone numbers
- Invalid names
- Empty field validation
- Incorrect data formats

### Functional Behavior
- Page load checks
- Field input usability
- Button state changes
- Modal window validation
- Ride option selections

---

## Skills Demonstrated

### Page Object Model (POM)
- Clean separation of locators and actions
- Increased reusability and maintainability
- No assertions inside page classes

### Explicit Waits
- Replaced all time.sleep calls with WebDriverWait
- Improved test stability and reliability

### Clean Test Design
- Readable, structured test cases
- Reusable functions and helpers
- Centralized test data
- Fixture-driven WebDriver setup

### Git Version Control
- Separate feature and fix branches
- Clean final `main` branch
- Proper branch cleanup (only main retained)

---

## How to Run Tests

1. Clone the repository:
