# Read-only calculation helpers

Python 3.9+ standard library only; no account credentials or TT4B business writes. Execute from the skill directory. Feed verified JSON through stdin; keep account evidence and source locators in the plan alongside results. The helpers calculate numbers, not account eligibility, source truth, user consent or creative quality.

## Budget

`python3 scripts/plan_math.py budget < verified_budget_input.json`

Input fields:

| Field | Meaning |
|---|---|
| `bau_total`, `bau_complete` | Related-object actual spend over all 30 BAU calendar days, in account currency; completeness must explicitly be true |
| `lower_multiplier`, `upper_multiplier` | Verified multiplier endpoints, not budget amounts |
| `current_budget` | Same-level/currency existing budget; omit for a new-plan reference |
| `brand_new_campaign`, `best_practice_applicable`, `best_practice_budget` | Verified new Brand Campaign Objective/registration-region Best Practice amount, with applicability explicitly true; account-currency amount after a verified conversion if needed |
| `historical_bau_daily_budget`, `recent_reference_budget` | Optional verified fallback amounts, in that precedence |
| `currency`, `currency_step` | Account currency and supported positive increment (default 0.01); the helper does not convert currencies |

Example verified input: `{"bau_total":900,"bau_complete":true,"lower_multiplier":2,"upper_multiplier":3,"current_budget":40,"currency":"USD"}` → unrounded interval 60–90, prefill 60, proposed delta 20. Invalid Benchmark endpoints are reported rather than used. Use an independent verified Brand Best Practice or historical reference when available. Prefill rounds upward to the supplied supported increment; inspect legal minimums and the approved amount before writes. There is no automatic account-wide allocation in this helper.

## Tier

`python3 scripts/plan_math.py tier < verified_tier_input.json`

Input `{"bau_total_usd":1000,"complete":true}` → T2. This is **account cumulative BAU USD spend**, not the budget command's per-plan average. Convert non-USD with a separately sourced, dated FX basis before passing it. Missing/incomplete inputs return an unknown tier.

## Creative phases and quantities

`python3 scripts/plan_math.py creative < verified_creative_input.json`

```json
{
  "schedules": [{"start_date":"2026-11-12","end_date":"2026-11-22"}],
  "as_of_utc_date":"2026-11-12",
  "phase_intervals": [
    {"phase_order":1,"lower":31,"upper":77},
    {"phase_order":2,"lower":28,"upper":70},
    {"phase_order":3,"lower":32,"upper":79}
  ],
  "available_count":20,
  "same_scope":true,
  "count_complete":true
}
```

These are illustrative values, not live matching rows. Dates passed here are **UTC inclusive dates** already converted from the confirmed schedule and endpoint conventions. Set `as_of_utc_date` from actual use time to remove past phases; do not copy the sample date. Multiple schedules represent the same account/Objective/scope and are unioned. Phase orders 1–5 map to `benchmark.json`. Return is target 32–79 and supplement 12–59, not a sum of phase targets. Missing phase rows suppress the complete reference. Missing scope/count completeness suppresses supplement calculation.

Instead of `available_count`, supply `verified_available_ids` as stable namespaced strings (e.g. `video:123`); duplicates are removed. These IDs must have already passed actual usability checks. Do not supply both count and ID list.

## Historical shares

`python3 scripts/plan_math.py shares < verified_shares_input.json`

Input `shares_percentage_points` as five percentage-point numbers, not fractions, e.g. `[18.8,14.8,20.8,16.0,29.5]`. Optional `display_step_percentage_points`, default `0.1`. Return preserves original values, distinguishes plausible display rounding from source error, and never normalizes or executes budgets.

## Offline Benchmark lookup and country mapping

Run from the skill directory; all data is bundled, with no network or login prerequisite.

`python3 scripts/benchmark.py lookup --purpose budget < verified_match.json`

The JSON must contain all four exact header keys: `Industry v3.2 L2 Name`, `Objective Type EN`, `Ad Sub Region`, `Spend Tier`. Creative lookup uses `--purpose creative` and also requires `Phase Order` (1–5) or `Peak Sale Phase`. Historical-share lookup uses `--purpose phase_allocation`. Alternatively use `--csv /absolute/path/to/export.csv` for an explicitly supplied compatible export. Duplicate named headers are rejected; zero/multiple hits remain missing/ambiguous. Output includes original header values, CSV row and file checksum. Only whitespace/case normalization is performed; no semantic guesses.

`python3 scripts/benchmark.py country --role target --code DE`

For multiple target countries: `python3 scripts/benchmark.py country --role target --code DE --code GB`. Role is mandatory. Returns each mapping independently and preserves all matching CSV rows. Target results only expose `target_region`; advertiser results only expose `mapped_value` from `Region (5-group)`. Exact case-sensitive country-code matching; no normalization, aliases, fallback, deduplication or default. Ambiguous (including identical duplicates), missing and unmapped values require correction. Location IDs must be resolved through TikTok before calling this helper.

`python3 scripts/benchmark.py country --role advertiser --code US`

Only pass the verified `country` from the matching `advertiser_info_get` record; the helper cannot query or authenticate the account itself. See `benchmark.md` for the API request and evidence requirements.

`python3 scripts/audit_data.py`

Audits all six checksums, headers, keys, numeric intervals, phase/calendar metadata and mapping coverage. Explicit source mapping issues remain listed even when file structure is valid. Numeric coverage includes unused source Objectives; skill eligibility is checked separately. Optionally pass `--out /path/to/report.json`.
