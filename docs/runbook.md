# Runbook — How to verify the parser works

## Quick check
docker compose up --build
ls data/raw/ | wc -l

## Step by step

### 1. Check urls.json was created
cat data/urls.json

Expected: list of 10-15 URLs like:
https://www.jobbank.gc.ca/jobsearch/jobposting/XXXXXXX

### 2. Check raw files
ls data/raw/

Expected: 10-15 JSON files

### 3. Check a normalized file
cat data/normalized/*.json | head -30

Expected: title, salary, location fields

## If something is broken

### 0 URLs found
- Job Bank changed HTML structure
- Run: cat data/worker_html.log
- Fix regex in src/worker_html.py

### worker-js fails
- Check urls.json exists: ls data/urls.json
- Check logs: cat data/worker_js.log

### Docker fails
- Make sure Docker Desktop is running
- Try: docker compose down && docker compose up --build
