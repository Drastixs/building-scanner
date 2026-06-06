# WORKFLOW — 8 Bishopsgate

## Source
Council: **City of London**
Portal: https://www.planning.cityoflondon.gov.uk/online-applications/
Application: `17/00447/FULEIA` (confidence: high)

## What Worked
The building was originally consented as 15/00443/FULEIA (submitted May 2015, approved August 2015, 40-storey scheme). A supersized revision — 17/00447/FULEIA — was registered May 2017 and approved October 2017 by the Planning and Transportation Committee; this is the scheme that was actually built (50/51 storeys, 204m). The site was known as 6-8 Bishopsgate and 150 Leadenhall Street (EC2N 4DA / EC3V 4QT); it was rebranded as 8 Bishopsgate on completion in 2023. Architect: WilkinsonEyre. Developer: Stanhope plc and Mitsubishi Estate London. Structural engineer: Arup. Planning consultant: Gerald Eve. The City of London planning portal (planning2.cityoflondon.gov.uk) was returning HTTP 503 at time of research, so the documents page could not be accessed live. However, a Wayback Machine snapshot from 14 April 2023 (http://web.archive.org/web/20230414210908/...) was successfully fetched for the 15/00443 documents tab (keyVal=NNOCY8FH0L600), yielding 159 documents including 8-part DAS, all floor level plans (Basement up to Level 40), two building sections (A-A and B-B), elevations, site location plan, and roof plan. The 17/00447 application's keyVal was not found in the Wayback Machine cache; its documents are likely on the same portal under a different keyVal. The documents URL listed (keyVal=NNOCY8FH0L600) refers to the original 15/00443/FULEIA consent; a separate search for 17/00447 on the live portal would be needed once it recovers. The GLA referral for the 2017 revision is at glaplanningapps.commonplace.is/en-GB/planningapps/17-00447-FULEIA but returned 403. The committee report PDF at democracy.cityoflondon.gov.uk/documents/s84785/6-8%20Bishopsgate.pdf covers the 2017 decision but was binary-encoded and unreadable via WebFetch. The DAS URL provided is Part 2 of 8 (Part 1 was not found as a separate file in the 15/00443 document set; the DAS was split into 8 parts numbered 294997-295003).

## Search Sequence Used
1. Web search: "8 Bishopsgate planning application City of London floor plans"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `17/00447/FULEIA` on https://www.planning.cityoflondon.gov.uk/online-applications/
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
