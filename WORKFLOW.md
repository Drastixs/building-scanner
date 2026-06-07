# Master Building Scanner Workflow

Synthesised from 26 individual building scans. This is the repeatable process for finding public schematics, floor plans, and building documents in London.

---

## 1. Core Principle

Every planning application in England/Wales is a public record. Most councils publish the full submitted drawing set (floor plans, elevations, sections, Design & Access Statement) as free PDFs on an online planning register. These are the drawings submitted *for planning permission* — the public-facing design record. They show layout, circulation, entrances, and room use. They are NOT the contractor's fire/security/MEP construction-issue set, which is not public. That boundary is correct and intentional.

---

## 2. Phase 0 — Building Identity

The street name you know is rarely the name on the planning application. Buildings are filed under the *legacy site address* or a developer's "Building N" label.

**Search method:**
```
"<building name>" planning application <borough> developer
```

Note down:
- Developer name
- Architect name
- The **site's old / legacy address** (e.g. "Ludgate House" for Bankside Yards)
- Year of approval (narrows the application reference)
- Whether the building falls within an **Enterprise Zone** (see Section 7)

**Key gotcha:** Large multi-phase schemes have one outline/masterplan reference and separate reserved matters applications per building. Always chase the reserved matters application for the specific building, not just the outline consent.

---

## 3. Phase 1 — Identify the Planning Authority and Portal

London borough boundaries are not obvious. Several buildings in the scan were filed under a different borough than expected.

| Building type / location | Authority | Portal |
|---|---|---|
| City of London (EC1–EC4) | City of London Corporation | https://www.planning.cityoflondon.gov.uk/online-applications/ (also planning2.cityoflondon.gov.uk) |
| Tower Hamlets / Canary Wharf | London Borough of Tower Hamlets | https://development.towerhamlets.gov.uk/online-applications/ |
| Southwark | London Borough of Southwark | https://planning.southwark.gov.uk/online-applications/ |
| Westminster (WC/W postcode) | City of Westminster | https://idoxpa.westminster.gov.uk/online-applications/ |
| Camden (NW/WC) | London Borough of Camden | https://planningrecords.camden.gov.uk/Northgate/PlanningExplorer/ (also camdocs.camden.gov.uk for raw docs) |
| Hackney (EC1V/N1/E8) | London Borough of Hackney | https://developmentandhousing.hackney.gov.uk/planning/ |
| Lambeth (SE1 Southbank) | London Borough of Lambeth | https://planning.lambeth.gov.uk/ |
| Newham (E16/E20) | London Borough of Newham | https://pa.newham.gov.uk/online-applications/ |
| Royal Borough of Kensington and Chelsea (SW7) | RBKC | https://rbkc.gov.uk/planningsearch (OFFLINE since Nov 2025 cyber-attack) |
| Olympic Park / Stratford (LLDC area) | Newham (post-LLDC) — old records at LLDC meetings archive | https://lldc-meetings.london.gov.uk (committee reports) |

**GLA involvement:** Very tall buildings (over ~150m) or strategic sites trigger a GLA referral. GLA Stage 1/2 reports are at:
- `london.gov.uk/what-we-do/planning/planning-applications-and-decisions`
- References take the form `PDU/XXXX/01` or `D&P/XXXX/02`
- GLA reports confirm the application reference, site description, and sometimes reproduce key drawings. They are text-searchable and often the fastest way to confirm a planning reference number.

---

## 4. Phase 2 — Finding the Application Reference

### Method A: Web search (fastest — try this first)
```
"<building name>" site:<council-domain>.gov.uk planning
"<building name>" planning application <borough> "floor plans" OR "design and access"
"<address>" planning reference <borough> approved <year>
```

Third-party aggregators that reliably index planning refs:
- **buildington.co.uk** — frequently has planning refs for London towers
- **skyscrapercity.com** — forum threads often cite refs and link to drawings
- **35percent.org** — Southwark-specific; often has refs for major Southwark schemes
- **constructionmap.info** — useful for Newham/LLDC-area schemes

### Method B: Council portal direct search (when web search fails)

All Idox portals use the same Simple Search:
1. Try the **legacy site name** first (best hit rate)
2. Try the scheme name or developer name
3. Try the postcode (often fails if the old postcode was used on the application)
4. Try a broad address substring

### Method C: Democracy / committee reports

Committee reports are almost always public, text-searchable PDFs even when the portal document set is locked or offline. The report will name the application reference and list all submitted drawings.

- City of London: `democracy.cityoflondon.gov.uk/documents/s<ID>/<building-name>.pdf`
- Tower Hamlets: `democracy.towerhamlets.gov.uk/documents/s<ID>/...`
- Southwark: `moderngov.southwark.gov.uk/documents/s<ID>/...`
- Westminster: `committees.westminster.gov.uk/documents/s<ID>/...`
- Camden: `camden.moderngov.co.uk/documents/s<ID>/...`
- LLDC (Stratford/Olympic Park): `lldc-meetings.london.gov.uk` — meeting archive contains appendix PDFs with GA plans

### Method D: Wayback Machine

If a portal is temporarily down (503/500), the Internet Archive often has recent snapshots of the documents tab. Search:
```
web.archive.org/web/*/planning2.cityoflondon.gov.uk/online-applications/applicationDetails.do?keyVal=<KEYVAL>
```
This recovered a full 159-document set for 8 Bishopsgate (15/00443 keyVal=NNOCY8FH0L600) when the live portal was returning 503.

---

## 5. Phase 3 — Documents Tab and Drawing Identification

### Idox URL pattern (works for Southwark, Tower Hamlets, Hackney, Newham, Westminster, City of London):
```
https://<portal-host>/online-applications/applicationDetails.do?activeTab=documents&keyVal=<KEYVAL>
```

The `keyVal` is not the planning reference — it is the portal's internal database key. Find it by:
1. Doing a portal search and clicking through to the application
2. Reading it from the URL in Google's cached results
3. In Tower Hamlets it takes the form `DCAPR_XXXXXX`; in Southwark `XXXXXXXX00300`-style alphanumeric; in City of London an uppercase alphanumeric string

Camden uses a different system — Northgate/CMWebDrawer:
```
http://camdocs.camden.gov.uk/CMWebDrawer/PlanRec?q=recContainer:<APP-REF>
```
Document downloads from `camdocs.camden.gov.uk` work without authentication.

### Drawing types to target

| Drawing code / naming pattern | What it shows |
|---|---|
| GA + floor level (e.g. `GA-GF`, `GA-L01`, `PA1999`) | General arrangement — the primary floor plan, one per level |
| DAS (Design & Access Statement) | Narrative: entrance strategy, circulation, public vs. servicing zones — **read this first** |
| Section AA / BB / CC | Vertical relationships, floor-to-floor heights, core position |
| Elevation N/E/S/W | Facade and fenestration |
| Site plan / location plan | Building in context |
| Area schedule | Floor-area totals by use (not room-by-room) |
| LBC_ prefix | Listed Building Consent version of plans — submitted in parallel when building is listed |

**Drawing numbering conventions by architect:**
- RSHP: `RSHP-P-XXXX-P-<floor>_Block<N>_<Level>` — clean and self-describing
- PLP (22 Bishopsgate, Bankside Yards): `PA<XXXX>` series — numeric, sequential
- Aspen / Tower Hamlets residential: `1406-A-[series]-[number]` where 100=plans, 200=elevations, 300=sections, 400=unit layouts, 500=bay studies
- BDP: MicroStation-produced, A0 size
- Vectorworks: common in managed venues and smaller practices

---

## 6. Phase 4 — Download

### TLS/cert issues (very common)

Most London council Idox portals have broken or self-signed TLS chains. Browsers auto-fix via AIA; `curl` and automated tools do not.

| Portal | TLS behaviour | Workaround |
|---|---|---|
| Southwark (planning.southwark.gov.uk) | SSL cert error | `curl -k` or `--insecure` |
| Tower Hamlets (development.towerhamlets.gov.uk) | Invalid/self-signed cert | `curl --insecure` |
| Westminster (idoxpa.westminster.gov.uk) | Self-signed cert | `curl --insecure`; WebFetch fails |
| Camden (camdocs.camden.gov.uk) | No auth required | Direct curl works |
| Camden planning portal | Returns HTTP 403 to non-browser | Use Playwright/browser |
| Hackney (developmentandhousing.hackney.gov.uk) | AWS WAF challenge | Playwright required for search; some doc URLs work directly |
| Westminster Idox (14/12261/FULL) | CAPTCHA on doc links | Browser session required; bulk download blocked |
| Lambeth | Session-gated docs | Browser session required; programmatic download gives 0-byte files |
| Newham | CSRF + reCAPTCHA | POST search blocked; GET search may work |

### Session / cookie requirements

Most Idox portals require a `JSESSIONID` cookie + `Referer` header for document downloads. Without these, the server returns an HTML login page instead of a PDF.

Procedure:
1. Load the search or application page to acquire a session cookie
2. Pass `Cookie: JSESSIONID=<value>` and `Referer: <portal-base-url>` in subsequent document download requests
3. Download **sequentially** with back-off (rate limiting is common — 429 on bursts)

### Verification
```bash
for f in *.pdf; do pdfinfo "$f" | awk -v F="$f" '/^Pages:/{print F" -> "$2" pages"}'; done
```
Pass criteria: HTTP 200, first 4 bytes `%PDF`, `pdfinfo` reports a sane page count. An image-only PDF (e.g. old scanned plans) reports 0 in logical text structure — treat as raster only.

### The dl.sh pattern (from Arbor-22-AP-2295)

The reference download script is in `buildings/Arbor-22-AP-2295/dl.sh`. Reuse it by swapping three values:
1. The register hostname
2. The search term / legacy site name
3. The `keyVal` from the Documents tab URL

Everything else (session acquisition, sequential download, back-off) is identical across Idox councils.

---

## 7. Enterprise Zone Buildings — Special Cases

Several Canary Wharf buildings (One Canada Square, One Churchill Place, 40 Bank Street) were built under Isle of Dogs Enterprise Zone permitted development rights (1982–1998, administered by LDDC). These buildings have **no standard planning application reference**. Office use was automatically permitted under the EZ scheme; no PA/ application was filed with Tower Hamlets.

**Consequences:**
- The Tower Hamlets online portal (covers from ~2000 onwards) will only show post-construction signage, alterations, and fitout applications for these addresses
- No Design & Access Statement was required for EZ-era developments
- No GA floor plans exist in the Tower Hamlets public register for the main building structure
- The best recent substitute is a later material-change or refurbishment application (e.g. PA/20/01832/NC for 40 Bank Street, PA/24/01241 for One Canada Square levels 48-49) — these sometimes include updated floor plans

**Where to look for EZ-era records:**
- National Archives (for LDDC records)
- Tower Hamlets historical planning archive (pre-2000, offline/archive request)
- The original architect's archive (e.g. Pelli Clarke & Partners for One Canada Square; HOK for One Churchill Place)
- Historic England archive

---

## 8. Listed Buildings — Better Document Sets

Listed building applications consistently produce richer drawing sets than speculative commercial schemes. Reasons:
- Historic England scrutiny requires more documentation
- Parallel Listed Building Consent (LBC) application lodges a separate drawing set
- Existing condition drawings are submitted alongside proposed drawings
- Conservation plans and heritage impact assessments add spatial context

**LBC applications to specifically look for:**
- Barbican Centre: CoL planning register, Silk Street EC2Y 8DS
- British Library: Camden Northgate/PlanningExplorer — full Block 1 + Block 2 sets including LBC variants
- Royal Festival Hall: Lambeth register, app `23/02466/LB` (LB = listed building)
- Shoreditch Town Hall: Hackney register (Grade II*) — `AH-floor-plans.pdf` + `complete-building-floor-plans.pdf`
- Royal Institution: Westminster Idox, app `25/01386/FULL` — existing floor plans LGF through 5th floor, heritage impact assessment, conservation plan

---

## 9. When the Planning Route Fails or Is Inadequate

### Venue / event buildings
Purpose-built and managed venues often publish technical documentation directly:

| Source type | What's available | Examples |
|---|---|---|
| Venue-hire / technical rider pages | Stage plans, rigging grids, dimension tables, sight-line drawings | Barbican Centre (barbican.org.uk/your-visit/venue-hire) |
| Venue hire floor plans PDF | Room-by-room layout, capacities | Royal Institution (venue.rigb.org/sites/default/files/attachments/Ri%20Floor%20Plans-Compressed.pdf) |
| Accessibility pages | Simplified floor plan with entrance/lift routes | Barbican Centre Access pages |
| Landlord letting team | Dimensioned GA plans, lease boundaries, service point locations | Old Truman Brewery (monika@trumanbrewery.com, events@trumanbrewery.com) |

Managed creative campuses (Old Truman Brewery, similar) accumulate plans informally and have no single consented drawing set. Go to the letting or events team first — faster than the planning register and operationally more accurate.

### University buildings
Universities manage floor plans via CAFM systems (computer-aided facilities management) — not publicly accessible. The planning route only works if a recent, significant refurbishment with new drawings was submitted. Otherwise:
- Campus maps (often published by Estates and the Students Union) give footprint and entrance data
- Building-specific access / directions guides give the best public spatial data
- FOI to the university estates department is the formal route

Examples: Imperial College SAF Building, LSE Houghton Street — campus maps were the only public source; no internal floor plans are publicly available via the planning route.

### Portal offline
- **RBKC**: Offline since November 2025 cyber-attack (cyber incident confirmed; all planning URLs redirect to incident page). Recovery path: wait for portal restoration, then search by address + date range.
- **City of London**: Intermittently returns HTTP 500/503. Use Wayback Machine (see Phase 2 Method D) or democracy.cityoflondon.gov.uk committee reports.
- **Southwark planbuild**: Older portal (planbuild.southwark.gov.uk) is offline; use planning.southwark.gov.uk.

### FOI requests
Formal fallback for any case where documents exist but are inaccessible:
- Address to the council's planning department
- Cite the specific application reference and request the GA drawing set
- Statutory 20 working-day turnaround
- Confirmed route for: ExCeL (email `env-dutyofficer@newham.gov.uk`), Royal Festival Hall (Lambeth), any portal-blocked Westminster application

---

## 10. Multi-Phase / Masterplan Schemes

| Scheme | Structure | How to navigate |
|---|---|---|
| Bankside Yards | Outline `12/AP/3940` → reserved matters per building | Arbor = Building 3, ref `18/AP/3696`; Building 1 = `22/AP/2295` |
| International Quarter London / Stratford Cross | OPP `10/90641/EXTODA` → RMAs per building | LLDC committee meeting archive at lldc-meetings.london.gov.uk for committee reports with GA appendices |
| South Quay Plaza | PA/14/00944 (SQP1/2) → PA/15/03073 (SQP4 third tower) → PA/21/02721 (S73 amendment +5 storeys) | Follow S73 amendments for updated drawings |
| 20 Fenchurch (Walkie-Talkie) | Original `06/00158/FULEIA` → amended `08/01061/FULMAJ` → further amendment `11/00234/FULL` (built scheme) | Always identify the **built scheme** application, not the original approval |
| 22 Bishopsgate | Original Pinnacle `06/01123/FULEIA` → revised `16/01150/FULEIA` (built scheme) | Same pattern — revised application is the one with drawings for the completed building |

Rule: for any building with a design revision history, the **last approved application before construction** is the one with the most accurate GA plans.

---

## 11. Document Storage Conventions

Across the scan, documents were saved using these naming patterns:

- Planning drawings: `<app-ref>-<drawing-type>-<level>.pdf` (e.g. `14_12261_FULL-committee-report-2015-03-17.pdf`)
- Architect series: `RSHP-P-<number>-P-<floor>_Block<N>_<Level>.pdf`
- Committee reports: `<app-ref>-committee-report-<YYYY-MM-DD>.pdf`
- Venue PDFs: descriptive name from source (e.g. `excel-phase3-vital-stats-floorplans-metric.pdf`)
- Landlord plans: descriptive name + year (e.g. `f-block-first-floor-brochure-2021.pdf`)

Each building directory contains:
- `BUILDING.md` — identity, application ref, confidence level, file inventory
- `WORKFLOW.md` — search sequence, what worked, blockers, next steps
- `dl.sh` — download script (where a full download was executed)
- `*.pdf` — downloaded documents

---

## 12. Quick Reference: Council Portal URLs and Application Reference Formats

| Council | Portal URL | Ref format | Idox system |
|---|---|---|---|
| City of London | planning2.cityoflondon.gov.uk/online-applications/ | `YY/XXXXX/FULL` or `YY/XXXXX/FULEIA` | Idox |
| Tower Hamlets | development.towerhamlets.gov.uk/online-applications/ | `PA/YY/XXXXX` | Idox (keyVal = `DCAPR_XXXXXX`) |
| Southwark | planning.southwark.gov.uk/online-applications/ | `YY/AP/XXXX` | Idox |
| Westminster | idoxpa.westminster.gov.uk/online-applications/ | `YY/XXXXX/FULL` | Idox |
| Camden | planningrecords.camden.gov.uk/Northgate/PlanningExplorer/ | `YYYY/XXXX/P` | Northgate (docs at camdocs.camden.gov.uk) |
| Hackney | developmentandhousing.hackney.gov.uk/planning/ | `YYYY/XXXX` | Custom (was Idox, migrated) |
| Lambeth | planning.lambeth.gov.uk | `YY/XXXXX/LB` (listed bldg) | Idox/Uniform |
| Newham | pa.newham.gov.uk/online-applications/ | `YY/XXXXX/FUL` | Idox |
| RBKC | rbkc.gov.uk/planningsearch | OFFLINE | — |

**GLA referral format:** `PDU/XXXX/01` (Stage 1) → `PDU/XXXX/02` or `D&P/XXXX/02` (Stage 2 / direction)

---

## 13. Lessons and Anti-Patterns

- **Search by legacy site name, not scheme name.** "Ludgate House" finds Bankside Yards. "245 Blackfriars Road" finds the right application. The marketing name almost never appears on the application.
- **The built scheme is rarely the first approval.** Design revisions are common for tall buildings. The original 2006 approval for 22 Bishopsgate (Pinnacle) is irrelevant; the 2016 revision `16/01150/FULEIA` is the right application.
- **Canary Wharf pre-2000 = no public planning docs.** One Canada Square, One Churchill Place, 40 Bank Street, and similar EZ-era buildings have no GA floor plan drawings in the public planning register. This is a structural gap, not a portal failure.
- **Idox document links require a browser session.** Direct curl without a `JSESSIONID` cookie always fails. Acquire the session first, then download sequentially.
- **Read the DAS before the GA plans.** The Design & Access Statement explains in plain language why the plan is arranged as it is — entrance hierarchy, public vs. staff/service zones, how the core organises the floor. The GA plans make more sense after the DAS.
- **For managed venues, go to the letting team.** Planning registers work for singular consented buildings. Fragmented historic estates (Truman Brewery etc.) accumulate their plans informally via the landlord — faster and more accurate than the public register.
- **Large PDFs may need retry.** Hackney's portal occasionally times out on files over ~10 MB. Direct URL access (bypassing the document list) sometimes works better.
- **Camden raw docs bypass auth.** `camdocs.camden.gov.uk` serves PDFs directly without a session; the `planningrecords.camden.gov.uk` portal itself returns 403 to non-browser clients.
