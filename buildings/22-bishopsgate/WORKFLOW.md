# WORKFLOW — 22 Bishopsgate

## Source
Council: **City of London**
Portal: https://www.planning.cityoflondon.gov.uk/online-applications/
Application: `16/01150/FULEIA` (confidence: high)

## What Worked
The primary confirmed planning reference for the built scheme is 16/01150/FULEIA — this is the revised/amended application submitted December 2016 and approved by the City of London Planning and Transportation Committee on 28 February 2017 (17 in favour, 4 against, 1 abstention). It replaced an earlier 2015 approval (committee date 17 November 2015) whose specific reference number could not be recovered via web search alone — the 2015 committee report PDF is hosted at http://static.guim.co.uk/ni/1447780787897/22-Bishopsgate-London-EC2N.pdf. The original Pinnacle scheme (KPF architects) was ref 06/01123/FULEIA (approved April 2006). The City of London planning portal is at planning2.cityoflondon.gov.uk — direct portal SSL certificate errors prevented scraping from this environment. The main committee report PDF for 16/01150/FULEIA is at democracy.cityoflondon.gov.uk but is a compressed binary PDF that cannot be parsed by WebFetch. The keyVal for the documents tab in the planning portal was not recoverable due to the SSL issue; the estimated URL uses a guessed keyVal. Floor plan drawing references were not accessible from publicly available web search results — these would need direct portal access. The architect is PLP Architecture (Karen Cook, co-founder, design lead). Developer consortium: AXA IM Real Assets acquired site February 2015 for ~£550m, retained Lipton Rogers as developer. The 2016 amendment reduced height from 62 storeys (278m) to 59 storeys (255m) due to London City Airport aviation safeguarding constraints. Not a Canary Wharf/LDDC building — fully within City of London jurisdiction.

## Search Sequence Used
1. Web search: "22 Bishopsgate planning application City of London floor plans"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `16/01150/FULEIA` on https://www.planning.cityoflondon.gov.uk/online-applications/
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
