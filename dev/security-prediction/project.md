# Security Prediction

Map and predict a target building's physical security mechanisms using OSINT + standards-based inference.

## Goal

Given a company name and/or address, produce a confidence-scored map of:
- Security vendors in use
- Hardware types (cameras, access control, guards)
- Predicted interior/exterior placement

## Data Sources

| Source | Method | Confidence |
|--------|--------|------------|
| Planning Applications / Building Permits | Search local council portals (UK) or municipal permit DBs (US) for address. Look for security schematics, door schedules, device placement docs. | 85–90% |
| Job Postings | LinkedIn/Indeed — job specs name vendors (Lenel, Genetec, Avigilon, Axis). Confirms product family in use. | 70–80% |
| Standards-Based Prediction | BS EN 50132 / IEC 62676 / ISO 27001 physical controls define placement rules. Compliant orgs are formulaic. | 65–75% |
| Google Street View / Maps | Visible cameras, access readers, guard booths, roof hardware. High accuracy exterior, ~50% interior inference. | 50–70% |
| Shodan / Censys | Search company ASN/domain IP ranges for camera banners (port 554 RTSP, HTTP banners). Confirms vendor, not placement. | 40–60% |

## Combined Accuracy Estimate

- Exterior: ~85% (permits + street view + standards)
- Interior: ~60–70% (degrades with retrofits, legacy installs, age of plans)

**Accuracy killers:** plans >5 years old, tenant fit-outs post-permit, non-compliant installs, NAT/VPN hiding Shodan results.

## Investment / Partnership Intel

- Crunchbase / PitchBook / CB Insights — check funding rounds and partnership press releases for named security vendors
- Search: `"[company] + selected [vendor] for"` or `"[company] + Genetec/Lenel/Avigilon"`

## Prediction Pipeline (proposed)

1. Input: company name + address
2. Fetch planning applications → extract device schedule if present
3. Scrape job postings → extract vendor mentions
4. Shodan query on company IP ranges → confirm vendor, firmware
5. Pull Street View imagery → detect visible hardware
6. Cross-ref against BS EN 50132 placement standards for building type
7. Output: confidence-scored placement map (exterior confirmed, interior predicted)

## Open Questions

- Can we automate planning portal scraping per-region?
- Street View camera detection — use CV model (YOLO) to auto-tag hardware?
- How to handle buildings with no public planning data?
- Scoring model: how to weight conflicting signals?
