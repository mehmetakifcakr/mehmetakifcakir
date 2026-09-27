import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "mehmetakifcakr"
URL = f"https://github.com/users/{USERNAME}/contributions"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; GitHubProfile/1.0)"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
days = []

for cell in soup.select("td[data-date]"):
    date = cell.get("data-date")
    level = int(cell.get("data-level", "0"))
    count = cell.get("data-count")

    if count is None:
        label = cell.get("aria-label", "")
        match = re.search(r"(\d[\d,]*)\s+contribution", label, re.IGNORECASE)
        count = match.group(1).replace(",", "") if match else "0"

    if date:
        days.append({
            "date": date,
            "level": level,
            "count": int(count),
        })

if not days:
    raise RuntimeError("GitHub contribution verileri bulunamadı.")

days.sort(key=lambda x: x["date"])

output = {
    "username": USERNAME,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "days": days,
}

Path("data").mkdir(exist_ok=True)
Path("data/contributions.json").write_text(
    json.dumps(output, indent=2),
    encoding="utf-8",
)

total = sum(item["count"] for item in days)
active_days = sum(1 for item in days if item["count"] > 0)

print(f"{len(days)} days collected.")
print(f"{total} contributions across {active_days} active days.")
