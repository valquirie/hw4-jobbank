# HW4 – Job Bank Aircraft Jobs Crawler

Automated web crawler for aircraft-related job postings from Canada's Job Bank.
Built with Crawl4AI, Docker Compose, and Python.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

## Quick Start

```bash
git clone https://github.com/valquirie/hw4-jobbank.git
cd hw4-jobbank
docker compose up --build
```

## Note
The data/raw/ and data/normalized/ folders are created automatically when Docker starts.

## Services

| Service | Role |
|---|---|
| worker-html | Collects job URLs from search page |
| worker-js | Crawls each job page for details |
| scheduler | Runs both workers every 24 hours |
| status | Shows system status and data freshness |

## Scalability

To crawl more jobs edit src/config.py:
MAX_JOBS = 15  # increase to 50, 100, etc.

## Check Status

```bash
python3 src/status.py
```

## Tools

- Crawl4AI https://docs.crawl4ai.com
- Docker Compose https://docs.docker.com/compose/
- Python json and logging
