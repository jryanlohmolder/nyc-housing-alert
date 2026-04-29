from playwright.sync_api import sync_playwright
import json

url = "https://housingconnect.nyc.gov/PublicWeb/search-lotteries"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    def log_response(response):
        try:
            # Only capture the real API call we care about
            if "SearchLotteries" in response.url:
                print("\nFOUND LOTTERY API:")
                print(response.url)

                data = response.json()

                print("\nSAMPLE DATA:\n")
                print(json.dumps(data, indent=2)[:2000])

        except Exception as e:
            print("JSON parse failed:", e)

    page.on("response", log_response)

    page.goto(url)

    # wait long enough for network calls to finish
    page.wait_for_timeout(10000)

    browser.close()