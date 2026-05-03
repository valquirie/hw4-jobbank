import logging
import subprocess
import time
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/app/data/scheduler.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

INTERVAL_HOURS = 24


def run_worker(script):
    log.info("starting %s", script)
    result = subprocess.run(["python", script])
    log.info("%s finished — code %d", script, result.returncode)
    return result.returncode == 0


def main():
    log.info("=== scheduler starting (every %dh) ===", INTERVAL_HOURS)
    while True:
        log.info("--- run started at %s ---", datetime.now(timezone.utc).isoformat())
        run_worker("src/worker_html.py")
        run_worker("src/worker_js.py")
        log.info("--- run done. sleeping %dh ---", INTERVAL_HOURS)
        time.sleep(INTERVAL_HOURS * 3600)


if __name__ == "__main__":
    main()