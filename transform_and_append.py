#!/usr/bin/env python3
import csv
from pathlib import Path

infile = Path('skaters_extracted.csv')
if not infile.exists():
    raise SystemExit('skaters_extracted.csv not found')

rows = []
with infile.open(encoding='utf-8') as f:
    reader = csv.reader(f)
    # skip any header lines in extracted file if present
    first = next(reader)
    # detect header like starting with 'G' or 'Player'
    if any(h.lower().startswith('g') and 'pts' in ''.join(first).lower() for h in first):
        pass
    else:
        # not a header, include it
        rows.append(first)
    for r in reader:
        rows.append(r)

out_lines = []
for r in rows:
    if not r:
        continue
    # ensure we have at least 22 fields (including bio)
    # pad with empty strings if needed
    while len(r) < 22:
        r.append('')

    # clean player name: take first non-empty line and strip
    name = r[1].splitlines()[0].strip()

    # mapping according to observed order in skaters_extracted.csv
    jersey = r[0].strip()
    gp = r[2].strip()
    g = r[3].strip()
    a = r[4].strip()
    pts = r[5].strip()
    sh = r[6].strip()
    shp = r[7].strip()
    plusminus = r[8].strip()
    ppg = r[9].strip()
    shg = r[10].strip()
    fg = r[11].strip()
    gwg = r[12].strip()
    gtg = r[13].strip()
    otg = r[14].strip()
    htg = r[15].strip()
    uag = r[16].strip()
    pn_pim = r[17].strip()
    minutes = r[18].strip()
    maj = r[19].strip()
    oth = r[20].strip()
    blk = r[21].strip()

    ordered = [jersey, name, gp, blk, g, a, pts, sh, shp, plusminus, ppg, shg, fg, gwg, gtg, otg, htg, uag, pn_pim, minutes, maj, oth]
    out_lines.append(ordered)

dst = Path('stats.csv')
if not dst.exists():
    raise SystemExit('stats.csv missing')

# Append rows to stats.csv
with dst.open('a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for row in out_lines:
        writer.writerow(row)

print(f'Appended {len(out_lines)} rows to stats.csv')
