#!/usr/bin/env python3
"""
Hand-author a neofetch-style info card SVG that looks like terminal command output:
Title bar, traffic light dots, and colored key-value rows:
Now, Role, Stack, Focus, Location, etc.
Fades in line by line with CSS keyframes.

    python scripts/make_info_card.py [output.svg]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

W, H = 840, 880
PAD = 32
TITLEBAR_H = 34

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#e6edf3"
ACCENT = "#22d3ee"
GREEN = "#39d353"
PURPLE = "#bc8cff"
BLUE = "#58a6ff"
GOLD = "#e3b341"

STATIC = bool(os.environ.get("STATIC"))

rows = [
    ("obeduri@github", "#", ACCENT, True),
    ("-------------------------", "", FRAME, False),
    ("OS", "GitHub / Cloud Architecture", BLUE, False),
    ("Role", "Senior Full Stack & AI Lead (13+ yrs)", GREEN, False),
    ("Focus", "Autonomous Agents · High-Velocity Microservices", GOLD, False),
    ("Backend", "Python, TypeScript, Node.js, FastAPI, Go", TEXT, False),
    ("Frontend", "Next.js, React, TailwindCSS, WebGL", TEXT, False),
    ("Cloud & AI", "Google Cloud (GCP), LLM Tooling, Agents", PURPLE, False),
    ("Location", "República Dominicana", TEXT, False),
    ("Website", "https://obeduri.com", ACCENT, False),
    ("GitHub", "https://github.com/obeduri", BLUE, False),
    ("", "", "", False),
    ("Highlight", "Architecting systems to optimize product delivery.", GREEN, False),
]

css = """
@keyframes fadeIn {
  0%   { opacity: 0; transform: translateY(8px); }
  100% { opacity: 1; transform: translateY(0); }
}
.row { opacity: 0; animation: fadeIn 0.4s ease-out forwards; }
@media (prefers-reduced-motion: reduce) {
  .row { opacity: 1 !important; transform: none !important; animation: none !important; }
}
""".strip()

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<style>{css}</style>',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    f'</linearGradient>'
    '</defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*18}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="13" '
             f'text-anchor="middle">obeduri@github: ~$ neofetch</text>')

start_y = TITLEBAR_H + 54
line_height = 42

for idx, (k, v, color, is_header) in enumerate(rows):
    delay = 0.15 + idx * 0.12
    y = start_y + idx * line_height
    cls_attr = "" if STATIC else f'class="row" style="animation-delay:{delay:.2f}s"'

    if is_header:
        parts.append(
            f'<g {cls_attr}>'
            f'<text x="{PAD+16}" y="{y}" fill="{color}" font-size="28" font-weight="700">{k}</text>'
            f'</g>'
        )
    elif not k and not v:
        continue
    elif not v:
        parts.append(
            f'<g {cls_attr}>'
            f'<text x="{PAD+16}" y="{y}" fill="{color}" font-size="20">{k}</text>'
            f'</g>'
        )
    else:
        parts.append(
            f'<g {cls_attr}>'
            f'<text x="{PAD+16}" y="{y}" fill="{color}" font-size="21" font-weight="600">{k}:</text>'
            f'<text x="{PAD+170}" y="{y}" fill="{TEXT}" font-size="21">{v}</text>'
            f'</g>'
        )

# Color swatches row at bottom (like neofetch)
swatch_y = H - PAD - 20
swatches = ["#ff5f56", "#ffbd2e", "#27c93f", "#22d3ee", "#58a6ff", "#bc8cff", "#e6edf3"]
swatch_w = 40
swatch_h = 24
swatch_cls = "" if STATIC else 'class="row" style="animation-delay:1.8s"'
parts.append(f'<g {swatch_cls}>')
for si, sc in enumerate(swatches):
    sx = PAD + 16 + si * (swatch_w + 10)
    parts.append(f'<rect x="{sx}" y="{swatch_y}" width="{swatch_w}" height="{swatch_h}" rx="4" fill="{sc}"/>')
parts.append('</g>')

parts.append('</svg>')
svg = "".join(parts)
open(OUT, "w", encoding="utf-8").write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)//1024} KB")
