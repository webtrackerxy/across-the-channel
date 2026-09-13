#!/usr/bin/env python3
"""Extract Home Office asylum support statistics (year ending June 2026 release).

Standard library only. Reads pinned raw files in research/raw/ and writes:

  asylum-support-long.csv      Asy_D11 (by local authority), one row per published cell
  asylum-support-national.csv  Asy_D09 aggregated to date x support type x accommodation type
  ho-rates-per-10000.csv       Reg_02 supported asylum by local authority, with HO population

and prints reconciliation checks:
  * Asy_D11 sum per quarter vs Asy_D09 national total per quarter
  * Asy_D11 and Asy_D09 by support type vs summary table Asy_09a (where Asy_09a publishes the quarter)
  * Asy_D11 30 June 2026 by LA vs Reg_02 supported asylum by LA, and Reg_02 UK total

Usage:  python3 research/extract_asylum_support.py
Exit code 1 if a reconciliation check fails.
"""
import csv
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE
OUT = RESEARCH / 'asylum'
RAW = RESEARCH / 'raw'

D11_FILE = RAW / 'support-local-authority-datasets-jun-2026.xlsx'
D09_FILE = RAW / 'asylum-seekers-receipt-support-datasets-jun-2026.xlsx'
SUMMARY_FILE = RAW / 'asylum-summary-jun-2026-tables.ods'
REG_FILE = RAW / 'regional-and-local-authority-dataset-jun-2026.ods'

D11_SOURCE = 'ASY-SRC-HO-D11-2026Q2'
D09_SOURCE = 'ASY-SRC-HO-D09-2026Q2'
SUMMARY_SOURCE = 'ASY-SRC-HO-ASY-SUMMARY-2026Q2'
REG_SOURCE = 'ASY-SRC-HO-REG-LA-2026Q2'

EARLIEST_REQUIRED = '2022-03-31'
LATEST_REQUIRED = '2026-06-30'

MONTHS = {m: i for i, m in enumerate(
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 1)}

# --------------------------------------------------------------------------- XLSX

XNS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
       'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def _col_index(ref):
    n = 0
    for ch in re.match(r'[A-Z]+', ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def xlsx_rows(path, sheet_name):
    """Yield rows (list of str) from a named worksheet, streaming."""
    z = zipfile.ZipFile(path)
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    rmap = {r.get('Id'): r.get('Target') for r in rels}
    target = None
    for s in wb.find('m:sheets', XNS):
        if s.get('name') == sheet_name:
            target = rmap[s.get('{%s}id' % XNS['r'])].lstrip('/')
            if not target.startswith('xl/'):
                target = 'xl/' + target
    if target is None:
        raise KeyError('sheet %r not found in %s' % (sheet_name, path.name))
    try:
        sroot = ET.fromstring(z.read('xl/sharedStrings.xml'))
        shared = [''.join(t.text or '' for t in si.iter('{%s}t' % XNS['m']))
                  for si in sroot.findall('m:si', XNS)]
    except KeyError:
        shared = []
    tag_row, tag_c = '{%s}row' % XNS['m'], '{%s}c' % XNS['m']
    for _, el in ET.iterparse(z.open(target)):
        if el.tag != tag_row:
            continue
        row = {}
        for c in el.findall(tag_c):
            t = c.get('t')
            v = c.find('m:v', XNS)
            if t == 's':
                val = shared[int(v.text)]
            elif t == 'inlineStr':
                val = ''.join(x.text or '' for x in c.iter('{%s}t' % XNS['m']))
            else:
                val = v.text if v is not None and v.text is not None else ''
            row[_col_index(c.get('r'))] = val
        yield [row.get(i, '') for i in range(max(row) + 1)] if row else []
        el.clear()


# --------------------------------------------------------------------------- ODS

ONS = {'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
       'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}
T = '{%s}' % ONS['table']


def ods_table(path, name):
    """Return rows (list of str, trailing blanks trimmed) from a named ODS table."""
    root = ET.fromstring(zipfile.ZipFile(path).read('content.xml'))
    for t in root.iter(T + 'table'):
        if t.get(T + 'name') != name:
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
        return rows
    raise KeyError('table %r not found in %s' % (name, path.name))


# --------------------------------------------------------------------------- helpers

def iso_date(label):
    """'31 Mar 2022' -> '2022-03-31'."""
    d, m, y = label.strip().split()
    return '%s-%02d-%02d' % (y, MONTHS[m[:3]], int(d))


def parse_count(value):
    """Return (int or None, note). Blank/marker values are never turned into zero."""
    v = value.strip()
    if re.fullmatch(r'-?\d+', v):
        return int(v), ''
    if re.fullmatch(r'-?\d{1,3}(,\d{3})+', v):
        return int(v.replace(',', '')), ''
    if v == '':
        return None, 'blank cell in source'
    return None, 'non-numeric value published as %r' % v


def write_csv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header)
        w.writerows(rows)


def na_note(la_name, region, code, accom):
    notes = []
    # Coverage labels look like 'N/A - Section 98 (pre-Dec 2022)'. A bare 'N/A' LAD code on
    # 'Unknown' rows is not a coverage label and is reported separately below.
    for label in {la_name, region, code, accom}:
        if label.startswith('N/A - '):
            notes.append('published as %r: no local-authority breakdown for this group in this period '
                         '(Asy_D11 notes 14-16)' % label)
    if la_name == 'Unknown':
        notes.append("local authority published as 'Unknown'; LAD code published as %r" % code)
    return '; '.join(sorted(notes))


# --------------------------------------------------------------------------- extraction

def extract_d11():
    rows = list(xlsx_rows(D11_FILE, 'Data_Asy_D11'))
    title, header = rows[0], rows[1]
    expected = ['Date (as at…)', 'Support Type', 'UK Region / Nation', 'Local Authority',
                'LAD Code', 'Accommodation Type', 'People']
    if header[:7] != expected:
        raise SystemExit('Unexpected Asy_D11 header: %r' % header)
    out = []
    for i, r in enumerate(rows[2:], start=3):
        r = (r + [''] * 7)[:max(7, len(r))]
        extra = [x for x in r[7:] if x.strip()]
        if extra:
            raise SystemExit('Unexpected content beyond People column at row %d: %r' % (i, r))
        date, support, region, la, code, accom, people_raw = r[:7]
        if not date.strip():
            continue
        people, pnote = parse_count(people_raw)
        notes = [n for n in (pnote, na_note(la, region, code, accom)) if n]
        code_out = code if re.fullmatch(r'[EWSN]\d{8}', code) else ''
        if code and not code_out and code not in (la,) and la != 'Unknown':
            notes.append('LAD code cell published as %r' % code)
        out.append([iso_date(date), code_out, la, region, support, accom,
                    '' if people is None else people, D11_SOURCE,
                    'Data_Asy_D11 (row %d)' % i, '; '.join(notes)])
    return title[0], out


def extract_d09():
    agg = defaultdict(int)
    blanks = defaultdict(int)
    for i, r in enumerate(xlsx_rows(D09_FILE, 'Data_Asy_D09')):
        if i == 1 and r[:7] != ['Date (as at…)', 'Nationality', 'Region', 'Support Type',
                                'Accommodation Type', 'UK Region / Nation', 'People']:
            raise SystemExit('Unexpected Asy_D09 header: %r' % r)
        if i < 2 or not r or not r[0].strip():
            continue
        people, _ = parse_count(r[6] if len(r) > 6 else '')
        key = (iso_date(r[0]), r[3], r[4])
        if people is None:
            blanks[key] += 1
        else:
            agg[key] += people
    if blanks:
        raise SystemExit('Asy_D09 has non-numeric People cells: %r' % dict(blanks))
    out = [[d, s, a, v, D09_SOURCE, 'Data_Asy_D09 (summed over Nationality, Region and UK Region / Nation)']
           for (d, s, a), v in sorted(agg.items())]
    return agg, out


def extract_asy09a():
    rows = ods_table(SUMMARY_FILE, 'Asy_09a')
    hdr = next(r for r in rows if r and r[0].startswith('As at the end of'))
    res = {}
    for r in rows:
        if r and r[0] in ('Section 95', 'Section 4', 'Section 98'):
            for label, v in zip(hdr[1:], r[1:]):
                m = re.fullmatch(r'(Mar|Jun|Sep|Dec) (\d{4})', label)
                if not m:
                    continue
                day = {'Mar': 31, 'Jun': 30, 'Sep': 30, 'Dec': 31}[m.group(1)]
                val, _ = parse_count(v)
                res[(iso_date('%d %s %s' % (day, m.group(1), m.group(2))), r[0])] = val
    return res


def extract_reg02():
    rows = ods_table(REG_FILE, 'Reg_02')
    title = rows[0][0]
    m = re.search(r'as at (\d{1,2} \w+ \d{4})', title)
    d, mon, y = m.group(1).split()
    date = iso_date('%s %s %s' % (d, mon[:3], y))
    hdr = rows[1]
    ix = {h: i for i, h in enumerate(hdr)}
    need = ['Local authority', 'Region / Nation', 'LTLA (ONS code)',
            'Supported Asylum (total) (population)', 'Population', 'Percentage of population (%)']
    for n in need:
        if n not in ix:
            raise SystemExit('Reg_02 column missing: %r' % n)
    rate_cols = [h for h in hdr if '10,000' in h or '10000' in h]
    notes = ods_table(REG_FILE, 'Notes')
    pop_notes = [r[1] for r in notes if len(r) > 1 and 'population estimates' in r[1]]
    pop_stated = ' | '.join(pop_notes)
    out = []
    for r in rows[2:]:
        r = r + [''] * (len(hdr) - len(r))
        name, code = r[ix['Local authority']], r[ix['LTLA (ONS code)']]
        sa, _ = parse_count(r[ix['Supported Asylum (total) (population)']])
        pop, _ = parse_count(r[ix['Population']])
        rate = ''
        if rate_cols:
            rate = r[ix[rate_cols[0]]]
        out.append([date, code if re.fullmatch(r'[EWSN]\d{8}', code) else '', name,
                    '' if sa is None else sa, '' if pop is None else pop, rate, pop_stated,
                    REG_SOURCE, 'Reg_02'])
    uk = next(r for r in ods_table(REG_FILE, 'Reg_01') if r[0] == 'United Kingdom - total')
    reg01_hdr = ods_table(REG_FILE, 'Reg_01')[1]
    uk_sa = parse_count(uk[reg01_hdr.index('Supported Asylum (population)')])[0]
    return date, out, rate_cols, uk_sa


# --------------------------------------------------------------------------- main

def main():
    ok = True
    title, d11 = extract_d11()
    write_csv(OUT / 'asylum-support-long.csv',
              ['date', 'la_code_published', 'la_name_published', 'region_or_nation_published',
               'support_type', 'accommodation_type', 'people', 'source_id', 'source_table', 'notes'],
              d11)
    dates = sorted({r[0] for r in d11})
    print('Asy_D11: %d rows, %d quarter-ends %s to %s' % (len(d11), len(dates), dates[0], dates[-1]))
    print('  blank people cells: %d' % sum(1 for r in d11 if r[6] == ''))

    # every quarter-end required must be present
    for y in range(2022, 2027):
        for md in ('03-31', '06-30', '09-30', '12-31'):
            q = '%d-%s' % (y, md)
            if EARLIEST_REQUIRED <= q <= LATEST_REQUIRED and q not in dates:
                print('  MISSING quarter %s' % q)
                ok = False

    nat_agg, d09 = extract_d09()
    write_csv(OUT / 'asylum-support-national.csv',
              ['date', 'support_type', 'accommodation_type', 'people', 'source_id', 'source_table'],
              [r[:5] + [r[5]] for r in d09])
    print('Asy_D09 national aggregate: %d rows' % len(d09))

    # Reconciliation 1: LA sum vs national per quarter
    la_sum = defaultdict(int)
    la_by = defaultdict(int)
    for r in d11:
        if r[6] != '':
            la_sum[r[0]] += r[6]
            la_by[(r[0], r[4], r[5])] += r[6]
    nat_sum = defaultdict(int)
    for (d, s, a), v in nat_agg.items():
        nat_sum[d] += v
    print('\nReconciliation: Asy_D11 local-authority sum vs Asy_D09 national total')
    print('  %-10s %10s %10s %8s' % ('date', 'LA_sum', 'national', 'diff'))
    cell_diffs = 0
    for d in sorted(set(la_sum) | set(nat_sum)):
        diff = la_sum[d] - nat_sum[d]
        print('  %-10s %10d %10d %8d' % (d, la_sum[d], nat_sum[d], diff))
        if diff:
            ok = False
    # Cell-level comparison. Published labels are kept verbatim in the CSVs, but the two
    # datasets capitalise some labels differently (e.g. 'Subsistence only' in Asy_D11 at
    # 31 Dec 2022 vs 'Subsistence Only' in Asy_D09), so compare on a case-folded key here.
    def fold(d):
        out = defaultdict(int)
        for (dd, s, a), v in d.items():
            out[(dd, s.casefold(), a.casefold())] += v
        return out
    la_f, nat_f = fold(la_by), fold(nat_agg)
    for k in sorted(set(la_f) | set(nat_f)):
        if la_f.get(k, 0) != nat_f.get(k, 0):
            cell_diffs += 1
            if cell_diffs <= 10:
                print('  cell difference %r: LA %d vs national %d' % (k, la_f.get(k, 0), nat_f.get(k, 0)))
    variants = sorted({(k[0], k[1], k[2]) for k in la_by if la_by[k] and k not in nat_agg})
    for v in variants:
        print('  label variant (case only) in Asy_D11 not used in Asy_D09: %r' % (v,))
    print('  support x accommodation cells differing (case-folded labels): %d' % cell_diffs)
    if cell_diffs:
        ok = False

    # Reconciliation 2: by support type vs Asy_09a
    a09 = extract_asy09a()
    print('\nReconciliation: support-type totals vs summary table Asy_09a')
    mism = 0
    detailed_dates = set(nat_sum)
    for (d, s), v in sorted(a09.items()):
        # Asy_09a starts in 2010; the detailed datasets start at 31 Mar 2014. Only compare
        # quarters both publish; ':' (not available) cells parse to None and are skipped.
        if v is None or d not in detailed_dates:
            continue
        la_v = sum(val for (dd, ss, _), val in la_by.items() if dd == d and ss == s)
        nat_v = sum(val for (dd, ss, _), val in nat_agg.items() if dd == d and ss == s)
        flag = '' if la_v == nat_v == v else '  MISMATCH'
        if d >= '2021-12-31' or flag:
            print('  %s %-10s Asy_09a %7d  D09 %7d  D11 %7d%s' % (d, s, v, nat_v, la_v, flag))
        if flag:
            mism += 1
    if mism:
        ok = False

    # Reg_02
    rdate, reg, rate_cols, uk_sa = extract_reg02()
    write_csv(OUT / 'ho-rates-per-10000.csv',
              ['date', 'la_code_published', 'la_name_published', 'supported_asylum_seekers',
               'population_used', 'rate_per_10000_published', 'population_source_stated',
               'source_id', 'source_table'], reg)
    print('\nReg_02 (%s): %d rows; per-10,000 column published: %s' %
          (rdate, len(reg), rate_cols if rate_cols else 'NONE (only an all-pathways percentage)'))
    d11_by_code = defaultdict(int)
    d11_by_name = defaultdict(int)
    for r in d11:
        if r[0] == rdate and r[6] != '':
            d11_by_code[r[1] or r[2]] += r[6]
            d11_by_name[r[2]] += r[6]
    reg_total = sum(r[3] for r in reg if r[3] != '')
    print('  Reg_02 supported asylum sum over rows: %d; Reg_01 UK total: %s; Asy_D11 %s total: %d'
          % (reg_total, uk_sa, rdate, la_sum[rdate]))
    if reg_total != uk_sa or uk_sa != la_sum[rdate]:
        print('  NOTE: totals differ')
    la_mism = []
    for r in reg:
        key = r[1] or r[2]
        v = r[3] if r[3] != '' else 0
        if d11_by_code.get(key, 0) != v:
            la_mism.append((key, r[2], v, d11_by_code.get(key, 0)))
    reg_keys = {r[1] or r[2] for r in reg}
    extra = {k: v for k, v in d11_by_code.items() if k not in reg_keys}
    print('  LAs where Reg_02 != Asy_D11: %d %s' % (len(la_mism), la_mism[:10]))
    print('  Asy_D11 LAs absent from Reg_02: %s' % extra)

    print('\nRESULT: %s' % ('all reconciliation checks passed' if ok else 'CHECKS FAILED'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
