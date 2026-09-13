#!/usr/bin/env python3
"""Phase 1C scenario build (research-asylum Parts 14-15). Standard library only.

SCENARIOS ARE NOT FORECASTS. Every output here is hypothetical arithmetic on stated
assumptions. Observed inputs are read from the research tree and are never modified.

Inputs (read-only):
  research/crossings/monthly-crossings.csv     IER_02a monthly people and arriving boats
  research/crossings/annual-crossings.csv      IER_02a calendar years
  research/asylum/asylum-support-national.csv  Asy_D09 quarter-end totals
  research/asylum/asylum-support-local-authority.csv  30 June 2026 snapshot, 361 LAs, harmonised
  research/claims.json                         anchor claims (checked, not edited)

Outputs (research/scenarios/):
  assumptions.json          every assumption, its anchor and rationale; observed H5 context
  capacity-scenarios.json   REDUCTION / CONTINUATION / EXPANSION presets + boats x occupancy grid
  geographic-scenarios.json models A, B, C for total support and dispersal accommodation
  scenario-claims.json      SCENARIO and DERIVED_STATISTIC claims (merged into research/claims.json)

Rules (implementation plan, "Scenario arithmetic"):
  * modelled arrivals = assumed arriving boats x assumed average people per arriving boat
  * average occupancy is not rated capacity; no utilisation or departure-success rate is used
  * the supported population is an independent assumption, never derived from modelled arrivals
  * geographic models are mathematical allocations of an assumed total, not predictions of policy

Usage: python3 research/build_scenarios.py   (exit 1 if a check fails)
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE
OUT = RESEARCH / 'scenarios'
AS_OF = '2026-09-11'
REVIEW = 'source_checked_pending_independent_review'
CROSSING_SOURCE = 'HO-TABLES-2026Q2'
CROSSING_URL = ('https://assets.publishing.service.gov.uk/media/6a8c11c3a8f84a582b84281a/'
                'illegal-entry-routes-to-the-uk-summary-jun-2026-tables.ods')
D09_SOURCE = 'ASY-SRC-HO-D09-2026Q2'
D09_URL = ('https://assets.publishing.service.gov.uk/media/6a85c2f1c9205b515d421eec/'
           'asylum-seekers-receipt-support-datasets-jun-2026.xlsx')
D11_SOURCE = 'ASY-SRC-HO-D11-2026Q2'
D11_URL = ('https://assets.publishing.service.gov.uk/media/6a85c5e654bcee010d514574/'
           'support-local-authority-datasets-jun-2026.xlsx')

# ----------------------------------------------------------------- scenario parameters
# These are the ONLY free choices. Each is justified in assumptions.json.
REDUCTION_BOAT_FACTOR = 0.5          # illustrative halving of arriving boats vs baseline
C_BLEND = 0.5                        # model C weight on the population-proportional model
GRID_BOATS = list(range(200, 1201, 100))
GRID_OCCUPANCY = list(range(40, 76, 5))

FAILURES = []


def check(cond, msg):
    if not cond:
        FAILURES.append(msg)
        print('CHECK FAILED: ' + msg)


def read_csv(rel):
    with open(RESEARCH / rel, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def r6(x):
    return round(x, 6)


# ----------------------------------------------------------------- observed inputs

def observed_crossings():
    monthly = read_csv('crossings/monthly-crossings.csv')
    annual = read_csv('crossings/annual-crossings.csv')
    base = [m for m in monthly
            if (int(m['year']), int(m['month'])) >= (2025, 7) and (int(m['year']), int(m['month'])) <= (2026, 6)]
    check(len(base) == 12, 'baseline must cover 12 months, found %d' % len(base))
    people = sum(int(m['people']) for m in base)
    boats = sum(int(m['boats']) for m in base)
    full_years = [a for a in annual if a['period_type'] == 'calendar_year']
    max_boats = max(full_years, key=lambda a: int(a['boats']))
    max_people = max(full_years, key=lambda a: int(a['people']))
    eligible = [m for m in monthly if m['boats'] and int(m['boats']) >= 10]
    peak = max(eligible, key=lambda m: int(m['people']) / int(m['boats']))
    return {
        'baseline': {'period_start': '2025-07-01', 'period_end': '2026-06-30', 'people': people,
                     'boats': boats, 'average_people_per_boat': people / boats},
        'max_boats_year': {'year': int(max_boats['year']), 'boats': int(max_boats['boats']),
                           'people': int(max_boats['people']),
                           'average_people_per_boat': int(max_boats['people']) / int(max_boats['boats'])},
        'max_people_year': {'year': int(max_people['year']), 'people': int(max_people['people'])},
        'peak_month': {'year': int(peak['year']), 'month': int(peak['month']), 'people': int(peak['people']),
                       'boats': int(peak['boats']),
                       'average_people_per_boat': int(peak['people']) / int(peak['boats'])},
        'annual_points': [{'year': int(a['year']), 'boats': int(a['boats']), 'people': int(a['people']),
                           'average_people_per_boat': r6(int(a['people']) / int(a['boats'])),
                           'period_type': a['period_type'], 'months_covered': int(a['months_covered'])}
                          for a in annual],
    }


def observed_support():
    nat = read_csv('asylum/asylum-support-national.csv')
    tot = defaultdict(int)
    for r in nat:
        tot[r['date']] += int(r['people'])
    since22 = {d: v for d, v in tot.items() if '2022-03-31' <= d <= '2026-06-30'}
    lo = min(since22, key=since22.get)
    hi = max(since22, key=since22.get)
    return tot, {'date': '2026-06-30', 'people': tot['2026-06-30']}, \
        {'date': lo, 'people': since22[lo]}, {'date': hi, 'people': since22[hi]}


def h5_robustness(annual_points, support_tot):
    """Which years move in opposite directions under different stock definitions (Phase 2 review)."""
    arr = {p['year']: p['people'] for p in annual_points if p['period_type'] == 'calendar_year'}
    def at(md):
        return lambda y: support_tot.get('%d-%s' % (y, md))
    def mean(y):
        vals = [support_tot.get('%d-%s' % (y, md)) for md in ('03-31', '06-30', '09-30', '12-31')]
        return sum(vals) / 4 if all(v is not None for v in vals) else None
    out = {}
    for name, f, lag in (('31_december', at('12-31'), 0), ('30_september', at('09-30'), 0),
                         ('annual_mean_of_quarter_ends', mean, 0), ('31_december_arrivals_lagged_one_year', at('12-31'), 1)):
        years = []
        for y in range(2019 + lag, 2026):
            a, a0 = arr.get(y - lag), arr.get(y - lag - 1)
            s1, s0 = f(y), f(y - 1)
            if None in (a, a0, s1, s0):
                continue
            if (a - a0) * (s1 - s0) < 0:
                years.append(y)
        out[name] = years
    ratios = {str(y): r6((support_tot['%d-12-31' % y] - support_tot['%d-12-31' % (y - 1)]) / arr[y])
              for y in range(2019, 2026)}
    return out, ratios


def h5_relationship(annual_points, support_tot):
    """Observed context for H5: calendar-year arrivals vs change in supported people (31 Dec)."""
    rows = []
    by_year = {p['year']: p for p in annual_points if p['period_type'] == 'calendar_year'}
    for y in range(2019, 2026):
        cur, prev = support_tot.get('%d-12-31' % y), support_tot.get('%d-12-31' % (y - 1))
        a, a_prev = by_year.get(y), by_year.get(y - 1)
        if cur is None or prev is None or not a or not a_prev:
            continue
        rows.append({
            'year': y, 'small_boat_arrivals': a['people'],
            'arrivals_change_pct': r6((a['people'] - a_prev['people']) / a_prev['people'] * 100),
            'supported_people_31_dec': cur, 'supported_people_31_dec_previous': prev,
            'supported_change_pct': r6((cur - prev) / prev * 100),
            'same_direction': (a['people'] - a_prev['people']) * (cur - prev) > 0})
    return rows


def snapshot():
    rows = read_csv('asylum/asylum-support-local-authority.csv')
    out = []
    for r in rows:
        out.append({'la_code': r['la_code'], 'la_name': r['la_name'], 'country': r['country'],
                    'region_name': r['region_name'], 'population': int(r['population']),
                    'population_mid_year': int(r['population_mid_year']),
                    'total': int(r['total_asylum_support']), 'dispersal': int(r['dispersal'])})
    return out


# ----------------------------------------------------------------- scenario arithmetic

def concentration(values):
    total = sum(values)
    s = sorted(values, reverse=True)
    cum, n50, n80 = 0, None, None
    for i, v in enumerate(s, 1):
        cum += v
        if n50 is None and cum >= 0.5 * total:
            n50 = i
        if n80 is None and cum >= 0.8 * total:
            n80 = i
    return {'share_top10_pct': r6(sum(s[:10]) / total * 100), 'share_top20_pct': r6(sum(s[:20]) / total * 100),
            'local_authorities_holding_50pct': n50, 'local_authorities_holding_80pct': n80,
            'herfindahl_index': r6(sum((v / total) ** 2 for v in values)),
            'local_authorities_with_nonzero_allocation': sum(1 for v in values if v > 0)}


def geographic(las, measure, totals):
    pop_total = sum(la['population'] for la in las)
    obs_total = sum(la[measure] for la in las)
    shares = {
        'A': [la[measure] / obs_total for la in las],
        'B': [la['population'] / pop_total for la in las],
    }
    shares['C'] = [(1 - C_BLEND) * a + C_BLEND * b for a, b in zip(shares['A'], shares['B'])]
    models = {}
    for m, sh in shares.items():
        check(abs(sum(sh) - 1) < 1e-9, '%s model %s shares sum to %r' % (measure, m, sum(sh)))
        models[m] = {'concentration': concentration(sh), 'totals': {}}
        for label, t in totals.items():
            alloc = [t * s for s in sh]
            check(abs(sum(alloc) - t) < 1e-6, '%s %s %s allocation sum' % (measure, m, label))
            models[m]['totals'][label] = {'assumed_total': t,
                                          'uk_rate_per_10000': r6(t / pop_total * 10000)}
    # model A with the observed total reproduces the observed snapshot exactly
    for la, s in zip(las, shares['A']):
        check(abs(s * obs_total - la[measure]) < 1e-6, 'model A reproduces observed for %s' % la['la_code'])
    rows = []
    for i, la in enumerate(las):
        row = {'la_code': la['la_code'], 'la_name': la['la_name'], 'country': la['country'],
               'region_name': la['region_name'], 'population': la['population'],
               'population_mid_year': la['population_mid_year'], 'observed_30_jun_2026': la[measure]}
        for m in ('A', 'B', 'C'):
            row['share_' + m] = r6(shares[m][i])
            for label, t in totals.items():
                v = t * shares[m][i]
                row['%s_%s' % (m, label)] = round(v, 2)
                row['%s_%s_per_10000' % (m, label)] = r6(v / la['population'] * 10000)
        rows.append(row)
    return pop_total, obs_total, models, rows


def ev(source_id, url, date, locator):
    return {'source_id': source_id, 'url': url, 'publication_date': date, 'locator': locator}


def main():
    oc = observed_crossings()
    base = oc['baseline']
    claims_reg = {c['id']: c for c in json.load(open(RESEARCH / 'claims.json', encoding='utf-8'))['claims']}
    check('33,374 people and 511 boats' in claims_reg.get('ROLLING-2026Q2', {}).get('claim', ''),
          'ROLLING-2026Q2 claim text must match 33,374 people and 511 boats')
    check(base['people'] == 33374 and base['boats'] == 511, 'baseline recomputed from monthly CSV = 33,374 / 511')
    check(oc['peak_month']['year'] == 2025 and oc['peak_month']['month'] == 11, 'peak month is 2025-11 (PEAK-OCCUPANCY-MONTHS)')

    support_tot, s_ref, s_low, s_high = observed_support()
    check(s_ref['people'] == 93293, 'supported people at 30 June 2026 = 93,293')
    h5 = h5_relationship(oc['annual_points'], support_tot)
    h5_opposite, h5_ratios = h5_robustness(oc['annual_points'], support_tot)

    # ------------------------------------------------------------- crossing presets
    occ = base['average_people_per_boat']
    # Boats are whole numbers (the frozen MVP's modelArrivals rejects non-integers); round half up.
    reduction_boats = int(base['boats'] * REDUCTION_BOAT_FACTOR + 0.5)
    presets = {
        'REDUCTION': {'boats': reduction_boats, 'occupancy': occ,
                      'boats_basis': 'baseline arriving boats x %.1f = %.1f, rounded half up to %d (illustrative '
                                     'assumption)' % (REDUCTION_BOAT_FACTOR, base['boats'] * REDUCTION_BOAT_FACTOR,
                                                      reduction_boats),
                      'occupancy_basis': 'baseline average people per arriving boat, held constant'},
        'CONTINUATION': {'boats': base['boats'], 'occupancy': occ,
                         'boats_basis': 'baseline arriving boats (July 2025-June 2026), held constant',
                         'occupancy_basis': 'baseline average people per arriving boat, held constant'},
        'EXPANSION': {'boats': oc['max_boats_year']['boats'], 'occupancy': oc['peak_month']['average_people_per_boat'],
                      'boats_basis': 'highest calendar-year arriving boats observed 2018-2025 (%d, %d boats)'
                                     % (oc['max_boats_year']['year'], oc['max_boats_year']['boats']),
                      'occupancy_basis': 'highest monthly average people per boat among months with at least 10 boats '
                                         '(%d-%02d, %.6f)' % (oc['peak_month']['year'], oc['peak_month']['month'],
                                                              oc['peak_month']['average_people_per_boat'])},
    }
    for name, p in presets.items():
        p['modelled_arrivals'] = p['boats'] * p['occupancy']
        p['change_vs_baseline_pct'] = (p['modelled_arrivals'] - base['people']) / base['people'] * 100
    check(abs(presets['CONTINUATION']['modelled_arrivals'] - base['people']) < 1e-6, 'CONTINUATION reproduces baseline')
    check(presets['REDUCTION']['modelled_arrivals'] < presets['CONTINUATION']['modelled_arrivals']
          < presets['EXPANSION']['modelled_arrivals'], 'presets ordered REDUCTION < CONTINUATION < EXPANSION')

    capacity = {
        'classification': 'SCENARIO', 'not_a_forecast': True, 'as_of': AS_OF, 'review_status': REVIEW,
        'approved_for_application': False,
        'horizon': 'An illustrative, undated 12-month period. No year is attached; these are not predictions.',
        'formula': 'modelled_arrivals = assumed_arriving_boats x assumed_average_people_per_arriving_boat',
        'variable_definitions': {
            'arriving_boats': 'Boats counted by the Home Office as arriving (IER_02a). Not departures, attempts or '
                              'boats intercepted and returned; no departure-success rate is modelled.',
            'average_people_per_arriving_boat': 'Detected arrivals / arriving boats over the same period. An average '
                                                'occupancy, not rated vessel capacity; no utilisation rate is applied.',
            'modelled_arrivals': 'Hypothetical detected small-boat arrivals in the 12-month period.'},
        'baseline': {'label': 'Observed, July 2025-June 2026', 'classification': 'OFFICIAL_STATISTIC (counts); '
                     'DERIVED_STATISTIC (average)', 'claim_ids': ['ROLLING-2026Q2'],
                     'people': base['people'], 'boats': base['boats'],
                     'average_people_per_boat': r6(occ), 'source_id': CROSSING_SOURCE, 'source_table': 'IER_02a'},
        'presets': [{'id': 'SCN-CROSSING-' + n, 'name': n, 'assumed_arriving_boats': r6(p['boats']),
                     'assumed_average_people_per_boat': r6(p['occupancy']),
                     'modelled_arrivals': r6(p['modelled_arrivals']),
                     'modelled_arrivals_display': int(round(p['modelled_arrivals'], -2)),
                     'change_vs_baseline_pct': r6(p['change_vs_baseline_pct']),
                     'boats_basis': p['boats_basis'], 'occupancy_basis': p['occupancy_basis'],
                     'assumption_ids': {'REDUCTION': ['ASM-BASELINE', 'ASM-REDUCTION-BOATS', 'ASM-OCCUPANCY-HELD'],
                                        'CONTINUATION': ['ASM-BASELINE', 'ASM-OCCUPANCY-HELD'],
                                        'EXPANSION': ['ASM-EXPANSION-BOATS', 'ASM-EXPANSION-OCCUPANCY']}[n]}
                    for n, p in presets.items()],
        'expansion_caveat': ('EXPANSION combines two observed maxima that never occurred together: in %d, when '
                             'arriving boats peaked at %d, the annual average was %.2f people per boat. Its output '
                             '(%s) exceeds every observed calendar year (maximum %s in %d).' % (
                                 oc['max_boats_year']['year'], oc['max_boats_year']['boats'],
                                 oc['max_boats_year']['average_people_per_boat'],
                                 format(int(round(presets['EXPANSION']['modelled_arrivals'])), ','),
                                 format(oc['max_people_year']['people'], ','), oc['max_people_year']['year'])),
        'sensitivity_grid': {
            'description': 'Modelled arrivals for each combination of assumed arriving boats and average people per '
                           'boat. Arithmetic only; combinations outside the observed points have never occurred.',
            'boats': GRID_BOATS, 'average_people_per_boat': GRID_OCCUPANCY,
            'modelled_arrivals': [[b * o for o in GRID_OCCUPANCY] for b in GRID_BOATS]},
        'observed_points_for_overlay': {'classification': 'OFFICIAL_STATISTIC (counts); DERIVED_STATISTIC (average)',
                                        'note': '2026 covers January-June only; do not plot it as a full year.',
                                        'points': oc['annual_points']},
        'not_modelled': ['departures or attempts', 'interceptions or returns to France', 'rated vessel capacity or '
                         'utilisation', 'route length or geography', 'asylum claims, support or accommodation'],
    }

    # ------------------------------------------------------------- geographic models
    las = snapshot()
    totals = {'ref': s_ref['people'], 'low': s_low['people'], 'high': s_high['people']}
    pop_total, obs_total, models_total, rows_total = geographic(las, 'total', totals)
    check(obs_total == s_ref['people'], 'LA snapshot total equals national 93,293')
    disp_share = sum(la['dispersal'] for la in las) / obs_total
    disp_totals = {k: v * disp_share for k, v in totals.items()}
    _, obs_disp, models_disp, rows_disp = geographic(las, 'dispersal', disp_totals)
    check(obs_disp == 69038, 'LA snapshot dispersal equals 69,038')
    summary = json.load(open(RESEARCH / 'asylum' / 'asylum-summary.json', encoding='utf-8'))
    dc = summary.get('dispersal_concentration', {})
    a_disp = models_disp['A']['concentration']
    check(dc and abs(float(dc['share_top10_pct']) - a_disp['share_top10_pct']) < 0.01
          and abs(float(dc['share_top20_pct']) - a_disp['share_top20_pct']) < 0.01
          and dc['local_authorities_holding_50pct'] == a_disp['local_authorities_holding_50pct']
          and dc['local_authorities_holding_80pct'] == a_disp['local_authorities_holding_80pct'],
          'model A dispersal concentration reproduces asylum-summary.json dispersal_concentration')
    # Published large-site capacities (claims PATH-LARGE-SITE-CROWBOROUGH, PATH-LARGE-SITE-WETHERSFIELD).
    # 'Other accommodation' at 30 June 2026 is the large-site population (ASYGEO-BRAINTREE-LARGE-SITE).
    sites = {'Wealden': ('Crowborough Training Camp', 540, 'full capacity 540 (PATH-LARGE-SITE-CROWBOROUGH)'),
             'Braintree': ('Wethersfield', 850, 'steady state around 850, surge 1,250 (PATH-LARGE-SITE-WETHERSFIELD)')}
    other = {}
    for r in read_csv('asylum/asylum-support-local-authority.csv'):
        other[r['la_name']] = int(r['other'])
    capacity_warnings = []
    for r in rows_total:
        if r['la_name'] in sites:
            site, cap, basis = sites[r['la_name']]
            for m in ('A', 'C'):
                for label, t in totals.items():
                    implied_site = other[r['la_name']] * (t / totals['ref']) if m == 'A' else None
                    alloc = r['%s_%s' % (m, label)]
                    if m == 'A' and implied_site and implied_site > cap:
                        capacity_warnings.append({'la_name': r['la_name'], 'model': m, 'total': label,
                                                  'allocated_people': alloc, 'implied_site_population': round(implied_site, 1),
                                                  'site': site, 'published_capacity': cap, 'capacity_basis': basis})
    ni = [la for la in las if la['country'] == 'Northern Ireland']
    ni_b_ref = sum(totals['ref'] * la['population'] / pop_total for la in ni)
    ni_obs = sum(la['total'] for la in ni)

    geo = {
        'classification': 'SCENARIO', 'not_a_forecast': True, 'as_of': AS_OF, 'review_status': REVIEW,
        'approved_for_application': False,
        'terminology': 'People receiving asylum support; dispersal accommodation by local authority. Not a count or '
                       'projection of small-boat arrivals.',
        'geography': '361 local authorities as at 30 June 2026 (research/asylum/asylum-support-local-authority.csv). '
                     'Barnsley/Sheffield split handled as in asylum-summary.json split_approximations.',
        'population': {'total': pop_total, 'mid_years_used': summary.get('population_mid_years_used'),
                       'publishers': 'ONS (England and Wales), NRS (Scotland), NISRA (Northern Ireland)'},
        'models': {
            'A': 'Existing proportions constant: share_i = observed_i / observed_total at 30 June 2026.',
            'B': 'Equal relative to local population: share_i = population_i / UK population. Every LA gets the '
                 'same rate per 10,000.',
            'C': 'Less concentrated: share_i = (1 - w) x A_i + w x B_i with w = %.1f. A stated midpoint between A '
                 'and B, not a policy model.' % C_BLEND},
        'assumed_totals': {
            'total_support': {k: {'people': v, 'anchor': a} for (k, v), a in zip(totals.items(), [
                'observed 30 June 2026', 'lowest quarter-end 31 Mar 2022-30 Jun 2026 (%s)' % s_low['date'],
                'highest quarter-end 31 Mar 2022-30 Jun 2026 (%s)' % s_high['date']])},
            'dispersal': {k: {'people': r6(v), 'anchor': 'total_support x observed dispersal share at 30 June 2026 '
                              '(%.6f)' % disp_share} for k, v in disp_totals.items()},
            'rule': 'Assumed totals are independent of the crossing presets. Pairing any crossing preset with any '
                    'total is a presentation choice, not a modelled relationship (see assumptions.json ASM-SUPPORT-INDEPENDENT).'},
        'policy_caveats': [
            'Model B allocates about %s people to Northern Ireland at the reference total (observed %s). Home Office '
            'Asy_D11 note 11: "Asylum seekers are accommodated in Northern Ireland only if they claim asylum there." '
            'Model B is therefore arithmetic, not a feasible allocation under current rules.' % (
                format(int(round(ni_b_ref)), ','), format(ni_obs, ',')),
            'No model reflects accommodation supply, procurement, the allocation policy, or the exit from hotels and '
            'large sites. None claims the government will use any allocation rule.',
            'Models A and C scale hotel and large-site populations with the assumed total, despite the commitment to '
            'end hotel use (PATH-HOTEL-EXIT-COMMITMENT). See capacity_warnings.'],
        'capacity_warnings': capacity_warnings,
        'presentation_rules': [
            'Never show a crossing preset and a supported-population total together, and label every supported '
            'total "set independently of arrivals".',
            'Round displayed allocations (nearest 10 for local authorities, nearest 100 for totals).',
            'Model A at the reference total reproduces the observed map; always label it as a scenario.',
            'Distinguish scenario maps with hatching or a dashed outline and a text label, not colour alone.'],
        'measures': {
            'total_support': {'observed_total': obs_total, 'concentration': {m: v['concentration'] for m, v in models_total.items()},
                              'uk_rates': {m: v['totals'] for m, v in models_total.items()},
                              'local_authorities': rows_total},
            'dispersal': {'observed_total': obs_disp, 'concentration': {m: v['concentration'] for m, v in models_disp.items()},
                          'uk_rates': {m: v['totals'] for m, v in models_disp.items()},
                          'local_authorities': rows_disp}},
        'rounding': 'Allocations keep 2 decimal places and rates 6; rounded displays need not sum to the total.',
    }

    # ------------------------------------------------------------- assumptions
    assumptions = {
        'as_of': AS_OF, 'review_status': REVIEW, 'approved_for_application': False,
        'rules': [
            'Scenarios are not forecasts and are stored separately from observed data.',
            'Modelled arrivals = assumed arriving boats x assumed average people per arriving boat.',
            'Average occupancy is not capacity; no utilisation, departure-success or interception rate is used.',
            'The supported population is an independent assumption and is never derived from modelled arrivals.',
            'Geographic models are mathematical allocations, not claims about government policy.',
            'Scenario values must be visually distinct from observed values without relying on colour alone.'],
        'assumptions': [
            {'id': 'ASM-BASELINE', 'classification': 'OFFICIAL_STATISTIC', 'value': {'people': base['people'], 'boats': base['boats'],
             'average_people_per_boat': r6(occ)}, 'anchor_claim_ids': ['ROLLING-2026Q2'],
             'rationale': 'Latest 12 months published (July 2025-June 2026). A rolling year avoids treating 2026 '
                          '(January-June only) as a full year.'},
            {'id': 'ASM-OCCUPANCY-HELD', 'classification': 'SCENARIO', 'value': r6(occ),
             'rationale': 'REDUCTION and CONTINUATION hold occupancy at the baseline so that only the boat count '
                          'differs. No evidence is used to predict occupancy.'},
            {'id': 'ASM-REDUCTION-BOATS', 'classification': 'SCENARIO', 'value': r6(base['boats'] * REDUCTION_BOAT_FACTOR),
             'rationale': 'Illustrative halving of arriving boats. Not tied to any policy, agreement or evidence of '
                          'effect; chosen only to show a clearly lower case.'},
            {'id': 'ASM-EXPANSION-BOATS', 'classification': 'SCENARIO', 'value': oc['max_boats_year']['boats'],
             'anchor_claim_ids': ['ANNUAL-%d' % oc['max_boats_year']['year']],
             'rationale': 'The highest calendar-year count of arriving boats observed 2018-2025. Using an observed '
                          'maximum bounds the scenario by recorded experience.'},
            {'id': 'ASM-EXPANSION-OCCUPANCY', 'classification': 'SCENARIO', 'value': r6(oc['peak_month']['average_people_per_boat']),
             'anchor_claim_ids': ['PEAK-OCCUPANCY-MONTHS', 'STAT-PUBOCC-MONTHLY-RECORD-2025'],
             'rationale': 'The highest monthly average among months with at least 10 boats, applied to a whole year. '
                          'A single-month value sustained for 12 months has never been observed.'},
            {'id': 'ASM-SUPPORT-INDEPENDENT', 'classification': 'SCENARIO',
             'value': {k: v for k, v in totals.items()},
             'anchor_claim_ids': ['ASY-NAT-2026Q2-TOTAL'],
             'rationale': 'Supported-population totals are set independently of arrivals: the observed 30 June 2026 '
                          'total and the lowest and highest quarter-ends since 31 March 2022. The observed record '
                          'below shows no stable proportional link between annual arrivals and the supported '
                          'population, and the supported population includes people who did not arrive by small boat '
                          '(research-asylum H5).'},
            {'id': 'ASM-DISPERSAL-SHARE', 'classification': 'SCENARIO', 'value': r6(disp_share),
             'anchor_claim_ids': ['ASY-NAT-2026Q2-DISPERSAL', 'ASY-NAT-2026Q2-TOTAL'],
             'rationale': 'Dispersal totals scale with the assumed supported total at the observed 30 June 2026 '
                          'dispersal share. The share has changed over time (hotel use fell from 2023), so this is a '
                          'simplification.'},
            {'id': 'ASM-MODEL-C-WEIGHT', 'classification': 'SCENARIO', 'value': C_BLEND,
             'rationale': 'research-asylum Part 15 names "less geographically concentrated" without defining it. A 50/50 '
                          'blend of models A and B is a transparent, reproducible definition; other weights are equally valid.'}],
        'observed_relationship_h5': {
            'classification': 'DERIVED_STATISTIC',
            'description': 'Calendar-year small-boat arrivals vs change in people receiving asylum support between '
                           'successive 31 December snapshots. Context for ASM-SUPPORT-INDEPENDENT; not a causal analysis.',
            'input_files': ['crossings/annual-crossings.csv', 'asylum/asylum-support-national.csv'],
            'rows': h5,
            'years_moving_in_opposite_directions': [r['year'] for r in h5 if not r['same_direction']],
            'opposite_direction_years_by_definition': h5_opposite,
            'december_change_in_supported_per_arrival': h5_ratios,
            'robust_finding': 'Not proportional: the change in supported people per small-boat arrival ranged from '
                              '%s to %s. Which years move in opposite directions depends on the stock definition, '
                              'and a partial or lagged national relationship is not excluded (2020-2022 moved together).'
                              % (min(h5_ratios.values()), max(h5_ratios.values())),
            'limitations': 'Support depends on claims from all routes, decision speed, appeals, grants and exits, not '
                           'only arrivals. Seven annual pairs cannot establish or rule out a relationship. Section 98 '
                           'figures before 30 June 2023 include everyone in initial or contingency accommodation '
                           'irrespective of support eligibility (Asy_D09 note 7). Year-on-year percentage comparisons '
                           'with small arrival bases (2019: 1,843) are not meaningful.'},
    }

    # ------------------------------------------------------------- claims
    claims = []
    for p in capacity['presets']:
        claims.append({
            'id': p['id'], 'claim': 'SCENARIO (not a forecast): %s assumes %s arriving boats at %s people per boat over an '
            'illustrative 12-month period, giving %s modelled arrivals (%+.1f%% vs July 2025-June 2026).' % (
                p['name'], format(round(p['assumed_arriving_boats'], 1), ','), round(p['assumed_average_people_per_boat'], 2),
                format(int(round(p['modelled_arrivals'])), ','), p['change_vs_baseline_pct']),
            'classification': 'SCENARIO', 'evidence_level': 'scenario_assumption', 'confidence': 'LOW',
            'confidence_rationale': 'Hypothetical arithmetic on stated assumptions; confidence refers to the plausibility of '
                                    'the outcome, which is not assessed. The arithmetic itself is exact.',
            'evidence': [ev(CROSSING_SOURCE, CROSSING_URL, '2026-08-27', 'IER_02a monthly and annual people and boats (anchors)')],
            'geography': {'scope': 'UK detected small-boat arrivals; origin not disaggregated'},
            'limitations': 'Not a prediction. Occupancy is an average, not capacity. No departures, interceptions or '
                           'routes are modelled. Says nothing about asylum support or where anyone lives.',
            'review_status': REVIEW, 'approved_for_application': False,
            'calculation': {'formula': 'assumed_arriving_boats x assumed_average_people_per_boat',
                            'input_files': ['crossings/monthly-crossings.csv', 'crossings/annual-crossings.csv'],
                            'input_claim_ids': sorted({c for a in assumptions['assumptions'] if a['id'] in p['assumption_ids']
                                                       for c in a.get('anchor_claim_ids', [])}),
                            'values': {'boats': p['assumed_arriving_boats'], 'people_per_boat': p['assumed_average_people_per_boat'],
                                       'modelled_arrivals': p['modelled_arrivals']}}})
    opp = assumptions['observed_relationship_h5']['years_moving_in_opposite_directions']
    claims.append({
        'id': 'SCN-H5-OBSERVED-NONPROPORTIONAL',
        'claim': 'Between 2019 and 2025, the national number of people receiving asylum support did not change in '
                 'proportion to annual small-boat arrivals: the change in supported people (31 December to 31 December) '
                 'per arrival ranged from %s to %s. The years in which the two moved in opposite directions depend on the '
                 'snapshot used (31 December: %s; 30 September: %s; annual mean: %s; one-year lag: %s).' % (
                     min(h5_ratios.values()), max(h5_ratios.values()),
                     ', '.join(map(str, h5_opposite['31_december'])), ', '.join(map(str, h5_opposite['30_september'])),
                     ', '.join(map(str, h5_opposite['annual_mean_of_quarter_ends'])),
                     ', '.join(map(str, h5_opposite['31_december_arrivals_lagged_one_year']))),
        'classification': 'DERIVED_STATISTIC', 'evidence_level': 'primary_official_statistics', 'confidence': 'MEDIUM',
        'confidence_rationale': 'Both series are official, but the direction test is sensitive to the snapshot and lag '
                                'chosen (Phase 2 review). Non-proportionality holds under every definition tested; a '
                                'partial or lagged national relationship is not excluded.',
        'evidence': [ev(CROSSING_SOURCE, CROSSING_URL, '2026-08-27', 'IER_02a annual people'),
                     ev(D09_SOURCE, D09_URL, '2026-08-27', 'Data_Asy_D09 quarter-end totals')],
        'geography': {'scope': 'United Kingdom'},
        'limitations': 'Not causal. Asylum support covers people from all routes and depends on decision speed, appeals '
                       'and exits. Section 98 definition break before 30 June 2023. Supports treating the supported '
                       'population as an independent scenario assumption; does not show that arrivals have no effect.',
        'review_status': REVIEW, 'approved_for_application': False,
        'calculation': {'formula': '(supported_31Dec_y - supported_31Dec_{y-1}) / arrivals_y; direction test under four '
                                   'stock definitions',
                        'input_files': ['crossings/annual-crossings.csv', 'asylum/asylum-support-national.csv'],
                        'values': {'december_change_per_arrival': h5_ratios,
                                   'opposite_direction_years': h5_opposite}}})
    for m in ('A', 'B', 'C'):
        c = models_total[m]['concentration']
        claims.append({
            'id': 'SCN-GEO-MODEL-' + m,
            'claim': 'SCENARIO (mathematical allocation, not a forecast or policy): model %s allocates an assumed total of '
                     'people receiving asylum support across 361 local authorities; the top 20 would hold %.1f%% and %d '
                     'authorities would hold half.' % (m, c['share_top20_pct'], c['local_authorities_holding_50pct']),
            'classification': 'SCENARIO', 'evidence_level': 'scenario_assumption', 'confidence': 'LOW',
            'confidence_rationale': 'Arithmetic allocation under a stated rule; no claim that any allocation will occur.',
            'evidence': [ev(D11_SOURCE, D11_URL, '2026-08-27', 'Data_Asy_D11 at 30 Jun 2026 (model A shares)')],
            'geography': {'scope': 'UK local authorities (boundaries at 30 June 2026)'},
            'limitations': geo['models'][m] + ' ' + ' '.join(geo['policy_caveats']),
            'review_status': REVIEW, 'approved_for_application': False,
            'calculation': {'formula': geo['models'][m],
                            'input_files': ['asylum/asylum-support-local-authority.csv'],
                            'values': c}})

    for name, obj in (('assumptions.json', assumptions), ('capacity-scenarios.json', capacity),
                      ('geographic-scenarios.json', geo), ('scenario-claims.json', claims)):
        OUT.mkdir(exist_ok=True)
        with open(OUT / name, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)

    print('Baseline Jul 2025-Jun 2026: %d people, %d boats, %.2f per boat' % (base['people'], base['boats'], occ))
    for p in capacity['presets']:
        print('  %-12s boats %8.1f x %6.2f = %9.0f (%+.1f%%)' % (p['name'], p['assumed_arriving_boats'],
              p['assumed_average_people_per_boat'], p['modelled_arrivals'], p['change_vs_baseline_pct']))
    print('H5 years in opposite directions: %s of %d' % (opp, len(h5)))
    print('Supported totals: ref %d, low %d (%s), high %d (%s)' % (s_ref['people'], s_low['people'], s_low['date'],
                                                                  s_high['people'], s_high['date']))
    for meas, mods in (('total', models_total), ('dispersal', models_disp)):
        for m in ('A', 'B', 'C'):
            c = mods[m]['concentration']
            print('  %-9s %s: top20 %.1f%%, LAs for 50%% %d, 80%% %d, HHI %.4f' % (meas, m, c['share_top20_pct'],
                  c['local_authorities_holding_50pct'], c['local_authorities_holding_80pct'], c['herfindahl_index']))
    print('Northern Ireland under model B at ref total: %.0f (observed %d)' % (ni_b_ref, ni_obs))
    print('\nRESULT: %s' % ('all checks passed' if not FAILURES else '%d CHECKS FAILED' % len(FAILURES)))
    return 1 if FAILURES else 0


if __name__ == '__main__':
    sys.exit(main())
