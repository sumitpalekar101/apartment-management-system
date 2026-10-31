import os
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000/"


def test_successful_login():
    email = os.environ.get("AVS_TEST_EMAIL")
    password = os.environ.get("AVS_TEST_PASSWORD")

    if not email or not password:
        raise RuntimeError(
            "Set AVS_TEST_EMAIL and AVS_TEST_PASSWORD first."
        )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            page = browser.new_page(
                viewport={"width": 1366, "height": 768}
            )

            page_errors = []

            page.on(
                "pageerror",
                lambda error: page_errors.append(str(error))
            )

            response = page.goto(
                BASE_URL,
                wait_until="networkidle"
            )

            assert response is not None
            assert response.status == 200

            page.locator('input[name="email"]').fill(email)
            page.locator('input[name="password"]').fill(password)

            page.locator("button.login-form__btn").click()

            page.wait_for_load_state("networkidle")

            current_path = urlparse(page.url).path

            print("Login page status:", response.status)
            print("Final URL:", page.url)
            print("Page title:", page.title())

            if current_path == "/":
                print("LOGIN RESULT: FAILED")
                print("Check the account credentials and login error message.")
                print("Page message:", page.locator("body").inner_text()[:1000])
                raise AssertionError("Login did not leave the login page.")

            assert page.locator(
                'input[name="password"]'
            ).count() == 0, "Login form is still visible."

            page.screenshot(
                path="dashboard-login-test.png",
                full_page=True
            )

            assert not page_errors, f"Browser errors: {page_errors}"

            print("LOGIN RESULT: SUCCESS")
            print("Dashboard screenshot: dashboard-login-test.png")
            print("Browser errors:", page_errors)

        finally:
            browser.close()


if __name__ == "__main__":
    test_successful_login()