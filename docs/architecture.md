# Architecture

## Overview
Job Bank Website
|
v
[worker-html] — fetches search page → extracts job URLs → saves data/urls.json
|
v
[worker-js] — reads urls.json → visits each job page → saves raw + normalized JSON
|
v
data/raw/          — raw JSON files (full content)
data/normalized/   — clean structured JSON files (title, salary, location)
## Services (Docker Compose)

| Service | File | Input | Output |
|---|---|---|---|
| worker-html | src/worker_html.py | Job Bank search URL | data/urls.json |
| worker-js | src/worker_js.py | data/urls.json | data/raw/*.json, data/normalized/*.json |

## Metrics logged
- success_rate — % of successfully crawled pages
- duration — time in seconds
- error_count — number of failed requests
- | scheduler | src/scheduler.py | — | Runs worker-html + worker-js every 24h |
| status | src/status.py | data/urls.json + data/ | Shows system status and data freshness |

## Data flow
1. worker-html starts → crawls search page → finds 15 job URLs → saves urls.json
2. worker-js starts → reads urls.json → crawls each job page → saves JSON files
