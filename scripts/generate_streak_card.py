import urllib.request
import re
import os
from datetime import datetime

USERNAME = "vishvjeettanwar1623"
OUTPUT_PATH = "assets/streak_card.svg"

def generate_streak_card():
    url = f"https://ghchart.rshah.org/{USERNAME}"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    
    html_res = urllib.request.urlopen(req).read().decode('utf-8')

    rect_pattern = re.compile(r'data-score="(\d+)" data-date="([^"]+)"')
    matches = rect_pattern.findall(html_res)

    if not matches:
        print("No contribution data found.")
        return

    contributions = []
    total_contributions = 0

    for score_str, date_str in matches:
        score = int(score_str)
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        contributions.append((dt, score))
        total_contributions += score

    contributions.sort(key=lambda x: x[0])

    start_date_str = contributions[0][0].strftime("%b %d, %Y")
    end_date_str = "Present"

    # Calculate longest streak
    max_streak = 0
    curr_streak_calc = 0
    longest_start = None
    longest_end = None

    temp_start = None

    for dt, score in contributions:
        if score > 0:
            if curr_streak_calc == 0:
                temp_start = dt
            curr_streak_calc += 1
            if curr_streak_calc > max_streak:
                max_streak = curr_streak_calc
                longest_start = temp_start
                longest_end = dt
        else:
            curr_streak_calc = 0

    # Calculate current active streak from latest date
    active_streak = 0
    active_start = None
    active_end = None

    rev_contribs = list(reversed(contributions))
    
    if rev_contribs:
        latest_dt, latest_score = rev_contribs[0]
        if latest_score > 0 or (len(rev_contribs) > 1 and rev_contribs[1][1] > 0):
            in_streak = False
            for dt, score in rev_contribs:
                if score > 0:
                    if not in_streak:
                        in_streak = True
                        active_end = dt
                    active_streak += 1
                    active_start = dt
                elif in_streak:
                    break

    longest_str = f"{longest_start.strftime('%b %d')} - {longest_end.strftime('%b %d')}" if longest_start and longest_end else "N/A"
    active_str = f"{active_start.strftime('%b %d')} - {active_end.strftime('%b %d')}" if active_start and active_end else "Recent"

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 195" width="100%" height="100%">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;display=swap');
      .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 8px; }}
      .title {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 34px; fill: #ffffff; text-anchor: middle; }}
      .subtitle {{ font-family: 'JetBrains Mono', monospace; font-weight: 400; font-size: 14px; fill: #8b949e; text-anchor: middle; }}
      .label-orange {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 15px; fill: #f78166; text-anchor: middle; }}
      .divider {{ stroke: #58a6ff; stroke-width: 1px; opacity: 0.6; }}
      .ring {{ fill: none; stroke: #58a6ff; stroke-width: 4.5px; }}
    </style>
  </defs>

  <!-- Background -->
  <rect class="bg" width="720" height="195" rx="8" />

  <!-- Total Contributions Column -->
  <g transform="translate(120, 0)">
    <text x="0" y="82" class="title">{total_contributions}</text>
    <text x="0" y="118" class="subtitle">Total Contributions</text>
    <text x="0" y="148" class="subtitle" font-size="12px">{start_date_str} - {end_date_str}</text>
  </g>

  <!-- Divider 1 -->
  <line x1="240" y1="35" x2="240" y2="160" class="divider" />

  <!-- Current Streak Column -->
  <g transform="translate(360, 0)">
    <circle cx="0" cy="72" r="32" class="ring" />
    <path d="M 360,52 C 354,60 350,65 354,73 C 356,77 360,80 364,74 C 366,71 366,67 364,65 C 368,69 370,74 367,78 C 364,82 357,84 353,79 C 349,74 352,65 360,52 Z" fill="#f78166" transform="translate(-360, -66)" />
    <text x="0" y="79" class="title" font-size="28px">{active_streak}</text>
    
    <text x="0" y="124" class="label-orange">Current Streak</text>
    <text x="0" y="152" class="subtitle" font-size="12px">{active_str}</text>
  </g>

  <!-- Divider 2 -->
  <line x1="480" y1="35" x2="480" y2="160" class="divider" />

  <!-- Longest Streak Column -->
  <g transform="translate(600, 0)">
    <text x="0" y="82" class="title">{max_streak}</text>
    <text x="0" y="118" class="subtitle">Longest Streak</text>
    <text x="0" y="148" class="subtitle" font-size="12px">{longest_str}</text>
  </g>
</svg>
'''

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated {OUTPUT_PATH}!")

if __name__ == "__main__":
    generate_streak_card()
