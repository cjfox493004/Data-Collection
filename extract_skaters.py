#!/usr/bin/env python3
import re
from pathlib import Path

html = Path('stats_page.html').read_text(encoding='utf-8')

# Extract the Individual Overall Skaters section
m = re.search(r'<section id="individual-overall-skaters">(.*?)<!-- \/Individual - Overall - Skaters -->', html, re.S)
if not m:
    raise SystemExit('Skaters section not found')
sec = m.group(1)

# Find all table rows
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', sec, re.S)

def cells_from_tr(tr_html):
    # mark cell boundaries then strip tags
    s = tr_html.replace('</td>', '|||').replace('</th>', '|||')
    # remove any remaining tags
    s = re.sub(r'<[^>]+>', '', s)
    parts = [p.strip() for p in s.split('|||') if p.strip()]
    return parts

out_lines = []
for r in rows:
    parts = cells_from_tr(r)
    if not parts:
        continue
    # skip header rows that contain 'Player' or 'Statistic'
    if any('Player' in p or 'Statistic' in p or 'GP' == p for p in parts[:3]):
        continue
    out_lines.append(parts)

# Write a CSV-like preview (comma-separated) with minimal cleaning
out = Path('skaters_extracted.csv')
with out.open('w', encoding='utf-8') as f:
    for parts in out_lines:
        # join with commas, quote fields that contain commas
        safe = [('"' + p.replace('"', '""') + '"') if ',' in p or ' ' in p else p for p in parts]
        f.write(','.join(safe) + '\n')

print(f'Wrote {len(out_lines)} rows to skaters_extracted.csv')
