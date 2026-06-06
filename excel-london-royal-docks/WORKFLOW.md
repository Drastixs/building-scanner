# ExCeL London — Research Workflow

## Date
2026-06-06

## Steps Taken

### 1. Identity confirmation
- Web search confirmed ExCeL London at 1 Western Gateway, E16 1XL is in London Borough of Newham
- Planning register confirmed at https://pa.newham.gov.uk/online-applications/
- GLA also involved (ExCeL Phase 3 triggered GLA referral — MD2948)

### 2. Planning application reference search
- Searched news sources (Newham Recorder, Royal Docks, Architects Journal, constructionmap.info)
- Found planning reference **21/00965/FUL** via web search cross-referencing (confirmed by Newham condition discharge applications that cite it by reference)
- Approval: 12 October 2021, Newham Strategic Development Committee (unanimous)
- S106 signed: 9 March 2022

### 3. Newham Idox register access
- Base URL: https://pa.newham.gov.uk/online-applications/
- Form POST requires CSRF token (extracted from search page HTML) and JSESSIONID cookie
- Direct application URL `applicationDetails.do?keyVal=21/00965/FUL` returns "Planning Application details not available" — application not yet migrated or restricted post-LLDC transfer (December 2024)
- Successfully queried condition discharge applications (child applications) at E16 1XL
- Downloaded decision notice for 26/00099/AOD (BREEAM condition) directly with session cookie — confirmed Idox document download works with valid session

### 4. Floor plan acquisition
- Planning application drawings: NOT available (main application blocked on Idox)
- Alternative source found: ExCeL's own website (excel.london/sales-brochures-and-floorplans)
- Downloaded full venue floor plan PDFs directly from excel.london:
  - `excel-phase3-vital-stats-floorplans-metric.pdf` — complete venue floor plans including Phase 3 (4.8 MB)
  - `excel-phase3-vital-stats-floorplans-imperial.pdf` — same, imperial (4.9 MB)
  - `excel-event-halls-floorplan-metric.pdf` — event halls Level 1 plan (261 KB, confirmed valid)
  - `excel-tenancy-master-all-areas.pdf` — tenancy master plan all areas (2.7 MB)
  - Two additional vital statistics brochures

## Failures and Blockers

| Issue | Detail |
|---|---|
| Newham Idox — main application unavailable | `21/00965/FUL` keyVal direct access returns "Planning Application details not available". Likely not migrated post-LLDC handover or marked restricted. |
| Newham Idox POST search CSRF | Form POST for address/keyword search requires valid CSRF token from the search page — automated search blocked without prior page load |
| Planning application drawings | Original Grimshaw GA floor plan drawings from the 21/00965/FUL planning submission are not publicly accessible on Newham Idox |
| ExCeL Phase 3 drawings via planning portal | Cannot download — see above |

## Recommendations for Follow-up

1. Email `env-dutyofficer@newham.gov.uk` requesting planning documents for 21/00965/FUL (council has directed users to do this for unavailable LLDC-era records)
2. Submit FOI request to London Borough of Newham for GA drawings submitted with 21/00965/FUL
3. Check GLA (Greater London Authority) planning portal for MD2948 appendix documents — site plan was listed there
4. Contact Grimshaw Architects directly for public-domain drawings

## Files Downloaded

See BUILDING.md for file inventory.
