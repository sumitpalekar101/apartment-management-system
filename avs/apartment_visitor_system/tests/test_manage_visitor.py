import os
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"

def test_manage_visitors():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            page = browser.new_page()

            # Login
            page.goto(BASE_URL)
            page.locator('input[name="email"]').fill(os.environ["AVS_TEST_EMAIL"])
            page.locator('input[name="password"]').fill(os.environ["AVS_TEST_PASSWORD"])
            page.locator("form.login-input button").click()
            page.wait_for_url("**/Index")

            # Open Manage Visitors
            page.goto(BASE_URL + "/ManageVisitor")
            page.wait_for_load_state("networkidle")

            # Verify visitor table
            assert page.locator("table").count() > 0
            assert page.get_by_text(
                "Playwright Test Visitor",
                exact=True
            ).count() > 0

            print("MANAGE VISITORS: PASSED")
            print("Test visitor found in visitor table.")

            page.screenshot(
                path="manage-visitors-test.png",
                full_page=True
            )

        finally:
            browser.close()


if __name__ == "__main__":
    test_manage_visitors()
