# TT4B MCP connection validation and setup guidance

Check the connection before first using account data. Answer ordinary knowledge questions without requiring MCP setup. Consult the [official TikTok for Business MCP connection guide](https://business-api.tiktok.com/portal/docs/how-to-connect-to-tiktok-for-business-mcp-server/v1.3).

## Determine current status

1. Discover TT4B tools in the current agent, distinguishing direct tools from layered discovery. No exposed tools establishes only that this session cannot use them, not that the user never configured the service.
2. If tools exist, make a minimal read-only request: prefer an account-access list, or request target-account information when advertiser_id is known. Follow live schemas; never create ads to test connectivity.
3. Report “connection and account access verified” only after a successful response confirms target-account readability. Visible tools or a user saying setup is complete are insufficient alone.

| Result | Response |
|---|---|
| No TT4B tools in this session | Guide setup; if already configured, first check enablement and reload tools |
| Explicitly unauthenticated or expired authorization | Guide reauthorization, then repeat read-only verification |
| Service responds but target account is denied/out of scope | Check advertiser_id, signed-in identity and account permissions; do not label it unconfigured |
| Network error, rate limit or temporary unavailability | Explain the actual error and follow available retry guidance; no repeated setup or unlimited retries |
| Account readable but country missing | Mark registered country unknown and continue under planning.md; this is not connection failure |

## Guide an unconnected user

Reuse known agent information. Ask which agent they use only when unknown and necessary for actionable steps. The official guide links agent-specific configuration instructions; a JSON format is not universal.

1. Add TikTok for Business MCP in an MCP-compatible agent. Select an endpoint suitable for its capabilities:
   - Layered discovery: `https://business-api.tiktok.com/open_mcp/tt-ads-mcp-layer`, for smaller initial tool loads and on-demand discovery.
   - Full disclosure: `https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat`, for agents able to handle the full tool library.
2. Save and enable the service using that agent's configuration method; reload/restart if necessary. Consult the linked agent documentation for exact menus, fields, transport or commands rather than guessing.
3. Have the user sign in to TikTok for Business, review requested permissions and complete authorization. The guide says no developer account or developer app is required. Service configuration alone does not authorize account resources.
4. Return to the agent, discover tools again and perform read-only verification. On success, read registered country and continue region matching and the first-campaign plan, reusing known URL, budget and assets.

For agents using a `mcpServers` JSON configuration, the guide illustrates this structure. Use it as specific configuration only after establishing that the selected agent supports it:

```json
{
  "mcpServers": {
    "tiktok-ads": {
      "url": "https://business-api.tiktok.com/open_mcp/tt-ads-mcp-layer"
    }
  }
}
```

The guide describes a 30-day authorization window; use actual authentication state to determine when reauthorization is needed. Do not ask users to paste passwords, tokens or authorization codes into chat, or store credentials in the plan or skill. Provide guidance rather than changing agent settings or granting permissions unless the user requests that work.

Example when unavailable:

> This session cannot currently use TT4B MCP. Please follow the [official connection guide](https://business-api.tiktok.com/portal/docs/how-to-connect-to-tiktok-for-business-mcp-server/v1.3) to add the service in your agent and authorize it with TikTok for Business. I will then verify account access through a read-only request, read your registered country and match the applicable Best Practice.

While disconnected, gather goals and prepare independent recommendations. Keep MCP-dependent country, region and currency unverified; do not claim matching is complete. Connection authorization does not replace confirmation of the concrete advertising plan.
