# Door / Egress Bypass and the Maglock Problem

> **Audience & framing.** This is a defensive threat-awareness brief for a building head of security preparing for an **authorized** physical penetration test. It describes, *conceptually*, what assessors attempt and — for each item — the concrete control that defeats or detects it. It deliberately omits precise how-to mechanics. The recurring theme: most door electronics are designed for *life safety and convenience first*, and an attacker's whole game is turning those features against you. Several widely-sold "security" measures are **theater** and are flagged as such.

---

## Summary

The single most reliable way into an electronically "secured" door is rarely picking the lock. It is **abusing the egress side** — the hardware that is legally required to let people *out* easily. Three failure clusters dominate, and every credible source (TrustedSec, CyberAdvisors' "Bypassing Doors" series, Bishop Fox, Ahrens Security) keeps landing on the same ones:

1. **Gaps** — under the door and between double doors — let mechanical tools reach the latch, lever, or panic bar from the secured side.
2. **Request-to-Exit (REX) motion sensors** — almost always PIR (heat/motion) — can be fooled from the *wrong* side of the door, releasing a maglock without any credential.
3. **Maglocks specifically** are a soft target: holding force collapses if the magnet face is fouled, and the lock fails open on power loss, so an attacker can simply *wait out* the battery.

The good news for a defender: nearly all of these have cheap, durable, mechanical countermeasures (latch guards, astragals, mullions, deadlatch hardware, repositioned/non-PIR egress sensing, supervised door-position switches, longer battery backup, tamper-resistant magnet mounting). The bad news: many sites have already bought "solutions" that **do not work** (a lock plate on a double door, a 4-hour battery, a maglock whose only health check is a green LED). Those are called out explicitly below.

**Overall confidence: High.** The attack categories and their defenses are consistent across at least 2–4 independent reputable sources. The one quantitative claim that needs a caveat — the exact "50%+ holding-force loss from a small object" figure and its patent provenance — is discussed under [Maglock Security Theater](#maglock-security-theater-what-does-not-work).

---

## Attack Categories (conceptual)

### 1. Under-door tools (reaching the inside lever/handle)
**Concept.** A long, thin tool is slid through the gap *beneath* a door and used to catch and actuate the **inside** lever handle — the side that, by design, opens freely. Lever handles are especially exposed because a hook can catch and pull/press them; round knobs are harder to engage. This works on any door with (a) enough floor gap and (b) operable inside hardware. *Confidence: High — TrustedSec and the CyberAdvisors series both call this out.*

**What enables it:** excessive floor clearance, lever (vs. knob) inside hardware, and hardware mounted low/near the gap.

### 2. Traveler's hooks / latch slips / loiding ("carding")
**Concept.** "Loiding" (from celluloid/"carding") means slipping a thin, stiff implement into the gap between door edge and frame to push a **spring latch** back into the door without turning the handle. A **traveler's hook / latch-bypass hook** is the purpose-built thin tool assessors use to reach and slip latches or poke at inside hardware. This is purely a *spring-latch* attack — see deadlatch below. *Confidence: High — corroborated by TrustedSec, CyberAdvisors, and the broader pentest tool literature (e.g. Red Team Tools' "traveler hook," popularized by Deviant Ollam).*

### 3. Deadlatch vs. spring latch (why the above sometimes fails)
**Concept.** A plain **spring latch** can be pushed back (loided) directly. A **deadlatch** (deadlocking latch) adds a small secondary plunger that, when the door is closed, rests against the strike and *blocks* the main latch from being depressed. If the deadlatch plunger lands correctly on solid strike material, loiding fails. The common real-world failure is a **missing or misaligned deadlatch plunger**, or a plunger that falls into the strike cutout instead of resting on the plate — which silently downgrades a deadlatch back to a defeatable spring latch. *Confidence: High — TrustedSec explicitly flags missing dead-latch plungers.*

### 4. Crash-bar / double-door tools (DDT, J-hook, wire tools)
**Concept.** Double doors with panic/crash-bar (push-to-exit) hardware are vulnerable at the **centerline gap** between the two leaves. An L-shaped "Double Door Tool," a J-hook, or a bent-wire tool is passed through that gap and manipulated to **depress the panic bar from the outside** — actuating the exact life-safety release the bar exists to provide. The vulnerability is the *gap*, not the bar. *Confidence: High — CyberAdvisors "Bypassing Doors Part 2 (DDT)," plus the DEF CON covert-entry tool literature (J-hook, wire crash-bar tools).*

### 5. REX / PIR request-to-exit motion sensors triggered from the wrong side
**Concept.** Most overhead REX sensors are **PIR** — they fire on a change in infrared (heat) within their field of view, then drop the lock so someone can leave. Two problems: (a) PIR cannot tell *which side* the motion came from, and (b) if the sensor is mounted close to the door, an attacker on the *outside* can introduce a stimulus **through the door gap**. The two canonical stimuli:
- **A thin object** (paper, shim) pushed through the gap and waved to create apparent motion.
- **Cold air** — an inverted can of compressed air / "keyboard duster" sprayed through the gap. The sudden temperature change reads as a body to the PIR. Purpose-built nozzles to deliver this air precisely are referred to colloquially as **"REX blaster"**–type tools.

TrustedSec's blunt framing: *"Your \$200 REX sensor / magnetic lock setup can be bested by an \$8 can of compressed air."* CyberAdvisors devotes its REX installment to the paper-through-the-gap technique and flags compressed air as the follow-on. *Confidence: High — TrustedSec and CyberAdvisors independently describe both the thin-object and cold-air variants.*

### 6. Door-position-switch (DPS) tampering
**Concept.** The contact that tells the system "door is closed/secure" is often a simple, **unsupervised magnetic reed switch**. If it can be reached or influenced, an attacker can make a propped/open door report **closed** (e.g., presenting an external magnet to the reed so it never sees the door leave), suppressing the door-forced / door-held alarm. The defense is a *supervised, balanced* switch that detects substitution, not a plain reed. *Confidence: Medium-High — this is standard access-control engineering guidance; less prominent in the four named blog sources but well established in the field and implied by their alarm-suppression discussions.*

---

## Maglock Security Theater (what does NOT work)

Maglocks deserve their own section because they are the most over-trusted device on the door, and several "fixes" sold for them are **theater**.

- **THEATER — "the magnet holds 1,200 lb so the door is solid."** Holding force is rated only with a *clean, flush, fully-seated* armature. Foul or shim the contact face — even a small object on the magnet face, the proverbial **band-aid** — and holding force drops sharply, after which the door can be **shoulder-forced**. Ahrens Security describes exactly this (small cover on the lock → "significantly decreased" holding force → brute-force/shoulder attack).
  - **The "50%+" / patent claim, with a confidence caveat:** the physics is real and well-understood — magnetic flux falls *exponentially* with air-gap, so even a thin shim/spacer causes a large force loss. Patent and engineering literature on electromagnetic locks/brakes describes deliberately using a shim/spacer to cut holding force (one electromagnetic-brake patent cites reducing holding voltage "by as much as 50%"), and field guidance commonly cites a ¼-inch gap cutting effective force ~30–50%. **Confidence: Medium** that a *specific single maglock patent* states ">50% from a small object"; **High** that "a small object on the magnet face cuts holding force by roughly half or more" is accurate. Treat the exact number as directional, not as a citable spec.

- **THEATER — "it has a battery backup, so power loss is covered."** Maglocks are **fail-safe**: no power, no lock. A typical **4-hour** backup is a documented attacker plan — Ahrens notes aggressors may simply **wait out the battery runtime** and walk in when it dies. A short battery isn't a defense; it's a countdown.

- **THEATER — the green/red status LED as "proof it's secure."** Ahrens flags that red/green indicators **tell the attacker which door is locked and live** without confirming the magnet is actually *bonded* to the armature. An LED that just means "energized" is reconnaissance for the attacker, not assurance for you. Real assurance comes from a **bond/holding-force sensor**, not a power LED.

- **THEATER — relying on a REX-released maglock as the *only* lock.** Because the maglock drops on any valid-looking REX event, a maglock-plus-PIR door inherits *every* REX weakness above. A maglock is only as strong as the egress sensing and the door-position monitoring around it.

- **Shear locks:** Ahrens advises **avoiding shear locks**; standard direct-hold maglocks of adequate force are preferred.

---

## Defensive Countermeasures

Mapped one-to-one to the attack categories. Prefer **mechanical, passive** controls — they don't have a battery to wait out.

| Threat | Control |
|---|---|
| Under-door tools | **Close the floor gap**: door sweeps / automatic door bottoms / **kick plates** sized to the gap. Move inside hardware higher/away from the gap; prefer knobs or shrouded levers; consider repositioning the lever ~90° so a hook can't easily catch it. |
| Loiding / latch slip | **Latch guard / astragal** over the door-edge gap so a thin tool can't reach the latch. Use a **rubber molding / door shoe** to deny the gap. |
| Spring latch defeat | Specify **deadlatch (deadlocking latch) hardware** and — critically — **verify the deadlatch plunger seats on solid strike**, not into the strike cutout. A deadlatch installed wrong is just a spring latch. |
| Crash-bar / double doors | Install a **vertical mullion** (removable if needed for egress width) to eliminate the centerline gap — this is the real fix. An **astragal / overlapping edge / blocking plate** helps but, as CyberAdvisors notes, only *inconveniences* an attacker; treat the mullion as primary. |
| REX / PIR wrong-side trigger | **Reposition and re-angle the REX** so its field of view points *into the room and away from the door leaf/gap* — it should not see anything that can be reached from outside. **Close the door gaps** (astragal/sweep/kick plate) so no object or air jet reaches the sensor. Best of all, **move away from single-PIR egress**: use **non-PIR egress sensing** — a **push-to-exit button**, **request-to-exit integrated in the panic bar (mechanical RX)**, or a **touch/press bar** — so release requires a deliberate human action on the inside, not just detected "motion/heat." Where PIR is retained, **dual PIRs on opposite sides wired in series** (must both agree) resist single-point spoofing. |
| Maglock holding-force loss | **Tamper-resistant, flush magnet mounting** with tamper-evident fasteners; **inspect the armature/magnet faces** for fouling; pair the maglock with a **mechanical latch (deadlatch)** so the door isn't relying on magnetism alone. Use a **strong door closer** so the leaf fully seats against the magnet. Specify adequate holding force (≥~1,200 lb) and **avoid shear locks**. |
| Maglock power/battery | **≥8-hour battery backup**, **batteries replaced annually**, and monitored so a depleted/aging battery raises a ticket *before* it dies. Longer runtime + supervision converts "wait out the battery" into "trip an alarm." |
| Status-LED recon | Use a **bond sensor** (confirms the magnet is actually holding the armature) feeding the access system; don't rely on a power LED. Where possible, avoid exterior-visible lock-status indicators that reveal which door is live. |
| Door-position switch tamper | Replace plain reed contacts with **balanced/biased (3-state) supervised magnetic switches** that detect magnet substitution and line tampering; alarm on **door-forced** and **door-held-open**; route DPS wiring out of reach. |

---

## Detection Signals

Even where prevention is imperfect, these signals catch an in-progress or rehearsed attack:

- **Door-forced-open (DFO)** alarm from a *supervised* DPS — fires if the door opens without a valid grant. The single highest-value alarm on the door.
- **Door-held-open (DHO)** alarm — flags propping and "wait out the battery" staging.
- **REX-without-egress-then-entry pattern:** a REX/exit event that drops the lock with **no badge read**, immediately followed by an *entry* — classic wrong-side trigger. Correlate REX events against camera and badge logs.
- **Repeated/irregular REX fires** at odd hours, or REX events with no corresponding human leaving on camera (the paper/cold-air signature).
- **Maglock bond-sensor faults / "not bonded while locked"** — indicates fouling, misalignment, or a propped/shimmed door.
- **Backup-battery low/aging telemetry** and **AC-power-loss events** on door controllers.
- **DPS supervision faults** (out-of-range/short/open) — the signature of switch tampering or magnet substitution.
- **Tamper-fastener disturbance** on maglock/armature/sensor housings, found on routine inspection.

---

## Pre-Pentest Door Walk Checklist

Walk every in-scope perimeter and sensitive-area door and check:

- [ ] **Floor gap** small enough to defeat under-door tools? Sweep / auto door bottom / kick plate present and intact?
- [ ] **Door-edge gap** covered by a **latch guard / astragal**? Can a thin tool reach the latch?
- [ ] **Inside hardware**: lever vs. knob; is it reachable/catchable from the gap? Shrouded or repositioned?
- [ ] **Latch type**: true **deadlatch**, and does the **plunger seat on solid strike** (not into the cutout)?
- [ ] **Double doors**: is there a **mullion**? If only an astragal/plate, note it as partial. Measure the **centerline gap**.
- [ ] **REX sensor**: PIR or non-PIR? **Field of view angled away from the door/gap?** Can paper or a cold-air jet reach it through the gap? Single PIR, or dual-PIR-in-series / button / mechanical bar RX?
- [ ] **Maglock**: holding force rating; **shear lock?** (flag); magnet face flush/clean; **tamper-evident mounting**; paired with a mechanical latch?
- [ ] **Maglock LED**: does an exterior indicator reveal lock status? Is there a real **bond sensor** vs. just a power LED?
- [ ] **Battery backup**: runtime **≥8h**? Battery age/last-replaced date? Monitored for low/aging?
- [ ] **Door-position switch**: plain reed or **balanced/supervised**? Wiring reachable? DFO/DHO alarms actually wired, armed, and **monitored** (not just logged)?
- [ ] **Door closer**: leaf fully self-closes and seats against the magnet/strike every time?
- [ ] **Alarm-to-response loop**: when DFO/DHO/bond-fault fires, does *someone* actually see and respond? (An unwatched alarm is theater too.)

---

## Sources (URLs + confidence)

| Source | Used for | Confidence |
|---|---|---|
| TrustedSec — *Three Most Common Physical Security Flaws and How to Fix Them* — https://trustedsec.com/blog/three-most-common-physical-security-flaws-and-how-to-fix-them | REX/PIR cold-air trigger ("\$8 can of compressed air"), under-door lever attack, missing deadlatch plunger, double-door gaps, fixes (door bottoms, plates, repositioned handles). | High |
| CyberAdvisors — *Bypassing Doors Part 3: REX Sensor* — https://blog.cyberadvisors.com/technical-blog/blog/bypassing-doors-part-3-rex-sensor | PIR works on heat/motion, paper-through-gap trigger, compressed-air follow-on; defenses (reposition sensor, kick plates, rubber moldings, door shoes). | High |
| CyberAdvisors — *Bypassing Doors Part 2: DDT* — https://blog.cyberadvisors.com/technical-blog/blog/bypassing-doors-part-2-ddt | Double-door / crash-bar centerline-gap attack; mullion as primary fix, lock plate only partial. | High |
| Ahrens Security (Sean Ahrens) — *Unveiling Vulnerabilities in Magnetic Locks* — https://www.ahrenssecurity.com/news/unveiling-vulnerabilities-in-magnetic-locks:-insights-from-a-security-consultant-and-expert-witness | Small object (band-aid) on magnet face → reduced holding force → shoulder-force; 4-hour battery "waited out"; red/green LED recon; bond sensors; ≥8h battery + annual replacement; ≥1,200 lb force, avoid shear locks; door closer; dual-PIR-in-series. | High |
| Bishop Fox — *Breaking & Entering: A Guide for Pentesters/Red Teams* — https://bishopfox.com/resources/breaking-and-entering-guide | General authoritative framing for authorized covert-entry/physical pentest methodology. (Note: the public guide leans toward overall engagement methodology; specific door-bypass mechanics were corroborated from the sources above and the DEF CON covert-entry tool literature.) | Medium |
| Red Team Tools — *Traveler Hook / Latch Bypass Tool* — https://www.redteamtools.com/traveler-hook-steel ; *We Hack People — Crash Bar Bypass Tools (DEF CON 26)* — https://wehackpeople.wordpress.com/2018/08/09/crash-bar-bypass-tools-for-def-con-26/ ; Fire Hooks Unlimited J-Hook — https://www.elevatorkeys.com/Fire-Hooks-Unlimited-J-Hook-double-door-rapid-entry-panic-lock-bypass-tool | Existence/role of traveler's hook (loiding), J-hook and wire crash-bar tools — names/roles only, conceptual. | High (that tools exist/are used) |
| Maglock air-gap physics / patent context — Google Patents *US20160047144A1 Low-power magnetic lock* https://patents.google.com/patent/US20160047144A1/en ; electromagnetic-brake shim patent (USPTO 6439355) https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6439355 ; National Lock Supply maglock guide https://nationallocksupply.com/blog/how-to-choose-a-magnetic-lock-maglock/ | Flux falls exponentially with air-gap; shim/spacer can cut holding force ~50%; ¼-inch gap ~30–50% loss. Supports the "small object cuts holding force by ~half+" claim. | Medium (exact ">50% per a single maglock patent"); High (the underlying physics & direction) |

**Confidence note on the headline maglock figure:** "a small object on the magnet face cuts holding force by more than 50%" is **directionally well-supported** (exponential flux-vs-gap physics; brake-shim patent citing ~50%; field guidance citing 30–50% for a ¼-inch gap). Attributing the exact ">50%" to one specific maglock patent is **Medium confidence** — present it as "roughly half or more," not as a hard spec.
