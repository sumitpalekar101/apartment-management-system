
import os
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


def test_create_visitor_pass():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            page = browser.new_page()

            # Login
            page.goto(BASE_URL)
            page.locator('input[name="email"]').fill(
                os.environ["AVS_TEST_EMAIL"]
            )
            page.locator('input[name="password"]').fill(
                os.environ["AVS_TEST_PASSWORD"]
            )
            page.locator("form.login-input button").click()
            page.wait_for_url("**/Index")

            # Open visitor pass form
            page.goto(BASE_URL + "/Visitorpass")

            page.locator("#category").select_option(index=1)
            page.locator("#visname").fill("Playwright Test Pass")
            page.locator("#mobilenumber").fill("9876543210")
            page.locator("#address").fill("Test Address, Pune")
            page.locator("#apartment").fill("A-101")
            page.locator("#floor").fill("First Floor")
            page.locator("#inputdate").fill("2026-10-30")
            page.locator("#todate").fill("2026-10-31")
            page.locator("#passdescription").fill(
                "Automated testing pass"
            )
            response = page.locator("#submit").click()

            page.wait_for_load_state("networkidle")

            print("Current URL:", page.url)
            print("Form method:", page.locator("form").get_attribute("method"))
            print("Form action:", page.locator("form").get_attribute("action"))
            print("Response status:", page.locator("body").inner_text()[:1000])

            print("Final URL:", page.url)
            print(
                "Page messages:",
                page.locator(".alert").all_text_contents()
            )

            print("VISITOR PASS FORM SUBMITTED")

        finally:
            browser.close()


if __name__ == "__main__":
    test_create_visitor_pass()
