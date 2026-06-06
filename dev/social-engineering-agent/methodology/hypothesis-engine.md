# Hypothesis Engine Design

*ACH + RPD loop for physical security assessment agent.*

---

## Core Loop

```
OBSERVE cue
    ↓
PATTERN MATCH (RPD) → known pattern? → CANDIDATE PLAN (fast path)
    ↓ (ambiguous)
BUILD HYPOTHESIS SET (ACH)
    ↓
IDENTIFY DISCRIMINATING EVIDENCE (what would disprove each?)
    ↓
SCORE by diagnosticity (not volume)
    ↓
SURFACE top hypotheses + gaps
    ↓
RECOMMEND next observation to close gap
```

---

## Hypothesis Schema

```json
{
  "id": "H3",
  "label": "Delivery pretext via loading bay",
  "graph": "social",
  "requires": ["loading_bay_accessible", "delivery_staff_low_scrutiny"],
  "disconfirmed_by": ["delivery_manifest_checked", "ID_required_at_bay"],
  "supporting_cues": [],
  "disconfirming_cues": [],
  "confidence": 0.0,
  "next_test": "Observe loading bay during 0800-1000 delivery window"
}
```

---

## Diagnosticity Weighting

Evidence weight = P(evidence | H_i) / P(evidence | ~H_i)

Strong disconfirming signals (high diagnosticity):
- Turnstile present → tailgating confidence → 0
- OSDP Secure Channel → Wiegand attacks confidence → 0
- Appointments verified live → IT pretext confidence → 0

Weak confirming signals (low diagnosticity):
- Staff friendly → any social pretext slightly boosted
- Badge visible → clone possible but not confirmed

---

## RPD Fast Paths (Pre-encoded Patterns)

| Pattern signature | Instant candidate |
|---|---|
| 125 kHz prox + no turnstile + herd entry | Clone → tailgate |
| Conference day + busy lobby + friendly staff | Blend + tailgate |
| Loading bay + no manifest check | Delivery pretext |
| IT job posting + open floor + no visitor escort | IT contractor pretext |
| Stairwell egress from public area | Badge in at lobby → stairwell cascade |
| Hi-vis culturally invisible | Maintenance pretext |

---

## Context Brain Population

Each session adds:
- Observed cues (timestamped, building-tagged)
- Hypotheses tested + outcome
- Links discovered (cross-graph pivots)
- Disconfirming signals found

Brain grows richer per building; patterns transfer across buildings via shared cue taxonomy.

---

## Mubit Integration

Mubit (https://mubit.ai/) is the persistent execution memory layer.

**What it does here:**
- End of each building run → `write_lesson(outcome, context)` → stores what was tried, confirmed, disconfirmed
- Start of next run (same or similar building) → `recall_lessons(building_type, cues_observed)` → auto-injects relevant past outcomes into agent context
- Cross-agent: OSINT agent, recon agent, credential agent all share the same lesson pool
- Sub-80ms retrieval → fast enough to inject mid-loop as new cues arrive

**Lesson schema (per run):**

```python
lesson = {
  "building_id": "arbor-bankside-yards",
  "building_type": "multi-tenant-commercial",
  "cues_observed": ["HID MaxiProx", "herd entry", "no turnstiles", "conference day"],
  "hypotheses_tested": [
    {"id": "H1", "label": "tailgate main entrance", "result": "confirmed", "notes": "door held 3/3 attempts"},
    {"id": "H5", "label": "IT pretext", "result": "disconfirmed", "notes": "appointments verified by desk"}
  ],
  "cross_graph_links": ["conference→busy lobby→low scrutiny", "HID MaxiProx→clone viable"],
  "key_lesson": "IT pretext fails here; tailgate during conference windows works without challenge"
}
```

**Integration pattern (Mubit SDK):**

```python
import mubit

mubit.init()  # single import, wraps Anthropic client

# Before run: recall
past_context = mubit.recall(query="building multi-tenant commercial HID prox conference")

# After run: write
mubit.write_lesson(lesson)
```

**What grows over time:**
- Pattern library: which cue combos predict which hypothesis outcomes
- Building-type clusters: lessons transfer across similar buildings (not just same building)
- Disconfirming signal library: which signals should immediately kill which hypotheses
- Operator signatures: which pretexts fail at which building cultures
