import json
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.svg")

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
days = {item["date"]: item for item in data["days"]}

today = date.today()
start = today - timedelta(days=364)
start -= timedelta(days=(start.weekday() + 1) % 7)

cell = 13
gap = 4
step = cell + gap
left = 48
top = 42
width = left + (53 * step) + 20
height = top + (7 * step) + 58

svg = [
    f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}" height="{height}"
    viewBox="0 0 {width} {height}"
    role="img"
    aria-label="GitHub contribution activity for {data["username"]}">
    <title>{data["username"]} GitHub contribution activity</title>
    <desc>Contribution activity over the trailing year.</desc>
    <rect width="100%" height="100%" rx="14" fill="#0d1117"/>
    <style>
      text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      .cell {{
        transform-box: fill-box;
        transform-origin: center;
      }}
    </style>
    <text x="{left}" y="22" fill="#c9d1d9" font-size="12" font-weight="600">
      GitHub Contributions — {data["username"]}
    </text>
    <text x="{width - 78}" y="22" fill="#8b949e" font-size="10">1 year</text>
    '''
]

for label, row in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
    y = top + row * step + 10
    svg.append(f'<text x="5" y="{y}" fill="#8b949e" font-size="10">{label}</text>')

for col in range(53):
    for row in range(7):
        current = start + timedelta(days=col * 7 + row)
        item = days.get(current.isoformat(), {"level": 0, "count": 0})
        level = min(int(item["level"]), len(PALETTE) - 1)
        count = int(item.get("count", 0))
        color = PALETTE[level]
        x = left + col * step
        y = top + row * step
        delay = (col * 7 + row) * 0.010
        label = f'{current.isoformat()}: {count} contributions'
        svg.append(
            f'''<rect class="cell" x="{x}" y="{y}" width="{cell}" height="{cell}"
            rx="3" fill="{color}" opacity="0">
              <title>{label}</title>
              <animate attributeName="opacity" from="0" to="1"
                dur="0.30s" begin="{delay:.3f}s" fill="freeze"/>
            </rect>'''
        )

total = sum(int(item.get("count", 0)) for item in data["days"])
active_days = sum(1 for item in data["days"] if int(item.get("count", 0)) > 0)

svg.append(
    f'''<text x="{left}" y="{height - 20}" fill="#8b949e" font-size="11">
      {total} contributions · {active_days} active days
    </text>
    <text x="{width - 142}" y="{height - 20}" fill="#8b949e" font-size="10">Less</text>'''
)

legend_x = width - 108
for i, color in enumerate(PALETTE):
    x = legend_x + i * 15
    svg.append(
        f'<rect x="{x}" y="{height - 30}" width="11" height="11" rx="2" fill="{color}"/>'
    )

svg.append("</svg>")
OUTPUT_FILE.write_text("\n".join(svg), encoding="utf-8")
print(f"Created {OUTPUT_FILE}")
