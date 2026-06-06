# WORKFLOW — One Canada Square

## Source
Council: **Tower Hamlets**
Portal: https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_register.aspx
Application: `PA/24/01241` (confidence: medium)

## What Worked
CRITICAL CONTEXT — NO ORIGINAL BUILDING PLANNING REF EXISTS IN STANDARD FORM: One Canada Square was built 1988-1991 under the Isle of Dogs Enterprise Zone (designated 1982). Under the enterprise zone framework, development conforming to the overall LDDC planning scheme was deemed to have planning consent automatically — the LDDC (not Tower Hamlets LBC) was the planning authority. No traditional PA/XX/XXXXX application reference was issued for the original building. Tower Hamlets' digital planning register only goes back to 2000. The most substantive recent application is PA/24/01241 (Levels 48 & 49, change of use, approved November 2024, applicant: Canary Wharf Management Limited). Its committee report PDF is publicly available on democracy.towerhamlets.gov.uk and lists all drawings. The committee report for PA/24/01241 was directly downloaded from https://democracy.towerhamlets.gov.uk/documents/s244778/PA2401241%20-%20Levels%2048%2049%20One%20Canada%20Square%20Canary%20Wharf%20London%20E14%205AB.pdf and text-extracted — this is the most reliable source found. The Tower Hamlets online planning portal (development.towerhamlets.gov.uk) uses SSL certificate issues that blocked direct access. The PA/25/01807/NC application (Levels 46 & 47) maps to internal key DCAPR_149193 on the planning portal. For original building floor plans and sections, these would need to be sourced from Pelli Clarke & Partners' archive, Adamson Associates' archive, or LDDC/Historic England archive records — not from Tower Hamlets' planning portal. The planning register search page confirmed to point to https://development.towerhamlets.gov.uk/online-applications/ for searches from year 2000 onwards.

## Search Sequence Used
1. Web search: "One Canada Square planning application Tower Hamlets floor plans"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `PA/24/01241` on https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_register.aspx
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
