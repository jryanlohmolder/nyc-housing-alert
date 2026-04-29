import os
from storage import read_json, write_json

def test_write_and_read(tmp_path):
    file_path = tmp_path / "test.json"

    data = [{"id": 1}, {"id": 2}]

    write_json(file_path, data)
    result = read_json(file_path)

    assert result == data

def test_missing_file_returns_empty(tmp_path):
    file_path = tmp_path / "does_not_exist.json"

    result = read_json(file_path)

    assert result == []

def test_corrupt_file_returns_empty(tmp_path):
    file_path = tmp_path / "bad.json"

    file_path.write_text("not valid json")
    
    result = read_json(file_path)

    assert result == []