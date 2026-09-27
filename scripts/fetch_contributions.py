import json
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "mehmetakifcakr"
URL = f"https://github.com/users/{USERNAME}/contributions"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td[data-date]"):
    date = cell.get("data-date")
    level = int(cell.get("data-level", "0"))

    if date:
        days.append({
            "date": date,
            "level": level
        })

if not days:
    raise RuntimeError("GitHub contribution verileri bulunamadı.")

days.sort(key=lambda x: x["date"])

output = {
    "username": USERNAME,
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "days": days
}

Path("data").mkdir(exist_ok=True)

with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"{len(days)} contribution days collected.")
