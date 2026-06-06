# Schematic Research Guide — Building Scanner Project

A consolidated end-to-end methodology for finding, accessing, and downloading publicly available architectural drawing sets (floor plans, sections, elevations, Design & Access Statements) from UK planning portals. Synthesised from research across 26 London buildings spanning City of London, Tower Hamlets, Southwark, Westminster, Camden, Hackney, Lambeth, Newham, and RBKC.

---

## Contents

1. [Scope and What You Will Actually Get](#1-scope-and-what-you-will-actually-get)
2. [Phase 0 — Establish the Building's Planning Identity](#2-phase-0--establish-the-buildings-planning-identity)
3. [Phase 1 — Identify the Correct Planning Authority](#3-phase-1--identify-the-correct-planning-authority)
4. [Phase 2 — Find the Planning Application Reference](#4-phase-2--find-the-planning-application-reference)
5. [Phase 3 — Access the Portal Documents Tab](#5-phase-3--access-the-portal-documents-tab)
6. [Phase 4 — Download and Verify the Files](#6-phase-4--download-and-verify-the-files)
7. [Alternative and Fallback Sources](#7-alternative-and-fallback-sources)
8. [Known Blockers and How to Handle Them](#8-known-blockers-and-how-to-handle-them)
9. [Portal Reference Table](#9-portal-reference-table)
10. [Drawing Conventions Reference](#10-drawing-conventions-reference)
11. [Edge Cases by Building Type](#11-edge-cases-by-building-type)

---

## 1. Scope and What You Will Actually Get

These are drawings submitted **for planning permission** — the public-facing design record. They show layout, circulation, entrances and room use. This is what an architecture researcher or interior-design student wants.

They are **not**:
- The contractor's fire/security/MEP construction issue set (not public)
- As-built record drawings (held by estates teams, not public registers)
- CAFM (facilities management) room-level data (internal to organisations)

What you can expect to find on a planning portal for a standard modern commercial or residential scheme:
- General Arrangement (GA) floor plans, one sheet per floor or group of typical floors
- Elevations (North, South, East, West)
- Building sections (typically 2–8 cuts)
- Roof plan
- Site location plan and proposed site plan
- Design and Access Statement (DAS) — narrative document explaining entrance hierarchy, circulation strategy, and public vs service zones; often split into 5–12 parts for large schemes
- Area schedule

For listed buildings and heritage applications, expect an additional LBC (Listed Building Consent) parallel drawing set, a heritage impact assessment, and a conservation plan.

---

## 2. Phase 0 — Establish the Building's Planning Identity

The street address you know is rarely the name on the application. Buildings are registered under the **legacy site address** (the name of whatever was demolished to make way) or a developer's internal "Building N" label. Getting this wrong wastes time.

### Step 0.1 — Web search for developer and architect

Search: `"<building name>" planning application <borough> developer`

Record: developer name, architect, the **old site address**, and approximate year of approval. The year narrows the application reference range.

**Why this matters:** 22 Bishopsgate was originally the Pinnacle site (ref 06/01123/FULEIA). Arbor at Bankside Yards was filed under "Ludgate House, 245 Blackfriars Road". One Canada Square was constructed under LDDC Enterprise Zone rules with no standard PA reference at all.

### Step 0.2 — Verify the correct building within a masterplan

Large sites have a masterplan (outline permission) and multiple Reserved Matters Applications (RMAs) for individual buildings. For example:

- Bankside Yards: outline `12/AP/3940`, individual buildings as RMAs (Arbor/Building 3 under `18/AP/3696`; Building 1 under `22/AP/2295`)
- International Quarter London (Stratford): outline `10/90641/EXTODA`, each building as a separate RMA

If you have the masterplan reference, search the portal for child applications tied to it. The committee report for each RMA should identify the building name and architect.

### Step 0.3 — Check for superseding amendments

Many buildings were consented twice: an original approval, then a revised scheme. The revision is what was actually built. Always check for amendment references — look for S73 (variation of condition), S96A (non-material amendment), or a completely new FULL/FULEIA application.

Examples:
- 8 Bishopsgate: `15/00443/FULEIA` (40 storeys, 2015) superseded by `17/00447/FULEIA` (50 storeys, 2017, as built)
- South Quay Plaza: `PA/14/00944` (original towers) followed by `PA/21/02721` (S73 adding 5 storeys to SQP2, approved 2024)
- 20 Fenchurch: original `06/00158/FULEIA`, then `08/01061/FULMAJ`, then `11/00234/FULL` (scheme actually built)

Target the amendment/revision, not the original, when you want the as-built layout.

---

## 3. Phase 1 — Identify the Correct Planning Authority

Postcode alone is not reliable. Borough boundaries cut through blocks, and some areas have special planning bodies that override the local borough.

### Standard borough lookup

Use planning.london.gov.uk or a postcode-to-borough lookup. Most London planning is at the borough level.

### Special cases that will trip you up

**LDDC / Canary Wharf Enterprise Zone (pre-1998)**

Buildings constructed in the Isle of Dogs Enterprise Zone (designated 1982, LDDC wound up 1998) did not require individual planning applications to Tower Hamlets. Development conforming to the LDDC scheme was deemed to have automatic consent. This applies to:

- One Canada Square (1988–1991): no PA reference exists in standard form
- One Churchill Place (Barclays HQ, completed 2005): EZ consent only; the Tower Hamlets register only shows minor signage/advertisement applications
- 40 Bank Street: built 2000–2003; original consent predates the online register

For these buildings, the online Tower Hamlets register will only show post-construction minor applications. Original EZ consent records are at the National Archives or via Tower Hamlets historical planning records (pre-2000).

**LLDC (London Legacy Development Corporation)**

Stratford/Olympic Park area. LLDC was the planning authority for the Stratford International Quarter and surrounding area. The LLDC portal (planning.agileapplications.co.uk/lldc) is now shut down and records have been migrated to the four host borough portals. The LLDC planning committee meeting archive at lldc-meetings.london.gov.uk still contains committee reports with drawing appendices for each RMA.

**GLA strategic referrals**

Buildings over a certain height or scale trigger a mandatory GLA (Greater London Authority) referral. The GLA does not hold the drawing sets — those remain on the borough portal. However, GLA Stage 1 and Stage 2 reports (searchable at glaplanningapps.commonplace.is) often confirm the application reference number and contain useful summary descriptions of the scheme.

**Multi-borough sites**

Some campuses straddle borough boundaries. The LSE Houghton Street building sits on a WC2A postcode but planning was decided by City of Westminster, not Camden — despite the postcode suggesting Camden. Always verify via planning committee minutes.

---

## 4. Phase 2 — Find the Planning Application Reference

Work through these in order of reliability:

### Method A — Web search with site: filter

`site:<council-democracy-domain> "<building name>"` — council committee reports reference the planning number explicitly. Democracy portals (moderngov, democracy.cityoflondon.gov.uk, etc.) are indexed by Google and often more accessible than the planning portal itself.

Example: `site:democracy.towerhamlets.gov.uk "One Canada Square"` returns committee report PDFs that cite the application reference.

### Method B — Planning portal address search

On Idox portals: go to `simpleSearchResults.do` with the legacy site name (not the marketed building name). Try in order:
1. Legacy site name (e.g. "Ludgate House")
2. Scheme name (e.g. "Bankside Yards")
3. Postcode — unreliable, apps often filed under old postcodes
4. Street name + number

Westminster Idox accepts GET requests for searches. Most other portals require a POST with a valid session cookie and sometimes a CSRF token (extract from the initial search page HTML).

### Method C — GLA planning applications search

For large schemes: search glaplanningapps.commonplace.is or london.gov.uk for PDU/XXXX stage referral reports. These confirm the borough planning reference directly.

### Method D — Planning press / specialist databases

buildington.co.uk, skyscrapercity.com, Wikipedia articles on major buildings often contain confirmed planning references. Cross-check against at least one official source before treating as confirmed.

### Confidence levels

Mark your reference as:
- **High** — confirmed from two independent authoritative sources (official document + committee report, or two official documents)
- **Medium** — found from one source, unverified on the portal
- **Low** — inferred from press/unofficial sources only; needs manual portal verification

---

## 5. Phase 3 — Access the Portal Documents Tab

### Idox portals (used by: Southwark, Tower Hamlets, Westminster, Newham, many others)

The keyVal is the internal record identifier — different from the human-readable application reference. You need it to construct the documents tab URL.

**How to find the keyVal:**
- It sometimes appears in Google-cached portal URLs
- It is in the URL bar when you navigate to the application on the portal
- For Tower Hamlets: format is `DCAPR_XXXXXX`
- For Southwark: format is `XXXXXXXX00300` (alphanumeric)
- For Westminster: format is `XXXXXXXXXX00` (alphanumeric)

**Documents tab URL pattern (Idox):**
```
https://<portal-host>/online-applications/applicationDetails.do?activeTab=documents&keyVal=<KEYVAL>
```

**Search URL pattern (Idox GET — Westminster, Southwark):**
```
https://<portal-host>/online-applications/simpleSearchResults.do?action=firstPage&searchType=Application&searchParamList=searchText&searchText=<QUERY>
```

### Northgate/PlanningExplorer portals (used by: Camden)

Camden uses `planningrecords.camden.gov.uk/Northgate/PlanningExplorer/`. The document management system is at `camdocs.camden.gov.uk/CMWebDrawer/PlanRec?q=recContainer:<REF>`.

Document downloads from `camdocs.camden.gov.uk` work without authentication — direct curl works. The portal frontend at `planningrecords.camden.gov.uk` often returns HTTP 403 to non-browser clients.

### Hackney — bespoke portal

Hackney uses `developmentandhousing.hackney.gov.uk`. This portal uses AWS WAF challenge protection that blocks curl and automated access. A real browser (Playwright) is required to pass the challenge. Direct application page URLs:
```
https://developmentandhousing.hackney.gov.uk/planning/index.html?fa=getApplication&reference=<REF>
```
Document download pattern:
```
https://developmentandhousing.hackney.gov.uk/planning/?fa=downloadDocument&id=<id>&public_record_id=<id>
```

Note: Hackney previously used `idox.hackney.gov.uk` (now connection-refused). The old IDOX reference format `2012/3871` still works as the application reference on the new portal.

### Identifying the right documents

Once you have the documents tab open, filter or scan for:
- Category label "Drawings" or "Plans"
- Filenames containing: `GA`, `GF`, `PROPOSED`, `FLOOR`, `PLAN`, `LEVEL`, `SECTION`, `ELEVATION`
- Drawing number series that follow architect conventions (see Section 10)
- The DAS (Design & Access Statement) — usually a multi-part PDF with "Design and Access" in the title; read this first before the GA plans

For major schemes, there may be 100–250+ documents. Ignore administrative docs (application forms, CIL forms, planning notices, drainage strategy, acoustic reports) unless specifically needed. Focus on the drawing series.

---

## 6. Phase 4 — Download and Verify the Files

### The `dl.sh` pattern (from Arbor-22-AP-2295)

Two issues affect automated downloads from Idox-family portals, both solved by this pattern:

**Problem 1 — Incomplete TLS certificate chain**

The portal server serves an incomplete TLS chain. Browsers fix this automatically via AIA (Authority Information Access); curl does not. This manifests as SSL certificate errors even when the certificate is genuinely valid.

Solution: use `-k` (insecure) flag with curl for these specific hosts. The URLs themselves are legitimate — you have validated them via the browser-based portal.

**Problem 2 — Session and rate limiting**

Document download endpoints require:
- A valid `JSESSIONID` cookie (establish by loading the portal search page first)
- A `Referer` header pointing to the portal
- Sequential downloads with back-off — burst downloading triggers HTTP 429

```bash
#!/usr/bin/env bash
# dl.sh — batch download planning drawings from an Idox portal
# Usage: ./dl.sh
# Writes PDFs to current directory, logs to dl.log

PORTAL="planning.southwark.gov.uk"   # change per council
KEYVAL="RE6N54KB00300"               # change per application
BASE="https://${PORTAL}/online-applications"
LOGFILE="dl.log"

# Step 1: Establish session — load the search page to get JSESSIONID
COOKIE_JAR=$(mktemp)
curl -s -k -c "${COOKIE_JAR}" \
  "${BASE}/search.do?action=simple&searchType=Application" \
  -o /dev/null

# Step 2: Load the documents tab to get the document list
DOC_PAGE=$(curl -s -k -b "${COOKIE_JAR}" \
  -H "Referer: ${BASE}/search.do" \
  "${BASE}/applicationDetails.do?activeTab=documents&keyVal=${KEYVAL}")

# Step 3: Extract document URLs from the page (adjust grep pattern per portal)
# Idox pattern: href="...downloadFile.do?appType=Planning&docNo=NNNNNN"
mapfile -t DOC_URLS < <(echo "${DOC_PAGE}" | grep -oP 'href="[^"]*downloadFile\.do[^"]*"' | sed 's/href="//;s/"//')

echo "Found ${#DOC_URLS[@]} documents" | tee -a "${LOGFILE}"

# Step 4: Download sequentially with back-off
for url in "${DOC_URLS[@]}"; do
  filename=$(echo "${url}" | grep -oP 'docNo=\K[0-9]+')
  outfile="${filename}.pdf"
  echo "Downloading ${outfile} from ${url}" | tee -a "${LOGFILE}"
  HTTP=$(curl -s -k -b "${COOKIE_JAR}" \
    -H "Referer: ${BASE}/applicationDetails.do?activeTab=documents&keyVal=${KEYVAL}" \
    -w "%{http_code}" \
    -o "${outfile}" \
    "https://${PORTAL}/online-applications/${url}")
  echo "  HTTP ${HTTP}" | tee -a "${LOGFILE}"
  if [[ "${HTTP}" != "200" ]]; then
    echo "  WARNING: non-200 response for ${outfile}" | tee -a "${LOGFILE}"
  fi
  sleep 2   # back-off between requests
done

rm -f "${COOKIE_JAR}"
echo "Done." | tee -a "${LOGFILE}"
```

**To reuse for any other building:** swap three values: `PORTAL` (the register hostname), `KEYVAL` (from the documents-tab URL), and the search URL path if the council uses a different Idox base path. Everything else is identical across Idox councils.

Non-Idox councils (Camden Northgate, Hackney bespoke) differ only in URL shape; the session/cookie/sequential-download principles are the same.

### Verifying downloads

After downloading, verify every file is a genuine, complete PDF:

```bash
for f in *.pdf; do
  pdfinfo "$f" | awk -v F="$f" '/^Pages:/{print F" -> "$2" pages"}'
done
```

Pass criteria:
- HTTP 200 during download
- First 4 bytes are `%PDF` (not an HTML error page)
- `pdfinfo` reports a sane page count (1–20 pages per drawing sheet is normal; 0 pages means a corrupt or image-only scan)

A file that passes HTTP 200 but contains HTML instead of a PDF means authentication failed — you need a fresh session cookie.

---

## 7. Alternative and Fallback Sources

When the planning portal is inaccessible or the application predates the digital register, try these in order:

### 7.1 — Wayback Machine (web.archive.org)

Idox portal pages are sometimes archived. Construct the documents tab URL with the keyVal and check if a snapshot exists. This retrieved the 15/00443/FULEIA document set for 8 Bishopsgate (159 documents, Wayback snapshot from April 2023) when the live portal was returning 503.

### 7.2 — Council democracy/committee portals

Planning committee reports are published on democracy.X.gov.uk or moderngov.X portals. These PDFs are almost always directly downloadable without authentication and frequently contain the full drawing schedule (list of all drawings submitted) even if the drawings themselves are not attached. This confirms you have the right reference and gives drawing numbers to request via FOI.

URLs to check:
- democracy.cityoflondon.gov.uk
- democracy.towerhamlets.gov.uk
- moderngov.southwark.gov.uk
- committees.westminster.gov.uk
- camden.moderngov.co.uk

### 7.3 — docs.planning.org.uk (Planning Inspectorate)

For applications called in by the Secretary of State or subject to public inquiry. The Planning Inspectorate indexes some submitted documents.

### 7.4 — Building/venue's own public documentation

Particularly useful for public venues, universities, and managed commercial estates:

- **Concert halls and theatres** (Barbican, Royal Festival Hall, Roundhouse, Peacock Theatre) publish production rider packs and technical specifications for venue hire. These contain stage plans, rigging grids, dimension tables — genuine architectural-level data, directly downloadable from the venue website without registration.
- **Universities** (Imperial College, LSE) publish campus maps from their Estates divisions. LSE Library publishes its own floor plans (8 floors) at lse.ac.uk/library. Imperial College Estates publishes the campus map at imperial.ac.uk/visit/campuses/south-kensington.
- **Exhibition and conference venues** (ExCeL London) publish full venue floor plan PDFs on their sales/hire pages. ExCeL's excel.london/sales-brochures-and-floorplans yielded better coverage than the blocked Newham Idox portal.
- **Managed creative estates** (Old Truman Brewery): go directly to the letting team. Truman Brewery's monika@trumanbrewery.com / events@trumanbrewery.com share high-quality Vectorworks floor plans as part of the letting and venue hire process — far more operationally accurate than planning drawings for this type of estate.
- **Professional institutions** (Royal Institution, Albemarle Street) publish venue hire floor plans at public-facing URLs (e.g. venue.rigb.org).

### 7.5 — FOI request

If the portal is inaccessible, the documents are restricted, or the application predates digital records: submit a Freedom of Information request to the planning authority. Cite the application reference and request the GA drawing set. Standard turnaround is 20 working days.

For ExCeL / LLDC-era records: email env-dutyofficer@newham.gov.uk (Newham's directed contact for unavailable LLDC records).

### 7.6 — Architect's public portfolio

Most architecture practices publish project pages with images. Some publish GA-grade drawings. RSHP (rshp.com) and other major practices sometimes share drawings for educational purposes on request.

### 7.7 — Listed building / heritage routes

Grade I and II* listed buildings generate richer planning submissions because Historic England scrutinises them. Listed Building Consent (LBC) applications are parallel to full planning applications and contain their own drawing sets — search for `LBC` or `listed building consent` applications at the same address alongside the main planning application. These sometimes yield interior floor plans that would not otherwise be submitted.

---

## 8. Known Blockers and How to Handle Them

### 8.1 — SSL certificate errors on Idox portals

**Affected portals:** planning2.cityoflondon.gov.uk, development.towerhamlets.gov.uk, planning.southwark.gov.uk (intermittently), idoxpa.westminster.gov.uk

**Symptom:** curl returns SSL handshake failure / certificate verification error. WebFetch tool reports certificate errors.

**Cause:** The server presents an incomplete TLS certificate chain (missing intermediate CA). Browsers resolve this via AIA; curl and most programmatic fetchers do not.

**Fix:** Use `curl -k` (insecure) or `curl --insecure`. The underlying certificate is genuine — this is a server misconfiguration, not a MITM. Alternatively, use a browser-based approach (Playwright) which handles TLS resolution automatically.

### 8.2 — HTTP 503 on City of London portal

**Affected portal:** planning2.cityoflondon.gov.uk (and www.planning.cityoflondon.gov.uk)

**Symptom:** All paths return HTTP 503 Service Unavailable or IDOX Page Not Found.

**Observed during:** Research on 8 Bishopsgate (April 2023 snapshot was reachable but live portal not), Tower 42 (December 2025 research session), 20 Fenchurch Street.

**Workarounds:**
1. Check Wayback Machine for a recent snapshot of the specific documents tab URL
2. Use democracy.cityoflondon.gov.uk to get the drawing schedule from committee reports
3. Wait and retry — City of London portal experiences intermittent extended outages

### 8.3 — LDDC Enterprise Zone buildings — no planning application exists

**Affected buildings:** One Canada Square, One Churchill Place, 40 Bank Street (original consent), and other Canary Wharf buildings completed before c. 2000.

**Symptom:** Exhaustive Tower Hamlets portal search finds only minor post-construction applications (signage, solar PV, etc.) — no building permission.

**Cause:** Isle of Dogs Enterprise Zone (1982–1998) granted automatic planning consent for development conforming to the LDDC scheme. No individual PA reference was issued.

**Fix:** Do not spend time searching Tower Hamlets for these buildings. Look for:
- Recent amendment applications (S73, S96A) which may have submitted updated floor plans
- Committee reports for the recent applications which sometimes describe the original scheme
- National Archives for original LDDC consent documents
- Pelli Clarke, SOM, HOK, or other original architect archives

### 8.4 — Portal returning "application is no longer available for viewing"

**Affected:** Southwark older applications including some Bankside Yards records on planning.southwark.gov.uk.

**Symptom:** Portal page says "application is no longer available for viewing — it may have been removed or restricted."

**Workarounds:**
1. Try the old planbuild.southwark.gov.uk URL with `casereference=` parameter (this portal is intermittently offline)
2. Check docs.planning.org.uk (Planning Inspectorate index)
3. Use the Wayback Machine
4. Submit an FOI request

### 8.5 — Westminster Idox CAPTCHA on document downloads

**Affected portal:** idoxpa.westminster.gov.uk

**Symptom:** Documents tab lists files with `recaptcha-link` class. Direct curl download returns "Document Unavailable" HTML (16 KB) instead of PDF.

**Cause:** Westminster has deployed CAPTCHA gating on document downloads, unlike most other Idox councils.

**Fix for primary application (14/12261/FULL for LSE):**
1. Use a real browser with CAPTCHA completion to download manually
2. Submit FOI request to Westminster City Council

**Note:** Some Westminster applications do allow unauthenticated download (the 2022 application 22/08664/FULL for LSE allowed downloads; the 2014 application 14/12261/FULL did not). Newer applications may have different security settings. Always attempt the session-cookie curl approach first — it works for Westminster for many applications (confirmed for Royal Institution 25/01386/FULL and Peacock Theatre 14/08584/FULL).

### 8.6 — Hackney AWS WAF challenge

**Affected portal:** developmentandhousing.hackney.gov.uk

**Symptom:** curl returns a Cloudflare/AWS challenge page instead of planning content. WebFetch fails.

**Fix:** Use Playwright (real browser automation). The challenge page loads normally in a browser. Once past the challenge, session cookies work for subsequent document downloads.

### 8.7 — RBKC portal offline (cyber-attack)

**Affected portal:** rbkc.gov.uk/planningsearch and all RBKC planning URLs including planningedm.rbkc.gov.uk

**Status as of research date (June 2026):** All RBKC planning URLs redirect to a cyber-incident notice page. The council confirmed a cyber-attack detected 24 November 2025 — data was copied and taken away. No timeline for restoration was published.

**Affected buildings:** Royal College of Music (Prince Consort Road), Sir Alexander Fleming Building (Imperial College), and any other buildings in the Royal Borough of Kensington and Chelsea.

**Recovery path when portal is restored:**
1. Go to rbkc.gov.uk/planningsearch
2. Search by address and date range (e.g. 2015-01-01 to 2016-12-31 for RCM "More Music" project)
3. Expect linked planning permission + listed building consent applications
4. Download existing and proposed floor plans from the documents tab

### 8.8 — Newham portal POST CSRF and reCAPTCHA

**Affected portal:** pa.newham.gov.uk

**Symptoms:**
- Form POST for address/keyword search requires CSRF token extracted from the search page HTML — automated searches fail without a prior page load
- reCAPTCHA blocks automated search on some paths
- LLDC-era applications (e.g. 21/00965/FUL for ExCeL Phase 3) return "Planning Application details not available" even when the reference is valid — likely not migrated post-LLDC transfer in December 2024

**Fix:** Use the LLDC meetings archive (lldc-meetings.london.gov.uk) for drawing sets rather than the Newham Idox portal for LLDC-era applications.

### 8.9 — Lambeth portal: 0-byte file downloads

**Affected portal:** planning.lambeth.gov.uk

**Symptom:** Document links are visible in the portal and `curl` returns HTTP 200, but downloaded files are 0 bytes.

**Cause:** Lambeth Idox requires an active authenticated browser session. Without it, the file endpoint returns nothing.

**Fix:** Manual browser download, or submit FOI request.

### 8.10 — Southwark portal intermittent SSL

**Affected portal:** planning.southwark.gov.uk

**Symptom:** SSL certificate verification errors when fetching directly, particularly for older planbuild.southwark.gov.uk URLs.

**Fix:** Use `curl -k`, or use the newer planning.southwark.gov.uk portal which has more stable TLS. The Arbor `dl.sh` pattern handles this with `-k` on a per-host basis.

---

## 9. Portal Reference Table

| Council / Authority | Portal URL | Software | Notes |
|---|---|---|---|
| City of London | https://www.planning.cityoflondon.gov.uk/online-applications/ (also planning2.cityoflondon.gov.uk) | Idox Public Access | Returns 503 intermittently; SSL chain issues; keyVal format: alphanumeric |
| Tower Hamlets | https://development.towerhamlets.gov.uk/online-applications/ | Idox (EXACOM) | SSL cert errors; keyVal format: DCAPR_XXXXXX; LDDC-era buildings not on register |
| Southwark | https://planning.southwark.gov.uk/online-applications/ | Idox Public Access | Some older apps "no longer available"; old URL was planbuild.southwark.gov.uk (intermittently offline); keyVal format: alphanumeric 13-char |
| Westminster | https://idoxpa.westminster.gov.uk/online-applications/ | Idox Public Access | Self-signed SSL cert (use curl -k); CAPTCHA on some document downloads; GET search works, POST returns 403 |
| Camden | https://planningrecords.camden.gov.uk/Northgate/PlanningExplorer/ | Northgate/PlanningExplorer | Portal frontend returns 403; document downloads via camdocs.camden.gov.uk work without auth |
| Hackney | https://developmentandhousing.hackney.gov.uk/planning/ | Bespoke | AWS WAF challenge; requires real browser (Playwright); old Idox portal was idox.hackney.gov.uk (now dead) |
| Lambeth | https://planning.lambeth.gov.uk/online-applications/ | Idox (Uniform) | Session-gated document downloads return 0 bytes without browser session |
| Newham | https://pa.newham.gov.uk/online-applications/ | Idox | POST CSRF required; reCAPTCHA present; LLDC-era apps not migrated post-Dec 2024 |
| RBKC | https://rbkc.gov.uk/planningsearch | Idox (offline) | OFFLINE since cyber-attack November 2025 — all URLs redirect to incident notice |
| GLA / LLDC | https://glaplanningapps.commonplace.is / https://lldc-meetings.london.gov.uk | Various | Not primary drawing sources; LLDC meetings archive has committee report PDFs with drawing appendices |
| Planning Inspectorate | https://docs.planning.org.uk | Custom | Indexes called-in applications; good fallback for SoS/public inquiry cases |

---

## 10. Drawing Conventions Reference

### Common drawing type prefixes

| Code | Type |
|---|---|
| GA | General Arrangement (floor plan) |
| GF | Ground Floor (sometimes used instead of GA for ground) |
| DAS | Design and Access Statement |
| LBC | Listed Building Consent drawing variant |
| GE | General Elevation |
| RC | Reflected Ceiling (plan view looking up) |
| S / SEC | Section |
| DET | Detail drawing |
| P | Plan (RSHP convention — e.g. RSHP-P-1150) |
| E | Elevation (RSHP convention) |

### Drawing naming patterns by architect

- **RSHP (Rogers Stirk Harbour + Partners):** `RSHP-P-XXXX-P-<FLOOR>_Block<N>_<Level>` — clean self-describing names; P=plan, E=elevation, S=section
- **PLP Architecture:** `PA<NNNN>` numeric series; 100s = site, 1900s–2000s = floor plans, 2200s = elevations, 2250s = sections
- **BDP (Building Design Partnership):** MicroStation-produced; A0 page size; floor series by level name
- **Feix & Merlin / Vectorworks practices:** `GE-XXX` elevations, `RC-XXX` plans, `S-XXX` sections, `DET-XXX` details
- **Tower Hamlets residential schemes (e.g. Aspen):** `XXXX-A-[series]-[number]` — 100-series = floor plans, 200-series = elevations, 300-series = sections, 400-series = unit layouts, 500-series = bay studies

### Drawing set priorities (read in this order)

1. **Design and Access Statement** — read first. Explains in words why the plan is arranged as it is: entrance hierarchy, public vs staff zones, how the core organises the floor, front-of-house vs servicing strategy.
2. **Ground floor / Upper ground floor GA** — entrances, lobby, reception, transition from street to vertical circulation
3. **Typical floor GA** — standard floor plate, core position, net-to-gross efficiency
4. **Sections (AA, BB)** — vertical relationships, floor-to-floor heights, how levels stack
5. **Basement plans** — plant, parking, loading, back-of-house
6. **Elevations** — facade, fenestration, entrance expression
7. **Roof plan** — plant zones, terraces
8. **Area schedule** — total floorspace by use (sanity check)

---

## 11. Edge Cases by Building Type

### 11.1 — Pre-digital consents (pre-1998)

Buildings consented before c. 1998 were not submitted digitally. The planning register may have no attached documents. Options:
- Look for a significant alteration/refurbishment application from the 2000s onwards that resubmitted floor plans
- FOI request to the council for original paper drawings (some have been scanned)
- Check the council's Local Studies Library

### 11.2 — Phased masterplans

For masterplan sites (Bankside Yards, Stratford IQL, South Quay Plaza), the individual building drawing sets are in the Reserved Matters Applications (RMAs), not the outline consent. Search for child applications by address after finding the outline OPP reference.

### 11.3 — Listed buildings

Grade I and II* listed buildings generate:
- A full planning permission application AND a separate Listed Building Consent (LBC) application
- LBC drawings often contain more interior detail than the planning drawings
- Historic England scrutiny means submissions are unusually complete
- May have a heritage impact assessment and conservation plan with useful spatial context

Search for both sets (planning permission + LBC) at the same address.

### 11.4 — Managed event venues and creative campuses

For buildings like Old Truman Brewery, Fabric, Oval Space, or other managed multi-tenanted creative venues: the planning register approach fails because the estate is too fragmented and too incrementally altered for any single application to contain the current layout.

**Go to the letting team first.** Letting and venue-hire managers share high-quality Vectorworks or AutoCAD floor plans as a matter of course — they are the primary sales tool. These plans include lease boundaries, ceiling heights, beam positions, service point locations, and accurate dimensions. They are more operationally accurate than planning drawings for these building types.

### 11.5 — University campuses

For pre-digital university buildings (Imperial College SAF Building, 1998): no substantive refurbishment application with floor plans will exist on the register. Campus maps from the university Estates division are the best publicly available spatial data. Internal CAFM (Computer-Aided Facilities Management) drawings are not public.

For newer university buildings with planning submissions (LSE Houghton Street, Camden/Westminster border): the planning drawings do exist but may be CAPTCHA-gated. The university library or IT services sometimes publishes floor plans on their websites (LSE Library is one such case).

### 11.6 — Exhibition and conference venues

Large-span single-storey exhibition halls (ExCeL London, Olympia) are typically better covered by the venue's own commercial floor plan publications than by the planning portal. Exhibition venues publish metric and imperial versions of their floor plan PDFs to serve international event organisers — these are freely downloadable from the venue's event sales pages and contain more operational detail than planning drawings.

When the planning portal is blocked or the application is under a special regime (LLDC transfer, post-cyber-incident), go straight to the venue's public sales materials.

---

*Guide synthesised from WORKFLOW.md files across 26 London buildings: 20 Fenchurch Street, 22 Bishopsgate, 40 Bank Street, 8 Bishopsgate, Arbor/22-AP-2295, Arbor Bankside Yards, Aspen Consort Place, Barbican Centre, British Library, ExCeL London, Imperial College SAF Building, LSE Houghton Street, Old Truman Brewery, One Blackfriars, One Canada Square, One Churchill Place, Peacock Theatre, Roundhouse, Royal College of Music, Royal Festival Hall, Royal Institution, Shoreditch Town Hall, South Quay Plaza, Stratford International Quarter, The Stage Shoreditch, Tower 42.*
