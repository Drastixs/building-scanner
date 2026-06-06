# WORKFLOW — British Library, Euston Road

## Source
Council: **Camden**
Portal: https://planningrecords.camden.gov.uk/Northgate/PlanningExplorer/
Planning authority: London Borough of Camden (LBC)
Architect: Rogers Stirk Harbour + Partners (RSHP)
Listed building status: Grade I (Colin St John Wilson, 1998)

## Outcome

**Full success — 32 PDFs retrieved.** This is one of the highest-yield scans in the project. The drawing set covers: a complete Block 1 floor plan series (Basement 1 through Level 01 + north elevation), a complete Block 2 floor plan series (Basement 1 through roof, all four elevations, eight cross-sections and longitudinal sections, a location plan), an area schedule, and two Listed Building Consent (LBC) variants of the main public floors. Total file size is approximately 54 MB.

## What Worked Well

Camden's planning portal (Northgate/PlanningExplorer) returned a well-indexed document set for this application. The RSHP drawing numbering convention is clean and self-describing — each filename encodes the drawing number, type prefix (P = plan, E = elevation, S = section), and a floor/orientation label — which made selecting the right documents straightforward without needing to open every file first.

The scheme is a major public institution extension touching a Grade I listed building, which means the planning submission was unusually complete: separate LBC drawings (`LBC_RSHP-P-2100`, `LBC_RSHP-P-2101`) were lodged alongside the full planning drawings, the application included an area schedule (`BL_AreaSchedule.pdf`), and the section set is extensive (eight cuts: four transverse C-series, four longitudinal L-series). High-profile public projects at listed buildings tend to produce richer drawing sets than speculative commercial schemes — this held true here.

The two-block structure of the scheme (Block 1 = existing campus, Block 2 = new extension) was immediately legible from the filenames, making it easy to understand the scope without a drawing register. Block 2 drawings are the most useful for interior-design study: they show the full vertical stack from basement plant to roof, with public entrance levels (UG) clearly distinguished from service levels (B1/LG) and office/research levels above.

## What Didn't Work / Limitations

No significant failures were encountered during download. The standard caveats for Camden apply: the Northgate portal requires an active browser session for some document endpoints (direct URL access may redirect to a login page), so a Playwright/browser-based fetch approach is more reliable than raw `curl`. Rate limiting was not encountered at the scale of 32 files, but back-off between downloads is still advisable as a precaution.

The downloaded set does not include a Design & Access Statement (DAS), which would normally be the first document to read for entrance strategy and circulation narrative. It is likely present in the full application document set but was not downloaded in this batch. If the DAS is needed, re-open the Camden portal documents tab and filter by document type to locate it — it will typically be a multi-part PDF with "Design and Access" in the title.

The area schedule (`BL_AreaSchedule.pdf`) is a single-page summary, not a full room-by-room schedule, so it gives floor-area totals but not individual room names or use classifications. For room-level programme, the floor plan GAs and the DAS are the primary sources.

## Where the Best Information Was Found

The Block 2 upper ground floor plan (`RSHP-P-1150-P-UG_Block2_UpperGround.pdf`) and Level 01 plan (`RSHP-P-1151-P-01_Block2_Level01.pdf`) are the key documents for entrance and front-of-house circulation — these show how the public enters, where reception sits, and how the lobby transitions to the floors above. The LBC equivalents (`LBC_RSHP-P-2100`, `LBC_RSHP-P-2101`) add heritage-context annotations on top of the same layouts.

The longitudinal sections (L01–L04, `RSHP-P-1305` to `RSHP-P-1308`) are the most revealing for understanding vertical relationships between the public programme, the existing library courtyard, and the new extension — in particular how the extension ties into the existing Grade I structure at multiple levels. The transverse sections (C01, C02, C04, C05) cut across the narrower dimension and expose floor-to-floor heights, structural bays, and the relationship between public and back-of-house zones.

The area schedule is a useful sanity-check document: it confirms total floorspace split by use (e.g. public, office, plant) without needing to scale off individual drawings.

## Search Sequence

1. Camden planning portal address search: `96 Euston Road NW1`
2. Application identified; opened Documents tab
3. Filtered to drawing documents — RSHP-P-xxxx series identified
4. Downloaded full plan, elevation, and section series for both blocks plus LBC variants and area schedule
5. Verified file integrity (PDF headers, file sizes)

## Notes

- This is a listed building extension, not a new-build commercial scheme. The Grade I listing means the planning submission is subject to Historic England scrutiny and is correspondingly more detailed and better documented than typical commercial applications.
- The `LBC_` prefix documents are the Listed Building Consent versions of floor plans — submitted as a parallel consent application to the main planning application. Both sets were publicly available.
- Drawing numbers suggest gaps in the sequence (e.g. no Level 03–06 plans downloaded for Block 2) — these may exist in the full document set if those levels follow the same floor plate and were submitted as a typical-floor plan rather than individual sheets.
- The area schedule filename (`BL_AreaSchedule.pdf`) uses a different prefix convention (no RSHP-P-xxxx number), suggesting it may have been authored by the British Library project team rather than RSHP directly.
