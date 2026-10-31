
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


def audit_login_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1366, "height": 768}
        )

        console_errors = []
        failed_requests = []

        page.on("pageerror", lambda error: console_errors.append(str(error)))
        page.on("requestfailed", lambda request: failed_requests.append(
            f"{request.method} {request.url}"
        ))

        response = page.goto(BASE_URL, wait_until="networkidle")

        print("\n===== LOGIN UI AUDIT =====")
        print("HTTP Status:", response.status)
        print("Page Title:", page.title())

        print("\nINPUT FIELDS:")
        for field in page.locator("input").all():
            print({
                "type": field.get_attribute("type"),
                "name": field.get_attribute("name"),
                "placeholder": field.get_attribute("placeholder")
            })

        print("\nBUTTONS:")
        for button in page.locator("button, input[type=submit]").all():
            print(button.inner_text() or button.get_attribute("value"))

        print("\nIMAGES:")
        images = page.locator("img").evaluate_all("""
            imgs => imgs.map(img => ({
                src: img.src,
                loaded: img.complete && img.naturalWidth > 0
            }))
        """)
        for img in images:
            print(img)

        print("\nPAGE ERRORS:", console_errors)
        print("FAILED REQUESTS:", failed_requests)

        page.screenshot(
            path="login-audit.png",
            full_page=True
        )

        print("\nScreenshot saved: login-audit.png")

        assert response.status == 200

        browser.close()


if __name__ == "__main__":
    audit_login_page()
