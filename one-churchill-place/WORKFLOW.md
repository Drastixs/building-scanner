# WORKFLOW — One Churchill Place

## Source
Council: **Tower Hamlets / Canary Wharf**
Portal: https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_register.aspx
Application: `PA/02/00060` (confidence: low)

## What Worked
One Churchill Place (the 32-storey Barclays HQ tower, HOK International, completed 2005) does NOT have a standard Tower Hamlets planning application (PA/ reference) for the main building itself. Exhaustive search of the Tower Hamlets Idox portal (development.towerhamlets.gov.uk) confirmed: the property history for Barclays Bank, 1 Churchill Place, E14 5HP shows only 9 planning applications, all of which are signage/advertisement consent, green roof, or solar PV prior approval — none is the building permission for the 32-storey tower.

The building was erected under Isle of Dogs Enterprise Zone permitted development rights (EZ designated 1982). Canary Wharf buildings in that zone did not require individual planning applications to Tower Hamlets — office use was automatically permitted under the EZ scheme. This was confirmed by a GLA planning report (PDU/2140a/02) for the adjacent 25 Churchill Place, which explicitly states 'there is an existing Enterprise Zone consent on this site' — the same framework applied to One Churchill Place.

The closest planning application found is PA/02/00060 (validated 16 Jan 2002, decided 4 March 2002) for 'Former Parcel Rt4, Churchill Place' — the two-storey Churchill Place retail block, not the Barclays tower. This application has 16 documents including floor plans (refs 550/55108/03, 550/55110/03), a section (550/55114/03) and an RT-04 location plan (55152/01).

The building control record for the tower shell is ref 20/02/15973 (submitted 11 March 2002, decided 7 May 2002) — this is a Building Regulations application, not planning permission.

All signage/advertisement applications for 1 Churchill Place show 'External Decision Issued' status — they were called in by the Secretary of State / GLA due to strategic significance (height of 150.95m). The earliest of these is PA/02/01217 (Aug 2002, signage at 150.95m, decided Nov 2002 — Permit, decided by Canary Wharf agent Montagu Evans on behalf of Barclays Bank Plc).

For original EZ consent records, these would be held at the National Archives or through Tower Hamlets historical planning records (pre-2000), not on the online Idox portal. The portal's online records for Churchill Place address start from 2002 only. No Design and Access Statement was found — DAS was not required for Enterprise Zone developments of this era. No floor plans for the main tower exist in the public online register.

## Search Sequence Used
1. Web search: "One Churchill Place Barclays Canary Wharf planning application floor plans"
2. Council planning portal search for application reference
3. Documents tab inspection for drawing schedule

## What Was Hard / Didn't Work
See `BUILDING.md` — if confidence is `low` or `medium`, the application ref needs manual verification on the council portal.

## Next Steps
- [ ] Verify planning ref `PA/02/00060` on https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_register.aspx
- [ ] Open Documents tab → filter to "Drawings" category
- [ ] Identify GA floor plan set (look for drawing numbers with "GA", "GF", "PROPOSED" in name)
- [ ] Run `dl.sh` adapted from `../Arbor-22-AP-2295/WORKFLOW.md` to batch-download
- [ ] Verify each PDF: `pdfinfo *.pdf`

## Notes
No additional context.
