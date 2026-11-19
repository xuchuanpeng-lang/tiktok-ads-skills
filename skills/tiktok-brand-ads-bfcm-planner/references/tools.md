# TT4B runtime tool contract

Use an authorized TT4B MCP connection in the current host. Verify available operations, account permissions and request schemas at runtime. Native tool names may have a host namespace prefix.

## Discovery

1. Discover exposed TT4B capabilities by their current tool names/descriptions. A common deployment exposes `tool_list`, `tool_get` and `tool_execute`; request the exact live schemas of needed operations, then follow the dispatcher's actual argument schema. If direct tools are exposed, use those directly. Do not fabricate a wrapper, authentication token, API URL or serialized payload shape.
2. Verify a read on the intended advertiser and resolve account ambiguity before business operations. Read current account currency/timezone. For creation Best Practice, follow the exact `advertiser_info_get` request and matching advertiser-ID selection in `benchmark.md`; its `country` is the only registration input. Resolve targeting location IDs through the current TikTok location query interface before target-country Benchmark mapping.
3. Inspect only needed route schemas, pagination/limits, filters, enum combinations, field mutability, status/review and errors. A field's existence is not proof that the combination is supported or the account is eligible.
4. No tool/permission: explain the precise unavailable action, retain the completed plan and continue independent work. Do not assume a read-only snapshot can execute a write.

## Operation map — names must be checked live

| Need | Known operation family |
|---|---|
| Account identity | `advertiser_info_get` / exposed advertiser access-list operation |
| Ordinary plans | `campaign_get`, `adgroup_get`, `ad_get`; create/update/status counterparts |
| Brand report | `report_integrated_get`; choose actual hierarchy, filters and legal metric dimensions |
| Bid suggestion | `tool_bid_recommend`: supported Traffic **Cost Cap**; not a daily-budget tool |
| Assets/identity | Exposed video/image/ad-library/identity read operations; inspect exact scopes and stable asset IDs |
| IDs/URLs | `tool_targeting_search`, `tool_url_validate` when exposed and applicable |

Read coverage must match the requested account and Brand Objectives. Pagination and undeleted-only defaults matter. For new-customer classification, missing deleted history/first-spend/activity history must remain evidence gaps. `country` meaning and `industry` taxonomy version must be verified.

### AOS native tool

`tiktok_ads_diagnosis_agent` may be exposed as a native tool rather than a `tool_get` item. Inspect its actual schema; do not fail discovery simply because dispatcher lookup lacks it.

Known scope: advertiser, **supported Brand Campaign**, Ad Group. Known issue categories: `NO_SPENDING`, `LOW_SPENDING`, `HIGH_CPA`, `CREATIVE_FATIGUE`, `UNCLEAR_DIAGNOSIS`. The tool also describes delivery/impression absence, spend decline, conversion-efficiency issues and overall follow-ups. Map questions to actual supported input, not invented issue enums.

Known context: `advertiser_id` required, optional Campaign/Ad Group ID and `issue_date` in account timezone; newest diagnostic day may differ from report dates. Pass the user’s actual relevant diagnostic question as required by the tool, without inventing user messages. Omit unrelated personal or confidential details under the data-handling rules in `execution.md`; described limit 2,000 characters. Caller-managed session ID maximum 32 characters in the inspected contract; reuse for a related follow-up, new ID for a different diagnostic task. No fixed output fields or Action enum have been established. A failure/empty result is not an all-clear.

`tool_diagnosis_get` is a separate read: active Ad Groups, maximum 20 IDs per request in the inspected schema, only suggestion-bearing groups returned, categories CREATIVE/BID_AND_BUDGET/EVENT_TRACK. Absence from this output is not universal proof of health; it does not replace required AOS without equivalent confirmed coverage.

## Important known schema details

- `adgroup_create`: read parent first. CBO ignores inappropriate Ad Group budget/pacing and requires compatible bid/optimization goals. Defaults and immutable attribution/placement fields need readback, not guesswork.
- Reporting enums/metric names are candidates until the actual hierarchy/date/attribution combination succeeds and agrees with Ads Manager. A create enum doesn't validate a report field.

Use the included read-only math tools for deterministic calculations; all account writes must still use authorized current TT4B tools, a confirmed plan, and post-write reads.
