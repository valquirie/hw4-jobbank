"""
worker_html.py — Worker 1
Збирає список URL вакансій з пошукової сторінки Job Bank
і зберігає їх у data/urls.json
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime, timezone

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from config import SEARCH_URL, URLS_FILE, MAX_JOBS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/app/data/worker_html.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)


async def main():
    log.info("=== worker-html starting ===")
    start_time = datetime.now(timezone.utc)

    async with AsyncWebCrawler() as crawler:
        config = CrawlerRunConfig(cache_mode="bypass", word_count_threshold=5)
        result = await crawler.arun(url=SEARCH_URL, config=config)

        if not result.success:
            log.error("failed to crawl search page: %s", result.error_message)
            return

        # знаходимо всі URL вакансій
        job_urls = re.findall(
            r"https://www\.jobbank\.gc\.ca/jobsearch/jobposting/\d+",
            result.markdown or ""
        )
        job_urls = list(dict.fromkeys(job_urls))[:MAX_JOBS]
        log.info("found %d job URLs", len(job_urls))

        # метрика — success rate
        success_rate = len(job_urls) / MAX_JOBS * 100
        log.info("success_rate: %.1f%%", success_rate)

        # зберігаємо URLs у файл
        os.makedirs(os.path.dirname(URLS_FILE), exist_ok=True)
        payload = {
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "count": len(job_urls),
            "success_rate": round(success_rate, 1),
            "urls": job_urls,
        }
        with open(URLS_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        log.info("saved urls → %s", URLS_FILE)

    duration = (datetime.now(timezone.utc) - start_time).seconds
    log.info("duration: %ds", duration)
    log.info("=== worker-html done ===")


if __name__ == "__main__":
    asyncio.run(main())