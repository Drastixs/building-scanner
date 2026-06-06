# LSE Houghton Street — Research Workflow

## Date
2026-06-06

## Steps Taken

### 1. Planning authority identification
- Initial assumption: Camden (WC2A postcode crosses borough boundary)
- Confirmed via planning committee minutes and Westminster Idox: **City of Westminster** granted permission
- Westminster Idox register: https://idoxpa.westminster.gov.uk/online-applications/

### 2. Planning application reference discovery
- Searched Westminster Idox with GET request for "houghton street" — returns live results page
- Found application **14/12261/FULL** in search results (keyVal: NGH91QRP0C400)
- Confirmed via Westminster planning sub-committee minute (committees.westminster.gov.uk, ID=2475, meeting 17 March 2015)
- Also confirmed via subsequent variations (16/05155/FULL, 17/05855/FULL) which cite 14/12261/FULL as parent

### 3. Westminster Idox register access
- Search works via GET request to `simpleSearchResults.do` with plain query parameters (no POST needed for GET search)
- Application details page accessible at `applicationDetails.do?activeTab=documents&keyVal=NGH91QRP0C400`
- 40+ RSHP drawing documents listed in the documents tab
- **Document download blocked**: Files return "Document Unavailable" HTML page (16 KB) instead of PDF
  - Westminster Idox uses `recaptcha-link` class on document links — CAPTCHA required for bulk download
  - Files endpoint returns HTML "Document Unavailable" for all documents without an authenticated browser session

### 4. Committee report download
- Westminster planning committee PDF downloaded directly (no auth required):
  `committees.westminster.gov.uk/documents/s12566/ITEM 03 - LONDON SCHOOL OF ECONOMICS AND POLITICAL SCIENCE HOUGHTON STREET WC2.pdf`
  - 7.5 MB, 50 pages, image-based PDF (not text-searchable)
  - Saved as `14_12261_FULL-committee-report-2015-03-17.pdf`

### 5. Later application — 22/08664/FULL
- Searched Westminster Idox for Houghton Street — found recent application 22/08664/FULL (air source heat pump works, 2022)
- Documents for this application ARE downloadable (different document security?)
- Downloaded 10 drawings: existing and proposed plans at levels 00, 04, and roof; section AA; north elevation; block plan; site plan
- These show the building as-built with rooftop plant information

### 6. LSE public materials
- LSE Library publishes its own floor plans (8 floors) publicly at lse.ac.uk/library — downloaded (6.7 MB)

## Failures and Blockers

| Issue | Detail |
|---|---|
| Westminster Idox — document download blocked | All documents under keyVal=NGH91QRP0C400 (14/12261/FULL) return "Document Unavailable" — CAPTCHA/authenticated session required. 16 plan-level drawings (B2 through 13) plus sections and elevations exist in the system but cannot be downloaded without a logged-in browser. |
| Committee report is image-based | The 50-page committee PDF is scanned (PDFlib 4.0.3, 2015) — no text extraction possible, but contains the planning officer report with context |
| POST search blocked | Westminster Idox returns "Permission Denied" for POST searches from non-browser clients; GET search works |

## Recommendations for Follow-up

1. Access Westminster Idox in a browser with CAPTCHA completion to download all 40+ RSHP drawings from 14/12261/FULL — documents are visible in the documents tab
   - Direct URL: https://idoxpa.westminster.gov.uk/online-applications/applicationDetails.do?activeTab=documents&keyVal=NGH91QRP0C400
2. Contact RSHP directly — they publish project images on rshp.com; may share GA drawings
3. Submit FOI request to Westminster City Council for GA floor plan drawings
4. The LSE Estates division (info.lse.ac.uk/estates) may have CAD drawings available to authorised parties
5. Also check 16/05155/FULL (keyVal not found in search) and 17/05855/FULL for updated drawings with any design changes

## Files Downloaded

See BUILDING.md for file inventory.
