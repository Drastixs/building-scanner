# WORKFLOW — One Blackfriars (The Vase)

## Source
Council: **Southwark**
Portal: https://planning.southwark.gov.uk/online-applications/
Application: `12/AP/1784` (confidence: high)

## What Worked
Primary planning ref 12/AP/1784 confirmed from multiple sources: GLA Stage 1 referral report PDU/2894/01 (dated 18 July 2012), Wikipedia, 35percent.org analysis, and Southwark planning portal URL pattern. Application was approved by Southwark planning committee on 10 October 2012, confirmed 14 December 2012. The antecedent application 06/AP/2117 was submitted 30 October 2006 (originally for Beetham Organisation), approved by Southwark July 2007, then subject to Secretary of State public inquiry with permission confirmed March 2009. St George (Berkeley Group) acquired site from administrators in October 2011 and filed the revised 12/AP/1784 application in May 2012. Architect throughout was Ian Simpson / SimpsonHaugh; agent was CBRE. Minor amendment refs: 12/AP/1050 (marketing building 2012) and 12/AP/2608 (three-storey marketing building October 2013). The direct documents URL planbuild.southwark.gov.uk and planning.southwark.gov.uk both return SSL certificate errors when fetched programmatically (unknown certificate verification error), so individual document URLs and floor plan drawing references could not be retrieved. The GLA Stage 1 report (PDU/2894/01) describes the scheme as: 50-storey tower (274 residential units, max height 170m AOD), 6-storey Rennie Street Building, 4-storey Podium Building; 11,267sqm hotel, 52,674sqm residential, 1,316sqm retail, 9,648sqm basement/plant. A Design and Access Statement was submitted with the application (referenced in planning analysis on 35percent.org) but no public direct PDF URL was found. The moderngov.southwark.gov.uk planning committee report for 12/AP/1784 (the October 2012 committee) was not found via search; the only planning committee document found for this site was a 2006 report for ref 06-AP-0974 (a different minor application). Floor plan drawing references could not be extracted without portal access.

## Search Sequence Used
1. Web search: "One Blackfriars Vase planning application Southwark floor plans"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `12/AP/1784` on https://planning.southwark.gov.uk/online-applications/
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
