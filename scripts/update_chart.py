import urllib.request
import re
import sys
import os

USERNAME = "vishvjeettanwar1623"

def get_chart_svg():
    url = f"https://github.com/users/{USERNAME}/contributions"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    
    with urllib.request.urlopen(req) as response:
        html_res = response.read().decode('utf-8')

    rect_pattern = re.compile(r'data-date="([^"]+)"[^>]*data-level="(\d+)"')
    matches = rect_pattern.findall(html_res)

    color_map = {
        "0": "#161b22",
        "1": "#0e4429",
        "2": "#006d32",
        "3": "#26a641",
        "4": "#39d353"
    }

    cells_svg = []

    for idx, (date_str, level_str) in enumerate(matches):
        col = idx // 7
        row = idx % 7
        
        x = 50 + (col * 12)
        y = 28 + (row * 12)

        delay = (col * 0.02) + (row * 0.03)
        dark_fill = color_map.get(level_str, "#161b22")
        
        cell_element = f'  <rect class="zoom-cell" style="fill:{dark_fill}; animation-delay: {delay:.2f}s;" data-date="{date_str}" data-level="{level_str}" x="{x}" y="{y}" width="10" height="10" rx="2" />'
        cells_svg.append(cell_element)

    svg_output = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 140" width="100%" height="100%">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&amp;display=swap');
      
      .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 8px; }}
      .label-text {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; fill: #8b949e; }}

      .zoom-cell {{
        opacity: 0;
        transform-box: fill-box;
        transform-origin: center;
        animation: zoomIn 0.8s cubic-bezier(0.215, 0.610, 0.355, 1.000) forwards;
      }}

      @keyframes zoomIn {{
        0% {{
          opacity: 0;
          transform: scale3d(0.3, 0.3, 0.3);
        }}
        50% {{
          opacity: 1;
        }}
        100% {{
          opacity: 1;
          transform: scale3d(1, 1, 1);
        }}
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect class="bg" width="720" height="140" rx="8" />

  <!-- Month Labels -->
  <g class="label-text" transform="translate(50, 20)">
    <text x="0">Aug</text><text x="50">Sep</text><text x="100">Oct</text>
    <text x="150">Nov</text><text x="250">Jan</text><text x="350">Mar</text>
    <text x="450">May</text><text x="550">Jul</text><text x="600">Aug</text>
  </g>

  <!-- Weekday Labels -->
  <g class="label-text" transform="translate(25, 25)">
    <text y="24">Mon</text>
    <text y="48">Wed</text>
    <text y="72">Fri</text>
  </g>

  <!-- Contribution Squares with animate__zoomIn -->
  <g>
{chr(10).join(cells_svg)}
  </g>

  <!-- Legend -->
  <g class="label-text" transform="translate(520, 122)">
    <text x="0" y="9">Less</text>
    <rect x="30" y="0" width="10" height="10" rx="2" fill="#161b22" />
    <rect x="44" y="0" width="10" height="10" rx="2" fill="#0e4429" />
    <rect x="58" y="0" width="10" height="10" rx="2" fill="#006d32" />
    <rect x="72" y="0" width="10" height="10" rx="2" fill="#26a641" />
    <rect x="86" y="0" width="10" height="10" rx="2" fill="#39d353" />
    <text x="102" y="9">More</text>
  </g>
</svg>
'''
    return svg_output

if __name__ == "__main__":
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "contribution_zoomin.svg")
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(get_chart_svg())
    except Exception:
        sys.stdout.write(get_chart_svg())
