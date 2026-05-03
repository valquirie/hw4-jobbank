import json
import os
from datetime import datetime, timezone

RAW_DIR = "data/raw"
NORM_DIR = "data/normalized"
URLS_FILE = "data/urls.json"

print("=" * 40)
print("  JOB BANK CRAWLER — STATUS")
print("=" * 40)

# перевіряємо urls.json
if os.path.exists(URLS_FILE):
    with open(URLS_FILE) as f:
        urls = json.load(f)
    print(f"Last crawl:    {urls['fetched_at']}")
    print(f"URLs found:    {urls['count']}")
    print(f"Success rate:  {urls['success_rate']}%")
else:
    print("urls.json: NOT FOUND — run docker compose up")

# перевіряємо файли
raw = len(os.listdir(RAW_DIR)) if os.path.exists(RAW_DIR) else 0
norm = len(os.listdir(NORM_DIR)) if os.path.exists(NORM_DIR) else 0
print(f"Raw files:     {raw}")
print(f"Normalized:    {norm}")

# перевіряємо свіжість
if os.path.exists(URLS_FILE):
    fetched = datetime.fromisoformat(urls['fetched_at'])
    now = datetime.now(timezone.utc)
    hours = (now - fetched).seconds // 3600
    if hours < 24:
        print(f"Data age:      {hours}h — FRESH ✓")
    else:
        print(f"Data age:      {hours}h — OUTDATED, run again!")

print("=" * 40)
