# Historical plans, budgets and creatives

Read `benchmark.md` for matching, dates, currency and citations.

## Historical branch: basic checks and applicable AOS

Read **all running plans matching confirmed promotion scope**, using pagination. Include low/zero spend and old-created plans that remain enabled in a valid schedule. Do not apply Top N, spend, or seven-day creation-date cutoffs. Paused/ended plans are separate and require confirmed reactivation.

Basic checks per plan:

- Matching URL/brand/activity, countries, destination, Objective and customer dates.
- Enabled status, schedule, review, permissions and readable delivery restrictions.
- Actual optimization event/goal, its results and unit cost. Separate Clicks/LPV and 6s/15s goals.
- Spend, budget utilization and changes; distinguish Campaign/Ad Group budgets; deduplicate CBO objects.
- Default latest seven complete available days vs preceding equal window. Customer window wins; disclose coverage, currency and attribution differences.

Judge against customer requirements, then the same plan's comparable history, then comparable plans (same countries, destination, event, attribution and currency). No universal pass score or cost cutoff. Scaling needs evidence beyond low spend.

For historical bulk handling, complete **AOS for every applicable Brand candidate**, even without an obvious anomaly; overall diagnosis is suitable when supported. Respect actual supported Objectives/issues. Account-level diagnosis does not prove every plan was individually diagnosed.

| AOS scenario | What it adds |
|---|---|
| Overall performance | Issues affecting continued use or proposed change |
| No spending/delivery/impressions | Supported blockers and remedies |
| Low budget utilization/declining spend | Whether adding budget has a basis |
| Creative fatigue/decline | Performance evidence, not actual content inspection |

Verify object, diagnosis date/timezone, applicability, evidence and action. Failed/empty/unsupported diagnosis is not “passed.” Do not require an unproven AOS Action enum. `tool_diagnosis_get` is a separate active-Ad-Group suggestion tool, not a comprehensive AOS substitute.

Group **eligible to continue / needs attention / needs verification**. Only required checks completed without an identified issue affecting the change enter the write batch. Isolate problems so other eligible plans can proceed. Budget-only changes preserve targeting, bid, promoted objects, assets and structure. Do not default to rebuilding/duplicating working plans. Creative quantity below reference alone does not disqualify a plan.

## Budget

BAU = September 1–30, 2026, UTC+0, **30 calendar days**. Average daily actual spend = complete BAU actual spend / 30, not configured budget and not spend per active day.

Budget range = applicable object's BAU average daily actual spend × [lower multiplier, upper multiplier]. Prefill the **lower bound**, checking currency precision and platform minimums separately. Never multiply current configured daily budget by the multiplier.

### Precedence

- **Brand new Campaign:** usable BAU × matched Benchmark range first; without a usable BAU-based amount, proactively use the selected Objective's registered-country Best Practice in `brand.md`, before asking the customer to supply a budget. This applies even when the account does not meet the narrow registered-new-advertiser definition. If the region or currency conversion is unverified, do not choose a regional default; continue region-independent recommendations, use reliable historical configuration/recent spend if available, or combine the remaining budget question with other required questions.
- **Brand existing Campaign:** BAU × Benchmark range; otherwise reliable historical configuration/recent actual spend. A verified, applicable absolute daily-budget Benchmark can be used only if the source explicitly supplies money/day and its eligibility and match are verified. The current budget sheet supplies multipliers, so it cannot produce a monetary recommendation with no BAU.
- Missing/incomplete/zero BAU or coefficients: do not recommend zero, invent a range or conclude “do not advertise.” Use the applicable branch fallback first. For new Brand Campaigns, show Objective Best Practice immediately when registration-region matching is verified. Only if no usable monetary source remains, ask once: “What daily budget range would you be comfortable starting with?” Briefly explain the missing source without presenting lack of BAU as inability to prepare the plan.
- Bid recommendations are not budget recommendations. Traffic `tool_bid_recommend` supports Cost Cap bids, not a proven Traffic budget suggestion.

### Existing plans

Compare same budget level, currency and period. Below applicable lower-bound value: propose that exact increase. Within/above the range: leave unchanged, **no per-plan keep-budget prompt and no reduction because the reference is lower**. A separate cost-control request may justify another confirmed proposal.

Example: BAU $30/day × 2–3 = $60–$90. Current $40 → propose $60. Current $60/$75/$100 → no increase prompt.

### New plans and aggregate allocation

Use an applicable account/Objective reference and supported allocation; never assign the entire account reference to every new Campaign. Existing plans use related-object BAU; new plans consider account/Objective arrangements. Missing allocation evidence means ask the intended range, not invent fixed percentages.

Deduplicate actual CBO Campaign or Ad Group budget objects. Preserve existing layer. Ordinary new Auction normally uses Ad Group budget. CBO requires compatible settings across its Ad Groups; inspect current requirements.

Customer total given: clarify dates, Objective, inclusion of existing plans and spent/remaining amounts; combine existing/new in one ledger. Carry shared commitments across sequential Objectives. Explain infeasible tradeoffs, never silently cut existing budgets. No total given: recommend with evidence and show aggregate; Benchmark is neither a cap nor a fixed pool from which to subtract existing budgets mechanically.

Keep currencies separate unless conversion is explicit. Estimate activity spend over actual remaining dates and label it an estimate. A daily budget is not guaranteed spend or always an absolute daily cap. Explain Dynamic Daily Budget averages where applicable.

### Wording and provenance

“I recommend setting the daily budget to at least **[lower multiplier] times your BAU average daily actual spend**, or **[amount]/day**, to leave more budget available for BFCM traffic opportunities. The full reference range is [lower–upper], and the lower bound is prefilled.” Not “increase the current budget by X times.”

Cite 2025 BFCM sample, matched Objective, delivery region, industry, USD BAU spend tier, coefficient range and snapshot. Keep percentile wording as defined; do not call a selected percentile typical behavior or promise proportional growth. Cite each matching group once. Platform suggestions need their own date/object source.

Action: “Would you like me to adjust the [Y] budget objects across these [X] Campaigns to their respective prefilled amounts?”

## Creative quantity and usability

For a new Brand Campaign without historical spend evidence, proactively present the Objective-specific Best Practice creative quantity from `brand.md` (Traffic: at least 6 including 2 images where supported; Reach: at least 6; Video Views: at least 4). Label it **Traffic / Reach / Video Views Best Practice**, not a generic skill suggestion or an account-specific BFCM Benchmark result. Report candidate/verified-usable assets separately and explain any supplement. Historical asset names alone do not prove language, content or expired offers. Best Practice quantity does not require regional mapping, and a mapping failure must not suppress it. Where a separate matched creative Benchmark is also available, identify its different source and units; do not silently combine targets or imply BAU is needed for absolute counts.


Creative Benchmark contains **absolute distinct-asset count intervals**, not multipliers. Use existing current/proposed confirmed dates or new proposed dates; for ongoing work use remaining delivery dates, not already ended phases. No end date: use confirmed activity scope. Date gaps join the consolidated question. Convert dates/times to UTC+0 before phase intersection.

1. Match classification and every covered **2026 phase** in `benchmark.json`; creative-table 2025 dates are historical sample dates. Partial overlap selects a phase, without prorating count by days.
2. One phase: direct count interval. Several: **maximum lower count, maximum upper count**, never their sum. Assets can be reused across phases.
3. Same account/Objective/promoted scope: union covered phases and deduplicate assets across plans; display the account reference once. Never compare account-wide target to single-product-only availability.
4. Find related assets through exact URL, brand, activity or source plan. Only normalize known tracking-only URL parameters. Check promotion relevance, country/language suitability, identity binding/authorization/expiry, status, format and placement. Different historical country or no prior spend is not automatic exclusion.
5. Count **verified usable** stable video/post/image IDs, including eligible assets without historical spend. Deduplicate across dates, ads and plans. Others are needs verification or unavailable with actual reasons. High spend is not proof of best quality.
6. Same-scope supplement = [max(0, lower − available), max(0, upper − available)]. Default advice: reach the lower bound. Unknown count/linkage, missing phase rows or inconsistent scope: disclose limitations, do not invent a complete interval or treat missing as zero. No phase overlap: use another applicable reference. BAU spend-generating creative count is optional context, **not a calculation input**.

Example: phases 31–77, 28–70, 32–79 → **32–79**. Available 20 → **12–59** more, first aim for 12. Available 40 → lower met, optionally add up to 39. Available 79+ → no push to add just to hit a count.

Wording: “The 2025 BFCM reference for comparable advertisers in the covered phases is [lower–upper] creatives. I found [available] verified usable assets for this scope. Aim to add at least [gap] more; eligible existing assets can be used now.” If lower already met, say so. Cite classification, phases and source briefly.

Shortfall does **not block creation** if platform requirements are met. Replenishment can mean reuse, authorization or production; advice does not authorize uploads/replacement. Invalid authorization blocks only the affected asset.

Only diagnose content when requested with readable actual video/script. Check expired offer dates, prices/products, visuals/subtitles/audio consistency, language, CTA and readability against known activity facts. Give reuse/change/new-content directions with evidence. IDs/performance metadata alone do not establish video contents; AOS fatigue is not video inspection.
