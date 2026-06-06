# WORKFLOW — The Stage (Shoreditch)

## Source
Council: **Hackney**
Portal: https://hackney.gov.uk/planning
Application: `2012/3871` (confidence: high)

## What Worked
Planning reference 2012/3871 was confirmed from two GLA strategic referral PDFs (PDU/2975/01 and D&P/2975/02) which explicitly state "planning application no. 2012/3871" and "planning application nos. 2012/3871". The applicant is Plough Yard Developments Ltd, architect is Pringle Brandon Drew Architects. Hackney Council resolved to grant permission in July 2013; Mayor signed off December 2013. A companion Listed Building Consent application 2012/3872 covers alterations to 24-26 Curtain Road. A subsequent revised/amendment application 2015/3453 was decided 01/11/2016. The Hackney planning portal (developmentandhousing.hackney.gov.uk) uses AWS WAF challenge protection that blocks curl/automated access but is accessible via real browser (Playwright confirmed the search page loads). Direct application page URLs take the form: https://developmentandhousing.hackney.gov.uk/planning/index.html?fa=getApplication&reference=2012/3871 — but returns login redirect. Document downloads use: https://developmentandhousing.hackney.gov.uk/planning/?fa=downloadDocument&id=<id>&public_record_id=<id>. The GLA reports confirm a Design & Access Statement and addendum were submitted as part of the 2012/3871 application, and floor plans showing residential unit layouts were reviewed, but individual drawing reference numbers (e.g. PBD-xxx) are not listed in the GLA reports. The actual drawing schedule would require portal access. SkyscraperCity forum thread referenced the old IDOX URL (idox.hackney.gov.uk/WAM/showCaseFile.do?action=show&appType=Planning&appNumber=2012/3871) which is now connection-refused — Hackney has migrated to the developmentandhousing portal.

## Search Sequence Used
1. Web search: "The Stage Shoreditch planning application Hackney floor plans Shakespeare theatre site"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `2012/3871` on https://hackney.gov.uk/planning
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
