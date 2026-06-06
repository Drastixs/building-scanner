# WORKFLOW — Tower 42

## Source
Council: **City of London**
Portal: https://www.planning.cityoflondon.gov.uk/online-applications/
Application: `24/01203/FULL` (confidence: medium)

## What Worked
The City of London planning portal (https://www.planning2.cityoflondon.gov.uk/online-applications/) is currently returning HTTP 503 (Service Unavailable) — all paths return IDOX Page Not Found, so no direct document URLs could be retrieved. The planning reference 24/01203/FULL was confirmed from multiple City of London Planning Applications Sub-Committee information packs found at democracy.cityoflondon.gov.uk. The application covers refurbishment works at Tower 42: removal of existing doors and associated canopies on northern and southern elevations, installation of new doors and associated canopies, new canopy and sign over main entrance, and alterations to panels. Applicant is Tower Nominees No.2 Jersey Limited. A non-material amendment (25/00883/NMA) to this permission was approved 25/09/2025. The older reference 05/01076/FULL (approved 06/06/2006) is also associated with Tower 42 and was being discharged against in 2025 (Condition 18 — Plant Noise Impact Assessment). A separate major refurbishment of the atrium and office floors by dMFK with DP9 as planning consultant was underway as of late 2025 but no FULMAJ reference for this was found in any committee documents reviewed — it may be proceeding under prior permissions or a permitted development route given the internal-only scope. The original 1970s planning consent predates the online portal entirely. The council register link and the democracy portal (democracy.cityoflondon.gov.uk) are the best routes to find full document sets once the portal recovers.

## Search Sequence Used
1. Web search: "Tower 42 NatWest Tower planning application City of London"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `24/01203/FULL` on https://www.planning.cityoflondon.gov.uk/online-applications/
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
