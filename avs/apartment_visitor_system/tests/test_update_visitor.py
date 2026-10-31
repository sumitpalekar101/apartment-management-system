import os
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"

def test_update_visitor():
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

            # Open test visitor update page
            page.goto(BASE_URL + "/ManageVisitor")
            row = page.locator("tr").filter(
                has_text="Playwright Test Visitor"
            ).first

            update_link = row.get_by_role("link", name="Update")
            href = update_link.get_attribute("href")

            assert href, "Update link not found"

            page.goto(BASE_URL + href)

            # Update remark and status
            page.locator("#remark").fill("Playwright automated test")
            page.locator("#status").select_option(label="Out")
            page.locator("button").filter(has_text="Submit").click()

            page.wait_for_url("**/ManageVisitor")

            print("UPDATE VISITOR: PASSED")

        finally:
            browser.close()


if __name__ == "__main__":
    test_update_visitor()
