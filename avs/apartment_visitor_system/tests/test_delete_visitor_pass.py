
import os
import subprocess
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


def test_delete_visitor_pass():
    # Get only the automated test pass ID
    result = subprocess.run(
        [
            r"..\..\.venv\Scripts\python.exe",
            "manage.py",
            "shell",
            "-c",
            "from avsapp.models import VisitorPass; "
            "p=VisitorPass.objects.filter("
            "visname='Playwright Test Pass').first(); "
            "print(p.id if p else '')"
        ],
        capture_output=True,
        text=True
    )

    pass_id = result.stdout.strip().splitlines()[-1]

    if not pass_id:
        raise AssertionError("Test visitor pass not found")

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

            # Delete only the test pass
            page.goto(BASE_URL + "/DeleteVisitorPass/" + pass_id)
            page.wait_for_url("**/ManageVisitorPass")

            # Verify deletion in database
            check = subprocess.run(
                [
                    r"..\..\.venv\Scripts\python.exe",
                    "manage.py",
                    "shell",
                    "-c",
                    "from avsapp.models import VisitorPass; "
                    "print(VisitorPass.objects.filter("
                    "id=" + pass_id + ").exists())"
                ],
                capture_output=True,
                text=True
            )

            exists = check.stdout.strip().splitlines()[-1]

            assert exists == "False", "Visitor pass was not deleted"

            print("DELETE VISITOR PASS: PASSED")
            print("Test pass ID:", pass_id)
            print("Database confirms deletion.")

        finally:
            browser.close()


if __name__ == "__main__":
    test_delete_visitor_pass()
