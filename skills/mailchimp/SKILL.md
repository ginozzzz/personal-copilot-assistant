---
name: mailchimp
description: 'Email marketing automation using Mailchimp. Use for: managing subscribers and audiences, creating and sending email campaigns, reviewing campaign performance reports, managing audience segments and tags. MCP server must be configured with a valid Mailchimp API key.'
argument-hint: 'Task or subscriber details (e.g. add subscribers, send campaign, get report)'
user-invocable: true
---

# Mailchimp Email Marketing

Manage subscribers, audiences, campaigns, and automation using Mailchimp.

## MCP Server

**Package:** `mcp-mailchimp`

**Install:** `pip install mcp-mailchimp` (provides CLI entry point `mcp-mailchimp`)

Configure in `~/Library/Application Support/Code/User/mcp.json`:
```json
{
  "mcpServers": {
    "mailchimp": {
      "command": "uvx",
      "args": ["mcp-mailchimp"],
      "env": {
        "MAILCHIMP_API_KEY": "${input:mailchimp_api_key}"
      }
    }
  }
}
```

**API Key:** Stored in VS Code secrets as `mailchimp_api_key`. Format encodes the data center in the suffix (e.g. `abc123def-us4`). Do NOT set `MAILCHIMP_SERVER_PREFIX`.

## MCP Tools

| Tool | Description |
|------|-------------|
| `mcp_mailchimp_ping` | Validate API key + get account info |
| `mcp_mailchimp_list_audiences` | List all audiences with subscriber counts |
| `mcp_mailchimp_get_audience` | Get audience details + stats |
| `mcp_mailchimp_list_members` | List members of an audience |
| `mcp_mailchimp_get_member` | Get a specific subscriber |
| `mcp_mailchimp_add_or_update_member` | Add or update a subscriber |
| `mcp_mailchimp_archive_member` | Archive (soft-delete) a subscriber |
| `mcp_mailchimp_get_member_activity` | Recent activity (opens, clicks, bounces) |
| `mcp_mailchimp_list_campaigns` | List campaigns |
| `mcp_mailchimp_get_campaign` | Get campaign details |
| `mcp_mailchimp_get_campaign_report` | Get campaign performance metrics |
| `mcp_mailchimp_get_campaign_content` | Get campaign HTML + plain text |
| `mcp_mailchimp_list_automations` | List classic automation workflows |

## Important MCP Limitations

**`add_or_update_member` tags parameter is broken.** The tool sends tags as a plain string, but Mailchimp's API expects `[{name: "tag", status: "active"}]`. Tags are NOT applied when using the MCP tool. **Use the Python script for tag application.**

**`last_name` has a default empty string** that is always sent to the API. Mailchimp rejects empty strings — use `[surname]` as a placeholder when no surname is available.

## Subscriber Management Script

For bulk subscriber operations, use the helper script (uses stdlib only — no external packages):

**Script:** `skills/mailchimp/scripts/add_subscribers.py`

**Usage:**
```bash
python skills/mailchimp/scripts/add_subscribers.py \
  --api-key "your-mailchimp-api-key" \
  --list-id "your-audience-id" \
  --csv subscribers.csv
```

**CSV Format:** `email,first_name,last_name,tags` (header required)
```csv
email,first_name,last_name,tags
jane@example.com,Jane,NA,customer,vip
john@example.com,John,Smith,newsletter
```

**Options:**
- `--status`: Subscription status — `subscribed` (default), `pending`, `unsubscribed`
- `--rate-limit-delay`: Delay between API calls (default: 0.1s)

**Key features:**
- Uses the dedicated tags endpoint (`POST /lists/{id}/members/{hash}/tags`) — the correct Mailchimp method
- Upsert semantics — safe to re-run; existing members are updated, new members are added
- Stdlib only — no `pip install` required

## Tags vs Static Segments

- **Tags** — applied via script or MCP; labels on individual members
- **Static segments** — manually curated lists; members must be explicitly added via Mailchimp UI or the segments API

The script applies tags only. To add members to a static segment, do it manually in Mailchimp.
