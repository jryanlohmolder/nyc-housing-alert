"""
storage.py

Simple JSON file storage utilities for reading and writing structured data.

This module provides basic helper functions for persisting Python data
structures (such as lists and dictionaries) to JSON files and loading them
back into Python objects.

It is designed to be used by higher-level application logic (e.g. tracker.py)
and intentionally contains no domain-specific logic about the data it stores.

Key behaviors:
- If a JSON file does not exist, read_json() returns an empty list.
- If a JSON file exists but is empty or invalid, read_json() returns an empty list.
- write_json() overwrites the file with the provided Python object in JSON format.

This module assumes all stored data is JSON-serializable.
"""

import json

def read_json(path):

    try:
        with open(path, 'r') as file:
            data = json.load(file)

            return data

    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_json(path, data):
    with open(path, 'w') as file:
        json.dump(data, file)
