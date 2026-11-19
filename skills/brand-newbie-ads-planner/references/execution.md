# TT4B tools, plan confirmation and execution

## Tool discovery

Before account operations, validate the connection, authorization and target-account access using [mcp-connection.md](mcp-connection.md). Guide configuration if unavailable. Resolve account permissions for an existing connection rather than asking the user to add the service again.

Discover exposed TT4B tools. If `tool_list`, `tool_get` and `tool_execute` are available, obtain operation definitions and follow their actual schemas. Use direct operations when exposed. Do not invent wrappers, API URLs, authentication methods, parameters or permissions.

| Capability | Known operation families; verify at runtime |
|---|---|
| Account identity | advertiser_info_get / advertiser access list |
| Historical/current objects | campaign_get / adgroup_get / ad_get, including pagination, lifecycle-state filters and coverage |
| Creation/status | campaign_create / adgroup_create / ad_create and applicable status operations |
| URL/location | tool_url_validate / tool_targeting_search or current equivalents |
| Assets/identity | Available video, image, ad-library and identity reads, plus necessary upload capabilities |
| On-demand reports | report_integrated_get; verify dimensions and reporting levels |

Read only what the current step needs. If a tool or permission is missing, identify the unavailable action and retain the completed plan. Do not claim a connection or creation occurred. Newcomer checks do not require full-account diagnosis or historical budget optimization.

## Concrete plan before creation

Use a compact two-column table. Show shared fields once; retain exact parameters and asset-ID lists for inspection in the authorized conversation/workspace:

- Account, Campaign name, Objective, Web destination or brand/activity.
- Optimization goal, Auction, applicable bidding and billing combination.
- Actual budget level, amount, currency, daily/lifetime basis, recommendation basis and estimated planned spend. Best Practice evidence includes MCP registered country → five-group region → selected Objective.
- Countries, targeting, placements and language.
- Real asset IDs, identity, usable count and remaining gap.
- Start/end time, account timezone and final included delivery date.
- Enabled or disabled-draft intent, and any asset uploads requiring authorization.
- Unverified incentive eligibility, slots and other conditions where applicable.

Keep an exact versioned execution list and budget ledger. Approval must correspond to that list. Analysis or filling a table is not write authorization. Budget-only approval does not authorize uploads, targeting changes or launch. Do not repeatedly ask for confirmation for individual calls implementing the same unchanged approved plan. Confirm only the changed subset when the plan changes.

## Execution

1. Verify permissions, currency/timezone, minimum budgets, asset/identity access, parent status, budget level and goal combinations. Live schemas take precedence over static examples.
2. Refresh mutable preconditions. If critical conditions change, pause that subset and prepare a revised concrete proposal; other unchanged approved items can continue.
3. Create Campaign → Ad Group → Ad, applying only approved fields and enabled/disabled state. Do not assume disabled defaults. If the interface cannot guarantee the approved draft state, stop that subset and explain.
4. Use current request-ID and idempotency requirements. For timeouts or unknown results, query known request/object identifiers before considering another create. Correct clear schema, payment or eligibility errors before retrying; do not retry indefinitely.
5. Preserve successful objects and IDs after partial failure. Do not automatically clean up created parents, roll back or create a duplicate structure. Report remaining steps.
6. Read back budgets, goals, dates, assets and enabled/disabled states. A successful create response does not prove actual delivery.

Report success/skips/failures, verified configuration, review/delivery state and remaining blockers. Use only authorized TT4B and task-required services. Exclude credentials and unrelated personal information from requests. Keep real account data out of this skill package.

## On-demand reporting

Reports do not authorize budget increases, campaign changes or monitoring. Verify current legal metrics/dimensions: Reach uses reach / impressions / CPM / frequency; Traffic Clicks uses clicks / CPC / CTR; LPV uses actual landing page views and corresponding unit cost. Report 6s and 15s Focused View separately; ordinary playback is not a substitute.

Calculate unit cost from total spend divided by corresponding total results within the same scope. A zero denominator is unavailable, not a valid unit cost. Do not sum reach/frequency across days or Campaigns, mix currencies, or double-count total/component rows. Distinguish missing, failed and zero data. Incentive progress requires actual qualifying spend and active delivery days; schedules do not establish completion.
