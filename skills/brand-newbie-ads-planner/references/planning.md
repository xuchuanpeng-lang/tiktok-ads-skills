# First-campaign planning and Best Practice

The amounts and quantities below are Objective Best Practice planning references, not current platform minimums or performance guarantees. Registered country determines the reference region; delivery countries determine targeting. Keep them separate.

## Registered-country mapping

Use this exact sequence:

`MCP advertiser_info_get: target account country → advertiser_country → Region (5-group) → Objective × region Best Practice`

Allow only NA, EUI, METAP, LATAM and APAC. Read the registered country through MCP first, map the region next, then select the corresponding budget-table column. Do not choose a budget first or infer registration region from delivery location. A user-stated country can be pending verification, but cannot replace the MCP account record in this sequence.

1. Obtain the target advertiser_id and inspect the current `advertiser_info_get` schema. Where supported, request `advertiser_ids: [advertiser_id]` and `fields: ["advertiser_id", "country"]`; obtain currency and timezone through supported fields separately.
2. Select the unique response record whose advertiser_id exactly matches the target. Its `country` is `advertiser_country`; never use another advertiser's country from the response.
3. Match `advertiser_country` exactly in [advertiser-country-region.csv](advertiser-country-region.csv) and read the physical column `Region (5-group)`. Record advertiser_id, MCP country, mapping row number and region.
4. No record, multiple records, a blank region or an unsupported region remains unknown. Do not infer from targeting, user location, language, currency or Business Center country. Do not silently fill gaps or deduplicate.

Briefly show the budget basis as “account registered country → region → Objective Best Practice,” retaining actual values for verification. When switching advertiser accounts, read the new account's country and map again.

Treat blank regions as unmatched. Creative and duration guidance remains available without a regional match. If no reliable monetary basis is available, consolidate a question about the advertiser's comfortable daily budget with other necessary questions.

## Proactive budget, creative and duration recommendations

Daily USD references:

| Objective | NA | EUI | METAP | LATAM | APAC |
|---|---:|---:|---:|---:|---:|
| Reach | 260 | 235 | 140 | 160 | 195 |
| Video Views | 140 | 125 | 75 | 85 | 100 |
| Traffic | ≥160 | ≥80 | ≥43 | ≥43 | ≥45 |

| Objective | Recommended duration | Recommended creatives |
|---|---|---|
| Reach | At least 7 days | At least 6 |
| Video Views | At least 7 days | At least 4 |
| Traffic | At least 14 days | At least 6, including 2 images where format/placement supports them |

Once registration region and currency applicability are verified, proactively prefill the budget; start Traffic at the regional lower bound by default. Name the basis Traffic Best Practice, Reach Best Practice or Video Views Best Practice. Respect user limits. If below the recommendation, explain the tradeoff and check actual platform minimums; do not raise the budget without authorization. Distinguish ordinary creation eligibility, Best Practice readiness and incentive qualification when assets are insufficient.

For non-USD accounts, require a reliable dated exchange rate and conversion basis. Do not copy USD digits into another currency. Without reliable conversion, show the USD reference and ask for an account-currency budget; do not invent a live rate.

Use actual current time, user goals and feasibility for scheduling. Do not backfill past dates or automatically schedule the entire quarter. Show cross-year dates explicitly and check the incentive window separately.

Normally budget at Ad Group level. Use CBO only when supported by live schemas, account eligibility and the plan. Count shared Campaign budgets once; do not assign the entire shared pool independently to multiple Ad Groups or Objectives. Daily budget × scheduled days is a planning estimate, not guaranteed spend or a hard cap; explain billing and daily-budget variation. If a hard limit is requested, verify an actual supported control rather than presenting a daily-budget estimate as a cap.

## Objectives and optimization goals

These known combinations require runtime schema verification; they are not freely composable enums.

| Direction | Known optimization enum / billing | Selection basis |
|---|---|---|
| Reach | REACH / CPM | More distinct people see the brand or activity |
| Traffic Clicks | CLICK / CPC | Clicks; starting recommendation when visit-quality intent is unspecified |
| Traffic LPV | TRAFFIC_LANDING_PAGE_VIEW / OCPM | Actual page arrivals; Pixel is not a universal prerequisite |
| Video Views 6s | ENGAGED_VIEW / CPV | 6s Focused View intent |
| Video Views 15s | ENGAGED_VIEW_FIFTEEN / CPV | 15s Focused View intent |

Recommend applicable Maximum Delivery during ramp-up without an explicit cost constraint. A Cost Cap bid suggestion is not a daily-budget recommendation. Traffic requires a usable Web URL. Briefly distinguish Clicks and LPV if intent is unclear. Reach / Video Views may proceed without a landing page where the selected configuration supports it; identify the brand/activity and assets.

Video Views requires a valid optimization goal. Consider 6s Focused View for 1–6s content and 15s for 7–15s content as material-fit guidance, not universal duration gates. For other lengths, use actual content, viewing intent and platform support.

## Assets and targeting

Use real authorized asset IDs and identity, valid content/language/rights, and matching specifications and placements. Names or past performance cannot establish actual video content. Do not claim content review without access to the content. Report candidate count, verified usable count, recommended count and gap separately. Filling the quantity gap does not guarantee incentive eligibility or delivery.

Recommend appropriately broad targeting within actual sales/service countries while retaining user constraints. Resolve confirmed countries to platform location IDs through current tools; never target by registered country automatically. If images are unsupported, explain the impact on Best Practice and incentive conditions rather than forcing an unsupported format.
