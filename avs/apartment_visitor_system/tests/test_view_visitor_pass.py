
import os
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


def test_view_visitor_pass():
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

            # Get test pass ID from database
            import subprocess

            result = subprocess.run(
                [
                    r"..\..\.venv\Scripts\python.exe",
                    "manage.py",
                    "shell",
                    "-c",
                    "from avsapp.models import VisitorPass; "
                    "print(VisitorPass.objects.filter("
                    "visname='Playwright Test Pass').first().id)"
                ],
                capture_output=True,
                text=True
            )

            pass_id = result.stdout.strip().splitlines()[-1]

            # Open individual visitor pass
            page.goto(BASE_URL + "/ViewVisitorPass/" + pass_id)
            page.wait_for_load_state("networkidle")

            page_text = page.locator("body").inner_text()

            assert "Visitor Pass Details" in page_text
            assert "Playwright Test Pass" in page_text
            assert "Test Address, Pune" in page_text

            print("VIEW VISITOR PASS: PASSED")
            print("Pass ID:", pass_id)
            print("Visitor details displayed correctly.")

        finally:
            browser.close()


if __name__ == "__main__":
    test_view_visitor_pass()
