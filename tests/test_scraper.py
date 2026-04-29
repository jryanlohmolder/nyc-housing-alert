import pytest
from unittest.mock import MagicMock, patch
from scraper import fetch_lotteries

def make_mock_page(json_data):
    """ 
    Helper that builds a fake Playwright page
    Factory function that builds a configured 
    mock for reuse across tests.
    """

    mock_response = MagicMock()
    mock_response.url = "https:///example.com/SearchLotteries"
    mock_response.json.return_value = json_data

    mock_page = MagicMock()
    mock_browser = MagicMock()
    mock_browser.new_page.return_value = mock_page

    # Simulate page.on("response", handler) actually calling the handler.
    # When page.on is called, we grab the handler and fire it immediately

    def trigger_handler(event, handler):
        if event == "response":
            handler(mock_response)

    mock_page.on.side_effect = trigger_handler

    return mock_browser, mock_page


@patch("scraper.sync_playwright")
def test_fetch_lotteries_return_sales_and_rentals(mock_playwright):
    
    fake_data = {
        "sales": [{"lotteryId": "S1", "lotteryName": "Sale One"}],
        "rentals": [{"lotteryId": "R1", "lotteryName": "Rental One"}],
    }
    mock_browswer, _ = make_mock_page(fake_data)
    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browswer

    listings = fetch_lotteries()

    # Assert shape and content
    assert len(listings) == 2
    assert listings[0]["lotteryId"] == "S1"
    assert listings[1]["lotteryId"] == "R1"

@patch("scraper.sync_playwright")
def test_fetch_lotteries_empty_responses(mock_playwright):
    
    fake_data = {}
    mock_browser, _ = make_mock_page(fake_data)
    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser

    listings = fetch_lotteries()

    assert listings == []

@patch("scraper.sync_playwright")
def test_fetch_lotteries_ignores_unrelated_responses(mock_playwright):

    mock_response = MagicMock()
    mock_response.url = "https://example.com/some-image.png"

    mock_page = MagicMock()
    mock_browser = MagicMock()
    mock_browser.new_page.return_value = mock_page

    def trigger_handler(event, handler):
        if event == "response":
            handler(mock_response)
        
    mock_page.on.side_effect = trigger_handler
    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser

    listings = fetch_lotteries()

    assert listings == []
