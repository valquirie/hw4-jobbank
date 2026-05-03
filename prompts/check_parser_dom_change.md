# Prompt: Check parser after DOM change

## Context
The Job Bank website may change its HTML structure.
If worker-html collects 0 URLs, the regex pattern is likely broken.

## Task for Claude Code
1. Check the current regex in src/worker_html.py
2. Fetch the live page and check if job URLs still match the pattern
3. If not — suggest a fix

## Prompt to use
"Look at src/worker_html.py. The crawler is returning 0 job URLs.
Check the regex pattern that extracts job posting URLs from the page.
Fetch https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=aircraft
and verify if the pattern still matches. If not, fix it."

## Expected output
- Updated regex pattern in worker_html.py
- At least 10 URLs found in data/urls.json after fix
