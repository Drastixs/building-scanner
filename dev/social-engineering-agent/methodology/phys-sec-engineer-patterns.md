# Physical Security Engineer — Pattern Cognition & Methodology

*Synthesised from: war stories (`06-real-world-war-stories.md`), threat briefs (`toolings/`), and cognitive science literature (`research/LITERATURE-REVIEW.md`).*

---

## 1. Mental Model: Three Fused Graphs

Expert practitioners don't think in checklists. They build and traverse three overlapping graphs simultaneously:

```
SOCIAL GRAPH          SPATIAL GRAPH         CREDENTIAL GRAPH
─────────────────     ─────────────────     ────────────────────
people                spaces                readers
  ↓ roles               ↓ barriers            ↓ RF technology
  ↓ trust routes        ↓ paths               ↓ card type
  ↓ routines            ↓ depth from entry    ↓ clonability
  ↓ authority           ↓ blind zones         ↓ facility codes
  ↓ social norms        ↓ egress logic        ↓ privilege tier
```

Entry is almost never a credential problem alone. It's a **collision** between social permissiveness, spatial bottleneck, and credential weakness.

---

## 2. Engagement Phases

### Phase 0: Passive OSINT (Pre-site)

**Goal:** Build initial frame before boots on ground.

**What they look for:**
- Company structure: org chart, LinkedIn roles, reporting lines, recent hires/leavers
- Event intelligence: conferences, public meetups at the target → legitimate foot traffic to blend with
- Job postings: "Security Operations Officer, 3+ years Lenel/CCure experience" → tells you the access control platform
- Planning drawings: UK planning registers (Idox) — floor plans, DAS (Design & Access Statement), sections publicly filed
- Satellite/street view: entrance locations, smoking doors, loading bays, secondary exits
- Social media: staff photos wearing badges (badge design, lanyard color, photo quality → clonability assessment)
- Glassdoor/Indeed: culture signals ("very welcoming team", "open door policy" = social engineering surface)

**Links made:**
- Job posting tech → access control platform → known CVEs/default configs
- Org size → badge volume → likelihood of unchallenged strangers
- Building age → legacy vs. modern access control stack

**Rapid test:** Does the job posting name the access control vendor? If yes, default credential and install-mode exploits are on the table immediately.

---

### Phase 1: On-Site Reconnaissance (Silent Observation)

**Goal:** Test OSINT frame, build spatial model, observe social patterns.

**Duration:** 1–3 passes; 20–45 min each. Not all in one day.

**What they observe:**

#### Social patterns
| Observation | Hypothesis triggered |
|---|---|
| Staff hold door for anyone who looks like they belong | Tailgating viable |
| Hi-vis / scrubs / lanyards unchallenged | Costume social engineering viable |
| Reception checks every visitor | Need appointment pretext or bypass to secondary entrance |
| Smoking door used by multiple staff, propped | Low-friction secondary entry point |
| Badges worn visibly outside building | Badge photography + design cloning possible |
| Staff chatty with strangers at coffee queue | Pretext conversation → internal intel |
| "Help desk mentality" staff at front desk | "I'm from IT" pretext viable |

#### Spatial patterns
| Observation | Hypothesis triggered |
|---|---|
| Double doors with centerline gap | Crash-bar gap tool / J-hook viable |
| Maglock with visible status LED | Recon + maglock fouling viable |
| Motion sensor in ceiling near door | REX/PIR external triggering possible |
| Loading bay with separate access | Delivery pretext / unlocked during hours |
| Stairwell exits (no badge re-entry) | Egress cascade: badge in at lobby, tailgate to floor, use stairwell |
| Floor gap >10mm at bottom of door | Under-door lever tool viable |

#### Credential patterns
| Observation | Hypothesis triggered |
|---|---|
| Reader bezel style → manufacturer ID | Platform identified (HID, Allegion, Gallagher) |
| Reader buzzes/clicks → frequency guess | 125 kHz prox vs. 13.56 MHz smart card |
| Antenna protrusion on reader | Long-range read possible (prox) |
| Card thickness/material visible | Card tech inference |
| Multiple card types in wallet | Downgrade possible (staff carry both legacy + modern) |

**Links made:**
- Spatial depth from entrance → how many social engineering interactions needed to reach target
- Social permissiveness × credential strength = composite risk score
- Timing: staff rush (0830-0900, 1200-1300) = low scrutiny windows; late evening = opposite

---

### Phase 2: Hypothesis Formation

Expert practitioners use **ACH (Analysis of Competing Hypotheses)** structure, often implicitly.

**Core hypotheses formed (typical engagement):**

```
H1: Tailgate at main entrance during rush
H2: Social engineer secondary/smoking door
H3: Delivery pretext → loading bay
H4: Badge clone → lone access
H5: IT pretext → reception bypass
H6: Visitor badge + escort abandonment
H7: REX/PIR bypass → controlled exit
H8: Contractor uniform + appointment story
```

**Hypothesis testing logic:**

For each hypothesis, identify **discriminating evidence** — signals that would DISPROVE it, not just confirm it:

| Hypothesis | Confirming signal (weak) | Disconfirming signal (strong) |
|---|---|---|
| Tailgate at main entrance | Door held once | Turnstile present / challenged once |
| IT pretext | Reception friendly | Appointments verified by IT directly |
| Badge clone | Reader antenna visible | OSDP Secure Channel + reader tamper alarm |
| Delivery pretext | Loading bay accessible | Pre-scheduled delivery list; ID checked |

**Rule:** Weight evidence by **diagnosticity** — power to discriminate between hypotheses. A single "no" from reception is more diagnostic than 5 friendly interactions.

---

### Phase 3: Rapid Testing (Active Probing)

**Goal:** Convert hypotheses to confirmed/disconfirmed in minimum passes.

#### Social engineering probes:
- **Proximity pass:** Walk toward door as staff exits — observe reaction (hold vs. challenge)
- **Lost badge story:** "I've left my badge at my desk, can you help me?" — observe: who complies, who says "I'll call reception"
- **Delivery box carry:** Approach with hands full — observe automatic door-holding
- **Phone call pretext:** Appear absorbed in phone call while someone else badges in — social cover
- **Visitor badge escalation:** Check in as visitor → observe how visitor escort supervision degrades

#### Spatial probes:
- Walk all publicly-accessible routes (lobby to lift, lobby to stairwell, lobby to toilets)
- Note: which doors require badge vs. which are passive open
- Time: how long between badge swipes on the same door before alarm
- Check: can stairwell be accessed from public area? Does egress lead back to badged zone?

#### Credential probes:
- Flipper Zero / Proxmark3 proximity scan at 125 kHz → read attempt → does card respond?
- Reader LED behavior on failed read vs. successful
- Tail antenna length on reader → long-range feasibility

---

### Phase 4: Entry Execution

Not detailed here (operational). Pattern: lowest-friction path, highest-distraction pretext, fewest human interactions.

**Key principle from war stories:** Entry succeeds or fails on the **first human interaction**, not the last. If the first person challenged says "I'll check," the engagement ends. If they say "Sure, follow me," it cascades.

---

## 3. Social Engineering: Core Patterns

### 3.1 Psychological Levers

| Lever | Mechanism | Counter |
|---|---|---|
| **Helpfulness vs. policy** | Staff default to helping; verification feels rude | Train: "Help by verifying" not "Help OR verify" |
| **Social proof / belonging** | Lanyard + role costume = assumed vetted | Challenge anyone not personally recognised |
| **Authority** | "I'm the CISO's contractor" | Verify with CISO directly, not via stranger |
| **Reciprocity** | Held door creates obligation to hold back | No obligation if you didn't see them badge |
| **Urgency / distraction** | "My meeting starts in 2 min, I just need to—" | Urgency is a social engineering signal |
| **Sympathy** | "Lost my badge, so embarrassing" | Sympathy → temp badge → escorted, not alone |
| **In-group signaling** | Internal jargon, name-drop of internal teams | Any stranger can memorise jargon; it proves nothing |

### 3.2 Pretext Archetypes

**IT Contractor**
- Signal: laptop bag, generic polo, vague "infrastructure upgrade" story
- Exploits: IT = universally trusted; "I just need 10 min in the comms room"
- Fails when: appointments verified with real IT team before entry

**Delivery / Courier**
- Signal: box, clipboard, uniform
- Exploits: loading bay = separate access chain from main reception; delivery staff = low scrutiny
- Fails when: delivery manifest checked; ID required

**Maintenance / Facilities**
- Signal: hi-vis, tool bag, work order printout (fabricated)
- Exploits: facilities staff = everywhere, all hours, treated as invisible
- Fails when: facilities manager queried; work order matched to job system

**Conference / Event Attendee**
- Signal: conference badge (different building), printed email "confirmation"
- Exploits: during events, reception overwhelmed; "overflow" story plausible
- Fails when: event check-in matched against list; escort required

**New Starter**
- Signal: "My access hasn't been set up yet, HR said to ask"
- Exploits: onboarding is messy; HR stories are hard to verify quickly
- Fails when: HR contacted before temp access granted

### 3.3 The Weakness That Beats Every Technical Control

From `06-real-world-war-stories.md`:

> Every successful engagement in the war stories succeeded via social permissiveness, not technical bypass. The "wetware" story (Black Hills): 100% badge-gated, camera-covered building → defeated by one helpful back-office receptionist.

**Technical controls don't fail. Human patterns fail.** RFID cloning matters only if the human social layer is at least somewhat hardened. If staff hold doors, the reader is irrelevant.

---

## 4. Tools Used

*From `dev/toolings/` briefs.*

### Reconnaissance
| Tool | Purpose |
|---|---|
| LinkedIn / OSINT frameworks | Org chart, roles, recent changes |
| UK Planning Register (Idox) | Public floor plans, DAS, sections |
| Google Street View / satellite | Entrance mapping, secondary exits, smoking areas |
| Shodan / Censys | Exposed network services, camera systems |
| Job postings | Access control platform identification |

### Credential
| Tool | Purpose | Notes |
|---|---|---|
| **Proxmark3** | 125 kHz / 13.56 MHz read, clone, emulate | Full research tool; T5577 write for cloning |
| **iCopy-XS** | Prox clone (one-button) | Field-portable; instant |
| **Flipper Zero** | 125 kHz / NFC read + emulate | Good for field recon; limited on smart cards |
| **ESPKey** | Wiegand inline tap; captures 80k credentials | $79; transparent; web UI for replay |
| **BLEKey** | Wiegand tap via BLE | ~$10; no cutting; BLE replay |
| **Doppelgänger** | ESP32 inside reader housing; WiFi/SMTP exfil | Highest stealth; multi-format decode |
| **RFID antenna extender** | Long-range prox read (3+ feet) | Works on 125 kHz; not 13.56 MHz |

### Door bypass
| Tool | Purpose |
|---|---|
| Under-door toolkit | Reaching inside lever; requires ≥10mm floor gap |
| Traveler's hook / loider | Latch-slip on single-latch doors |
| J-hook / wire tool | Crash-bar trigger on double doors via centerline gap |
| Cold-air can ("REX blaster") | Triggers motion/PIR sensor from outside |
| Paper / tape shim | Interrupts PIR beam to trigger egress zone |
| Rare-earth magnet | Reduces maglock holding force; foul face to degrade bond |

### Network / device (once inside)
| Tool | Purpose |
|---|---|
| Rogue AP (WiFi Pineapple / custom) | MITM on open/weak WiFi |
| Rubber Ducky / O.MG cable | HID injection on unlocked workstation |
| LAN Turtle / Shark Jack | Inline MITM on live network jack |
| Bash Bunny | Multi-mode attack platform; exfil + HID + network |

---

## 5. Hypothesis-Making: Speed Heuristics

How experienced practitioners generate and test fast:

### "What's the fastest path to the target space?"

Map: entrance → target room → depth (how many badged doors).  
Each badged door = one required social engineering OR credential bypass.  
**Heuristic:** Path with fewest badged doors + lowest scrutiny staff = best candidate route.

### "What's the social norm here?"

Read: do people challenge strangers? Is there one-by-one badge culture or herd-entry culture?  
**Heuristic:** Herd entry + no turnstiles = tailgate viable with zero credential attack.

### "What does the reader tell me?"

- Old HID MaxiProx bezel → 125 kHz → instantly cloneable  
- No visible antenna → smart card likely  
- Touchless + LED pattern on success → card type inference  
**Heuristic:** Reader ID → credential attack tree pruned/expanded immediately.

### "What human interactions are on my path?"

Count: reception desk, corridor security, floor receptionist, server room keypad.  
Each = a social engineering moment.  
**Heuristic:** One well-placed pretext beats four sequential ones. Find the single person with high access + low skepticism.

### "What's the asymmetric risk?"

Social engineering: if challenged early, story collapses. Badge clone: if cloned badge is on wrong access group, hard failure at reader.  
**Heuristic:** Test social layer first (low commitment); escalate to credential only once social layer assessed.

---

## 6. Link Taxonomy (Cross-Graph)

These are the typed links expert practitioners make between the three graphs — the "cross-graph pivots" that non-experts miss:

| From | To | Link type | Example |
|---|---|---|---|
| Job posting (social) | Access control platform (credential) | `REVEALS` | "Lenel experience required" → C•CURE/Lenel installed |
| Staff role (social) | Physical access zone (spatial) | `GRANTS_ACCESS_TO` | IT staff → comms room, server floor |
| Event (social) | Peak traffic window (spatial) | `CREATES` | Conference → busy lobby → low scrutiny |
| Reader model (credential) | Bypass tool (credential) | `ENABLES` | HID MaxiProx → Proxmark3 clone |
| Floor gap (spatial) | Door tool (credential) | `ENABLES` | >10mm gap → under-door lever |
| Culture ("help first") (social) | Tailgate success rate (spatial) | `AMPLIFIES` | Friendly culture → held doors → bypass |
| Badge visible (social) | Long-range clone (credential) | `ENABLES` | Badge outside shirt + 125 kHz → 3-ft read |
| Delivery bay (spatial) | Delivery pretext (social) | `SUPPORTS` | Loading bay = separate chain → low scrutiny |
| Smoking door (spatial) | Social proof (social) | `CREATES` | Propped door + smokers = zero challenge |
| Access group misconfiguration (credential) | Privilege escalation (spatial) | `ENABLES` | New starter card with broad access → unrestricted |

---

## 7. What Gets Testers Caught (Signal Patterns for the Agent)

From war stories — **disconfirming signals** to weight heavily:

1. **Reception queries IT/organiser before granting access** → terminate pretext, no escalation
2. **Turnstiles present** → tailgating ruled out entirely
3. **Appointments verified against a live system, not a story** → IT/vendor pretext ruled out
4. **OSDP Secure Channel confirmed** (from install docs / job posting) → Wiegand tap attacks ruled out
5. **DESFire EV3 + custom keys** → downgrade attack ruled out
6. **Active camera monitoring with human review** → on-site probing risk elevated
7. **Badge-reader on stairwell doors** → egress cascade closed
8. **Network jacks locked/802.1X NAC enforced** → rogue device attacks constrained
9. **Security culture: staff challenge strangers** (observed during recon pass) → social engineering cost elevated
10. **Mantraps / airlocks at entry** → tailgating physically impossible

---

## 8. Agent Design Implications

For the context-brain agent:

**Input:** Observed cue (e.g. "reader is HID MaxiProx, staff hold doors, conference happening today")

**Process:**
1. Map cue → social/spatial/credential node
2. Traverse links to connected hypotheses
3. Score hypotheses by: evidence weight + disconfirming signal absence
4. Surface top 3 candidates with: supporting cues, missing evidence needed, next test

**Key cognition to encode:**
- RPD: instant pattern → candidate plan (no enumeration for well-known patterns)
- ACH: for ambiguous situations, disprove candidates systematically
- Space-syntax depth: fewer badged doors = lower hypothesis complexity
- Diagnosticity weighting: absence of turnstile is more diagnostic than 5 friendly staff
