
import os
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


def test_manage_visitor_pass():
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

            # Open Manage Visitor Pass
            page.goto(BASE_URL + "/ManageVisitorPass")
            page.wait_for_load_state("networkidle")

            # Verify test pass is displayed
            page_text = page.locator("body").inner_text()

            if "Playwright Test Pass" in page_text:
                print("MANAGE VISITOR PASS: PASSED")
                print("Test visitor pass found in the list.")
            else:
                print("MANAGE VISITOR PASS: FAILED")
                print("Test visitor pass not found.")

                raise AssertionError(
                    "Visitor pass not displayed in management list"
                )

        finally:
            browser.close()


if __name__ == "__main__":
    test_manage_visitor_pass()
