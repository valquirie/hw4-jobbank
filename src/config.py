# Налаштування проекту — всі параметри в одному місці

# URL пошуку вакансій на Job Bank
SEARCH_URL = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=aircraft&sort=D"

# Папки для збереження даних
RAW_DIR = "/app/data/raw"
NORM_DIR = "/app/data/normalized"

# Файл де worker-list зберігає знайдені URL
URLS_FILE = "/app/data/urls.json"

# Максимальна кількість вакансій для збору
MAX_JOBS = 15

# Максимальна кількість символів в контенті
MAX_CONTENT_CHARS = 5000