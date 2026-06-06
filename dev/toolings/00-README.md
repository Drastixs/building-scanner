# Physical Pentest Tools → Defensive Countermeasures

A threat-awareness briefing set for a **building head of security hardening against an authorized physical penetration test.** Each file maps what testers actually do with a tool category to the concrete control that detects, blocks, or neutralizes it. Written at awareness level — not intrusion how-to.

## Sections

| # | File | Covers | One-line defensive takeaway |
|---|------|--------|------------------------------|
| 01 | [01-rfid-nfc-cloning.md](01-rfid-nfc-cloning.md) | 125kHz prox cloning, Proxmark3, long-range readers, 13.56MHz credential crypto, downgrade attacks | Migrating credentials is worthless until you **disable legacy tech at the reader** and run **custom/Elite keys** — then verify a legacy card is actually rejected. |
| 02 | [02-wiegand-implants-osdp.md](02-wiegand-implants-osdp.md) | ESPKey / BLEKey / Doppelgänger wiretap implants behind readers, persistent remote exfil | Wiegand is plaintext and untamper-monitored. Move to **OSDP + Secure Channel (hardened, not just enabled)** and add **reader tamper alarms**. |
| 03 | [03-flipper-zero-hype-vs-reality.md](03-flipper-zero-hype-vs-reality.md) | What the Flipper Zero really defeats vs the hype | It only beats legacy/misconfigured systems. **Encrypted-credential migration neutralizes it** — don't overspend chasing the toy. |
| 04 | [04-door-egress-bypass.md](04-door-egress-bypass.md) | Under-door/latch tools, REX/PIR exploitation, maglock theater | Most door attacks abuse the **egress side**. Reposition REX sensors, close door gaps, use deadlatches; maglock holding-force specs and battery backup are largely **theater**. |
| 05 | [05-network-usb-rogue-devices.md](05-network-usb-rogue-devices.md) | Rogue APs/implants on live jacks, Hak5 HID injection (Rubber Ducky/Bash Bunny), why NAC alone fails | **Disable unused switch ports** (cheapest high-value fix). NAC alone won't stop rogue APs — layer **WIPS + MACsec**; enforce **short auto-lock**. |
| 06 | [06-real-world-war-stories.md](06-real-world-war-stories.md) | 10 real-engagement vignettes, what got testers caught, recurring defender mistakes | Entry is almost always a **people/culture** failure. What stops testers: **alert challenging staff, locked screens, verified appointments, encrypted credentials.** |

## Cross-cutting priorities (do these first)

1. **Audit your credential base** — how many 125kHz prox readers/cards are still live? This is finding #1 for the testers (§01, §03).
2. **Disable legacy credential tech at the readers** with a hard cut-off date and **custom/Elite keys**, then physically test that a legacy card is rejected (§01).
3. **Walk every door**: reposition REX sensors away from the gap, close door gaps, confirm deadlatches and that magnet faces can't be tampered (§04).
4. **Disable unused network jacks**; layer 802.1X with WIPS + MACsec; enforce endpoint auto-lock and USB HID control (§05).
5. **Plan Wiegand → OSDP Secure Channel**; in the meantime add reader tamper alarms and faceplate inspection to guard patrols (§02).
6. **Fix the help-vs-policy culture**: train the awkward-moment script and *visibly reward* staff who correctly challenge someone who turns out to be legitimate (§06).

## Confidence & provenance note

These briefs were produced by parallel research agents, each corroborating claims across 2+ sources with per-source confidence flags (see each file's Sources section). Strongest evidence: RFID downgrade attacks, Wiegand/OSDP, rogue-AP/NAC limits (authoritative vendor + practitioner sources). Weaker/directional: the "~half of credentials still 125kHz" prevalence figure, the exact maglock holding-force-loss percentage, and Flipper demo specifics behind paywalled video. Treat specific numbers as order-of-magnitude; treat the directional findings as solid.

**Recovered sources (update).** Two sources that bot-blocked during the agent runs were retrieved with a real-browser User-Agent and folded in:
- **Black Hills "Let's Get Physical — Defeating Wetware Access Controls"** → now **Vignette 11 in §06**, the most on-profile case in the set (a building with RFID-everywhere, no-tailgating signs, guard, cameras, badge elevators — defeated entirely through people).
- **Black Hills "Offensive IoT for Red Team Implants"** → new **LoRa / 915 MHz sub-GHz C2 blind spot in §05** (and cross-referenced in §02): implants that backhaul over LoRa evade Wi-Fi/Bluetooth WIPS and are controllable from the parking lot.
- The **Bishop Fox "Breaking & Entering" PDF** was also retrieved, but proved to be a **network-pentest command pocket-reference, not physical case studies** — so it is *not* load-bearing for any physical finding (corrected in §06 sources). Honest negative result rather than a silent gap.
