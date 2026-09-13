"""Build a small, source-linked MVP dataset without changing the research registry.

The user authorized an MVP before independent research review on 11 September 2026.
Only checked numeric records are exposed. Research review status is preserved.
"""
import csv
import json
import sys
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sources = json.loads((ROOT / 'research/sources.json').read_text())['sources']
source = next(s for s in sources if s['id'] == 'HO-TABLES-2026Q2')
records = []
for row in csv.DictReader((ROOT / 'research/crossings/annual-crossings.csv').open()):
    if row['year'] == '2026':
        continue  # The MVP uses the later, separately labelled operational snapshot.
    people, boats = int(row['people']), int(row['boats'])
    assert people >= 0 and boats > 0
    assert abs(people / boats - float(row['average_people_per_boat'])) < 0.000001
    records.append({
        'year': int(row['year']), 'people': people, 'boats': boats,
        'periodStart': row['period_start'], 'periodEnd': row['period_end'],
        'partial': False, 'provisional': False, 'sourceId': source['id'],
        'claimId': 'ANNUAL-' + row['year'],
    })
snapshot = json.loads((ROOT / 'research/mvp-2026-snapshot.json').read_text())
ns = {'t': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0', 'x': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}
with ZipFile(ROOT / 'research/raw/small-boats-2026-09-04.ods') as book:
    tree = ET.fromstring(book.read('content.xml'))
table = next(t for t in tree.findall('.//t:table', ns) if t.get('{' + ns['t'] + '}name') == 'SB_01')
daily = []
for row in table.findall('t:table-row', ns):
    cells = [' '.join(''.join(p.itertext()) for p in c.findall('.//x:p', ns)) for c in row.findall('t:table-cell', ns)]
    if cells and cells[0].endswith('/2026'):
        daily.append(cells)
assert len(daily) == 246 and daily[0][0] == '01/01/2026' and daily[-1][0] == '03/09/2026'
assert sum(int(row[1].replace(',', '')) for row in daily) == snapshot['record']['people']
assert sum(int(row[2].replace(',', '')) for row in daily) == snapshot['record']['boats']
records.append(snapshot['record'])
assert [r['year'] for r in records] == list(range(2018, 2027))
output = {
    'updatedAt': '2026-09-11',
    'reviewStatus': 'Source-checked MVP; independent research review pending',
    'records': records,
    'sources': [{
        'id': source['id'], 'title': source['title'], 'publisher': source['publisher'],
        'url': source['url'], 'publishedAt': source['publication_date'],
        'table': 'IER_02a', 'note': 'Official annual counts, subject to revisions. Average occupancy is calculated as people divided by boats.',
    }, snapshot['source']],
}
target = ROOT / 'src/data/crossings.json'
text = json.dumps(output, indent=2) + '\n'
if '--check' in sys.argv:
    assert target.read_text() == text, 'Application data is stale. Run yarn data:build.'
    print('PASS: source-linked application data matches research inputs.')
else:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    print('Generated', target.relative_to(ROOT))
