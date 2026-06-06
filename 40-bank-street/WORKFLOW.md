# WORKFLOW — 40 Bank Street

## Source
Council: **Tower Hamlets / Canary Wharf**
Portal: https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_register.aspx
Application: `PA/20/01832/NC` (confidence: medium)

## What Worked
The Tower Hamlets online planning register (Idox/EXACOM system at development.towerhamlets.gov.uk) was searched by address "40 Bank Street" and returned 11 applications. The earliest is PA/03/01073 (August 2003, satellite dish at roof level) — which is a post-construction installation, not the original building consent. The building was constructed 2000–2003, meaning the original full planning permission predates the online register and was handled under the Canary Wharf Enterprise Zone arrangement. Canary Wharf was developed under a special regime with LDDC (London Docklands Development Corporation) which wound up in 1998; after that, Tower Hamlets took over but the online register only covers applications from ~2003 onwards for this address. The most substantive application on the register is PA/20/01832/NC — "Application for the change of use of part of the ground floor office reception to retail (Class A1/A3/A4 or forthcoming Class E), external alterations, outdoor seating area, change of use of part of the existing car park to provide cycle parking and associated works" at 40 Bank Street and Jubilee Place Car Park, E14 5NR, validated 28 Aug 2020, Status: Decided. This application involved Spring Planning (agent) and Stiff + Trevillion (architect) for Canary Wharf Group. The Tower Hamlets portal has SSL certificate issues preventing direct WebFetch access; browser automation via Playwright was used to retrieve the search results. The original construction planning ref is not available via the online register and would require a manual/archive request to Tower Hamlets Planning department or review of pre-2000 LDDC records. No Design &amp; Access Statement URL could be retrieved due to SSL issues on the portal, but documents should be accessible under the PA/20/01832/NC keyVal=DCAPR_132901 record. The direct documents tab URL is: https://development.towerhamlets.gov.uk/online-applications/applicationDetails.do?keyVal=DCAPR_132901&amp;activeTab=documents

## Search Sequence Used
1. Web search: "40 Bank Street Canary Wharf planning application floor plans"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `PA/20/01832/NC` on https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_register.aspx
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
