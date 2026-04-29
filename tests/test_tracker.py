from tracker import (
    load_json,
    save_seen,
    get_new_items,
    run_tracker
)

def test_load_json(tmp_path):
    file = tmp_path / "seen.json"
    file.write_text("[1, 2, 3]")

    result = load_json(file)

    assert result == {1, 2, 3}

def test_load_json_empty(tmp_path):
    file = tmp_path / "seen.json"

    result = load_json(file)

    assert result == set()

def test_save_seen(tmp_path):
    file = tmp_path / "seen.json"

    save_seen(file, {1, 2, 3})

    data = file.read_text()

    assert "1" in data
    assert "2" in data
    assert "3" in data

def test_get_new_items():
    current = [
        {"lotteryId": 1, "name": "A"},
        {"lotteryId": 2, "name": "B"},
        {"lotteryId": 3, "name": "C"},
    ]

    seen = {1, 2}

    result = get_new_items(current, seen)

    assert len(result) == 1
    assert result[0]["lotteryId"] == 3

def test_run_tracker(tmp_path, monkeypatch):
    seen_file = tmp_path / "seen.json"
    archive_file = tmp_path / "archive.json"

    current = [
        {"lotteryId": 1, "name": "A"},
        {"lotteryId": 2, "name": "B"},
        {"lotteryId": 3, "name": "C"},
    ]

    # Mock previous seen state
    monkeypatch.setattr("tracker.load_json", lambda x: {1, 2})

    # Capture what gets saved instead of writing to disk
    saved_seen = {}

    def fake_save_seen(path, seen):
        saved_seen["data"] = seen

    monkeypatch.setattr("tracker.save_seen", fake_save_seen)

    # Capture archive writes
    archived = {}

    def fake_append_json(path, data):
        archived["data"] = data

    monkeypatch.setattr("tracker.append_json", fake_append_json)

    result = run_tracker(
        current,
        seen_path=seen_file,
        archive_path=archive_file
    )

    # Only new item should be returned
    assert len(result) == 1
    assert result[0]["lotteryId"] == 3

    # Seen should be updated to full current set
    assert saved_seen["data"] == {1, 2, 3}

    # Removed items should be empty in this case
    assert archived["data"] == []
