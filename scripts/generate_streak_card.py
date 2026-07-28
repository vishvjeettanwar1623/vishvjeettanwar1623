import urllib.request
import re
import os
from datetime import datetime

USERNAME = "vishvjeettanwar1623"
OUTPUT_PATH = "assets/streak_card.svg"

def generate_premium_streak_card():
    url = f"https://github.com/users/{USERNAME}/contributions"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    
    html_res = urllib.request.urlopen(req).read().decode('utf-8')

    header_match = re.search(r'([\d,]+)\s+contributions', html_res, re.IGNORECASE)
    total_contribs = 377
    if header_match:
        total_contribs = int(header_match.group(1).replace(',', ''))

    rect_pattern = re.compile(r'data-date="([^"]+)"[^>]*data-level="(\d+)"')
    matches = rect_pattern.findall(html_res)

    contributions = []
    for date_str, level_str in matches:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        level = int(level_str)
        contributions.append((dt, level))

    contributions.sort(key=lambda x: x[0])

    max_streak = 0
    curr_calc = 0
    longest_start = None
    longest_end = None
    temp_start = None

    for dt, level in contributions:
        if level > 0:
            if curr_calc == 0:
                temp_start = dt
            curr_calc += 1
            if curr_calc > max_streak:
                max_streak = curr_calc
                longest_start = temp_start
                longest_end = dt
        else:
            curr_calc = 0

    active_streak = 0
    active_start = None
    active_end = None

    rev = list(reversed(contributions))
    if rev:
        if rev[0][1] > 0 or (len(rev) > 1 and rev[1][1] > 0):
            in_streak = False
            for dt, level in rev:
                if level > 0:
                    if not in_streak:
                        in_streak = True
                        active_end = dt
                    active_streak += 1
                    active_start = dt
                elif in_streak:
                    break

    active_str = f"{active_start.strftime('%b %d')} - {active_end.strftime('%b %d')}" if active_start and active_end else "Active"
    longest_str = f"{longest_start.strftime('%b %d')} - {longest_end.strftime('%b %d')}" if longest_start and longest_end else "Max"

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 210" width="100%" height="100%">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&amp;display=swap');
      
      .card-bg {{
        fill: url(#cardGradient);
        stroke: #30363d;
        stroke-width: 1.5px;
        rx: 12px;
      }}

      .val-blue {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 34px; fill: #58a6ff; text-anchor: middle; filter: drop-shadow(0px 2px 8px rgba(88,166,255,0.3)); }}
      .val-orange {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 34px; fill: #f78166; text-anchor: middle; filter: drop-shadow(0px 2px 8px rgba(247,129,102,0.3)); }}
      .val-green {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 34px; fill: #7ee787; text-anchor: middle; filter: drop-shadow(0px 2px 8px rgba(126,231,135,0.3)); }}

      .lbl-main {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 14px; fill: #ffffff; text-anchor: middle; letter-spacing: 0.5px; }}
      .lbl-sub {{ font-family: 'JetBrains Mono', monospace; font-weight: 500; font-size: 12px; fill: #8b949e; text-anchor: middle; }}
      
      .divider {{ stroke: #30363d; stroke-width: 1px; stroke-dasharray: 4 4; }}
      .bar-bg {{ fill: #161b22; rx: 4px; }}
      .bar-commits {{ fill: #7ee787; rx: 4px; }}
      .bar-prs {{ fill: #a371f7; rx: 4px; }}
    </style>

    <linearGradient id="cardGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="50%" stop-color="#161b22" />
      <stop offset="100%" stop-color="#0d1117" />
    </linearGradient>

    <linearGradient id="flameGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f78166" />
      <stop offset="100%" stop-color="#e36049" />
    </linearGradient>
  </defs>

  <!-- Background Card -->
  <rect class="card-bg" width="740" height="210" rx="12" />

  <!-- Column 1: Total Contributions -->
  <g transform="translate(125, 0)">
    <text x="0" y="75" class="val-blue">{total_contribs}</text>
    <text x="0" y="112" class="lbl-main">Total Contributions</text>
    <text x="0" y="136" class="lbl-sub">2026 Year-to-Date</text>
  </g>

  <!-- Divider 1 -->
  <line x1="245" y1="30" x2="245" y2="150" class="divider" />

  <!-- Column 2: Current Active Streak -->
  <g transform="translate(370, 0)">
    <!-- Ring Container -->
    <circle cx="0" cy="55" r="28" fill="#161b22" stroke="#f78166" stroke-width="2.5" />
    <path d="M 370,39 C 365,46 362,50 365,57 C 367,60 370,62 373,57 C 375,55 375,52 373,50 C 376,53 378,57 375,60 C 373,64 368,65 365,61 C 361,57 364,50 370,39 Z" fill="url(#flameGrad)" transform="translate(-370, -48)" />
    
    <text x="0" y="105" class="val-orange">{active_streak} Days</text>
    <text x="0" y="132" class="lbl-main" fill="#f78166">Current Streak</text>
    <text x="0" y="154" class="lbl-sub">{active_str}</text>
  </g>

  <!-- Divider 2 -->
  <line x1="495" y1="30" x2="495" y2="150" class="divider" />

  <!-- Column 3: Longest Streak -->
  <g transform="translate(615, 0)">
    <text x="0" y="75" class="val-green">{max_streak} Days</text>
    <text x="0" y="112" class="lbl-main">Longest Streak</text>
    <text x="0" y="136" class="lbl-sub">{longest_str}</text>
  </g>

  <!-- Bottom Activity Bar -->
  <g transform="translate(40, 172)">
    <rect class="bar-bg" x="0" y="0" width="660" height="8" rx="4" />
    <rect class="bar-commits" x="0" y="0" width="646" height="8" rx="4" />
    <rect class="bar-prs" x="646" y="0" width="14" height="8" rx="4" />
    <text x="0" y="24" class="lbl-sub" text-anchor="start">🟢 98% Commits</text>
    <text x="660" y="24" class="lbl-sub" text-anchor="end">🟣 2% Pull Requests</text>
  </g>
</svg>
'''

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated premium {OUTPUT_PATH}!")

if __name__ == "__main__":
    generate_premium_streak_card()
