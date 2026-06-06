# Workflow — Finding & downloading a building's planning drawings (free, public)

Reproducible method used to obtain the architectural drawing set for **Arbor**
(Building 1, Bankside Yards, Southwark). Generalises to any building in
England/Wales: every planning application is a public record, and most councils
publish the full submitted drawing set (floor plans, elevations, sections,
Design & Access Statement) as free PDFs on an online planning register.

> Scope note: these are the drawings submitted *for planning permission* —
> the public-facing design record. They show layout, circulation, entrances and
> room use, which is exactly what an interior/architecture student wants. They are
> **not** the contractor's fire/security/MEP construction issue set, which is not
> public. That's the correct boundary.

---

## Phase 0 — Identify the building's planning identity
The street name you know is rarely the name on the application. Buildings are
filed under the *legacy site address* or a developer's "Building N" label.

1. Web-search: `"<building name>" planning application <borough> developer`.
2. Note: developer, architect, the **site's old address**, and any approval news
   (gives you the year → narrows the application reference).

**Result:** developer Native Land · architect PLP · site = *Ludgate House,
245 Blackfriars Road* (the old tower demolished for the scheme).

> ⚠️ **IDENTITY CORRECTION (read this).** "Building 1" and "Arbor" are **not the
> same building.** Southwark's own drawing legend labels **Arbor = Building 3**
> (a.k.a. "Bankside Yards 3") — PLP's 19-storey, ~223,000 sq ft office, *first*
> delivered, completed 2022/23, original planning won **2014** with **+3 storeys
> approved 2018**. The set downloaded in this folder is **22/AP/2295 = Building 1**,
> a *separate, newer* 18-storey "concept office" (≈80,600 sq ft) approved 2023 on
> the adjacent plot. Same developer, architect, site and typology — a near-perfect
> study analogue — but **not Arbor itself.** To get Arbor's own drawings, repeat
> Phases 1–4 against its 2014 detailed consent + 2018 amendment (sits within the
> Bankside Yards masterplan chain; start from outline ref `12/AP/3940` and follow
> its reserved-matters / amendment applications for "Building 3").

## Phase 1 — Find the right council register
- Southwark uses the **Idox Public Access** system at
  `https://planning.southwark.gov.uk/online-applications/`.
- Most UK councils run the same Idox software → identical URL patterns and steps.

## Phase 2 — Search the register for the application
Simple Search is literal — try, in order of usefulness:
1. The **legacy site name** (`Ludgate House`) — best hit rate.
2. The scheme name (`Bankside Yards`) — catches minor apps (hoardings, signage).
3. Postcode — often fails (apps filed under the old postcode).

**Arbor application found:** `22/AP/2295` — *"Construction of a lower ground,
upper ground and 18 storey building comprising Use Class E (office and retail)…"*
Status: **Granted**. Internal record key `keyVal=RE6N54KB00300`.

(Masterplan-wide consent for the whole site is `18/AP/3696`.)

## Phase 3 — Open the Documents tab & locate the drawings
Direct URL pattern (Idox):
```
.../applicationDetails.do?activeTab=documents&keyVal=<KEYVAL>
```
22/AP/2295 has **206 documents**. The ones that answer "how is it built / how do
rooms connect":

| Drawing no. | What it shows | Relevance to your question |
|---|---|---|
| PA0202 | Proposed site plan | Building in its context, approach routes |
| PA1997/98 | Basement, B1 | Plant, parking, back-of-house |
| PA1999/2000 | Ground floor lower/upper | **Entrances, lobby, reception** |
| PA2001 | Level 1 GA | First office/amenity floor |
| PA2002 | Levels 2–5 GA | Typical low-rise office floors |
| PA2006/2010/2014 | Levels 6–17 GA | Typical floor plates, core position |
| PA2018 | Roof | Plant, terraces |
| PA2250/2251 | Sections AA/BB | Vertical relationships, floor-to-floor |
| PA2200–2203 | Elevations N/E/S/W | Façade, fenestration |
| DAS (10 parts) | Design & Access Statement | **Narrative**: entrance strategy, circulation, front-of-house vs servicing, accessibility |

> Read the **Design & Access Statement first** — it explains in words *why* the
> plan is arranged the way it is (entrance hierarchy, public vs staff/practical
> zones, how the core organises the floor). Then read the GA plans against it.

## Phase 4 — Download & verify (the script)
Two gotchas, both solved in `dl.sh`:
- **Cert chain:** the server serves an incomplete TLS chain; browsers auto-fix via
  AIA, `curl` doesn't. URLs are sourced from the genuine CA-validated portal, so we
  fetch the public PDFs with `-k` for this host only.
- **Rate limiting:** the file endpoint needs the `JSESSIONID` cookie + a referer,
  and 429s on bursts. `dl.sh` establishes a session, then downloads **sequentially
  with back-off**.

Run:
```bash
./dl.sh          # writes PDFs here, logs to dl.log
```
Verify every file is a real, complete PDF:
```bash
for f in *.pdf; do pdfinfo "$f" | awk -v F="$f" '/^Pages:/{print F" -> "$2" pages"}'; done
```
Pass criteria: HTTP 200, first 4 bytes `%PDF`, `pdfinfo` reports a sane page count.

## Reuse for any other building
Swap three values: the **register hostname**, the **search term** (legacy site
name), and the **keyVal** from the Documents-tab URL. Everything else is identical
across Idox councils. Non-Idox councils (some use Northgate/Civica) differ only in
URL shape; the phases are the same.
