import urllib.request
import re
import os

USERNAME = "vishvjeettanwar1623"
OUTPUT_PATH = "assets/contribution_zoomin.svg"

def generate_chart():
    url = f"https://ghchart.rshah.org/{USERNAME}"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    
    html_res = urllib.request.urlopen(req).read().decode('utf-8')

    rect_pattern = re.compile(r'<rect style="fill:(#.*?);[^"]*" data-score="(\d+)" data-date="([^"]+)" x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"\/>')
    matches = rect_pattern.findall(html_res)

    color_map = {
        "#eeeeee": "#161b22",
        "#c6e48b": "#0e4429",
        "#7bc96f": "#006d32",
        "#239a3b": "#26a641",
        "#196127": "#39d353"
    }

    cells_svg = []

    for idx, (style_fill, score, date_str, x_str, y_str, w_str, h_str) in enumerate(matches):
        x = int(x_str) + 20
        y = int(y_str) + 5
        col = (int(x_str) - 27) // 12
        row = (int(y_str) - 20) // 12
        
        delay = (col * 0.025) + (row * 0.04)
        dark_fill = color_map.get(style_fill, "#161b22")
        
        cell_element = f'  <rect class="zoom-cell" style="fill:{dark_fill}; animation-delay: {delay:.2f}s;" data-date="{date_str}" data-score="{score}" x="{x}" y="{y}" width="10" height="10" rx="2" />'
        cells_svg.append(cell_element)

    svg_output = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 140" width="100%" height="100%">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&amp;display=swap');
      
      .bg {{ fill: #0d1117; }}
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
  <rect class="bg" width="720" height="140" rx="8" stroke="#30363d" stroke-width="1" />

  <!-- Month Labels -->
  <g class="label-text" transform="translate(47, 20)">
    <text x="0">Jul</text><text x="50">Aug</text><text x="100">Sep</text>
    <text x="150">Oct</text><text x="250">Dec</text><text x="350">Feb</text>
    <text x="450">Apr</text><text x="550">Jun</text><text x="600">Jul</text>
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

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_output)

    print(f"Successfully generated {OUTPUT_PATH} with {len(matches)} contribution cells.")

if __name__ == "__main__":
    generate_chart()
