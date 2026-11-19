# Brand Ads BFCM Planner

Plan TikTok 2026 Black Friday Brand Ads for **Reach**, **Traffic (Clicks / Landing Page View)** and **Video Views (6s / 15s Focused View)**.

Brand Ads BFCM Planner reviews relevant running Campaigns, diagnoses applicable issues, recommends budgets and creative quantities, and prepares Campaign creation or adjustments for confirmation. Advertising writes require a concrete confirmed plan and live configuration readback.

## Install with your AI assistant

Copy this prompt into an assistant that supports installing skills from GitHub:

```text
Install the complete tiktok-brand-ads-bfcm-planner skill from:
https://github.com/xuchuanpeng-lang/tiktok-ads-skills/tree/main/skills/tiktok-brand-ads-bfcm-planner

Download the entire skill directory, including SKILL.md, agents, references, scripts and all six bundled CSV files. Use the skill installation mechanism supported by this assistant. If it is already installed, compare versions and report any local customization conflicts before replacing them.
```

Use the skill directory URL with an assistant that supports GitHub skill installation. Installation support varies by assistant; a URL alone is not an installation button in every client.

## Connect TikTok for Business

Configure the TikTok for Business MCP server in your assistant and authorize the intended advertising account:

```text
https://business-api.tiktok.com/open_mcp/tt-ads-mcp-layer
```

[Official connection guide](https://business-api.tiktok.com/portal/docs/how-to-connect-to-tiktok-for-business-mcp-server/v1.3)

Installing the skill does not create the MCP connection or grant account permissions.

## Start planning

```text
Use tiktok-brand-ads-bfcm-planner to prepare my Brand Ads Black Friday plan. Review my account and recommend budgets and creatives before changing anything.
```

## Contents

- `skills/tiktok-brand-ads-bfcm-planner/SKILL.md`: skill entrypoint.
- `agents/`: display metadata inside the skill directory.
- `references/`: Objective guidance, execution rules, on-demand reports and six bundled Benchmark CSV files.
- `scripts/`: read-only budget, creative-count, Benchmark lookup and validation helpers.

Version: **1.1.1**. BFCM dates: **November 12–30, 2026, UTC+0**. Use actual remaining customer dates. Default advertiser-facing language is English unless another language is requested.

Benchmark data supports matched recommendations rather than outcome guarantees. Exact country-region mappings and data gaps are documented in the skill. Live tool schemas, permissions and account eligibility must be verified before execution.
