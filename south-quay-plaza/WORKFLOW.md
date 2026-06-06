# WORKFLOW — South Quay Plaza

## Source
Council: **Tower Hamlets**
Portal: https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_register.aspx
Application: `PA/14/00944` (confidence: high)

## What Worked
Primary ref PA/14/00944 found immediately via web search — first result on both "floor plans" and "site:towerhamlets.gov.uk" queries. The internal Tower Hamlets portal key is DCAPR_109607 (confirmed by a cached Google result showing the full URL pattern for development.towerhamlets.gov.uk). The portal's SSL certificate is currently invalid/self-signed, so WebFetch cannot directly retrieve the documents tab — the URL pattern is however confirmed from Google's cache. The committee report PDF (democracy.towerhamlets.gov.uk/documents/s62786/...) was successfully parsed via pdftotext after WebFetch returned a binary blob; it yielded the full drawing schedule (A-0-xxxx through A-3+-xxxx series) and document list including the Design and Access Statement and its addenda. Note: the DAS itself is not hosted at a standalone URL in the search results — it is referenced in the application bundle held on the development.towerhamlets.gov.uk portal. Secondary refs identified: PA/15/03073 (SQP4, a third 56-storey tower approved 2016), PA/21/02721 (S73 amendment to SQP2 adding 5 storeys, approved March 2024), DCAPR_135662 (2021 S73 amendment documents on docs.planning.org.uk — returned 403), DCAPR_149335 (2025 S96A application for SQP2 — also 403). The building is not an LDDC/Canary Wharf Enterprise Zone holdover — it falls fully within the Tower Hamlets planning system. Architect is Foster + Partners (confirmed across multiple sources including F+P's own project page). Developer is Berkeley Homes (South East London) Ltd (confirmed from committee report PDF). GLA reference was not returned by any search result in numeric form (GLA Stage 1 review is referenced in the committee report but no PDU/GLA number surfaced).

## Search Sequence Used
1. Web search: "South Quay Plaza Marsh Wall planning application Tower Hamlets floor plans"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `PA/14/00944` on https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_register.aspx
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
