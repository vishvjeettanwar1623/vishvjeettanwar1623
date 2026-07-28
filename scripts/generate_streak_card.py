import urllib.request
import re
import os
from datetime import datetime

USERNAME = "vishvjeettanwar1623"
OUTPUT_PATH = "assets/streak_card.svg"

def generate_minimal_streak_card():
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

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 185" width="100%" height="100%">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&amp;display=swap');
      
      .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 8px; }}
      .title-white {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 32px; fill: #ffffff; text-anchor: middle; }}
      .title-orange {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 32px; fill: #f78166; text-anchor: middle; }}
      .title-green {{ font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 32px; fill: #7ee787; text-anchor: middle; }}

      .lbl-main {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 14px; fill: #c9d1d9; text-anchor: middle; }}
      .lbl-sub {{ font-family: 'JetBrains Mono', monospace; font-weight: 400; font-size: 12px; fill: #8b949e; text-anchor: middle; }}
      
      .divider {{ stroke: #30363d; stroke-width: 1px; }}

      .track-ring {{ fill: #161b22; stroke: #30363d; stroke-width: 3px; }}
      .progress-ring {{ fill: none; stroke: #f78166; stroke-width: 3.5px; stroke-dasharray: 105 30; stroke-linecap: round; transform: rotate(-90deg); transform-origin: 360px 48px; }}
    </style>
  </defs>

  <!-- Clean Flat Background -->
  <rect class="bg" width="720" height="185" rx="8" />

  <!-- Column 1: Total Contributions -->
  <g transform="translate(120, 0)">
    <text x="0" y="80" class="title-white">{total_contribs}</text>
    <text x="0" y="118" class="lbl-main">Total Contributions</text>
    <text x="0" y="144" class="lbl-sub">2026 Year-to-Date</text>
  </g>

  <!-- Divider 1 -->
  <line x1="240" y1="28" x2="240" y2="155" class="divider" />

  <!-- Column 2: Current Streak with Custom Dual Ring Progress Dial -->
  <g transform="translate(360, 0)">
    <!-- Base Circle Container & Glowing Progress Ring Arc -->
    <circle cx="0" cy="48" r="23" class="track-ring" />
    <circle cx="360" cy="48" r="23" class="progress-ring" />
    
    <!-- Centered Flame Icon -->
    <path d="M 0,35 C -4,42 -8,46 -5,52 C -3,56 1,58 5,53 C 7,51 7,48 5,46 C 9,49 10,52 8,55 C 6,58 1,60 -2,57 C -6,52 -4,46 0,35 Z" fill="#f78166" />
    
    <text x="0" y="104" class="title-orange">{active_streak} Days</text>
    <text x="0" y="132" class="lbl-main" fill="#f78166">Current Streak</text>
    <text x="0" y="154" class="lbl-sub">{active_str}</text>
  </g>

  <!-- Divider 2 -->
  <line x1="480" y1="28" x2="480" y2="155" class="divider" />

  <!-- Column 3: Longest Streak -->
  <g transform="translate(600, 0)">
    <text x="0" y="80" class="title-green">{max_streak} Days</text>
    <text x="0" y="118" class="lbl-main">Longest Streak</text>
    <text x="0" y="144" class="lbl-sub">{longest_str}</text>
  </g>
</svg>
'''

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Generated custom ring dial {OUTPUT_PATH}!")

if __name__ == "__main__":
    generate_minimal_streak_card()
