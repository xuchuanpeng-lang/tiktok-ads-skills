# Brand Ads BFCM Planner

Plan TikTok 2026 Black Friday Brand Ads for **Reach**, **Traffic (Clicks / Landing Page View)** and **Video Views (6s / 15s Focused View)** using TikTok for Business MCP.

Brand Ads BFCM Planner reviews relevant running Campaigns, recommends budgets and creative quantities, and prepares Campaign creation or adjustments for confirmation. Its installable directory is `skills/tiktok-brand-ads-bfcm-planner`.

## Install

Copy this prompt into an AI assistant that supports installing skills from GitHub:

```text
Install tiktok-brand-ads-bfcm-planner from:
https://github.com/xuchuanpeng-lang/tiktok-ads-skills/tree/main/skills/tiktok-brand-ads-bfcm-planner

Download the complete skill directory, including SKILL.md, agents, references, scripts and all six bundled Benchmark CSV files. Use the installation mechanism supported by this assistant. If already installed, check for local customizations and report conflicts before updating.
```

Use the directory URL to identify the skill to install. Installation support varies by assistant. The ZIP is an optional download artifact.

- [Installable skill directory](skills/tiktok-brand-ads-bfcm-planner)
- [Usage guide](skills/tiktok-brand-ads-bfcm-planner/README.md)
- [Complete ZIP package](brand-ads-bfcm-skill.zip)

## Connect TikTok for Business

Configure the TikTok for Business MCP server using your assistant's supported connection flow and authorize the intended advertising account:

```text
https://business-api.tiktok.com/open_mcp/tt-ads-mcp-layer
```

[Official connection guide](https://business-api.tiktok.com/portal/docs/how-to-connect-to-tiktok-for-business-mcp-server/v1.3)

Installing the skill does not create the MCP connection or grant advertising-account access. Campaign creation and adjustments require confirmation of the concrete plan and live configuration readback.

## Start planning

```text
Use tiktok-brand-ads-bfcm-planner to prepare my Brand Ads Black Friday plan. Review my account and recommend budgets and creatives before changing anything.
```

The skill supports existing Campaign review, new Campaign preparation, registered new advertisers and on-demand reports. Benchmark recommendations use confirmed delivery countries; new-campaign Best Practice uses the account's registered country. Default advertiser-facing language is English unless another language is requested.

BFCM dates are **November 12–30, 2026, UTC+0**. Plans use the customer's confirmed remaining dates. Benchmark references are not outcome guarantees.

## Repository layout

```text
skills/
  tiktok-brand-ads-bfcm-planner/
    README.md
    SKILL.md
    agents/
    references/
      data/
    scripts/
brand-ads-bfcm-skill.zip
```
