import json
from storage import read_json, write_json

def load_json(path):
    """
    Load previously seen lottery IDs from a JSON file.

    Args:
        path (str): Path to the seen.json file.

    Returns:
        set: A set of previously seen lottery IDs.
             Returns an empty set if file is missing or empty.
    """
    
    data = read_json(path)

    if not data:
        return set()

    return set(item["lotteryId"] for item in data)

def save_seen(path, seen):
    """
    Save the current set of seen lottery IDs to disk.

    Args:
        path (str): Path to the seen.json file.
        seen (set): Set of lottery IDs to persist.
    """
    write_json(path, list(seen))

def get_new_items(current, seen):
    """Return listings whose lotteryId is not present in the seen set.

    Args:
        current (list[dict]): Current scraped listings.
        seen (set | list): Previously seen lottery IDs.

    Returns:
        list[dict]: Listings that are new (not previously seen).
    """

    new_items = []

    for item in current:
        if item["lotteryId"] not in seen:
            new_items.append(item)

    return new_items

def append_json(path, data):
    # Load existing archive safely
    try:
        archive = read_json(path)
        if archive is None:
            archive = []
    except (FileNotFoundError, json.JSONDecodeError):
        archive = []

    # Ensure archive is a list
    if not isinstance(archive, list):
        archive = []

    # Build a set of existing IDs for fast lookup
    existing_ids = {item["lotteryId"] for item in archive if "lotteryId" in item}

    # Add only new items
    for item in data:
        item_id = item.get("lotteryId")
        if item_id and item_id not in existing_ids:
            archive.append(item)
            existing_ids.add(item_id)

    # Save updated archive
    write_json(path, archive)

def run_tracker(current, seen_path="data/seen.json", archive_path="data/archive.json"):
    """
    Append new items to an archive JSON file without duplicates.

    Args:
        path (str): Path to archive file.
        data (list): List of items (or IDs) to add to archive.

    Returns:
        None
    """
    seen = load_json(seen_path)

    new_items = get_new_items(current, seen)

    current_ids = {item["lotteryId"] for item in current}
    removed_ids = seen - current_ids

    append_json(archive_path, list(removed_ids))

    save_seen(seen_path, current_ids)

    return new_items



