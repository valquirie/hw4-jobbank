# HW4 – Job Bank Aircraft Jobs Crawler

Crawls aircraft-related job postings from Canada's Job Bank (jobbank.gc.ca) and saves them as structured JSON files.

## How to run

```bash
docker compose up --build
```

## What it does

1. Crawls job postings for "aircraft" from jobbank.gc.ca
2. Saves raw JSON to `data/raw/`
3. Saves normalized JSON to `data/normalized/`

## Project structure
hw4-jobbank/
├── compose.yaml
├── Dockerfile
├── README.md
├── worker/
│   └── crawler.py
└── data/
├── raw/
└── normalized/
## JSON structure

```json
{
  "url": "https://www.jobbank.gc.ca/jobsearch/jobposting/123",
  "title": "Aircraft Maintenance Engineer",
  "fetched_at": "2026-05-03T12:00:00Z",
  "source": "www.jobbank.gc.ca",
  "content": "Job description...",
  "links": []
}
```

## Tools used

- [Crawl4AI](https://docs.crawl4ai.com)
- [Docker Compose](https://docs.docker.com/compose/)
- Python `json` and `logging`