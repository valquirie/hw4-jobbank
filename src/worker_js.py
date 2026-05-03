"""
worker_js.py — Worker 2
Читає urls.json, заходить на кожну вакансію
і зберігає деталі в data/raw/ та data/normalized/
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from config import RAW_DIR, NORM_DIR, URLS_FILE, MAX_CONTENT_CHARS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/app/data/worker_js.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)


def slug(url):
    parsed = urlparse(url)
    raw = parsed.netloc + parsed.path
    return re.sub(r"[^a-zA-Z0-9_-]", "_", raw)[:120]


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info("saved → %s", path)


def extract_structured(content, url, title, fetched_at):
    """Structured extraction — витягуємо конкретні поля з тексту"""
    # зарплата
    salary_match = re.search(r"\$[\d,.]+ to \$[\d,.]+\s*\w+", content)
    salary = salary_match.group(0) if salary_match else "Not specified"

    # локація
    location_match = re.search(r"Location\s+([^\n]+)", content)
    location = location_match.group(1).strip() if location_match else "Not specified"

    # компанія
    company_match = re.search(r"by\s+(?:a licensed third-party for\s+)?(?:Employer details\s+)?([^\n]+)", content)
    company = company_match.group(1).strip() if company_match else "Not specified"

    return {
        "url": url,
        "title": title.replace(" - Job posting - Job Bank", "").strip(),
        "fetched_at": fetched_at,
        "source": "www.jobbank.gc.ca",
        "company": company,
        "location": location,
        "salary": salary,
        "content": content[:MAX_CONTENT_CHARS],
        "links": [],
    }


async def crawl(crawler, url):
    log.info("crawling %s", url)
    try:
        config = CrawlerRunConfig(cache_mode="bypass", word_count_threshold=5)
        result = await crawler.arun(url=url, config=config)
        if not result.success:
            log.warning("failed: %s", result.error_message)
            return None
        return result
    except Exception as e:
        log.error("error: %s", e)
        return None


async def main():
    log.info("=== worker-js starting ===")
    start_time = datetime.now(timezone.utc)

    # читаємо URLs від worker-html
    if not os.path.exists(URLS_FILE):
        log.error("urls.json not found — run worker-html first!")
        return

    with open(URLS_FILE, encoding="utf-8") as f:
        payload = json.load(f)

    urls = payload.get("urls", [])
    log.info("loaded %d URLs from %s", len(urls), URLS_FILE)

    # метрики
    success_count = 0
    error_count = 0

    async with AsyncWebCrawler() as crawler:
        for url in urls:
            result = await crawl(crawler, url)
            if not result:
                error_count += 1
                continue

            fetched_at = datetime.now(timezone.utc).isoformat()
            content = (result.markdown or "").strip()
            title = result.metadata.get("title", "") if result.metadata else ""

            # raw JSON
            raw = {
                "url": url,
                "title": title,
                "fetched_at": fetched_at,
                "source": "www.jobbank.gc.ca",
                "status_code": result.status_code,
                "content": content,
                "links": [],
            }
            s = slug(url)
            save_json(f"{RAW_DIR}/{s}.json", raw)

            # normalized JSON зі structured extraction
            norm = extract_structured(content, url, title, fetched_at)
            save_json(f"{NORM_DIR}/{s}.json", norm)
            success_count += 1

    # фінальні метрики
    duration = (datetime.now(timezone.utc) - start_time).seconds
    success_rate = success_count / len(urls) * 100 if urls else 0
    log.info("success: %d, errors: %d, success_rate: %.1f%%",
             success_count, error_count, success_rate)
    log.info("duration: %ds", duration)
    log.info("=== worker-js done ===")


if __name__ == "__main__":
    asyncio.run(main())