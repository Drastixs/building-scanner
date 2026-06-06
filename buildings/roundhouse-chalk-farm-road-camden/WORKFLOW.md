# Workflow — The Roundhouse, Chalk Farm Road

## Date
2026-06-06

## Steps

1. Created output directory.
2. Searched Camden planning register (planningrecords.camden.gov.uk) for "Chalk Farm Road" and "Roundhouse". Direct portal access returned HTTP 403.
3. Found planning application 2014/0853/P via site:planningrecords.camden.gov.uk Google search.
4. Accessed Camden document management system at `http://camdocs.camden.gov.uk/CMWebDrawer/PlanRec?q=recContainer:2014/0853/P`. WebFetch confirmed 37 documents listed including floor plans for the proposed annex building.
5. Extracted record IDs for floor plan drawings from the CMWebDrawer document list.
6. Downloaded 5 floor plan PDFs directly via curl from camdocs.camden.gov.uk (no authentication required).
7. Also downloaded the planning officer committee report from camden.moderngov.co.uk (document s34187).

## Outcomes

- **6 PDFs downloaded**: existing/proposed ground floor, first through fourth floor plans, roof plan, and planning officer report.
- All drawing PDFs confirmed genuine (PScript5.dll/Postscript origin, 1 page each, 43–185 KB) — architectural drawings from Urban Space Management for the Roundhouse Annex Building.

## Failures / Issues

- **Roundhouse drum interior floor plans not found.** The original 2004–2006 John McAslan + Partners refurbishment of the Roundhouse building itself predates Camden's digitised planning records. No floor plans for the circular drum structure were retrievable from the online planning register.
- Camden planning portal (planningrecords.camden.gov.uk) returned HTTP 403 to WebFetch and direct browser-style GET. Document downloads from camdocs.camden.gov.uk worked without authentication.
- Application 2022/3646/P (Camden Goods Yard variation) was not relevant to the Roundhouse building itself.
