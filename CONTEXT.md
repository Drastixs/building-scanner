# Context — building-scanner

Full background for this repo: the idea, the target building, what was found, how, and what's still open. Written so anyone (or any agent) picking this up later has the complete picture without re-deriving it.

---

## The idea

Find a large building's **architectural drawings for free**, online, to study interior design *after* the main structure is built — specifically:

- how **entrances** are made,
- how **rooms connect** to each other,
- which rooms are for **comfort** (front-of-house) vs **staff & practicality** (back-of-house / servicing).

Framed from an architecture-student angle: understand real built layouts, not renders.

The key insight that makes this possible for free: **UK planning applications are public records.** When a building is approved, the council publishes the *full submitted drawing set* — floor plans, elevations, sections, and the Design & Access Statement (DAS) — as free PDFs on an online planning register. That's the public-facing design record, and it directly answers the entrance / circulation / front-vs-back-of-house questions.

> Boundary: these are the drawings submitted **for planning permission**, not the contractor's fire/security/MEP construction-issue set (which is not public). That's the correct and intended limit.

---

## The target building — Arbor, Bankside Yards

- **Arbor** — a multi-award-winning office building at **Bankside Yards, Southwark, SE1 9AX**.
- Part of the Bankside Yards redevelopment of the former **Ludgate House (245 Blackfriars Road) + Sampson House**.
- Developer: **Native Land** · Architect: **PLP Architecture** · Contractor: **Multiplex**.
- Arbor is a **commercial office building** (tenants incl. Carbon Trust, Lewis Silkin) — *not* residential. Nobody lives there. (The original ask described it as "a private residential building I live at," which doesn't match Arbor; if the real target is a home address, that's a different search.)

### Critical identity finding ⚠️

**Arbor = "Building 3"** in the masterplan (a.k.a. "Bankside Yards 3"):
- 19-storey, ~223,000 sq ft office, **first** delivered, completed **2022/23**.
- Original detailed planning won **2014**, with **+3 storeys approved 2018**.
- Sits within the Bankside Yards masterplan chain; outline ref **`12/AP/3940`**.

The drawing set actually downloaded in this repo is **`22/AP/2295` = Building 1** — a *separate, newer* 18-storey "concept office" (~80,600 sq ft) approved **2023** on an adjacent plot. Same developer, architect, site and typology → a **near-perfect study analogue** — but **not Arbor itself.**

This was caught during verification: Southwark's own drawing legend on sheet PA2000 labels "H. Building 3, Arbor" while the title block reads "Building 1". Confirmed via web search afterward.

| | Arbor (the real target) | What was downloaded |
|---|---|---|
| Masterplan name | **Building 3** | Building 1 |
| Size | 19-storey, ~223,000 sq ft | 18-storey, ~80,600 sq ft |
| Planning | won 2014, +3 storeys 2018 | approved 2023 |
| Status | completed 2022/23 | newer "concept office" |
| App ref | (2014 consent + 2018 amend, under `12/AP/3940`) | `22/AP/2295` |

---

## What's in this repo

- **`Arbor-22-AP-2295/`** — 15 verified planning PDFs for **Building 1** (the analogue set) plus the workflow doc:
  - `00_DRAWING_REGISTER.pdf` — index of the full drawing set
  - `DAS_PART_01.pdf` — Design & Access Statement (the **narrative**: entrance strategy, circulation, public vs staff/servicing zones, accessibility) — **read this first**
  - `PA0202_PROPOSED_SITE_PLAN.pdf` — building in context, approach routes
  - `PA1997_BASEMENT.pdf`, `PA1998_BASEMENT_B1.pdf` — plant, parking, back-of-house
  - `PA1999_GROUND_FLOOR_LOWER.pdf`, `PA2000_GROUND_FLOOR_UPPER.pdf` — **entrances, lobby, reception** (sheet labels confirm "Office Entrance", "Office Reception", cycle parking, lift core)
  - `PA2001_LEVEL_1_GA.pdf` — first office/amenity floor
  - `PA2002_LEVEL_2-5_GA.pdf` — typical low-rise office floors
  - `PA2006_LEVEL_6-9_GA.pdf`, `PA2010_LEVEL_10-13_GA.pdf`, `PA2014_LEVEL_14-17_GA.pdf` — typical floor plates, core position
  - `PA2018_ROOF_GA.pdf` — plant, terraces
  - `PA2250_SECTION_AA.pdf`, `PA2251_SECTION_BB.pdf` — vertical relationships, floor-to-floor heights
  - (GA = General Arrangement = the floor-plate layout drawing.)
- **`Arbor-22-AP-2295/WORKFLOW.md`** — the reproducible 5-phase method to find & download any UK building's planning drawings.

All 15 PDFs passed integrity verification: first 4 bytes `%PDF`, sane `pdfinfo` page counts, `%%EOF` present, 0 failures. ~12 MB total.

---

## How it was done (method, condensed)

Full version in `Arbor-22-AP-2295/WORKFLOW.md`. Phases:

0. **Identify the building's planning identity** — the street name is rarely the name on the application. Web-search for developer, architect, and the *legacy site address* (here: Ludgate House, 245 Blackfriars Road).
1. **Find the council register** — Southwark uses **Idox Public Access**: `https://planning.southwark.gov.uk/online-applications/`. Most UK councils run the same Idox software (identical URL patterns).
2. **Search the register** — by legacy site name (best hit rate), then scheme name, then postcode (often fails). Found `22/AP/2295`, status Granted, `keyVal=RE6N54KB00300`.
3. **Open the Documents tab** — `applicationDetails.do?activeTab=documents&keyVal=<KEYVAL>`. 206 documents; pick register + DAS + GA plans + sections.
4. **Download & verify** — confirm each is a real, complete PDF.

### Technical obstacles hit & how they were solved
- **Incomplete TLS chain** on the Southwark host → `curl` fails cert validation (browsers auto-fix via AIA). Solved by sourcing URLs from the genuine CA-validated portal and fetching with `-k` for that host only.
- **Rate limiting (HTTP 429) + 404s** on the file endpoint → needs a `JSESSIONID` session cookie + referer, and throttles bursts. Solved with a session cookie jar, referer header, and sequential downloads with back-off.
- **Final approach (per user instruction):** instead of `curl`, used the **Playwright Chromium** browser session to fetch the files in-session (valid session, no rate-limit), via `fetch(url, {credentials:'include'})` → arrayBuffer → chunked base64 → decoded to disk. This retrieved all remaining files cleanly.

Tools used: Playwright MCP (browser_navigate / snapshot / evaluate), web search for identity confirmation, `pdfinfo`/`pdftotext` for verification.

---

## Status & open thread

**Done:**
- Reproducible workflow built and documented.
- Building 1 (`22/AP/2295`) full drawing set downloaded, verified, and committed.
- This repo created (public) and a collaborator invited (DeepNandre, write/Developer access).

**Open / next step:**
- The downloaded set is **Building 1, not Arbor.** To get **Arbor's own** drawings, repeat Phases 1–4 against its **2014 detailed consent + 2018 amendment**, starting from masterplan outline **`12/AP/3940`** and following its reserved-matters / amendment applications for **"Building 3"**. (Masterplan-wide consent for the whole site: `18/AP/3696`.) Arbor's exact detailed-permission reference is not yet pinned down — register searches for "Arbor" matched only "Arboricultural", and "Bankside Yards Building 3" returned nothing, so it needs drilling via the masterplan chain in the Chromium browser.

---

## Sources

- Native Land — Bankside Yards: https://www.native-land.com/projects/bankside-yards/
- PLP Architecture — Arbor: https://www.plparchitecture.com/projects/arbor
- BD — "PLP completes Arbor in Bankside Yards": https://www.bdonline.co.uk/news/in-pictures-plp-architecture-completes-arbor-in-bankside-yards/5124254.article
- Southwark planning register (Idox): https://planning.southwark.gov.uk/online-applications/
