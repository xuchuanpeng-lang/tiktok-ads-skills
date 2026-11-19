#!/usr/bin/env python3
"""Offline exact lookup of bundled user-supplied Benchmark CSVs; no ad writes."""
import argparse
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEYS = ['Industry v3.2 L2 Name', 'Objective Type EN', 'Ad Sub Region', 'Spend Tier']


def config():
    return json.loads((ROOT / 'references/benchmark.json').read_text())


def source(purpose):
    sheet = next(s for s in config()['sheets'] if s['purpose'] == purpose)
    path = ROOT / 'references' / sheet['file']
    if hashlib.sha256(path.read_bytes()).hexdigest() != sheet['sha256']:
        raise ValueError('Bundled CSV checksum differs from release manifest')
    return path


def norm(value):
    return ' '.join(str(value).split()).casefold()


def csv_rows(text):
    if text.lstrip().lower().startswith(('<!doctype', '<html', '<script')):
        raise ValueError('HTML/login response, not CSV')
    rows = list(csv.reader(io.StringIO(text.lstrip('\ufeff'))))
    if len(rows) < 2 or max(map(len, rows), default=0) < 2:
        raise ValueError('No tabular CSV data')
    return rows


def lookup(path, match):
    raw = path.read_bytes()
    rows = csv_rows(raw.decode('utf-8-sig'))
    normalized = {norm(k): v for k, v in match.items()}
    if len(normalized) != len(match) or not all(norm(k) in normalized for k in KEYS):
        raise ValueError('Exact lookup requires all four V3.2 L2 classification keys without duplicates')
    if norm(normalized[norm('Objective Type EN')]) not in {norm(v) for v in config()['supported_objective_rows']}:
        raise ValueError('Objective/buying type is outside this skill scope')
    headers = rows[0]
    positions = {}
    for idx, key in enumerate(headers):
        if not key.strip() or norm(key) in positions:
            raise ValueError('Blank or duplicate header; cannot safely bind columns')
        positions[norm(key)] = idx
    if 'phase order' in positions and not ({'phase order', 'peak sale phase'} & normalized.keys()):
        raise ValueError('Creative lookup requires Phase Order or Peak Sale Phase')
    if any(k not in positions for k in normalized):
        raise ValueError('Match header not present in this release')
    hits = []
    for line, row in enumerate(rows[1:], 2):
        if not any(c.strip() for c in row):
            continue
        if len(row) != len(headers):
            raise ValueError(f'Invalid row width at CSV row {line}')
        if all(norm(row[positions[k]]) == norm(v) for k, v in normalized.items()):
            hits.append({'csv_row': line, 'values': dict(zip(headers, row))})
    return {'status': 'unique' if len(hits) == 1 else 'missing' if not hits else 'ambiguous',
            'matches': hits, 'source_file': path.name, 'sha256': hashlib.sha256(raw).hexdigest(),
            'lookup_method': 'exact_whitespace_case_normalized_not_semantic_guess', 'writes_performed': False}


def country_rows(rows, role):
    expected = ['target_country', 'target_region'] if role == 'target' else ['advertiser_country', 'Region (5-group)']
    if rows[0] != expected:
        raise ValueError('Unexpected/duplicate mapping headers')
    result = []
    for line, row in enumerate(rows[1:], 2):
        if len(row) != len(expected):
            raise ValueError(f'Invalid mapping row width at {line}')
        if not any(c.strip() for c in row):
            continue
        result.append((line, dict(zip(expected, row))))
    return expected, result


def country(code, role):
    if role not in {'target', 'advertiser'}:
        raise ValueError('Explicit target or advertiser role is required')
    if not isinstance(code, str) or not code.strip():
        raise ValueError('Country code is required')
    path = source(role + '_country_mapping')
    headers, records = country_rows(csv_rows(path.read_text(encoding='utf-8-sig')), role)
    hits = [{'csv_row': line, 'values': values} for line, values in records if values[headers[0]] == code]
    status = 'unique' if len(hits) == 1 else 'missing' if not hits else 'ambiguous'
    value = hits[0]['values'][headers[1]] if len(hits) == 1 else None
    if status == 'unique' and (not value or value.strip().upper() == 'NULL'):
        status = 'unmapped'
    if role == 'advertiser' and status == 'unique' and value not in {'NA','EUI','METAP','LATAM','APAC'}:
        status = 'unsupported_region'
    out = {'role': role, 'country': code, 'status': status, 'matches': hits,
           'source_file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
           'source_column': headers[1], 'lookup_method': 'exact_case_sensitive',
           'requires_correction': status != 'unique', 'writes_performed': False}
    out['target_region' if role == 'target' else 'mapped_value'] = value if status == 'unique' else None
    if status != 'unique':
        out['action'] = 'Explain this country mapping issue and request supplementation or correction; no defaults or deduplication.'
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    lookup_ap = sub.add_parser('lookup')
    loc = lookup_ap.add_mutually_exclusive_group(required=True)
    loc.add_argument('--purpose', choices=['budget','creative','phase_allocation'])
    loc.add_argument('--csv', type=Path)
    c = sub.add_parser('country'); c.add_argument('--role', choices=['target','advertiser'], required=True); c.add_argument('--code', action='append', required=True)
    args = ap.parse_args()
    try:
        result = ({'results': [country(code, args.role) for code in args.code], 'writes_performed': False} if args.command == 'country' else lookup(args.csv or source(args.purpose), json.load(sys.stdin)))
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'error': str(exc), 'writes_performed': False}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
