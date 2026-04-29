from scraper import fetch_lotteries
from tracker import load_json, save_seen, get_new_items, append_json
from notifier import send_notification

def main():
    # Get current lottery listings
    data = fetch_lotteries()

    # Load previously seen listings
    seen = load_json("data/seen.json")
    archive = load_json("data/archive.json")

    # Get new listings
    new_items = get_new_items(data, seen)

    # Send email
    if new_items:
        send_notification(new_items)

    # Update Seen File
    save_seen("data/seen.json", data)

    # Update Archive File
    append_json("data/archive.json", data)

if __name__ == "__main__":
    main()