# Workflow — Royal Institution, 21 Albemarle Street

## Date
2026-06-06

## Steps

1. Created output directory.
2. Searched City of Westminster planning register (idoxpa.westminster.gov.uk) for "21 Albemarle Street". Initial site search returned too many results.
3. Searched by application reference `25/01386/FULL` — found keyVal `SSJN2VRPLGE00`.
4. Fetched the documents tab for keyVal `SSJN2VRPLGE00` — 68 documents listed including existing floor plans (LGF through 5th floor), proposed floor plans, cross-sections, long sections, elevations, heritage impact assessment, conservation plan, design & access statement.
5. Downloaded existing floor plans (LGF–5th) plus cross sections, long section, and proposed ground/LGF/first/second floor plans via curl with session cookie.
6. Separately downloaded the Royal Institution's own venue hire floor plans PDF from https://venue.rigb.org/sites/default/files/attachments/Ri%20Floor%20Plans-Compressed.pdf — confirmed genuine (159 KB, shows all main rooms).

## Outcomes

- **14 PDFs downloaded** covering all existing floors, key proposed floors, sections, and venue hire plan.
- All floor plan PDFs confirmed as genuine BDP (Building Design Partnership Ltd) architectural drawings produced in MicroStation, A0 page size, dated February 2025.

## Failures / Issues

- None. Westminster planning portal (idoxpa.westminster.gov.uk) was accessible and session-cookie authenticated curl worked for document downloads.
- Note: Westminster idoxpa portal uses SSL with a self-signed cert; WebFetch failed but curl --insecure worked fine.
