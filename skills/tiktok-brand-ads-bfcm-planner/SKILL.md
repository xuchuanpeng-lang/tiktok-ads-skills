---
name: tiktok-brand-ads-bfcm-planner
description: Plan and execute TikTok 2026 Black Friday Brand Ads with TT4B MCP for Reach, Traffic Clicks/LPV, and Video Views 6s/15s Focused View. Review all matching running campaigns, diagnose applicable plans, recommend budgets and creatives, and create or adjust campaigns after confirmation. Includes registered new advertisers and on-demand reports.
metadata:
  version: "1.1.1"
  default-language: "en"
---

# Brand Ads BFCM Planner

Scope: **Reach, Traffic and Video Views**. Support ordinary Auction Reach, Traffic Clicks/LPV, and Video Views 6s/15s Focused View.

Customer-facing replies should describe objectives, recommendations, evidence and actions. Keep internal skill names, file paths and implementation details out of advertiser-facing replies unless specifically requested.

Default to **English** for advertiser-facing replies, tables, prompts, and artifacts. Follow an explicit request for another language. Keep platform product names, Objectives, optimization goals and exact API field names in their original English in every response language, including introductions and tables. Use Reach, Traffic, Video Views, Campaign, Ad Group, destination, Pixel, Maximum Delivery, Clicks and Landing Page View (LPV); do not replace them with translated labels. Explain their meaning in the requested language when useful. The skill prepares and executes a reviewable plan; it does not grant permissions or supply the TT4B connection itself.

## Load relevant guidance

- For account entry, task routing or new advertisers: [entry.md](references/entry.md).
- Before historical selection or budget/creative advice: [recommendations.md](references/recommendations.md) and [benchmark.md](references/benchmark.md).
- For all three supported Objectives: [brand.md](references/brand.md).
- Before any business write: [execution.md](references/execution.md). For tool discovery and legal combinations: [tools.md](references/tools.md), plus the current tool schemas. For reports: [reporting.md](references/reporting.md).
- [sources.md](references/sources.md) traces approved business rules, official guidance and tool evidence. Example requests: [prompts.md](references/prompts.md).
- [benchmark.json](references/benchmark.json) identifies the six bundled user-supplied CSV files, checksums and calendar. Use the bundled V3.2 L2 Brand Ads Benchmark release. `scripts/benchmark.py` performs offline exact lookup and country mapping; `scripts/plan_math.py` computes recommendations. Neither changes ads. Read [data-quality.json](references/data-quality.json) for audited coverage and mapping gaps.
- [policy.json](references/policy.json) provides the approved machine-readable routing and recommendation settings. Read [calculations.md](references/calculations.md) when using the helper commands; no helper authorizes account actions.

## Workflow

1. **Understand the task.** Answer knowledge questions directly. Explicit new-campaign requests go directly to creation preparation, without mandatory historical cleanup. For unspecified planning, start with account overview and historical opportunities. New-advertiser routing follows `entry.md`.
2. **Connect and identify scope.** Discover TT4B tools; check access to the current/requested advertiser. Read the last seven complete available days. Summarize Objectives, actual spend, distinct Campaign counts, spend shares, promoted objects and target countries. Reuse information and combine necessary questions into one short scope confirmation. Full creative/data-source validation is not an entry prerequisite.
3. **Work on one scenario at a time.** Identify the supported Brand Objective, promoted object and countries. For multiple Objectives use the customer’s order; otherwise select from desired outcome and relevant history per `brand.md`. Reuse known information and a shared budget ledger, but prepare/confirm/execute each direction separately.
4. **Prepare the branch.** Historical: paginate through **all matching running plans**, including low/zero spend; basic checks and applicable AOS precede the eligible budget-increase set. New: prepare the supported configuration with applicable official Best Practice and actual account/tool eligibility.
5. **Keep country roles separate.** Use configured or confirmed target countries → `target_country` → `target_region` for every Benchmark, including budget multipliers and creative count ranges. Resolve location IDs with TikTok location lookup first. For new Reach/Traffic/Video Views Best Practice, use only the matching advertiser record’s `advertiser_info_get.country` → `advertiser_country` → `Region (5-group)` (logical `mapped_value`). Never substitute these fields. Read `benchmark.md` for exact requests and missing/duplicate handling.
6. **Recommend in the right units.** Budget Benchmark is a **multiplier range × BAU average daily actual spend**; prefill the lower bound. Creative Benchmark is an **absolute count range by covered phase**; take the maximum lower and maximum upper across covered phases, never sum and never multiply by BAU creative count. For a new Brand Campaign without usable BAU, proactively prefill Objective-specific Best Practice budget and creative advice from `brand.md`, matched by verified registration-country mapping, without waiting for a budget follow-up. Attribute it to that Objective’s Best Practice, not account Benchmark math. Existing Brand Campaigns cannot convert a multiplier into money without a valid spend baseline.
7. **Present concise decisions.** Lead with key changes and a compact two-column summary. Summarize historical scope, counts, rule, impact and exceptions; exact IDs and before/after amounts remain inspectable in a fixed batch. New plans use one compact two-column table per plan; show shared fields once. Users can change defaults through conversation, without checking dozens of interface fields or ticking every row.
8. **Confirm and execute.** Analysis/prefill do not change ads. Form the exact batch before showing totals, obtain confirmation of the concrete plan, refresh mutable conditions and execute only confirmed unchanged objects. Budget-only confirmation does not authorize bidding, targeting, creative changes or reactivation. Read back actual configuration; distinguish success, skips, partial failures, review, enablement and delivery.
9. **Finish the task.** After historical work, optionally mention new-campaign help. Creative advice is not completed replenishment. Reports are lightweight and on demand; do not start monitoring or automatically optimize spend.

## Boundaries

- AOS is for applicable Brand Campaigns and Ad Groups. CPA/conversion-efficiency diagnosis does not apply to Reach or Video Views.
- Create only the three supported Objectives and optimization goals listed above; do not expand to other buying types or optimization paths.
- Use applicable ordinary Auction **Maximum Delivery bidding** when recommended in the selected Objective’s guidance.
- Existing budgets at/above applicable recommendations receive no per-plan budget prompt or reduction recommendation. Low spend alone does not justify more budget. No universal ROI/CPA/decline threshold.
- Handle account data under the data-handling rules in `execution.md`: use only authorized task services, retain only necessary task information in the current authorized workspace, and keep real account data out of skill packages and repositories.
- Unknown, failed, unsupported, empty and zero differ. Never invent data, mappings, event volumes, tool parameters, enrollment status or successful writes. Continue independent preparation if one action is blocked.
- BFCM is **November 12–30, 2026, UTC+0**. Schedule from actual use time and confirmed customer dates; never hardcode an adoption date or backfill past dates. Five-phase historical budget shares appear only on request, never as automatic budget actions.

## Starting request

> Help me prepare my Brand Ads Black Friday advertising for Reach, Traffic or Video Views. Review my account and recommend a plan before changing anything.

For new advertisers, first recommend **Traffic only**, briefly describe the incentive and request the promotion URL. Only after an explicit no-URL reply, explain Reach (more people see the brand/activity) and Video Views (people watch and learn about the content), then recommend by desired outcome. Reuse an already supplied URL or already stated lack of URL.
