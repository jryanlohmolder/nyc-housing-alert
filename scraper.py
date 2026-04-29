from playwright.sync_api import sync_playwright
import logging as log

URL = "https://housingconnect.nyc.gov/PublicWeb/search-lotteries"

def fetch_lotteries():
    results = {"sales": [], "rentals": []}

    def handle_response(response):
        if "SearchLotteries" in response.url:
            try:
                data = response.json()
                results["sales"] = data.get("sales", [])
                results["rentals"] = data.get("rentals", [])

            except Exception as e:
                log.error("Parse error: %s", e)


    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("response", handle_response)
        page.goto(URL)
        page.wait_for_timeout(8000)
        browser.close()

    return results["sales"] + results["rentals"]

if __name__ == "__main__":
    items = fetch_lotteries()
    print(f"Listing: {len(items)}")