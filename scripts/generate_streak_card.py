import urllib.request
import re
import sys
import os
from datetime import datetime

USERNAME = "vishvjeettanwar1623"

def get_streak_svg():
    url = f"https://github.com/users/{USERNAME}/contributions"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    
    with urllib.request.urlopen(req) as response:
        html_res = response.read().decode('utf-8')

    header_match = re.search(r'([\d,]+)\s+contributions', html_res, re.IGNORECASE)
    total_contribs = 502
    if header_match:
        total_contribs = int(header_match.group(1).replace(',', ''))

    tbody_match = re.search(r'<tbody>(.*?)</tbody>', html_res, re.DOTALL)
    cell_list = []
    if tbody_match:
        tbody_html = tbody_match.group(1)
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbody_html, re.DOTALL)
        for r_html in rows:
            cell_matches = re.findall(r'data-date="([^"]+)"[^>]*data-level="(\d+)"', r_html)
            if not cell_matches:
                cell_matches = re.findall(r'data-level="(\d+)"[^>]*data-date="([^"]+)"', r_html)
                cell_matches = [(d, l) for l, d in cell_matches]
            cell_list.extend(cell_matches)
    
    if not cell_list:
        rect_pattern = re.compile(r'data-date="([^"]+)"[^>]*data-level="(\d+)"')
        cell_list = rect_pattern.findall(html_res)

    contributions = []
    for date_str, level_str in cell_list:
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
