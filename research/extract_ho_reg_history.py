#!/usr/bin/env python3
"""Extract supported asylum by local authority from every Home Office Reg_02 vintage.

Standard library only. Reads the pinned 'Regional and local authority data - Immigration
groups' files (31 March 2023 to 30 June 2026) and the Asy_D11 dataset from research/raw/, and
the code lookup from research/asylum/. Writes, in research/asylum/:

  ho-reg-supported-asylum-history.csv  one row per Reg_02 local-authority row per vintage
  reg-history-report.json              reconciliation and code-coverage results

Checks (reported, not forced to agree):
  1. Reg_02 supported-asylum total per LA vs Asy_D11 (year ending June 2026 release) for the same
     quarter-end. Reg_02 is a point-in-time extract; Asy_D11 is revised, so differences would be
     reported as revisions. The 31 March 2023 vintage counts accommodated people only (no
     subsistence-only column), so it is compared with Asy_D11 excluding Subsistence Only.
  2. Reg_02 dispersal column vs Asy_D11 'Dispersal Accommodation' for the same quarter-end.
  3. Every LAD code in Reg_02 (all vintages) and in Asy_D11 from 31 March 2022 is either in
     research/asylum/la-lookup.csv (current codes) or an old_code in la-code-changes.csv.

The Home Office publishes no supported-asylum rate per 10,000 in any Reg_02 vintage, so
rate_per_10000_published is always blank. The published percentage covers all three
immigration groups combined and is kept verbatim for reference only.

Usage: python3 research/extract_ho_reg_history.py
Exit code 1 only on structural problems (missing file, unexpected header, unmapped code).
"""
import csv
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE
RAW = RESEARCH / 'raw'
ASYLUM = RESEARCH / 'asylum'
D11_FILE = RAW / 'support-local-authority-datasets-jun-2026.xlsx'

# (file, source_id). The June 2026 vintage is registered as ASY-SRC-HO-REG-LA-2026Q2.
VINTAGES = [
    ('regional-and-local-authority-dataset-mar-2023.ods', 'ASY-SRC-HO-REG-LA-2023Q1'),
    ('regional-and-local-authority-dataset-jun-2023.ods', 'ASY-SRC-HO-REG-LA-2023Q2'),
    ('regional-and-local-authority-dataset-sep-2023.ods', 'ASY-SRC-HO-REG-LA-2023Q3'),
    ('regional-and-local-authority-dataset-dec-2023.ods', 'ASY-SRC-HO-REG-LA-2023Q4'),
    ('regional-and-local-authority-dataset-mar-2024.ods', 'ASY-SRC-HO-REG-LA-2024Q1'),
    ('regional-and-local-authority-dataset-jun-24.ods', 'ASY-SRC-HO-REG-LA-2024Q2'),
    ('regional-and-local-authority-dataset-sep-2024.ods', 'ASY-SRC-HO-REG-LA-2024Q3'),
    ('regional-and-local-authority-dataset-dec-2024.ods', 'ASY-SRC-HO-REG-LA-2024Q4'),
    ('regional-and-local-authority-dataset-mar-2025.xlsx', 'ASY-SRC-HO-REG-LA-2025Q1'),
    ('regional-and-local-authority-dataset-jun-2025.ods', 'ASY-SRC-HO-REG-LA-2025Q2'),
    ('regional-and-local-authority-dataset-sep-2025.ods', 'ASY-SRC-HO-REG-LA-2025Q3'),
    ('regional-and-local-authority-dataset-dec-2025.ods', 'ASY-SRC-HO-REG-LA-2025Q4'),
    ('regional-and-local-authority-dataset-mar-2026.ods', 'ASY-SRC-HO-REG-LA-2026Q1'),
    ('regional-and-local-authority-dataset-jun-2026.ods', 'ASY-SRC-HO-REG-LA-2026Q2'),
]

MONTHS = {m: i for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
     'September', 'October', 'November', 'December'], 1)}
SHORT = {k[:3]: v for k, v in MONTHS.items()}
CODE_RE = re.compile(r'[EWSN]\d{8}')

# --------------------------------------------------------------------------- readers

XNS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
       'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def _col(ref):
    n = 0
    for ch in re.match(r'[A-Z]+', ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def xlsx_table(path, sheet):
    z = zipfile.ZipFile(path)
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    target = None
    for s in wb.find('m:sheets', XNS):
        if s.get('name') == sheet:
            target = rels[s.get('{%s}id' % XNS['r'])].lstrip('/')
            target = target if target.startswith('xl/') else 'xl/' + target
    if target is None:
        raise KeyError('%s: sheet %s not found' % (path.name, sheet))
    try:
        shared = [''.join(t.text or '' for t in si.iter('{%s}t' % XNS['m']))
                  for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', XNS)]
    except KeyError:
        shared = []
    rows = []
    for _, el in ET.iterparse(z.open(target)):
        if el.tag != '{%s}row' % XNS['m']:
            continue
        row = {}
        for c in el.findall('{%s}c' % XNS['m']):
            v = c.find('m:v', XNS)
            t = c.get('t')
            if t == 's':
                val = shared[int(v.text)]
            elif t == 'inlineStr':
                val = ''.join(x.text or '' for x in c.iter('{%s}t' % XNS['m']))
            else:
                val = v.text if v is not None and v.text is not None else ''
            row[_col(c.get('r'))] = val
        cells = [row.get(i, '') for i in range(max(row) + 1)] if row else []
        while cells and cells[-1] == '':
            cells.pop()
        if cells:
            rows.append(cells)
        el.clear()
    return rows


ONS = {'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
       'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}
T = '{%s}' % ONS['table']


def ods_tables(path, names):
    root = ET.fromstring(zipfile.ZipFile(path).read('content.xml'))
    out = {}
    for t in root.iter(T + 'table'):
        name = t.get(T + 'name')
        if name not in names:
            continue
        rows = []
        for r in t.iter(T + 'table-row'):
            cells = []
            for c in r:
                if c.tag not in (T + 'table-cell', T + 'covered-table-cell'):
                    continue
                n = int(c.get(T + 'number-columns-repeated', '1'))
                txt = '\n'.join(''.join(p.itertext()) for p in c.findall('{%s}p' % ONS['text']))
                cells.extend([txt] * min(n, 200))
            while cells and cells[-1] == '':
                cells.pop()
            if cells:
                rows.append(cells)
        out[name] = rows
    return out


def load(path):
    if path.suffix == '.xlsx':
        return {n: xlsx_table(path, n) for n in ('Reg_02', 'Notes')}
    return ods_tables(path, {'Reg_02', 'Notes'})


# --------------------------------------------------------------------------- parsing

def parse_count(v):
    """Return (int or None, note). Never converts a marker to zero."""
    s = v.strip()
    if re.fullmatch(r'\d+', s):
        return int(s), ''
    if re.fullmatch(r'\d{1,3}(,\d{3})+', s):
        return int(s.replace(',', '')), ''
    if re.fullmatch(r'\d+\.0+', s):  # xlsx numeric stored as float
        return int(float(s)), ''
    if s == '':
        return None, 'blank cell'
    if s == '*':
        return None, "published as '*' (suppressed, fewer than 5 people)"
    return None, 'published as %r' % s


def find_col(hdr, *patterns, required=True):
    for p in patterns:
        for i, h in enumerate(hdr):
            if re.search(p, h, re.I):
                return i
    if required:
        raise SystemExit('column %r not found in header %r' % (patterns, hdr))
    return None


def vintage_date(title):
    m = re.search(r'as at (\d{1,2}) (\w+) (\d{4})', title)
    return '%s-%02d-%02d' % (m.group(3), MONTHS[m.group(2)], int(m.group(1)))


def extract_vintage(fname, source_id):
    path = RAW / fname
    tables = load(path)
    reg, notes = tables['Reg_02'], tables['Notes']
    date = vintage_date(reg[0][0])
    hdr = [h.strip() for h in reg[1]]
    ix = {
        'name': find_col(hdr, r'^Local authority$'),
        'region': find_col(hdr, r'^Region / Nation$'),
        'code': find_col(hdr, r'^LTLA \(ONS code\)$'),
        'total': find_col(hdr, r'^Supported Asylum \(total\)'),
        'initial': find_col(hdr, r'Supported Asylum - Initial', required=False),
        'dispersal': find_col(hdr, r'Supported Asylum - Dispers(al|ed)', required=False),
        'contingency': find_col(hdr, r'Supported Asylum - Contingency', required=False),
        'other': find_col(hdr, r'Supported Asylum - Other', required=False),
        'subsistence': find_col(hdr, r'Subsistence only', required=False),
        'population': find_col(hdr, r'^Population$'),
        'pct': find_col(hdr, r'^Per capita \(%\)$', r'^Percentage of population \(%\)$'),
    }
    # Population-source notes appear as 'Source for the mid-year ...' (2025+ vintages, note text
    # in its own cell) or '1. Source for the mid-year ...' (2024 vintages, numbered in one cell).
    src_re = re.compile(r'^(?:\d+\.\s*)?Source for the mid-year', re.I)
    pop_notes = []
    for r in notes:
        for c in r[:3]:
            if src_re.search(c.strip()):
                pop_notes.append(re.sub(r'\s+', ' ', re.sub(r'^\d+\.\s*', '', c.strip())))
                break
    pop_stated = ' | '.join(pop_notes) if pop_notes else 'not stated in this vintage (no population-source note on the Notes sheet)'
    out = []
    for r in reg[2:]:
        if not r or not r[0].strip() or r[0].strip() == 'End of table':
            continue
        r = r + [''] * (len(hdr) - len(r))
        notes_row = []
        vals = {}
        for k in ('total', 'initial', 'dispersal', 'contingency', 'other', 'subsistence', 'population'):
            if ix[k] is None:
                vals[k] = ''
                if k != 'population':
                    notes_row.append('%s: column not published in this vintage' % k)
                continue
            v, n = parse_count(r[ix[k]])
            vals[k] = '' if v is None else v
            if n:
                notes_row.append('%s: %s' % (k, n))
        pct_raw = r[ix['pct']].strip()
        if pct_raw and not pct_raw.endswith('%') and re.fullmatch(r'[\d.Ee+-]+', pct_raw):
            notes_row.append('percentage stored as a numeric fraction in the xlsx; kept as published')
        code = r[ix['code']].strip()
        code_out = code if CODE_RE.fullmatch(code) else ''
        if not code_out:
            notes_row.append('LTLA code published as %r' % code)
        out.append([date, code_out, r[ix['name']].strip(), r[ix['region']].strip(),
                    vals['total'], vals['initial'], vals['dispersal'], vals['contingency'],
                    vals['other'], vals['subsistence'], vals['population'], pct_raw, hdr[ix['pct']],
                    '', pop_stated, source_id, 'Reg_02', '; '.join(notes_row)])
    return date, out


def d11_by_date():
    """Asy_D11 people by (date, LAD code): total, dispersal and subsistence only."""
    rows = xlsx_table(D11_FILE, 'Data_Asy_D11')
    tot, disp, sub, grand, grand_sub, codes22 = (defaultdict(int), defaultdict(int), defaultdict(int),
                                                  defaultdict(int), defaultdict(int), set())
    for r in rows[2:]:
        if len(r) < 7 or not r[0].strip():
            continue
        d, mon, y = r[0].split()
        date = '%s-%02d-%02d' % (y, SHORT[mon[:3]], int(d))
        n = int(r[6])
        grand[date] += n
        code = r[4] if CODE_RE.fullmatch(r[4]) else 'NONGEO:' + r[3]
        tot[(date, code)] += n
        if r[5] == 'Dispersal Accommodation':
            disp[(date, code)] += n
        if r[5].casefold() == 'subsistence only':
            sub[(date, code)] += n
            grand_sub[date] += n
        if date >= '2022-03-31' and CODE_RE.fullmatch(r[4]):
            codes22.add(r[4])
    return tot, disp, sub, grand, grand_sub, codes22


def main():
    structural_ok = True
    allrows, dates = [], []
    for fname, sid in VINTAGES:
        if not (RAW / fname).exists():
            print('MISSING raw file %s' % fname)
            structural_ok = False
            continue
        date, rows = extract_vintage(fname, sid)
        dates.append(date)
        allrows.extend(rows)
        print('%s %s: %d rows, supported asylum sum %d, population source: %s' % (
            date, fname, len(rows), sum(r[4] for r in rows if r[4] != ''),
            'stated' if not rows[0][14].startswith('not stated') else 'NOT STATED'))
    header = ['date', 'la_code_published', 'la_name_published', 'region_or_nation_published',
              'supported_asylum_seekers', 'initial_accommodation', 'dispersal_accommodation',
              'contingency_accommodation', 'other_accommodation', 'subsistence_only',
              'population_used', 'percentage_of_population_published_all_three_groups',
              'percentage_column_label', 'rate_per_10000_published', 'population_source_stated',
              'source_id', 'source_table', 'notes']
    with open(ASYLUM / 'ho-reg-supported-asylum-history.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header)
        w.writerows(allrows)

    tot, disp, sub, grand, grand_sub, codes22 = d11_by_date()
    # Code lookup built by the geography workstream (ONS CHD). Used to compare a Reg_02 row
    # published under an older code with Asy_D11 published under the successor code.
    lookup = {r['la_code'] for r in csv.DictReader(open(ASYLUM / 'la-lookup.csv', encoding='utf-8'))}
    # old_code -> list of (new_code, new_name). A split (e.g. Barnsley E08000016 -> E08000038 and
    # E08000039) has more than one successor, so keep them all rather than the last one read.
    changes = defaultdict(list)
    for r in csv.DictReader(open(ASYLUM / 'la-code-changes.csv', encoding='utf-8')):
        changes[r['old_code']].append((r['new_code'], r['new_name']))
    reverse = defaultdict(set)
    for old, succ in changes.items():
        for new, _ in succ:
            reverse[new].add(old)

    def d11_value(table, date, code, name=''):
        """Asy_D11 value for a code: same code, else the successor, else predecessors.

        With several successors (a split), use only the successor with the same published name;
        if none matches, do not guess (return 0 with the code unchanged, so it shows as a difference).
        """
        if (date, code) in table:
            return table[(date, code)], code
        succ = [(n, nm) for n, nm in changes.get(code, ()) if (date, n) in table]
        if len(succ) > 1:
            succ = [(n, nm) for n, nm in succ if nm.casefold() == name.casefold()]
        if len(succ) == 1:
            return table[(date, succ[0][0])], succ[0][0]
        preds = [p for p in reverse.get(code, ()) if (date, p) in table]
        if preds:
            return sum(table[(date, p)] for p in preds), '+'.join(sorted(preds))
        return 0, code

    report = {'vintages': [], 'code_coverage': {}}
    print('\nReg_02 vs Asy_D11 (year ending June 2026 release), same quarter-end')
    print('  %-10s %8s %8s %8s  %s' % ('date', 'Reg_02', 'Asy_D11', 'diff', 'LAs differing (total / dispersal); basis'))
    for date in dates:
        rows = [r for r in allrows if r[0] == date]
        # Vintages without a subsistence-only column (31 March 2023) count accommodated people only
        # (that vintage's note: 'in receipt of Home Office accommodation'), so compare like with like.
        no_sub = all('subsistence: column not published' in r[17] for r in rows)
        basis = 'Asy_D11 excluding Subsistence Only' if no_sub else 'Asy_D11 all support'
        d11_total = grand[date] - (grand_sub[date] if no_sub else 0)
        reg_sum = sum(r[4] for r in rows if r[4] != '')
        la_diff, disp_diff, examples, recoded = 0, 0, [], []
        for r in rows:
            if not r[1]:
                continue
            v, used = d11_value(tot, date, r[1], r[2])
            if no_sub:
                v -= d11_value(sub, date, r[1], r[2])[0]
            if used != r[1]:
                recoded.append({'reg02_code': r[1], 'la_name': r[2], 'asy_d11_code': used})
            if r[4] != '' and r[4] != v:
                la_diff += 1
                if len(examples) < 5:
                    examples.append({'la_code': r[1], 'la_name': r[2], 'reg02': r[4], 'asy_d11': v})
            if r[6] != '' and r[6] != d11_value(disp, date, r[1], r[2])[0]:
                disp_diff += 1
        print('  %-10s %8d %8d %8d  %d / %d; %s%s' % (date, reg_sum, d11_total, reg_sum - d11_total, la_diff,
                                                    disp_diff, basis, '; recoded %d' % len(recoded) if recoded else ''))
        report['vintages'].append({
            'date': date, 'reg02_rows': len(rows), 'reg02_supported_asylum_sum': reg_sum,
            'comparison_basis': basis, 'asy_d11_total_same_date': grand[date],
            'asy_d11_subsistence_only_same_date': grand_sub[date], 'asy_d11_comparable_total': d11_total,
            'difference': reg_sum - d11_total,
            'local_authorities_total_differs': la_diff, 'local_authorities_dispersal_differs': disp_diff,
            'examples_total_differs': examples, 'codes_compared_via_lookup': recoded,
            'population_source_stated': rows[0][14] if rows else ''})

    reg_codes_all = {r[1] for r in allrows if r[1]}
    unmapped_reg = sorted(c for c in reg_codes_all if c not in lookup and c not in changes)
    unmapped_d11 = sorted(c for c in codes22 if c not in lookup and c not in changes)
    report['code_coverage'] = {
        'lookup_file': 'asylum/la-lookup.csv', 'changes_file': 'asylum/la-code-changes.csv',
        'current_codes_in_lookup': len(lookup), 'reg02_codes_all_vintages': len(reg_codes_all),
        'reg02_codes_not_current': sorted(c for c in reg_codes_all if c not in lookup),
        'reg02_codes_unmapped': unmapped_reg,
        'asy_d11_codes_from_2022': len(codes22), 'asy_d11_codes_from_2022_unmapped': unmapped_d11}
    print('\nCode coverage: Reg_02 codes not current: %s; unmapped: %s; Asy_D11 (2022+) unmapped: %s' % (
        report['code_coverage']['reg02_codes_not_current'], unmapped_reg, unmapped_d11))
    if unmapped_reg or unmapped_d11:
        structural_ok = False
    with open(ASYLUM / 'reg-history-report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print('\nRESULT: %s' % ('structural checks passed' if structural_ok else 'STRUCTURAL CHECKS FAILED'))
    return 0 if structural_ok else 1


if __name__ == '__main__':
    sys.exit(main())
