# Brand Ads strategy sources

## Business rules

The approved Brand Ads rules cover account entry, all matching running Campaigns, applicable AOS diagnosis, BAU-based budgets, Objective-specific Best Practice, phase-based creative counts, concrete-plan confirmation, readback and on-demand reporting. They are business rules rather than official platform requirements.

For new Campaigns without usable BAU, show registered-country Objective Best Practice budgets proactively. Industry Benchmark uses target country, while Best Practice uses registered country. Creative counts and duration advice remain available when regional budget matching is unknown.

The 2026 Q4 Traffic incentive is business-provided material: no sign-up required, 50% qualifying-spend ad credit capped at USD 100 per Advertiser ID, subject to all conditions in `entry.md`. Eligibility, slot availability and actual credit are not established by this skill.

## Official references

These are reference links, not a claim that every current rule or API combination has been verified. Verify current schemas and relevant platform documentation when preparing account actions.

| ID | Reference | Applicable scope |
|---|---|---|
| O09 | [Reach objective](https://ads.tiktok.com/resources/help/article/reach-objective) | Auction Reach outcome definition |
| O10 | [Traffic objective](https://ads.tiktok.com/resources/help/article/traffic-objective) | Traffic outcome definition |
| O11 | [Landing Page View](https://ads.tiktok.com/resources/help/article/landing-page-view) | LPV goal and configuration; do not infer required Pixel |
| O12 | [Video Views objective](https://ads.tiktok.com/resources/help/article/video-views-objective) | Focused View goal/material-fit recommendations |
| O13 | [Campaign Budget Optimization](https://ads.tiktok.com/resources/help/article/campaign-budget-optimization) | Campaign-level budgeting and compatible configuration |
| O14 | [Dynamic Daily Budget](https://ads.tiktok.com/resources/help/article/about-dynamic-daily-budget) | Average daily budget and permitted variation |
| O31 | [Basic report dimensions and metrics](https://business-api.tiktok.com/portal/docs/supported-metrics-for-a-dimension-in-basic-reports/v1.3) | Legal metric/dimension combinations require actual verification |
| O32 | [Objective and optimization enums](https://business-api.tiktok.com/portal/docs/enumerations-appendix/v1.3) | Backend enums require destination/mode compatibility |

## Benchmark data

The six bundled CSVs are the unmodified contents of `Brand_BFCM_V3_2_L2_CSV.zip`, supplied November 19, 2026. `benchmark.json` records checksums, calendar and separate country mapping contracts; `data-quality.json` records audited data and explicit mapping gaps. Numeric source rows include Reach (R&F), which is not enabled by this skill: use only Reach (Auction), Traffic and Video Views (Auction). File integrity is verified against the checksums in `benchmark.json`. Target country maps directly to `target_region` for Benchmark; `advertiser_info_get.country` maps independently to `Region (5-group)` for new-campaign Best Practice. Do not infer aliases, deduplicate mapping records or fill blank values.
