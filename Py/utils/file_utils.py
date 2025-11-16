import os

# Pastikan folder data selalu ada
if not os.path.exists("data"):
    os.makedirs("data")
import json, os

def safe_read(path, default):
    if not os.path.exists(path):
        write_json(path, default)
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"[!] File rusak, reset {path}")
        write_json(path, default)
        return default

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)