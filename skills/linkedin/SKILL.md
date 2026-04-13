---
name: linkedin
description: 'Professional networking research for B2B sales and customer discovery. Use for: finding company employees and decision-makers, mapping professional networks, researching prospects before outreach, discovering company growth signals (hiring, promotions), verifying professional backgrounds, finding mutual connections for warm introductions.'
argument-hint: 'Person name, company, or professional topic to research'
user-invocable: true
---

# LinkedIn Research

Research professionals and companies on LinkedIn for B2B sales, customer discovery, and due diligence.

## MCP Server

**Package:** `linkedin-mcp` (RapidAPI-based)

Configure in `~/Library/Application Support/Code/User/mcp.json`:
```json
{
  "mcpServers": {
    "linkedin": {
      "command": "npx",
      "args": ["-y", "linkedin-mcp"],
      "env": {
        "RAPIDAPI_KEY": "${input:linkedin_rapidapi_key}"
      }
    }
  }
}
```

**Get RapidAPI Key:**
1. Sign up at [rapidapi.com](https://rapidapi.com)
2. Search for **"LinkedIn Profile Scraper"** (by Aicayzer)
3. Subscribe to free tier (100 requests/month)
4. Store the key via VS Code command: **Preferences: Open Remote Settings (JSON)** and add:
   ```json
   "linkedin_rapidapi_key": "your_key_here"
   ```

## Tools (83 available)

| Category | Tools |
|----------|-------|
| Profile | Search profiles, get details, mutual connections |
| Company | Search companies, get employees, jobs, insights |
| Connection | List 1st/2nd/3rd connections, invitations |
| InMail | Send messages, view sent messages |
| Profile Views | See who's viewed your profile |
| Search | People search (requires RapidAPI for full access) |
| Invite | Invite people to connect |
| Post | Create posts, get comments, react |
| Scraper | RapidAPI-based data extraction |

## Procedures

### Research a Company
1. `company_search` by company name
2. `company_get_employees` to list staff
3. `company_get_jobs` for recent hires/growth signals
4. Cross-reference with Companies House for directors

### Find Decision-Makers
1. `company_get_employees` for target company
2. Identify by title (CEO, CTO, Director, Head of...)
3. `profile_get` for full profile details
4. Check mutual connections

### Warm Outreach Prep
1. Find person via `profile_search`
2. `profile_mutual_connections` to identify warm contacts
3. Note shared groups/interests for personalization

## Limitations

| Feature | Cost |
|---------|------|
| Profile/company search | Free (limited) or RapidAPI Pro ($50/mo) |
| Messaging | Free |
| Posting | Free |
| Analytics | Free |

## Verified (2026-03-31)

| Search | Result |
|--------|--------|
| London Blind Co | Not yet tested |
