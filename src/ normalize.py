"""
normalize.py — функції для нормалізації даних
"""

import re
from config import MAX_CONTENT_CHARS


def normalize(raw: dict) -> dict:
    """Перетворює сирий JSON у чистий нормалізований формат"""
    content = raw.get("content", "")
    
    # прибираємо зайві пробіли і порожні рядки
    content = re.sub(r"\n{3,}", "\n\n", content).strip()
    content = content[:MAX_CONTENT_CHARS]

    # витягуємо зарплату
    salary_match = re.search(r"\$[\d,.]+ to \$[\d,.]+\s*\w+", content)
    salary = salary_match.group(0) if salary_match else "Not specified"

    # витягуємо локацію
    location_match = re.search(r"Location\s+([^\n]+)", content)
    location = location_match.group(1).strip() if location_match else "Not specified"

    return {
        "url": raw["url"],
        "title": (raw.get("title") or "").replace(" - Job posting - Job Bank", "").strip(),
        "fetched_at": raw["fetched_at"],
        "source": raw["source"],
        "location": location,
        "salary": salary,
        "content": content,
        "links": raw.get("links", [])[:10],
    }