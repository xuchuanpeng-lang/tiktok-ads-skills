#!/usr/bin/env python3
"""Read-only recommendation arithmetic. JSON stdin; no network or ad writes."""
import argparse
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from pathlib import Path


def number(value, label, positive=False):
    if value is None or isinstance(value, bool):
        raise ValueError(f"{label} must be a number, not missing/boolean")
    try:
        n = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"Invalid {label}") from exc
    if not n.is_finite() or n < 0 or (positive and n == 0):
        raise ValueError(f"{label} must be finite and {'positive' if positive else 'nonnegative'}")
    return n


def interval(lower, upper, label, integer=False):
    lo, hi = number(lower, label + ' lower'), number(upper, label + ' upper')
    if lo > hi:
        raise ValueError(f"{label} lower exceeds upper; verify the source")
    if integer and (lo != lo.to_integral_value() or hi != hi.to_integral_value()):
        raise ValueError(f"{label} requires integer counts")
    return lo, hi


def spend_tier(total_usd, complete=True):
    if not complete or total_usd is None:
        return {"tier": None, "status": "needs_verification", "basis": "complete_account_BAU_total_actual_spend_USD"}
    n = number(total_usd, 'account BAU total USD')
    tier = 'T3' if n < 1000 else 'T2' if n < 5000 else 'T1'
    return {"tier": tier, "status": "calculated", "basis": "complete_account_BAU_total_actual_spend_USD"}


def money(n, precision):
    # Round UP to the supported step so an increase target does not fall below lower bound.
    return (n / precision).to_integral_value(rounding=ROUND_CEILING) * precision


def budget(data):
    step = number(data.get('currency_step', '0.01'), 'currency step', positive=True)
    current = number(data['current_budget'], 'current budget') if data.get('current_budget') is not None else None
    benchmark = None
    benchmark_issue = None
    if data.get('bau_complete') is True and data.get('bau_total') is not None:
        total = number(data['bau_total'], 'BAU total')
        if total > 0 and data.get('lower_multiplier') is not None and data.get('upper_multiplier') is not None:
            try:
                lo, hi = interval(data['lower_multiplier'], data['upper_multiplier'], 'budget multiplier')
                if lo == 0:
                    raise ValueError('A zero multiplier cannot supply a positive budget recommendation')
                benchmark = (total / Decimal(30) * lo, total / Decimal(30) * hi)
            except ValueError as exc:
                # Preserve the issue while allowing an independent verified fallback.
                benchmark_issue = str(exc)
    source, target = None, None
    if benchmark:
        target = money(benchmark[0], step)
        source = 'BAU_average_daily_actual_spend_times_lower_multiplier'
    elif data.get('brand_new_campaign') is True and data.get('best_practice_applicable') is True and data.get('best_practice_budget') is not None:
        target = money(number(data['best_practice_budget'], 'Best Practice budget', positive=True), step)
        source = 'Objective_Best_Practice_verified_registered_region'
    else:
        for key in ['historical_bau_daily_budget', 'recent_reference_budget']:
            if data.get(key) is not None:
                target = money(number(data[key], key, positive=True), step)
                source = key
                break
    out = {"source": source, "recommended_range_unrounded": [str(v) for v in benchmark] if benchmark else None,
           "prefilled_budget": str(target) if target is not None else None,
           "current_budget": str(current) if current is not None else None,
           "currency": data.get('currency'), "currency_step": str(step), "writes_performed": False,
           "benchmark_issue": benchmark_issue}
    if target is None:
        out.update(status='ask_investment_range', prompt_existing_budget=False, delta=None)
    elif current is None:
        out.update(status='new_plan_reference_requires_allocation_and_confirmation', prompt_existing_budget=False, delta=None)
    elif current < target:
        out.update(status='propose_increase_after_eligibility_checks', prompt_existing_budget=True, delta=str(target-current))
    else:
        out.update(status='unchanged_no_budget_prompt', prompt_existing_budget=False, delta='0')
    return out


def manifest():
    return json.loads((Path(__file__).resolve().parent.parent / 'references/benchmark.json').read_text())


def covered_phases(schedules, as_of=None):
    phases = manifest()['phases']
    found = set()
    floor = date.fromisoformat(as_of) if as_of else None
    for schedule in schedules:
        start = date.fromisoformat(schedule['start_date'])
        end = date.fromisoformat(schedule['end_date'])
        if start > end:
            raise ValueError('Schedule start is after end')
        if floor:
            start = max(start, floor)
        if start > end:
            continue
        for phase in phases:
            if start <= date.fromisoformat(phase['end_2026']) and end >= date.fromisoformat(phase['start_2026']):
                found.add(phase['order'])
    return sorted(found)


def creative(data):
    orders = covered_phases(data['schedules'], data.get('as_of_utc_date'))
    by_order = {}
    for row in data['phase_intervals']:
        order = int(row['phase_order'])
        if order in by_order:
            raise ValueError('Duplicate phase interval; resolve the matching row first')
        lo, hi = interval(row['lower'], row['upper'], 'creative count', integer=True)
        by_order[order] = (int(lo), int(hi))
    missing = [order for order in orders if order not in by_order]
    if 'verified_available_ids' in data:
        ids = data['verified_available_ids']
        if not isinstance(ids, list) or any(not isinstance(i, str) or not i.strip() for i in ids):
            raise ValueError('Asset IDs must be a list of nonempty stable strings')
        available = len(set(ids))
        if data.get('available_count') is not None:
            raise ValueError('Provide verified IDs OR an available count, not both')
    elif data.get('available_count') is not None:
        n = number(data['available_count'], 'available count')
        if n != n.to_integral_value():
            raise ValueError('Available count must be an integer')
        available = int(n)
    else:
        available = None
    present = [by_order[o] for o in orders if o in by_order]
    partial = [max(v[0] for v in present), max(v[1] for v in present)] if present else None
    out = {"covered_phases": orders, "missing_phases": missing, "available_count": available,
           "reference": None, "supplement": None, "writes_performed": False,
           "blocks_creation_due_to_count": False}
    if not orders:
        out['status'] = 'no_BFCM_overlap_use_other_applicable_reference'
    elif missing:
        out.update(status='partial_phase_coverage', partial_reference_not_complete=partial)
    else:
        out['reference'] = partial
        if data.get('same_scope') is not True or data.get('count_complete') is not True or available is None:
            out['status'] = 'reference_only_verify_availability_scope'
        else:
            gap = [max(0, v-available) for v in partial]
            out.update(supplement=gap, minimum_additional=gap[0], status='lower_met' if gap[0] == 0 else 'suggest_supplement_to_lower')
    return out


def shares(values, step_percentage_points='0.1'):
    if len(values) != 5 or any(v is None for v in values):
        return {'status': 'verify_missing_phase_shares', 'normalize': False}
    ns = [number(v, 'share percentage points') for v in values]
    if any(n > 100 for n in ns):
        raise ValueError('Each share must be at most 100 percentage points')
    total = sum(ns, Decimal(0))
    tolerance = Decimal(len(ns)) * number(step_percentage_points, 'display step', positive=True) / 2
    status = 'totals_100' if total == 100 else 'display_rounding_difference' if abs(total-100) <= tolerance else 'verify_source_total'
    return {'status': status, 'total_percentage_points': str(total), 'rounding_tolerance_percentage_points': str(tolerance),
            'original_values': [str(n) for n in ns], 'normalize': False, 'automatic_budget_action': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=['tier', 'budget', 'creative', 'shares'])
    args = ap.parse_args()
    try:
        data = json.load(sys.stdin)
        if args.command == 'tier':
            out = spend_tier(data.get('bau_total_usd'), data.get('complete') is True)
        elif args.command == 'budget':
            out = budget(data)
        elif args.command == 'creative':
            out = creative(data)
        else:
            out = shares(data['shares_percentage_points'], data.get('display_step_percentage_points', '0.1'))
        print(json.dumps(out, indent=2))
    except (ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc), 'writes_performed': False}), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
