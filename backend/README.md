# Building Scanner API

Automated pipeline for building intelligence gathering. Submit a building ID to kick off a multi-phase analysis. Each phase is independently pollable.

---

## API Overview

```
POST /buildings                        → register building + start pipeline
GET  /buildings                        → list all scans
GET  /buildings/{id}/status            → full status across all phases
GET  /buildings/{id}/phase/a0          → Phase A0 status
GET  /buildings/{id}/phase/a1          → Phase A1 status
GET  /buildings/{id}/phase/b           → Phase B status
GET  /buildings/{id}/people            → people found (Phase B)
GET  /buildings/{id}/phase/c           → Phase C status
GET  /buildings/{id}/phase/d           → Phase D status
GET  /health                           → health check
```

---

## Phases

### Phase A0 — Schematic Discovery

Runs first. An AI agent searches public sources to locate floor plans and architectural documents for the building.

**Sources searched:**
- Local authority planning portals (by borough)
- City of London planning register
- Venue hire / technical rider packs
- University/institution public document stores
- FOI requests (where applicable)
- Wayback Machine for historic portal snapshots

**Pollable fields:**
| Field | Description |
|---|---|
| `status` | `pending` → `running` → `complete` / `failed` |
| `documents_found` | Count of located documents |
| `documents` | List of document URLs/filenames |
| `sources_searched` | Which sources have been checked |

---

### Phase A1 — Schematic Ingestion & 3D Mapping

Runs after A0 completes. Ingests each discovered document and extracts spatial features to build a 3D model of the building.

**Extracts:**
- Stairwell locations and connections between floors
- Lift/elevator positions
- Entry and exit points
- Restricted or access-controlled zones
- Floor-by-floor layout

**Pollable fields:**
| Field | Description |
|---|---|
| `status` | `pending` → `running` → `complete` / `failed` |
| `documents_total` | Total docs to process |
| `documents_processed` | Docs processed so far |
| `features.stairs` | Located stairwells |
| `features.lifts` | Located lifts |
| `features.entry_points` | Entry/exit points |
| `features.restricted_zones` | Restricted areas identified |

---

### Phase B — People Research *(parallel with A1)*

Runs in parallel with A1 once A0 is complete. Scouts the building/organisation's web presence and enriches people found.

**Sub-stages (in order):**

1. **Website Scout** — crawl the organisation's website, build a page index, identify About/Team/Staff sections
2. **LinkedIn Search** — search for employees at the organisation; target roles: head of security, facilities manager, building manager, reception
3. **Enrichment** — for each person found, call the enrichment API with their name + organisation to surface email, LinkedIn profile, and additional details

**Pollable fields:**
| Field | Description |
|---|---|
| `status` | Overall phase status |
| `current_stage` | `website_scout` / `linkedin_search` / `enrichment` |
| `website_indexed` | Whether the site crawl is complete |
| `website_pages_found` | Number of pages indexed |
| `people` | List of people found so far |
| `sources_searched` | Sources checked |

**Person record fields:**
| Field | Description |
|---|---|
| `name` | Full name |
| `role` | Job title |
| `source` | Where they were found |
| `enriched` | Whether enrichment API has been called |
| `linkedin_url` | LinkedIn profile URL |
| `email` | Email address (if found) |

---

### Phase C — OSINT *(parallel with A1 + B)*

Passive internet scanning to identify the building's physical and digital security posture.

**Sub-stages (in order):**

1. **Camera Scan** — search for internet-exposed camera feeds (Shodan, public CCTV indexes, Google dorks)
2. **Access Control Scan** — identify RFID/NFC systems in use (job postings mentioning systems, vendor contracts, procurement records)
3. **Services Scan** — enumerate internet-facing services hosted by the organisation (open ports, SSL certs, DNS records, cloud assets)

**Pollable fields:**
| Field | Description |
|---|---|
| `status` | Overall phase status |
| `current_stage` | `camera_scan` / `access_control_scan` / `services_scan` |
| `cameras_found` | List of camera feed references |
| `rfid_systems` | Identified access control systems |
| `exposed_services` | Internet-exposed services with metadata |

---

### Phase D — Simulation

Runs after A1, B, and C are complete. Uses AI agents to simulate how people within the building communicate and operate, then models how an ethical approach would be made.

**What it models:**
- Employee personas constructed from Phase B people data
- Building layout and access patterns from Phase A1
- Security posture from Phase C
- Simulated social engineering scenarios: tailgate approach, event attendee cover, delivery persona, contractor persona
- Agent communication and challenge/response protocols
- Optimal approach vectors given the building layout

**Pollable fields:**
| Field | Description |
|---|---|
| `status` | Overall phase status |
| `scenarios_total` | Number of scenarios to simulate |
| `scenarios_complete` | Scenarios finished |
| `scenarios` | List of scenario results with approach, outcome, notes |

---

## Phase Dependency Map

```
POST /buildings
        │
        ▼
    Phase A0  (schematic discovery)
        │
        ├──────────────────────┐
        ▼                      ▼
    Phase A1              Phase B + C  (parallel)
    (ingestion)           (people + OSINT)
        │                      │
        └──────────┬───────────┘
                   ▼
              Phase D  (simulation)
```

---

## Running

```bash
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Docs: `http://127.0.0.1:8000/docs`

---

## Example

```bash
# Start a scan
curl -X POST http://localhost:8000/buildings \
  -H "Content-Type: application/json" \
  -d '{"building_id": "barbican-centre-silk-street"}'

# Poll overall status
curl http://localhost:8000/buildings/barbican-centre-silk-street/status

# Poll schematic discovery
curl http://localhost:8000/buildings/barbican-centre-silk-street/phase/a0

# Get people found so far
curl http://localhost:8000/buildings/barbican-centre-silk-street/people
```
