# WORKFLOW — Stratford International Quarter

## Source
Council: **Newham**
Portal: https://pa.newham.gov.uk/online-applications/
Application: `10/90641/EXTODA` (confidence: high)

## What Worked
The International Quarter London (IQL), now rebranded as Stratford Cross, sits within the former LLDC (London Legacy Development Corporation) planning area, NOT Newham's standard planning register. The master outline planning permission is 10/90641/EXTODA (an extension of the original 2005 Newham permission P/03/0603). All individual buildings were approved as Reserved Matters Applications (RMAs) under that OPP.

Key findings:
1. The LLDC portal (planning.agileapplications.co.uk/lldc) is now shut down and redirects to the four host borough portals (Newham, Hackney, Tower Hamlets, Waltham Forest). IQL falls under Newham (pa.newham.gov.uk).
2. The most useful document source is the LLDC Planning Decisions Committee meeting archive at lldc-meetings.london.gov.uk — this has full committee reports with floor plans and drawing appendices for each building RMA. Meeting MId=6052 (25 April 2017) covers N22 IQL North; MId=6051 (28 March 2017) covers S9.
3. S5 (FCA) and S6 (TfL) planning refs extracted from committee report text: 14/00482/REM + 15/00002/REM (S5), 14/00483/REM + 15/00003/REM (S6), both approved 2015 LLDC.
4. The Newham portal (pa.newham.gov.uk) has a reCAPTCHA blocking automated searches. LLDC records are being migrated but may not all be available yet.
5. Section 106 agreements are available at queenelizabetholympicpark.co.uk/planning-policy/section-106-library, which confirms refs: 20/00146/OUT (S10), 21/00414/NMA and 21/00416/FUL (S1 and S11), 23/00441/FUL (IQL North/Hadley scheme).
6. The Zonal Masterplan for Zone 2 (IQL South) was ref 11/90463/AODODA (March 2012) superseded by 15/00005/AOD (Sept 2015).
7. Architect for all main IQL office buildings is Rogers Stirk Harbour + Partners (RSHP). Agent was Quod Ltd. Developer is SCBD Ltd (Lendlease/LCR JV).
8. For floor plans specifically: the committee report appendices PDFs (e.g. 05b Combined Appendices at the April 2017 meeting) contain GA plans, sections and elevations but are large PDFs accessed through the LLDC meetings archive.

## Search Sequence Used
1. Web search: "International Quarter London Stratford planning application Newham floor plans"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `10/90641/EXTODA` on https://pa.newham.gov.uk/online-applications/
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
