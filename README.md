# TikTok Ads Skills

Two skills for planning and setting up TikTok Brand Ads with TikTok for Business MCP (TT4B MCP). Both support ordinary Auction Reach, Web Traffic (Clicks / Landing Page View) and Video Views (6s / 15s Focused View).

## Choose a skill

| Skill | When to use it | Installable directory | Download |
|---|---|---|---|
| **Brand Newbie Ads Planner** | Set up a new advertiser's first Brand Ads campaign according to Best Practice, with guidance on objectives, budgets, targeting, creatives and schedules. | [brand-newbie-ads-planner](skills/brand-newbie-ads-planner) | [ZIP](brand-newbie-ads-planner.zip) |
| **Brand Ads BFCM Planner** | Prepare 2026 Black Friday Brand Ads: review relevant running campaigns, recommend budgets and creative quantities, and prepare new campaigns or adjustments. | [tiktok-brand-ads-bfcm-planner](skills/tiktok-brand-ads-bfcm-planner) | [ZIP](brand-ads-bfcm-skill.zip) |

Each directory is a complete, independently installable skill. Use its directory URL for assistants that support installation from GitHub. ZIP files are optional download packages.

## Install

Copy the prompt for the skill you need into an assistant that supports GitHub skill installation. Installation support varies by assistant.

### Brand Newbie Ads Planner

```text
Install brand-newbie-ads-planner from:
https://github.com/xuchuanpeng-lang/tiktok-ads-skills/tree/main/skills/brand-newbie-ads-planner

Install the complete directory, including SKILL.md, agents, references and the bundled country-to-region CSV.
```

[Usage guide](skills/brand-newbie-ads-planner/README.md) · [Skill instructions](skills/brand-newbie-ads-planner/SKILL.md)

### Brand Ads BFCM Planner

```text
Install tiktok-brand-ads-bfcm-planner from:
https://github.com/xuchuanpeng-lang/tiktok-ads-skills/tree/main/skills/tiktok-brand-ads-bfcm-planner

Install the complete directory, including SKILL.md, agents, references, scripts and all six bundled Benchmark CSV files.
```

[Usage guide](skills/tiktok-brand-ads-bfcm-planner/README.md) · [Skill instructions](skills/tiktok-brand-ads-bfcm-planner/SKILL.md)

## Connect TikTok for Business

Configure TT4B MCP in your agent and authorize the intended advertising account using the [official connection guide](https://business-api.tiktok.com/portal/docs/how-to-connect-to-tiktok-for-business-mcp-server/v1.3).

For layered, on-demand tool discovery, the service address is:

```text
https://business-api.tiktok.com/open_mcp/tt-ads-mcp-layer
```

Installing a skill does not establish the MCP connection or grant account access. Before using account data, verify the connection, authorization and target-account access through a read-only request. Brand Newbie Ads Planner includes setup guidance when the connection is unavailable.

## Start planning

### First campaign

```text
Use $brand-newbie-ads-planner to set up my first TikTok Brand Ads campaign according to Best Practice. Recommend the objective, budget, targeting, creatives and schedule, and show the concrete plan before making changes.
```

### 2026 Black Friday

```text
Use $tiktok-brand-ads-bfcm-planner to prepare my Brand Ads Black Friday plan. Review my account and recommend budgets and creatives before changing anything.
```

## Planning rules

- Advertiser-facing replies default to English unless another language is explicitly requested.
- New-campaign Best Practice uses the account's registered `country`, read through MCP and mapped to NA, EUI, METAP, LATAM or APAC. Confirmed delivery countries determine targeting.
- BFCM Benchmark matching uses delivery countries, separately from registered-country Best Practice. Its activity window is November 12–30, 2026, UTC+0; plans respect the customer's confirmed remaining dates.
- The 2026 Q4 Traffic incentive has separate dates and eligibility conditions. Newcomer status alone does not establish eligibility, available slots or a payout.
- Advertising writes require confirmation of a concrete plan and configuration readback. Recommendations do not guarantee delivery or business outcomes.

## Repository layout

```text
skills/
  brand-newbie-ads-planner/
    README.md
    SKILL.md
    agents/
    references/
  tiktok-brand-ads-bfcm-planner/
    README.md
    SKILL.md
    agents/
    references/
    scripts/
brand-newbie-ads-planner.zip
brand-ads-bfcm-skill.zip
```
