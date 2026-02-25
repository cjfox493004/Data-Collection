#!/usr/bin/env python3
import csv
from pathlib import Path

src = Path('stats.csv')
dst = Path('stats_new.csv')
if not src.exists():
    raise SystemExit('stats.csv not found')

with src.open(newline='', encoding='utf-8') as f_in, dst.open('w', newline='', encoding='utf-8') as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    rows = list(reader)
    if not rows:
        raise SystemExit('empty file')
    header = rows[0]
    # normalize header names
    header = [h.strip() for h in header]
    # find index of Player
    try:
        pidx = header.index('Player')
    except ValueError:
        raise SystemExit('Player column not found')

    # build new header: replace Player with First_Name,Last_Name
    new_header = []
    for i, h in enumerate(header):
        if i == pidx:
            new_header.extend(['First_Name', 'Last_Name'])
        else:
            new_header.append(h)
    writer.writerow(new_header)

    # process data rows
    for r in rows[1:]:
        # pad row to header length if short
        while len(r) < len(header):
            r.append('')
        player = r[pidx].strip()
        first = last = ''
        if player:
            # entries may be "Last, First" or single token like Team or Total
            if ',' in player:
                parts = [p.strip() for p in player.split(',', 1)]
                last = parts[0]
                first = parts[1]
            else:
                # no comma: treat as First_Name only
                first = player
        # build new row
        new_row = []
        for i, cell in enumerate(r):
            if i == pidx:
                new_row.append(first)
                new_row.append(last)
            else:
                new_row.append(cell)
        writer.writerow(new_row)

print('Wrote', dst.name)
