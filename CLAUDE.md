# CLAUDE.md — AI Assistant Guide

## What this project does
Crawls aircraft-related job postings from Canada's Job Bank (jobbank.gc.ca).
Two workers run in sequence:
1. worker-html — collects job URLs from search page → saves to data/urls.json
2. worker-js — visits each URL → saves raw and normalized JSON

## Project structure
- src/worker_html.py — Worker 1: collects URLs
- src/worker_js.py — Worker 2: collects job details
- src/normalize.py — data cleaning functions
- src/config.py — all settings in one place
- data/raw/ — raw JSON files
- data/normalized/ — clean structured JSON files

## How to run
docker compose up --build

## How to verify parser works
cat data/urls.json
ls data/raw/ | wc -l

## Common issues
- If worker-js fails — check that data/urls.json exists
- If 0 URLs found — Job Bank may have changed their HTML structure
- If Docker fails — make sure Docker Desktop is running

## Key files to check after DOM change
- src/worker_html.py — regex pattern for job URLs
- src/worker_js.py — extract_structured() function
