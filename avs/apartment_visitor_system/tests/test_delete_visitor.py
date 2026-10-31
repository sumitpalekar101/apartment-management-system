import os
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"

def test_delete_visitor():
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

            # Find only the test visitor
            page.goto(BASE_URL + "/ManageVisitor")

            row = page.locator("tr").filter(
                has_text="Playwright Test Visitor"
            ).first

            assert row.count() > 0, "Test visitor not found"

            delete_link = row.get_by_role("link", name="Delete")
            delete_url = delete_link.get_attribute("href")

            assert delete_url, "Delete link not found"

            # Delete the test record
            page.goto(BASE_URL + delete_url)
            page.wait_for_url("**/ManageVisitor")

            # Verify deletion
            assert page.get_by_text(
                "Playwright Test Visitor",
                exact=True
            ).count() == 0

            print("DELETE VISITOR: PASSED")

        finally:
            browser.close()


if __name__ == "__main__":
    test_delete_visitor()