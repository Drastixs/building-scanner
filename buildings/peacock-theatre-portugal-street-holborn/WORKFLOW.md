# Workflow — Peacock Theatre, Portugal Street

## Date
2026-06-06

## Steps

1. Created output directory.
2. Searched City of Westminster planning register by description "Peacock Theatre". Established a fresh session cookie with the idoxpa.westminster.gov.uk portal.
3. POST search to /online-applications/advancedSearchResults.do with description="Peacock Theatre" returned two application records.
4. Identified application 14/08584/FULL (keyVal: NB1BTURPKH400) — "Refurbishment and redecoration of the main entrance elevation (Portugal Street) of the Peacock Theatre". Second result (16/04705/FULL) was bicycle stands at the LSE Lionel Robbins Building opposite.
5. Fetched documents tab for keyVal NB1BTURPKH400 — found 16 PDF documents including 11 architectural drawings (GE series, RC series, S series, DET series) and administrative docs.
6. Downloaded 11 architectural drawing PDFs via curl with session cookie.
7. Verified PDFs are genuine Vectorworks/Feix & Merlin drawings (all 1 page each, 81 KB–3.6 MB).

## Outcomes

- **11 architectural drawing PDFs downloaded** covering general elevations, plan views (RC drawings), site/OS plans, and detail drawings.
- All confirmed genuine Vectorworks-produced drawings from Feix & Merlin Architects.

## Failures / Issues

- Internal floor plans of the theatre (auditorium, stage, backstage, FOH) were not part of the 2014 planning application. That application covered exterior facade refurbishment only.
- Note: The Peacock Theatre is not a listed building, so listed building consent applications (which often contain comprehensive interior floor plans) do not apply here.
- Westminster idoxpa portal uses SSL with a self-signed certificate — WebFetch failed with certificate error; curl --insecure with session cookies succeeded.
- Note: planning authority listed in the brief was "London Borough of Westminster" — this is technically City of Westminster (which uses the same idoxpa.westminster.gov.uk portal). No issue in practice.
