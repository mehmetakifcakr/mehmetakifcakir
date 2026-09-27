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

data = json.loads(DATA_FILE.read_text())
days = {
    item["date"]: item["level"]
    for item in data["days"]
}

today = date.today()

# Start on Sunday and show 53 weeks
start = today - timedelta(days=364)
start -= timedelta(days=(start.weekday() + 1) % 7)

cell = 13
gap = 4
step = cell + gap

left = 45
top = 35

width = left + (53 * step) + 20
height = top + (7 * step) + 55

svg = []

svg.append(
    f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}" height="{height}"
    viewBox="0 0 {width} {height}">
    <rect width="100%" height="100%" rx="12" fill="#0d1117"/>
    <style>
        text {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}
    </style>
    <text x="{left}" y="20"
          fill="#8b949e"
          font-size="12">GitHub Contributions — {data["username"]}</text>
    '''
)

# Day labels
labels = [
    ("Mon", 1),
    ("Wed", 3),
    ("Fri", 5),
]

for label, row in labels:
    y = top + row * step + 10
    svg.append(
        f'<text x="4" y="{y}" fill="#8b949e" font-size="10">{label}</text>'
    )

# Contribution cells
for col in range(53):
    for row in range(7):
        current = start + timedelta(days=col * 7 + row)
        level = days.get(current.isoformat(), 0)

        x = left + col * step
        y = top + row * step

        color = PALETTE[min(level, len(PALETTE) - 1)]
        delay = (col * 7 + row) * 0.012

        svg.append(
            f'''
            <rect x="{x}" y="{y}"
                  width="{cell}" height="{cell}"
                  rx="3"
                  fill="{color}"
                  opacity="0">
                <animate attributeName="opacity"
                         from="0" to="1"
                         dur="0.35s"
                         begin="{delay:.3f}s"
                         fill="freeze"/>
            </rect>
            '''
        )

total = sum(days.values())

svg.append(
    f'''
    <text x="{left}" y="{height - 20}"
          fill="#8b949e"
          font-size="11">
        {total} contributions in the last year
    </text>

    <text x="{width - 145}" y="{height - 20}"
          fill="#8b949e"
          font-size="10">Less</text>
    '''
)

# Legend
legend_x = width - 110

for i, color in enumerate(PALETTE):
    x = legend_x + i * 15
    svg.append(
        f'<rect x="{x}" y="{height - 30}" width="11" height="11" rx="2" fill="{color}"/>'
    )

svg.append("</svg>")

OUTPUT_FILE.write_text("\n".join(svg), encoding="utf-8")

print(f"Created {OUTPUT_FILE}")
