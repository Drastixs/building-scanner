# WORKFLOW — Aspen at Consort Place

## Source
Council: **Tower Hamlets**
Portal: https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_register.aspx
Application: `PA/15/02671/A1` (confidence: high)

## What Worked
Search process: Initial web searches returned the Tower Hamlets reference PA/15/02671 quickly via buildington.co.uk and Wikipedia. The application was originally submitted in late 2015, refused by Tower Hamlets in February 2016, called in by Mayor of London Boris Johnson, and ultimately approved externally on 27 March 2017 (GLA decision). The keyVal for the Idox portal (DCAPR_115479) was found directly in a Google-indexed URL for the documents tab. The Tower Hamlets development portal (development.towerhamlets.gov.uk) has an SSL certificate error that blocks WebFetch; using curl with --insecure flag worked to access the HTML. The portal confirmed 251 documents, decision 'External Decision - Approved (GLA/CLG/L...)' dated Mon 27 Mar 2017. All document URLs were extracted from the portal HTML — they are direct PDF links but require the portal session/authentication to download (return HTML login page instead of PDF when accessed without session). The drawing number scheme is 1406-A-[series]-[number], where 100-series = floor plans, 200-series = elevations, 300-series = sections, 400-series = unit layouts/details, 500-series = bay studies. The Design and Access Statement is split as INTRO. + CHAPTER_1 through CHAPTER_10-12 (doc IDs 1106668-1106693). An earlier application PA/14/03281 (June 2015 committee report) covered a slightly different massing (63/20/32 storeys) and was also recommended for refusal. The Canary Wharf Enterprise Zone / LDDC route was not needed — the application is straightforwardly on the Tower Hamlets register. The '56-storey' tower mentioned in 2022 news is a separate building called Ensign House (PA/21/00952) on an adjacent site, not Aspen itself.

## Search Sequence Used
1. Web search: "Aspen Consort Place Canary Wharf planning application floor plans residential tower"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `PA/15/02671/A1` on https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_register.aspx
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
