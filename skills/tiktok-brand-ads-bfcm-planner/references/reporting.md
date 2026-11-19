# Lightweight reports on request

Return five parts: scope/definitions, core results, relevant Campaign detail, statuses/comparable changes, limitations. Product/asset detail, trends, BAU and year-over-year expand only when requested. A report request does not authorize optimization, a full creation flow or continuing notifications.

| Branch | Entry and candidate metrics |
|---|---|
| Reach | `report_integrated_get`: `spend`, `reach`, `impressions`, `frequency`, `cpm` |
| Traffic Click | Integrated: `clicks`, `cpc`, `ctr`, spend; LPV auxiliary if available |
| Traffic LPV | Integrated: `total_landing_page_view`, applicable `cost_per_landing_page_view`, or same-scope calculated cost |
| Video Views 6s | Integrated: `engaged_view`, same-scope cost |
| Video Views 15s | Integrated: `engaged_view_15s`, same-scope cost |

Validate metric + dimensions + level + dates at runtime. Do not interpret generic `result/cost_per_result` identically for all goals. Focused View isn't ordinary playback or `video_watched_6s`. Evaluate 6s vs 15s separately. If a metric combination is rejected, explain the unavailable field and retain supported results; don't invent a zero.

Use total cost / total corresponding results, not mean row CPA. Zero denominator → unavailable with an explanation, not free results/infinite growth. Missing differs from zero. Reach/frequency do not add across days/Campaigns. Don't add total rows and component rows twice. Keep currencies, event, attribution, scope and comparable windows aligned; use stable IDs, not name matching.

Non-delivering plans can return all zeros; that is not sufficient evidence of poor performance.

For write completion, first report verified success/skips/failures and exact changes per `execution.md`. Performance reporting requires actual subsequent data. Deeper diagnosis happens only when needed/requested; follow applicable AOS boundaries and prepare a newly confirmed change plan before any writes.
