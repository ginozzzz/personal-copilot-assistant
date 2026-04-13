---
name: uk-companies-house
description: 'Company and customer research using UK Companies House data. Use for: finding company details by name or postcode, retrieving directors and officers, mapping company networks, due diligence on UK businesses, finding contact surnames from company names, verifying company registration, checking company status and history.'
argument-hint: 'Company name or postcode to research'
user-invocable: true
---

# UK Company & Customer Research

Research UK companies using Companies House data. Combines company search, officer lookup, and network mapping for customer due diligence.

## MCP Server (Primary)

**Package:** `companies-house-mcp` (aicayzer)

Configure in `~/Library/Application Support/Code/User/mcp.json`:
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

## Tools

| Tool | Purpose |
|------|---------|
| `search_companies` | Find company by name |
| `advanced_company_search` | Filter by postcode, status, type |
| `get_officers` | List current directors (names + addresses) |
| `get_appointments` | All companies an officer has served |
| `officer_network` | Map director's company connections |
| `get_filing_history` | Company filings and accounts |
| `get_charges` | Mortgages and charges |

## Procedures

### Find Company by Postcode
1. `advanced_company_search` with postcode filter
2. `get_officers` on company number
3. Cross-reference officer address with target contact

### Find Company by Name
1. `search_companies` by name
2. Refine with `advanced_company_search` if multiple results
3. `get_officers` for contact details

### Company Network Mapping
1. `get_officers` for company
2. `officer_network` on key director
3. `get_appointments` to find related companies

## CLI Fallback

```bash
npm install -g companies-house-cli
export COMPANIES_HOUSE_API_KEY=your_key
ch search "Company Name"
ch officers COMPANY_NUMBER
ch network "Director Name"
```

## Verified (2026-03-31)

| Search | Result |
|--------|--------|
| DA7 5AF | London Blind Co. Ltd #05080103, 205a Long Lane, Bexleyheath |
| United Blinds (UK) Ltd | #07421966, Director: Leiming Yu |

