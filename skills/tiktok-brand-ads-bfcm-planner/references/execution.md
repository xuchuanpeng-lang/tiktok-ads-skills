# Plan presentation, confirmation and execution

## Summary first

Default to concise English; on an explicit language request, use that language for explanations while preserving English platform terminology as required by SKILL.md. One current Objective/scenario, short outcome summary plus compact tables; no HTML/image/cards dependency and no action/checkbox column. Show shared account/currency/country/dates once. Do not require each row or field to be re-confirmed.

Historical plans: report checked/eligible/attention/verification counts and the **change set** rather than the full list. Summarize applicable rule/source, before/after daily budget totals, count of Campaigns and actual budget objects, creative quantity/gap and important exceptions. Unchanged budgets get no per-plan keep prompt. All candidates are checked regardless of display length.

Example layout (fill with actual evidence):

“**Key change: increase 32 budget objects across 26 Campaigns; current eligible creatives can be used now.** Of 48 relevant running plans, 40 passed applicable checks; 8 need attention or verification.”

| Item | Proposed plan |
|---|---|
| Budget | Exact changed-object daily total before → after and delta, grouped by currency |
| Basis | Lower Benchmark bounds or Objective Best Practice values, each correctly sourced |
| Creatives | Same-scope available / absolute phase reference / supplement |
| Exceptions | Counts and main supported reasons; excluded from this batch |
| Other changes | Only specifically proposed dates, reactivation, with impacts |

Ask whether to apply this **specific batch**. User can confirm the summary without reading every ID. Exact detail remains available: Campaign name/ID and a key-change line, then a two-column table including actual Ad Group/Campaign budget ID, layer, current→proposed value, currency, source, dates and separate non-budget changes. Do not use a vague “all good campaigns” as the execution list.

New plans: “New campaigns: X.” For each, lead with key configuration then a two-column table: name/promoted object, Objective/destination, optimization goal and Auction settings, actual budget layer/amount and interval/source, real creative/identity IDs or a stable exact list reference, audience/placement/bidding, dates/timezone and enabled/disabled intent. Show shared settings/assets once, with exact references. Unknown required fields remain missing; an example is not executable data.

## Account data

Use account information only for the current authorized advertising task. Send only necessary fields to the authorized TT4B MCP operations and services required by that task. Do not include credentials, unrelated conversations, personal contact details or unrelated account information in tool requests.

Keep only the task information needed for planning, confirmed execution and readback in the current authorized conversation or workspace, under its existing access and retention controls. Exact advertiser/object IDs may be necessary for those actions.

Do not place real account data, conversation records or Ads Manager screenshots in this skill package or its GitHub repository. A request to plan or report does not authorize sending account information to other people, public links, external storage or unrelated services. Any such sharing requires explicit authorization for the specific information and destination; minimize the content and redact unrelated identifiers, personal details and confidential information. Normal use of the already-authorized TT4B connection remains within the advertising task’s confirmed scope.

## Fixed execution batch

Before presenting totals, form a structured, locally retained batch containing:

- A stable batch ID/version, advertiser and selected Objective/scenario.
- For each actual write object: type/ID, Campaign parent, actual budget level, currency, current value, exact proposed value, comparison/scope basis, dates/timezone, source and required preconditions.
- Explicit field changes and planned enabled/disabled state. New creation has exact proposed fields and real asset IDs, not a source-plan “copy everything” shortcut.
- Separate entries for any schedule, creative/targeting or status changes. A budget-only batch leaves them untouched.
- Totals computed from these exact distinct write objects, not from an independently sampled report. Shared totals across sequential Objectives also track commitments/remaining budget.

The human-readable summary and inspectable details must refer to that retained exact batch. Keep it available through execution/readback; if state is lost or cannot be reconstructed, re-read and re-present a concrete plan before writing. Do not silently add newly found Campaigns after confirmation. Editing or looking at a table is not write authorization.

Confirm only meaningful gaps or changes. Existing explicit approval of an unchanged concrete plan need not be requested for each tool call; follow any host/tool-required review steps. Broad “help plan” does not authorize writes. The customer can approve part: execute only that part.

## Preconditions and tool calls

1. Inspect live write/read schemas and permissions, account eligibility, valid enum combinations and applicable minimums. Never fabricate parameters from UI names. Discovery/reads are not authorization to grant access.
2. Refresh mutable status, budget and affected dependencies immediately before execution. Changed critical preconditions/current values → skip that object and explain; other unchanged approved entries can continue. Revised IDs/amounts/enablement require confirmation of the changed subset.
3. Execute the confirmed field delta only. Budget batches preserve targeting, bids, structure, promoted scope and creatives. Confirming a supplement count does not authorize asset upload. Restoring paused plans, new authorizations, deletion/rollback are explicit separate actions.
4. Use current tool request-ID/idempotency requirements. For creation, Campaign → Ad Group → Ad as applicable. Do not treat tool-created drafts as permission to launch. Where no launch state was confirmed, present a disabled-draft default in the plan, not a silent enabled launch.
5. Partial failure keeps successful writes and exact IDs. Do not auto-delete created parents or undo existing budgets. Timeout/unknown result: query by stable request/object identifiers before considering retry. Do not repeat an uncertain create blindly or enter an unbounded retry loop. Clear schema/payment/eligibility errors need correction, not repeating unchanged values.
6. Read back requested settings and relevant statuses. Distinguish object created, configuration matches, pending/rejected review, enabled/disabled and actual delivery. Successful create response alone is not “live.”

Multiple API calls can implement a bulk operation; do not promise atomic execution or a nonexistent batch endpoint. If a supported read or necessary verification is missing, state exactly what remains unverified rather than claiming completion.

## Completion

Summarize successful/skipped/failed objects, verified budget delta, remaining work and important statuses. Provide IDs/details on request; do not hide partial failure behind a successful total. “Creatives to add” remains advice unless a separately authorized asset write actually succeeded. On finishing historical work, optionally offer new-campaign help; don't automatically create one or make every problem plan's repair a prerequisite to completing other tasks.
