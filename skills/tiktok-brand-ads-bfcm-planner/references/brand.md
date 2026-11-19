# Brand Ads: Reach, Traffic, Video Views

Use ordinary Auction creation. Read `tools.md` for current enums/combinations and `execution.md` before writes. Use the supported ordinary Auction optimization goals below. Explain the current skill boundary if requested; don't pretend the platform itself lacks the feature.

## Select the Objective and promotion scope

Explicit supported Objective wins. Otherwise use desired outcome and relevant recent history, then one scope confirmation:

- More people see brand/activity → Reach.
- Clicks/visits to a page → Traffic.
- People watch content → Video Views.

Website Traffic needs an actual promoted URL for creation; retrieve a known applicable URL first. Reach/Video Views can proceed without a landing page when the selected configuration supports that; still identify brand/activity/assets. Do not make Pixel mandatory for Traffic or LPV.

For new advertisers, apply `entry.md`: first Traffic and URL question, not this three-way menu until explicitly no URL.

| Branch | Create optimization enum, known snapshot | Evaluate |
|---|---|---|
| Reach | `REACH`, applicable CPM | Reach, impressions, CPM, frequency; no uniform frequency default |
| Traffic Click | `CLICK`, CPC | Clicks/CPC; do not infer sales from cheap clicks |
| Traffic LPV | `TRAFFIC_LANDING_PAGE_VIEW`, OCPM | Landing page views and same-scope unit cost; Pixel optional |
| Video Views 6s | `ENGAGED_VIEW`, CPV | `engaged_view` and same-scope cost |
| Video Views 15s | `ENGAGED_VIEW_FIFTEEN`, CPV | `engaged_view_15s` and same-scope cost |

Treat goal+bid+billing combinations as route-specific live contracts, not universally composable enums. Inspect current parent campaign before creating Ad Groups. CBO requires consistent supported bid/optimization combinations and Campaign-level budget handling.

Traffic: honor explicit click/visit-quality goal. If unclear, briefly distinguish Clicks vs LPV and explain Best Practice starts with Clicks. LPV is not a Pixel PageView event. Ramp-up with no explicit cost constraint: recommend applicable Maximum Delivery; reuse preserves applicable current cost constraints.

Video Views requires a valid supported optimization goal in the creation payload. Recommend 6s/15s from content and user intent rather than assuming an undocumented default: official material-fit guidance suggests 6s Focused View for 1–6s content and 15s for 7–15s content. This is a recommendation, not a universal asset-duration gate. Preserve an applicable original goal on reuse. Focused View is not ordinary watched-6s playback; verify metric combinations at report time.

## Brand new-campaign Best Practice

For **all Brand Ads creation**, both new and established advertisers, select this table by **advertiser registered country**, using `advertiser_info_get.country` and the separate `advertiser_country-to-Region Mapping.csv` column `Region (5-group)` directly (the logical `mapped_value`); follow the exact request and response selection in `benchmark.md`. It is not selected by target country. Missing mapping is unknown, not inferred from the region label. Industry Benchmark still uses actual delivery country. Actual targeting still follows user countries. This rule does not change budget recommendation precedence.

USD references:

| Objective | NA | EUI | METAP | LATAM | APAC |
|---|---:|---:|---:|---:|---:|
| Reach daily budget | 260 | 235 | 140 | 160 | 195 |
| Video Views daily budget | 140 | 125 | 75 | 85 | 100 |
| Traffic daily budget | ≥160 | ≥80 | ≥43 | ≥43 | ≥45 |

| Objective | Duration/creative reference |
|---|---|
| Reach | At least 7 days, at least 6 creatives |
| Video Views | At least 7 days, at least 4 creatives |
| Traffic | At least 14 days, at least 6 creatives including 2 images if format/placement supports them |

Prefer appropriately broad targeting in actual sales/service countries, retaining customer constraints. Do not force unsupported image formats because a quantity Best Practice includes images. A duration/count recommendation is not a platform creation requirement. Incentive conditions are separate from ordinary Best Practice. Non-USD needs an explicit exchange basis, not copying USD digits into another currency.

For any new Brand Campaign with no usable historical-spend basis, proactively prefill the Objective-specific budget from this table once registered-country region and currency applicability are verified, subject to customer limits and actual minimums. Do not wait for a follow-up budget request. Also state the Objective-specific creative quantity and duration, even if regional budget mapping is currently unavailable. With a usable BAU and matched Benchmark, retain the common Benchmark precedence. Recommended counts do not block otherwise valid creation.

Always name the recommendation source: “Traffic Best Practice”, “Reach Best Practice” or “Video Views Best Practice”. Never call it a generic skill recommendation, platform minimum or an account-based BFCM calculation. Distinguish verified usable assets from candidates needing checks.

Example advertiser-facing explanation: “Traffic Best Practice recommends at least 6 creatives, including 2 images where the selected formats and placements support them. The starting daily-budget reference depends on the region mapped from the account’s registered country.” If regional mapping is verified, replace the last sentence with the actual region and applicable amount; if not, explain that regional amount selection remains unverified rather than choosing a country by geography.

Historical plans: all matching running candidates, basic checks and applicable AOS; budget suggestions only below the applicable value. New ordinary Auction: Campaign → Ad Group → Ad with current schemas; read back settings and statuses after confirmation/execution. Use only the supported Auction Reach, Traffic and Video Views configurations.
