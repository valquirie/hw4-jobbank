import asyncio
import json
import logging
import os
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/app/data/crawler.log", encoding="utf-8"),
    ],
)

log = logging.getLogger(__name__)

SEARCH_URL = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=aircraft&sort=D"
RAW_DIR = "/app/data/raw"
NORM_DIR = "/app/data/normalized"
MAX_PAGES = 15


def slug(url):
    parsed = urlparse(url)
    raw = parsed.netloc + parsed.path + parsed.query
    return re.sub(r"[^a-zA-Z0-9_-]", "_", raw)[:120]


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info("saved → %s", path)


def normalize(raw):
    content = re.sub(r"\n{3,}", "\n\n", raw.get("content", "")).strip()[:5000]
    return {
        "url": raw["url"],
        "title": (raw.get("title") or "").strip(),
        "fetched_at": raw["fetched_at"],
        "source": raw["source"],
        "content": content,
        "links": raw.get("links", [])[:10],
    }


async def crawl(crawler, url):
    log.info("crawling %s", url)
    try:
        config = CrawlerRunConfig(cache_mode="bypass", word_count_threshold=5)
        result = await crawler.arun(url=url, config=config)
        if not result.success:
            log.warning("failed: %s", result.error_message)
            return None
        links = []
        if result.links:
            for lnk in result.links.get("internal", [])[:10]:
                href = lnk.get("href", "")
                if href:
                    links.append(href)
        return {
            "url": url,
            "title": result.metadata.get("title", "") if result.metadata else "",
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source": urlparse(url).netloc,
            "status_code": result.status_code,
            "content": (result.markdown or "").strip(),
            "links": links,
        }
    except Exception as e:
        log.error("error: %s", e)
        return None


async def main():
    log.info("=== worker-html starting ===")

    async with AsyncWebCrawler() as crawler:
        # Step 1: crawl search results page
        raw = await crawl(crawler, SEARCH_URL)
        if not raw:
            log.error("failed to crawl search page")
            return

        # extract job posting URLs from content
        job_urls = re.findall(
            r"https://www\.jobbank\.gc\.ca/jobsearch/jobposting/\d+",
            raw["content"]
        )
        job_urls = list(dict.fromkeys(job_urls))[:MAX_PAGES]
        log.info("found %d job URLs", len(job_urls))

        if not job_urls:
            # fallback: save search page itself
            job_urls = [SEARCH_URL]

        # Step 2: crawl each job posting
        for url in job_urls:
            r = await crawl(crawler, url)
            if not r:
                continue
            s = slug(url)
            save_json(f"{RAW_DIR}/{s}.json", r)
            save_json(f"{NORM_DIR}/{s}.json", normalize(r))

    log.info("=== worker-html done ===")


if __name__ == "__main__":
    asyncio.run(main())
    
