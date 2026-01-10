# Polymarket Link Format Specification

## Problem Description

Generated Polymarket links return "Oops...we didn't forecast this" error page, even when HTTP status code is 200.

## Root Cause

Polymarket API returns two different slugs:

| Field | Name | Usage |
|------|------|------|
| `slug` | Market Slug | Market identifier, **cannot be used for URL** |
| `events[0].slug` | Event Slug | Event identifier, **must be used for URL** |

### Example Comparison

```
Market: "Lighter market cap (FDV) >$1B one day after launch?"

API returns:
  slug: "lighter-market-cap-fdv-1b-one-day-after-launch"        ❌ Wrong
  events[0].slug: "lighter-market-cap-fdv-one-day-after-launch" ✅ Correct

Wrong link: https://polymarket.com/event/lighter-market-cap-fdv-1b-one-day-after-launch
Correct link: https://polymarket.com/event/lighter-market-cap-fdv-one-day-after-launch
```

Note the difference: market slug contains `-1b-`, event slug doesn't.

## Why HTTP 200 But Page Errors?

Polymarket frontend is an SPA (Single Page Application):
- All `/event/*` paths return HTTP 200 (returns HTML shell)
- Frontend JS loads and then requests data
- If slug is invalid, frontend displays "Oops" error

**Conclusion: HTTP status code cannot validate link validity.**

## Correct Link Generation Method

```javascript
// ✅ Correct
const getLink = (market) => {
  const events = market.events || [];
  const slug = events[0]?.slug || market.slug;  // Prioritize event slug
  return `https://polymarket.com/event/${slug}`;
};

// ❌ Wrong
const getLink = (market) => {
  return `https://polymarket.com/event/${market.slug}`;
};
```

## API Response Structure

```json
{
  "question": "Lighter market cap (FDV) >$1B one day after launch?",
  "slug": "lighter-market-cap-fdv-1b-one-day-after-launch",
  "events": [
    {
      "slug": "lighter-market-cap-fdv-one-day-after-launch",
      "title": "Lighter Market Cap (FDV) One Day After Launch"
    }
  ]
}
```

## Validation Methods

Can't just check HTTP status code, need to:

```bash
# Method 1: Check if page content contains error
curl -s "https://polymarket.com/event/xxx" | grep -q "didn't forecast" && echo "Invalid"

# Method 2: Compare slug returned by API
curl -s "https://gamma-api.polymarket.com/markets?slug=xxx" | jq '.events[0].slug'
```

## Affected Files

When fixing, check link generation logic in these files:

- `scripts/csv-report-api.js`
- `scripts/csv-report.js`
- `signals/*/formatter.js` (if generating links)

## Fix Record

- **Date**: 2024-12-31
- **Issue**: csv-report-api.js uses `m.slug` to generate links
- **Fix**: Changed to `m.events[0]?.slug || m.slug`

---

**Rule: Any code generating Polymarket links must use `events[0].slug`, not `slug`.**
