# UK Companies House Lookup Skill

## Purpose
Find surname/full name of a contact when you have their company name but not their personal details.

## Input
- Company name (from email domain or address)
- Optional: partial address to disambiguate

## Approach

### Step 1: Get API Key
Register at https://developer.company-information.service.gov.uk/
Free tier: 600 requests/5 minutes.

### Step 2: Configure MCP Server
Two options:
1. **stefanoamorelli/companies-house-mcp** — 45+ tools, full API coverage
2. **aicayzer/companies-house-mcp** — CLI + MCP, same coverage

MCP config (~/.config/claude/claude_desktop_config.json):
```json
{
  "mcpServers": {
    "companies-house": {
      "command": "npx",
      "args": ["-y", "companies-house-mcp"],
      "env": {
        "COMPANIES_HOUSE_API_KEY": "your_key_here"
      }
    }
  }
}
```

### Step 3: Workflow
1. `search_companies` — find company by name (filter by status=active, location=UK)
2. `get_officers` — retrieve directors list (gives names + addresses)
3. Cross-reference officer address with contact's address for match

### Key Tools
| Tool | Purpose |
|------|---------|
| `search_companies` | Find company by name |
| `get_officers` | List current directors (names + addresses) |
| `get_appointments` | All companies an officer has served |
| `officer_network` | Map director's company connections |

## CLI Setup
```bash
npm install -g companies-house-cli
ch config set-key YOUR_API_KEY
```
Or: `export COMPANIES_HOUSE_API_KEY=your_key`

## CLI Commands
```bash
ch search "Company Name"                    # Find company
ch officers COMPANY_NUMBER                  # Current officers
ch officers COMPANY_NUMBER --all            # All officers (incl. resigned)
ch report COMPANY_NUMBER                    # Full report
ch check COMPANY_NUMBER                     # Due diligence scan
ch network "Director Name"                  # Director's other companies
```

## Workflow (3 steps)
1. `ch search "Company Name"` → get company number
2. `ch officers COMPANY_NUMBER --all` → directors with addresses
3. Match address → surname found

## Verified (2026-03-31)
| Input | Result |
|-------|--------|
| United Blinds (UK) Ltd | #07421966, Director: Leiming Yu |

## MCP Server
- Package: `companies-house-mcp` (aicayzer) — 37 tools
- Tools: search_companies, get_officers, get_appointments, officer_network, company_report, etc.
- Rate limit: 600 req/5 min
