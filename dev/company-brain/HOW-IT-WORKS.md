# Company Brain — How It Works

*A memory layer that learns at one building and arrives smarter at the next.*

This is a guided tour. Read top-to-bottom; each section builds on the last. Code
lives next to this file — every component named here is one small Python module.

---

## 1. The one-sentence idea

> We have lots of recon tools that each see **one slice** of a building. The
> Company Brain fuses what they find into a single memory, lets specialist AI
> agents reason over it to rank ways in, and — the whole point — **remembers the
> lesson from building #1 and uses it to pre-bias building #2 before any local
> recon arrives.**

That last part is the "whoa": **visible cross-building learning.**

```
   Building #1                         Building #2
   ┌──────────┐    write_lesson()      ┌──────────┐
   │  recon   │ ─────────────────────► │  BRAIN   │  "I've seen a building like
   │  + run   │      (the lesson)      │ recalls  │   this. Expect the IT pretext
   └──────────┘                        │  it FIRST│   to fail and tailgating during
                                       └──────────┘   the conference to work."
                                            ▲
                                    ...said BEFORE anyone
                                    sets foot inside #2.
```

---

## 2. The mental model: three graphs + a hypothesis engine

Every physical-security assessment really lives in three overlapping maps:

| Graph | Question it answers | Example cues |
|-------|---------------------|--------------|
| **Social** | Who can I impersonate / blend with? | `conference_day`, `no_visitor_escort` |
| **Spatial** | Where are the bottlenecks and gaps? | `no_turnstile`, `loading_bay` |
| **Credential** | What badge/reader weakness exists? | `hid_maxiprox`, `osdp_secure` |

A **cue** is a single observable tag (e.g. `hid_maxiprox` = an old 125 kHz prox
reader). Cues either **open** an attack or **close** one:

```
  hid_maxiprox  ──ENABLES──►   clone_badge
  herd_entry    ──ENABLES──►   tailgate
  turnstile     ─DISCONFIRMS─► tailgate        (kills it)
  osdp_secure   ─DISCONFIRMS─► clone_badge      (kills it)
```

Those two edge types — **ENABLES** and **DISCONFIRMS** — are the entire graph in
v1. (The full methodology has 7 edge types; we deliberately ship only the 2 that
earn their keep. See `brain/taxonomy.py` for the complete cue list and edge maps.)

The reasoning style on top is **ACH + RPD**:
- **RPD** (Recognition-Primed Decision) = fast pattern match. *"125 kHz prox + no
  turnstile + herd entry → clone then tailgate."* Instant candidate.
- **ACH** (Analysis of Competing Hypotheses) = when it's ambiguous, list the
  hypotheses and ask *what evidence would disprove each?* Score by how
  **diagnostic** the evidence is, not how much of it there is.

---

## 3. The architecture at a glance

```
                         COMPANY BRAIN  (per building_id)
  FEEDERS                ┌───────────────────────────────┐      AGENT TEAM
  ───────                │  graph (NetworkX, typed)      │      ─────────
  enricher    ──social──►│   social / spatial / cred     │◄──── Social agent
  planning-scout ─spat──►│   cue nodes + ENABLES/DISCONF │◄──── Spatial agent
  extractor (live) ─cue─►│   edges + provenance          │◄──── Credential agent
                         └───────────────┬───────────────┘            │
                                         │                            ▼
                         CROSS-BUILDING LESSON STORE          collide() function
                         ┌───────────────────────────┐        (ranks routes)
                         │ {profile_embedding, cues,  │              │
                         │  hypotheses+outcomes,      │◄─ write_lesson() after run
                         │  key_lesson}   JSONL       │              ▼
                         └───────────────┬───────────┘      ranked entry routes
                                         │                  + per-door attack
                    TRANSFER AGENT (runs first at each building)   + next test
                    embed new profile → cosine top-k ────────────► prepends a
                    nearest → cue-set intersection ("why")         templated prior
                                                                   to each specialist
```

Two scopes of memory, on purpose:

1. **Per-building graph** — the *substrate* for one building. Throwaway-ish.
2. **Cross-building lesson store** — the *transfer engine*. This is what makes the
   agents smarter over time. It outlives any single building.

---

## 4. The two data shapes you need to know

Everything flows through just two dicts.

**BuildingProfile** — the thing we embed and reason over:

```python
{
  "building_id": "arbor-bankside",
  "name": "Arbor Bankside",
  "building_type": "multi-tenant-commercial",
  "scope": "ENG-2026-PTB-002 (authorized red-team)",   # authorization, banners every run
  "cues": ["hid_maxiprox", "conference_day", "open_floor"],   # tags from the taxonomy
  "osint_summary": "Bankside Yards tower, 19 floors, shared lobby, HID readers...",
}
```

**Lesson** — what `write_lesson()` stores after a building is assessed:

```python
{
  "building_id": "meridian-quay",
  "name": "Meridian Quay",
  "building_type": "multi-tenant-commercial",
  "cues": [...],
  "profile_embedding": [0.0123, -0.044, ...],   # precomputed, so recall never re-embeds
  "hypotheses": [{"id","label","result","notes"}],  # result ∈ confirmed | disconfirmed
  "key_lesson": "IT-contractor pretext gets verified and fails; tailgating during
                 the conference window works.",
}
```

The `key_lesson` string is the payload that transfers. Get that sentence right and
the demo works; no amount of infra saves a weak lesson.

---

## 5. The magic step, slowed down: recall + "why"

When the brain meets a new building, the **transfer agent** runs *first* — before
any local recon. Here is exactly what happens:

```
  new BuildingProfile
        │
        │ 1. embed:  building_type + cues + osint_summary  ──► vector
        ▼
  ┌─────────────────────────────────────────────┐
  │ recall():  brute-force cosine vs every stored │   (pool is <10 lessons,
  │ lesson's profile_embedding                    │    a numpy loop beats a DB)
  └─────────────────────────────────────────────┘
        │
        │ 2. keep matches with similarity ≥ SIM_FLOOR (0.75)
        ▼
  ┌─────────────────────────────────────────────┐
  │ for each match, compute WHY =                 │
  │   set(new.cues) ∩ set(lesson.cues)            │   ← this is the explanation
  └─────────────────────────────────────────────┘
        │
        ▼
  3. render a DETERMINISTIC announcement line:

     From {lesson.name} (shared cues: {why}), expect: {lesson.key_lesson}
```

Two design choices make this trustworthy on stage:

- **Why = set intersection.** Embedding similarity is fuzzy and opaque. We pair it
  with a literal, checkable reason: *these exact cue tags overlapped.* The audience
  sees **why** the lesson transferred, not just that it did.
- **The announcement is a template, not free LLM text.** The headline line is
  Python string formatting (`agents/transfer.py::announce`). It is reproducible
  every rehearsal and physically cannot ramble or hallucinate a cue. The LLM
  specialists still reason freely — *after* the templated prior is shown.

If recall finds nothing above the floor, it returns `[]` and the agent says
*"No strong analog in memory — proceeding cold."* The whoa path is seeded so
building #2 is guaranteed a match; the cold path is real but isn't the demo.

---

## 6. The agents and the collision

Each **specialist** is one LLM agent (a prompt) — but there's only **one class**,
`agents/specialist.py::Specialist`, instantiated three times (social / spatial /
credential). Per-graph differences live in an overridable `score_hook`; the shared
loop is written once.

```
                 transferred prior (templated)
                            │  prepended to every specialist prompt
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  ┌──────────┐        ┌──────────┐        ┌──────────┐
  │  SOCIAL  │        │ SPATIAL  │        │CREDENTIAL│   each reasons over ITS
  │ agent    │        │ agent    │        │ agent    │   slice of cues + the prior
  └────┬─────┘        └────┬─────┘        └────┬─────┘
       │  candidate routes  │                   │
       │  {hypothesis_id, label, target, confidence, next_observation}
       └─────────┬──────────┴───────────────────┘
                 ▼
          ┌─────────────┐   merges candidates that share a `target` (same door):
          │  collide()  │   score = social_conf × spatial_conf × credential_conf
          └──────┬──────┘   ranks: more graphs agreeing first, then higher score
                 ▼
        RANKED ENTRY ROUTES  (per-door attack + single best next test)
```

`collide()` (`brain/collide.py`) is **deterministic** — no LLM, no graph. It's a
merge: candidates pointing at the same physical `target` (e.g. `main_lobby`) stack
into one composite route, scored by the product of the three confidences. A route
where all three graphs agree on the same door ranks above a lone clever idea.

Each specialist's JSON output is parsed with the **same fence-strip → validate →
drop-on-failure** idiom the existing `extractor.py` uses: a malformed or
hallucinated route is logged and dropped, never crashes the run.

---

## 7. End-to-end: the demo, narrated

Run it:

```bash
# load OPENAI_API_KEY from the repo-root .env, then:
python run_demo.py --rehearsal --recon seeds/arbor_recon.txt
```

What each flag does:
- `--recon <file>` reads live recon as **observation sentences** (no live typing
  required on stage — type live only if you want the theater).
- `--rehearsal` **hard-asserts** building #2 recalls building #1 above `SIM_FLOOR`.
  If the transfer would silently no-fire, it crashes *now*, at rehearsal — never
  on stage.

The sequence:

```
 ① BUILDING #1  (Meridian Quay — canned, ships with its outcomes)
     run the 3 specialists → collide() → ranked routes
     write_lesson():  "IT pretext fails; tailgate during the conference works"
                                   │
                                   ▼  (stored in the lesson JSONL)
 ② BUILDING #2  (Arbor Bankside — live)
     TRANSFER AGENT fires FIRST, before any recon:
        ★ "From Meridian Quay (shared cues: conference_day, hid_maxiprox,
            open_floor), expect: IT-contractor pretext ... fails; tailgating
            during the conference window works."
                                   │
                                   ▼
     live recon sentences → extractor adapter → new cues
        new cues: no_turnstile, herd_entry, no_visitor_escort
                                   │
                                   ▼
     run the 3 specialists WITH the prior + the new cues → collide()
        RANKED ENTRY ROUTES:
          1. main_lobby   (all 3 graphs agree)  — tailgate during conference
          2. loading_bay  (2 graphs)            — delivery pretext
```

The audience sees the brain make the agents smart **on arrival** at #2 — and sees
the exact cues that justified it.

---

## 8. Why these specific engineering choices

| Choice | Why it matters |
|--------|----------------|
| **In-house brain behind a Mubit-shaped facade** (`init/recall/write_lesson`) | `mubit-sdk` was imported but never verified. We control the seam and can swap real Mubit in later without touching agents. |
| **Brute-force cosine, no vector DB** | Pool is <10 lessons. A numpy loop is faster and drops all install friction (chromadb/sqlite-vss gone). |
| **Embeddings pre-computed & cached** | No embedding network call sits on the live critical path during the demo. |
| **Deterministic announcement template** | The whoa line can't ramble or hallucinate — same every rehearsal. |
| **"Why" = cue set intersection** | Turns an opaque similarity score into a checkable reason. |
| **Central `taxonomy.py` + load-time validation** | A misspelled cue is a loud load error, not a silent empty "why". |
| **One Specialist class + score_hook** | Three agents, one code path to keep green. |
| **`--rehearsal` SIM_FLOOR assert** | Makes a silent on-stage no-fire impossible. |
| **OpenAI for chat + embeddings** | The only key the project's `.env` carries (Anthropic was removed). One file, `brain/llm.py`, is the provider seam. |

Explicitly **out of scope** for v1: Whisper/audio, the `reflect()` dream-cycle
(interface stub only), the full 7-edge graph + pathfinder, hard authorization
enforcement (we banner the scope, we don't block on a blank one), and live
enricher/planning-scout API calls (canned data for non-live buildings).

---

## 9. File map

```
company-brain/
├── run_demo.py                  ① the entrypoint — narrates the whole flow
├── brain/
│   ├── __init__.py              the Mubit-shaped facade: init / recall / write_lesson
│   ├── taxonomy.py              ★ cue vocabulary + ENABLES/DISCONFIRMS edges (start here)
│   ├── recall.py                embed → cosine → top-k + "why"   (the transfer engine)
│   ├── lesson_store.py          JSONL append/load of lessons
│   ├── graph.py                 minimal NetworkX cue graph (2 edge types)
│   ├── collide.py               deterministic route ranking
│   ├── llm.py                   OpenAI chat + embeddings (the provider seam)
│   └── ingest/
│       └── extractor_adapter.py recon sentence → taxonomy cue tag
├── agents/
│   ├── specialist.py            one Specialist class ×3 + CandidateRoute model
│   └── transfer.py              recall → deterministic announcement template
├── seeds/
│   ├── profiles.py              building #1 (canned + outcomes) and #2 (live)
│   └── arbor_recon.txt          sample live-recon observation sentences
└── tests/                       20 CI-gating unit tests (no live LLM)
```

**Read order to understand the code:** `taxonomy.py` → `recall.py` →
`agents/transfer.py` → `agents/specialist.py` → `collide.py` → `run_demo.py`.

---

## 10. The honest caveat

This is for **authorized** red-team / CTF physical-security assessment. Every
profile carries a `scope` field and the demo banners it on every run. v1 banners
but does not *enforce* a non-empty scope — that's a deliberate, documented tradeoff
to revisit if this outlives the hackathon.
```
