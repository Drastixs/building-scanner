# WORKFLOW.md — Old Truman Brewery, Shoreditch

**Planning authority:** London Borough of Tower Hamlets
**Building:** Old Truman Brewery estate, Brick Lane / Hanbury Street / Dray Walk / Wilkes Street, London E1
**Date of research:** June 2026

---

## Summary

The Old Truman Brewery is a privately managed creative estate, not a single permitted building with one planning reference. The site has been continuously adapted since the 1990s under a series of smaller Tower Hamlets applications. The files in this directory were obtained **not from the planning register** but directly from Truman Brewery's letting/venue team — they are internal landlord floor plan PDFs produced in Vectorworks.

This outcome was the result of the planning-register approach hitting a wall: the estate is too fragmented, too incrementally altered, and too well-documented commercially for the public planning drawings to be the most useful source. The landlord route was faster and yielded more operationally accurate plans.

---

## Phase 0 — Building identity

The Old Truman Brewery is not a single building. It is a campus of interconnected Victorian industrial blocks managed by Truman's (the current estate company). Key named blocks:

- **F Block** — the large Events Building spanning the full island block between Brick Lane, Hanbury Street, Wilkes Street and Dray Walk. First floor (~50,000 sq ft across rooms T1–T5) and second floor (~31,000 sq ft across S2–S5) are primary events spaces. Ground floor has a mix of retail, market, and office tenancies.
- **Block O / Boiler House** — 152 Brick Lane. The former boiler house with its distinctive chimney, now an events and office venue. Ground floor + mezzanine.
- Other blocks (Dray Walk, Ely's Yard, etc.) were not researched in this pass.

The planning identity is complicated. Applications are filed against individual sub-plots under various predecessors and under the current estate management company. There is no single "Truman Brewery" masterplan application analogous to a Southwark development consent.

---

## Phase 1 — Tower Hamlets planning register

**Register:** Tower Hamlets runs Idox Public Access at `https://www.towerhamlets.gov.uk/lgnl/planning_and_building_control/planning_applications/planning_applications.aspx` (links to the Idox portal at `https://development.towerhamlets.gov.uk/online-applications/`).

**What worked:**
- The register is accessible and uses the same Idox URL patterns as Southwark and most other UK councils.
- Searches by postcode (E1 6QL) return results, though many are for small alterations (signage, shop-front changes, licences) rather than full floor-plan submissions.

**What failed:**
- Searching by "Truman Brewery" returns a very large number of minor applications spanning decades — it is not practical to trawl them for a floor-plan-grade drawing set without a specific application reference.
- The complex's history of incremental adaptation means no single application covers the whole estate. F Block's floor plans, for instance, reflect decades of ad hoc internal subdivision, none of which necessarily required a full planning submission with GA drawings.
- The publicly filed drawings (where they exist) tend to be elevation/façade or signage drawings — not the interior general arrangement plans that are most useful for understanding room layout and circulation.

---

## Phase 2 — Direct landlord route

**What worked — best information source:** The Truman Brewery letting team publishes and shares floor plans directly as part of their letting/venue-hire process. These are produced in Vectorworks by the estate's in-house or retained architect and are of high quality: they include lease boundary, ceiling heights, beam positions, service point locations (power, water, lifts, loading) and accurate dimensions.

Contact point on the plans: **monika@trumanbrewery.com**, 91 Brick Lane, London E1 6QL, tel 0207 770 6011.

The venue brochures (F Block first floor, second floor) are also publicly available or easily obtained by emailing the events team at events@trumanbrewery.com (or equivalent). They combine marketing copy with real floor plans and are the closest equivalent to a DAS + GA plan pack for a building of this type.

**What failed:** The brochures do not include a Design & Access Statement equivalent — there is no narrative explaining entrance hierarchy, circulation strategy, or front-of-house vs back-of-house intent. For that analysis you would need to either: (a) find a specific Tower Hamlets application for a significant alteration to F Block and read its DAS, or (b) supplement with a site visit.

---

## Phase 3 — File quality and gaps

| File | Coverage | Quality | Source |
|------|----------|---------|--------|
| `block-o-boiler-house-all-floor-plans.pdf` | Block O ground + mezzanine | Good — 7 A3 sheets, dimensioned | Landlord (2021) |
| `block-o-ground-floor-3241-floorplan.pdf` | Block O ground floor | Good — 2 A3 sheets, updated boundary | Landlord (2025) |
| `f-block-first-floor-brochure-2021.pdf` | F Block 1F, all rooms (T1–T5) | Good — venue brochure with plans | Landlord (2021) |
| `f-block-ground-floor.pdf` | F Block ground floor | Good — 11 pages, most detailed | Landlord (2023) |
| `f-block-second-floor-brochure-2021.pdf` | F Block 2F, all rooms (S2–S5) | Good — venue brochure with plans | Landlord (2021) |
| `f-block-t1-exhibition-hall.pdf` | F Block 1F, room T1 only | Unknown — image-only PDF (2005), no text layer | Landlord archive |
| `f-block-t2-plans.pdf` | F Block 1F, room T2 only | Good — 4 A4 sheets, ceiling heights noted | Landlord (2023) |

**Gaps:** No basement drawings. No section or elevation drawings. No ground-floor coverage of rooms T1–T5 individually at the level of detail of the T2 standalone plan. No Design & Access Statement.

---

## Lessons / replicability notes

1. **For managed event venues and creative campuses, go to the letting team first.** Planning registers work best for singular consented buildings (offices, residential blocks) where a single application produced a coherent drawing set. Fragmented historic estates like Truman Brewery accumulate their plans informally.

2. **Tower Hamlets Idox works the same way as Southwark.** If you need a specific application's drawings (e.g. for a major alteration with a known planning reference), the workflow from `Arbor-22-AP-2295/WORKFLOW.md` applies without modification: search by address/postcode, open the Documents tab, download GA plans and DAS.

3. **Vectorworks is common for managed venues.** Both Block O and F Block plans were produced in Vectorworks. Files are A3 or A4, scale stated on each sheet, dimensions in millimetres. Quality is high — these are genuine architectural drawings, not sketches.

4. **The 2025 Block O file** (`block-o-ground-floor-3241-floorplan.pdf`, created April 2025) shows a significantly larger lease area (10,266 sq ft vs 6,970 sq ft in the 2021 pack). This likely reflects a boundary renegotiation or a different lettable configuration. Always check file dates — landlord drawings can be revised silently.

5. **The 2005 T1 file** (`f-block-t1-exhibition-hall.pdf`) appears to be an image-only scan with no text layer (pdfinfo reports 0 pages in its logical structure). It renders visually but cannot be text-extracted. For analysis, treat it as a raster image.
