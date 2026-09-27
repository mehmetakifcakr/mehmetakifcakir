from pathlib import Path

svg = r'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="320" viewBox="0 0 520 320" role="img" aria-label="Mechatronics engineer profile information">
<rect width="520" height="320" rx="14" fill="#0d1117"/>
<circle cx="494" cy="24" r="5" fill="#39d353"/>
<text x="24" y="34" fill="#39d353" font-family="monospace" font-size="16" font-weight="700">mehmetakifcakr@github</text>
<text x="24" y="57" fill="#484f58" font-family="monospace" font-size="12">──────────────────────────────────────────────</text>

<text x="24" y="90" fill="#58a6ff" font-family="monospace" font-size="14">ROLE</text>
<text x="155" y="90" fill="#c9d1d9" font-family="monospace" font-size="14">Mechatronics Engineer</text>

<text x="24" y="122" fill="#58a6ff" font-family="monospace" font-size="14">FOCUS</text>
<text x="155" y="122" fill="#c9d1d9" font-family="monospace" font-size="14">Robotics / Automation</text>

<text x="24" y="154" fill="#58a6ff" font-family="monospace" font-size="14">STACK</text>
<text x="155" y="154" fill="#c9d1d9" font-family="monospace" font-size="14">Python / C++ / Arduino</text>

<text x="24" y="186" fill="#58a6ff" font-family="monospace" font-size="14">DESIGN</text>
<text x="155" y="186" fill="#c9d1d9" font-family="monospace" font-size="14">3D CAD / Prototyping</text>

<text x="24" y="218" fill="#58a6ff" font-family="monospace" font-size="14">INTEREST</text>
<text x="155" y="218" fill="#c9d1d9" font-family="monospace" font-size="14">Embedded Systems / CV</text>

<text x="24" y="250" fill="#58a6ff" font-family="monospace" font-size="14">STATUS</text>
<text x="155" y="250" fill="#39d353" font-family="monospace" font-size="14">Building things...</text>

<text x="24" y="286" fill="#8b949e" font-family="monospace" font-size="12">[ profile.system ]</text>
<text x="168" y="286" fill="#39d353" font-family="monospace" font-size="12">ONLINE</text>
</svg>
'''
Path("info-card.svg").write_text(svg, encoding="utf-8")
print("Created info-card.svg")
