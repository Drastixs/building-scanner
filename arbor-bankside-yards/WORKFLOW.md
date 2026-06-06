# WORKFLOW — Arbor — Bankside Yards

## Source
Council: **Southwark**
Portal: https://planning.southwark.gov.uk/online-applications/
Application: `18/AP/3696` (confidence: high)

## What Worked
Planning history confirmed via Southwark Cabinet appendix document (moderngov.southwark.gov.uk/documents/s104205/Appendix D Description of site planning and public benefits.pdf), which states explicitly: "a shared basement has been constructed on BYW and construction of what is referred to Building 3 is far advanced; pursuant to a reserved matters permission ref 18/AP/3696." The outline permission 12/AP/3940 was granted 28 March 2014. 18/AP/3696 is the reserved matters (appearance, access, landscaping, layout, scale) for Building 3 (also known as Ludgate C or Arbor), decision dated 18 December 2019. A related condition discharge application 21/AP/2840 at Sampson House describes itself as "Discharge of Condition 19 for external materials (relating to Building 3, formerly Ludgate House C only) for planning permission 18/AP/3696 dated 18/12/2019." Secondary refs: 12/AP/3940 = outline consent (2014); 18/AP/1702 = amendment to 17/AP/2286; 18/AP/1316 = condition discharge; 18/AP/1603 = BYE permission (Sampson House east side, separate 2020 permission); 21/AP/2840 = Condition 19 discharge for Building 3. The older planbuild.southwark.gov.uk portal (casereference=18/AP/3696) returns empty — it is offline. The newer planning.southwark.gov.uk portal says "application is no longer available for viewing — it may have been removed or restricted." Only one doc is indexed on docs.planning.org.uk for the 2024 amended application (case SAJM96KBFVY00): a location plan. No floor plan or DAS drawings were found indexed publicly. The casereference URL is the best known entry point for documents. Note: context clue that 22/AP/2295 (Building 1) already has downloaded documents in the project folder — the same planbuild pattern should work if the portal comes back online, or via a Playwright session. Canary Wharf / LDDC note: not applicable here — this is Southwark Borough entirely, no LDDC involvement.

## Search Sequence Used
1. Web search: "Arbor Bankside Yards Building 3 planning application Southwark floor plans 14/AP"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `18/AP/3696` on https://planning.southwark.gov.uk/online-applications/
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
PDFs already downloaded in Arbor-22-AP-2295/ (22/AP/2295 — Building 1 analogue). Arbor itself = Building 3, refs: outline 12/AP/3940, detailed 2014, amendment 2018 18/AP/3696.
