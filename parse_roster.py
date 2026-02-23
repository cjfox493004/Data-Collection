#!/usr/bin/env python3
import re
import csv
import html
import urllib.request
import time

infile = 'roster_page.html'
outfile = 'roster.csv'

with open(infile, 'r', encoding='utf-8') as f:
    data = f.read()

# Find individual player URLs on the roster list page
ids = re.findall(r'roster.aspx\?rp_id=\d+', data)
ids = sorted(set(ids), key=lambda x: int(x.split('=')[1]))
rows = []

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', errors='replace')

for rel in ids:
    url = 'https://hurstathletics.com/' + rel
    try:
        page = fetch(url)
    except Exception:
        time.sleep(1)
        try:
            page = fetch(url)
        except Exception:
            continue

    # Attempt to locate player header block
    parts = page.split('<div class="sidearm-roster-player-header-details')
    if len(parts) < 2:
        continue
    block = '<div class="sidearm-roster-player-header-details' + parts[1]

    # Extract fields
    m = re.search(r'sidearm-roster-player-jersey-number">\s*([0-9]+)', block)
    number = m.group(1).strip() if m else ''

    m = re.search(r'sidearm-roster-player-name [^>]*>\s*<span>([^<]+)</span>\s*<span>([^<]+)</span>', block, re.S)
    first = m.group(1).strip() if m else ''
    last = m.group(2).strip() if m else ''

    pairs = dict(re.findall(r'<dt>([^<:]+):?</dt>\s*<dd>([^<]+)</dd>', block, re.S))

    def clean(x):
        return html.unescape(x.strip()).replace('\n',' ').strip()

    position = clean(pairs.get('Position', ''))
    height = clean(pairs.get('Height', ''))
    weight = clean(pairs.get('Weight', ''))
    classyr = clean(pairs.get('Class', ''))
    hometown = clean(pairs.get('Hometown', ''))
    highschool = clean(pairs.get('High School', ''))

    rows.append({
        'Number': number,
        'First Name': first,
        'Last Name': last,
        'Position': position,
        'Weight': weight,
        'Height': height,
        'Hometown': hometown,
        'Class': classyr,
        'High School': highschool,
    })

    time.sleep(0.2)

# Write CSV (overwrite existing roster.csv)
fieldnames = ['Number','First Name','Last Name','Position','Weight','Height','Hometown','Class','High School']
with open(outfile, 'w', newline='', encoding='utf-8') as csvf:
    w = csv.DictWriter(csvf, fieldnames=fieldnames)
    w.writeheader()
    for r in rows:
        w.writerow(r)

print(f'Wrote {len(rows)} players to {outfile}')
