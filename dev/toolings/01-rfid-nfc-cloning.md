# RFID/NFC Badge Cloning & Credential Cryptography

**Audience:** Building head of security hardening against an authorized physical penetration test.
**Level:** Threat awareness — what testers do and how you detect/counter it. This is not an intrusion how-to; specific attack steps are deliberately omitted in favor of the defensive controls that neutralize each technique.

---

## Summary

- **~Half of deployed access-control credentials are still 125 kHz low-frequency prox** (HID Prox, Indala, EM4102, AWID). These have **no encryption at all** — the card transmits a static facility code + card number in clear. A tester reads and re-writes one in **under a second**. This is the single highest-impact finding and the cheapest to exploit. *(Confidence: High — corroborated across DEF CON 32 talk, GuidePoint, vendor docs.)*
- **The 13.56 MHz upgrade only helps if you configured it correctly.** iCLASS **Legacy** has been cryptographically broken since **2010** ("Heart of Darkness," Milosch Meriac, 27C3). MIFARE **Classic** with default keys falls in seconds. Only **iCLASS SE / Seos** and **MIFARE DESFire EV3** with **AES-128 and CUSTOM (Elite) keys** are currently considered safe. *(Confidence: High.)*
- **The Elite-key vs. Standard/default-key distinction is the whole ballgame.** A "secure" 13.56 MHz card running the vendor's shared **Standard Profile** key is roughly as good as no encryption, because that key is common across customers and is known to attackers. Customer-specific **Elite/CUSTOM** keying is what actually raises the bar. *(Confidence: High.)*
- **Downgrade attacks defeat your expensive cards if the reader still accepts cheap ones.** A multi-tech ("multiCLASS") reader left in default config accepts both legacy 125 kHz and modern formats. A tester reads the PACS payload off a secure credential and **re-encodes the same facility code + card number onto a $2 legacy T5577/Picopass card** the reader happily accepts. Your DESFire migration is worthless until legacy tech is disabled at the reader. *(Confidence: High — Proxmark3 project `hid_downgrade.md`, DEF CON 32.)*
- **Long-range "Tastic Thief"-style readers and Wiegand-tap implants (ESPKey) move the attack off the door.** A weaponized HID MaxiProx in a backpack lifts a 125 kHz badge from **3+ feet** in a lobby/elevator; an ESPKey spliced into the reader-to-controller cable captures every credential in clear regardless of card type, because the **Wiegand protocol itself is unencrypted**. *(Confidence: High.)*

---

## Tools & What They Defeat

| Tool | What it is | What it defeats | Defensive takeaway |
|---|---|---|---|
| **Proxmark3 RDV4 (RRG/Iceman firmware)** | The reference RFID research/attack platform. Reads, writes, emulates, brute-forces LF and HF. | All 125 kHz prox (instant clone), iCLASS Legacy, MIFARE Classic w/ default keys, and **performs downgrade attacks** (re-encoding secure data onto T5577/Picopass). | Cannot read AES-keyed DESFire EV3 / Seos without the key. Migrating to those + disabling legacy is the counter. |
| **iCopy-XS** | Handheld, point-and-shoot cloner (no laptop, no skill needed). Now lightly supported but widely circulated. | Same LF/weak-HF targets as Proxmark, with near-zero operator skill. Lowers the bar so a non-expert insider can clone. | Same migration counter. Treat "anyone can do it in seconds" as the realistic threat model. |
| **Flipper Zero** | Consumer multi-tool. User-friendly LF/HF read/emulate. | 125 kHz prox instantly; MIFARE Classic with default keys in ~seconds, custom keys in ~a minute via dictionary. | Custom (non-default) keys meaningfully slow it; default keys make encryption meaningless. |
| **Tastic Thief / weaponized long-range reader** (e.g. HID MaxiProx 5375 + ESP32/ESPKey capture) | A commercial long-range reader concealed in a bag, capturing badges at distance. | **125 kHz prox at 3+ feet** — victim never presents the card to a door. Also a parallel HF/iCLASS build where default keys are unchanged. | Range is the danger: defends not at the door but in approach zones (turnstiles, mantraps, distance, defeating tailgating). |
| **Doppelgänger / ESPKey (Wiegand tap implant)** | Postage-stamp board spliced onto the reader's power + Wiegand data lines, MITM-capturing credentials and broadcasting them. | **Every credential type**, because it sits *behind* the card on the unencrypted Wiegand wire. Card crypto is irrelevant here. | Counter is OSDP (encrypted, supervised) + physical tamper protection of reader/cable runs. |

---

## Hype vs. Reality

- **"We upgraded to 13.56 MHz, so we're secure."** — *Reality:* Only true for iCLASS SE/Seos or DESFire EV3 **with custom keys**. iCLASS Legacy (broken 2010) and MIFARE Classic/default-key cards are also 13.56 MHz and are *not* safe. Frequency is not the security property; the cipher and **key management** are.
- **"Encryption protects our access system."** — *Partly theater.* Card encryption protects **data at rest on the card**. It does nothing for the **Wiegand transmission** between reader and controller, which is plaintext. An ESPKey tap bypasses all card crypto. You must address both card-level *and* transmission-level (OSDP) security. *(GuidePoint emphasizes this explicitly.)*
- **"Elite/custom keys aren't worth the hassle."** — *Reality:* Standard Profile keys are shared across the vendor's customer base and effectively public to attackers. Running secure cards on Standard keys gives you a false sense of security at full migration cost.
- **RFID-blocking sleeves/wallets for employee badges = security theater for this threat.** — A sleeve only blocks reads **while the badge is inside it**. The badge gets removed to tap the door, and that's exactly when a long-range reader or shoulder-surfing clone grabs it. Sleeves do nothing against downgrade attacks, Wiegand taps, or a card cloned during normal use. They address a consumer payment-card narrative, not enterprise PACS cloning. Don't fund them as a control. *(Confidence: High — multiple sources note the threat is overstated and sleeves only work when fully covering the card.)*
- **"Multi-tech readers are convenient and safe."** — *Reality:* The convenience (accepting old + new cards) is exactly the downgrade-attack surface. Convenience here = leaving the legacy door open.

---

## Defensive Countermeasures

**1. Migrate credentials to a genuinely secure stack.**
- Target: **Seos** or **MIFARE DESFire EV3** (AES-128, secure messaging, SIO with key diversification). iCLASS SE is acceptable if SE-mode/Seos is enforced, not legacy fallback.
- **Provision CUSTOM/Elite keys, never the vendor Standard Profile / default keys.** Confirm in writing with the integrator that customer-specific keys were loaded on both cards and readers.
- Treat key material like crypto secrets: documented custodian, rotation plan, no sharing across sites unless intended.

**2. Disable legacy technology at the reader — this is what actually kills the downgrade attack.**
- Use the reader management tool (e.g., HID Reader Manager) to **turn off 125 kHz prox and iCLASS Legacy acceptance** on every multi-tech reader.
- Set a **hard organization-wide cut-off date** for legacy. Until that date passes and legacy is disabled, your secure cards provide no real protection — a tester downgrades around them.
- Audit which formats each reader *actually needs* to accept and disable the rest.

**3. Encrypt and supervise the reader-to-controller link.**
- Replace **Wiegand with OSDP (Secure Channel / SCBK)**. This defeats ESPKey/Doppelgänger taps and is supervised (detects line cut). Note OSDP must be run in *secure* mode with custom keys — OSDP in clear mode is no better than Wiegand.

**4. Physically protect readers and cable runs.**
- Tamper-evident or tamper-switched reader housings; route reader cabling inside the secure side of the wall where possible. The ESPKey lives inside the reader/cable bundle precisely to stay hidden.

**5. Reduce reliance on the card alone.**
- Add a second factor at sensitive doors (PIN, mobile credential with device binding, biometric). A cloned card alone then fails.
- Address **long-range/tailgating** physically: mantraps/turnstiles, distance between approach paths and readers, and anti-tailgate enforcement so a badge is never readable from the public approach.

---

## Detection Signals

- **Duplicate / impossible access events.** A cloned badge produces the same card number used in two places, or two reads with timestamps too close together / geographically impossible ("anti-passback" violations). Alert on these.
- **Legacy-format reads after cut-off.** Once legacy is disabled, *any* 125 kHz or iCLASS Legacy read attempt logged at a reader is a strong tampering/downgrade signal. Instrument for it.
- **Reader line/tamper events.** OSDP supervision flags cable interruptions; reader tamper switches flag housing removal — both indicate possible ESPKey installation.
- **Physical inspection findings.** Periodic inspection of door hardware, reader mounting, and cable routes to spot implanted devices before exfiltration.
- **Off-hours / unusual-zone reads** for a credential whose owner is known to be elsewhere.
- **Network/RF anomalies** near readers (an ESPKey may broadcast captured data over Wi-Fi).

---

## Pre-Pentest Checklist

Hand this to the integrator/internal team before the assessment — these are the things the tester will go straight for.

- [ ] **Inventory every reader and credential type.** What % of doors are still 125 kHz prox / iCLASS Legacy / MIFARE Classic? (Expect to find legacy you forgot about.)
- [ ] **Confirm secure credentials use CUSTOM/Elite keys**, not vendor Standard/default keys — get it in writing.
- [ ] **Verify legacy tech is DISABLED at every multi-tech reader.** Don't assume — pull the reader config.
- [ ] **Test it for real:** take a known legacy/T5577 clone card to a production reader and confirm it is **rejected**. A downgrade-attack defense that isn't tested in production is unverified. (Coordinate with the team; do not test live without authorization.)
- [ ] **Confirm reader-to-controller link is OSDP Secure Channel**, not Wiegand and not OSDP-in-clear.
- [ ] **Reader tamper switches enabled and monitored;** cable runs on the secure side.
- [ ] **Anti-passback / duplicate-use alerting enabled** in the PACS and routed to someone who watches it.
- [ ] **Approach-zone review:** can a badge be read from public space (lobby, elevator, queue) at 1–3 ft? Add distance/turnstiles.
- [ ] **Confirm no RFID-blocking-sleeve budget is being counted as a real control.**
- [ ] **Key-management owner identified;** rotation/revocation plan exists for lost/cloned credentials.

---

## Sources

| # | Source | URL | Used for | Confidence |
|---|---|---|---|---|
| 1 | MWR / mwgroup — *Badge Cloning: A Guide for Physical Penetration Testing* (DEF CON 32) | https://mwgroup.slides.com/mwgroup/badge-cloning-a-guide-for-physical-penetration-testing-defcon32 | 125 kHz unencrypted; multiCLASS prevalence driver; Standard vs Elite keys; downgrade to T5577; Heart of Darkness 2010; tools; OSDP recommendation | High |
| 2 | GuidePoint Security — *How Hackers Steal Your RFID Cards* | https://www.guidepointsecurity.com/blog/how-hackers-steal-your-rfid-cards/ | Sub-second LF clone; Proxmark/Flipper; MIFARE Classic default vs custom keys; Wiegand/ESPKey tap; "encryption protects data at rest not transmission"; detection advice | High |
| 3 | NetSPI — *A New Tastic Thief* | https://www.netspi.com/blog/technical-blog/adversary-simulation/a-new-tastic-thief/ | Long-range weaponized reader (HID MaxiProx + ESPKey), 3+ ft 125 kHz capture, HF/iCLASS default-key note | High |
| 4 | RfidResearchGroup Proxmark3 — `hid_downgrade.md` | https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/hid_downgrade.md | Downgrade attack mechanics; readers left in default w/ legacy enabled; disable legacy + use Elite/MOB keys + HID Reader Manager | High |
| 5 | Kevin Chung — *Reverse Engineering HID iClass Master Keys* + Meriac *Heart of Darkness* (27C3, 2010) | https://blog.kchung.co/reverse-engineering-hid-iclass-master-keys/ ; https://get.meriac.com/docs/HID-iCLASS-security.pdf | 2010 iCLASS Legacy break; master-key recovery; Standard vs Elite attacks | High |
| 6 | HID Global product pages (DESFire EV3 / Seos) | https://www.hidglobal.com/products/mifare-desfire-ev3-iclass ; https://www.hidglobal.com/products/single-tech | DESFire EV3 AES-128 + SIO; Seos TÜViT certification; confirms which 13.56 MHz tech is current-secure | Med-High (vendor source; corroborated by independent talks) |
| 7 | RFID-blocking sleeve effectiveness coverage (Norton, Walletopia, Cybernews) | https://us.norton.com/blog/privacy/rfid-blocking ; https://www.walletopia.info/educate/rfid-wallet-still-a-scam/ | Sleeves only work fully covering card; threat overstated; basis for "security theater" flag in enterprise PACS context | Med (consumer-payment framing; reasoned extension to PACS) |

**Notes on confidence:**
- The **~half of credentials still 125 kHz prox** figure is widely repeated across vendor/integrator and pentest sources as a rule-of-thumb, but I did not find a single authoritative survey nailing the exact percentage — treat "roughly half / a very large share" as directionally solid, not a precise statistic. *(Confidence: Medium on the exact number, High on "still a dominant share.")*
- All core technical claims (LF unencrypted, iCLASS Legacy broken 2010, Standard-vs-Elite, downgrade attack, Wiegand plaintext, DESFire EV3/Seos as current-secure) are corroborated across **two or more independent sources** and are High confidence.
- The RFID-sleeve "security theater" judgment is my defensive reasoning applied to the enterprise PACS threat model; the cited sources discuss it mainly in the consumer payment-card context.
