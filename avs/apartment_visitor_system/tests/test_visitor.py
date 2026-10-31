import os
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"

def test_add_visitor():
    email = os.environ["AVS_TEST_EMAIL"]
    password = os.environ["AVS_TEST_PASSWORD"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            page = browser.new_page()

            # Login
            page.goto(BASE_URL)
            page.locator('input[name="email"]').fill(email)
            page.locator('input[name="password"]').fill(password)
            page.locator("form.login-input button").click()
            page.wait_for_url("**/Index")

            # Open visitor form
            page.goto(BASE_URL + "/Visitor")
            page.wait_for_load_state("networkidle")

            # Fill visitor details
            page.locator("#category").select_option(label="Guest")
            page.locator("#fullname").fill("Playwright Test Visitor")
            page.locator("#email").fill("playwright.test@example.com")
            page.locator("#mobilenumber").fill("9876543210")
            page.locator("#address").fill("Test Address, Pune")
            page.locator("#apartmentno").fill("A-101")
            page.locator("#floororwings").fill("First Floor")
            page.locator("#whomtomeet").fill("Test Resident")
            page.locator("#reasontomeet").fill("Automated Testing")

            page.locator('button[type="submit"]').click()
            page.wait_for_load_state("networkidle")

            body = page.locator("body").inner_text()

            assert "Visitor details have been saved" in body

            print("VISITOR REGISTRATION: PASSED")

        finally:
            browser.close()


if __name__ == "__main__":
    test_add_visitor()