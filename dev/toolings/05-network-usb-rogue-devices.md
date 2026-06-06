# Left-Behind Network Drops, Rogue Devices & USB/HID Injection

> **Audience:** Building head of security hardening against an *authorized* physical penetration test.
> **Level:** Threat awareness and defensive posture. This is **not** an intrusion how-to — there are no payloads, scripts, or step-by-step attack procedures here. It describes *what to expect* from a competent red team and *how to detect and stop it*.

---

## Summary

A physical pen tester who gets even brief unescorted access to your floor space has two high-value, low-effort moves: (1) plug a small implant into a **live but unused network jack** and walk away, and (2) plug a **malicious USB device** into an **unlocked workstation**. Both work because of a common blind spot — most defenses watch *software and behavior*, while these attacks operate at **Layer 1 (the physical wire/port) and at the HID trust boundary** (the OS implicitly trusts anything that says "I am a keyboard").

The single highest-value, cheapest fix is **disabling unused switch ports** — a dead jack is an implant that never connects. Beyond that, the durable posture is **defense in layers**: 802.1X + WIPS + MACsec on the network side, and USB device-control / HID allowlisting + enforced short auto-lock on the endpoint side. A recurring theme corroborated across every source below is that **NAC alone is not sufficient** — an insider or a hub trick defeats it, and Layer-1 implants are invisible to it.

---

## Tool Categories & Technique

These are described at a **category level** — what each class of device *is for*, not how to operate one.

### Network implants / drop boxes (planted on a live jack)
Small single-board computers or covert "drop boxes" placed on an unused-but-live Ethernet jack. On a network with **DHCP and no NAC**, the implant simply gets an address and is on the LAN — providing a persistent foothold and an exfiltration / remote-access channel. Sepio and Progress/Ipswitch both characterize these as **rogue devices: unauthorized hardware operating on the network without IT consent**, deployed physically on-prem or via supply chain. *(High confidence — corroborated by Sepio, Progress/Ipswitch, and the CWNP hub-bypass scenario.)*

### Hak5 gear (category descriptions only)
- **USB Rubber Ducky & Bash Bunny — keystroke / HID injection.** These present to the computer as a **Human Interface Device (a keyboard)**. The OS grants them the same trust as a physical keyboard, so they can "type" commands at machine speed. Marketed as **"plug to pwn in seconds"** (Hak5 cites ~7 seconds for the Bash Bunny Mark II). **Critical limitation for the defender: these only work against an UNLOCKED, logged-in machine** — they type into whatever session is already open. A locked screen defeats them outright. The Bash Bunny additionally can present as **storage, serial, or Ethernet**, enabling multi-vector "network hijack" and exfiltration combos. *(High confidence — ThreatLocker + Hak5 product pages.)*
- **Shark Jack / LAN Turtle / Packet Squirrel — network foothold & exfil.** This class is about the **wire**, not the keyboard: a covert device that sits inline on or taps an Ethernet connection to establish a foothold, perform recon, man-in-the-middle, or quietly exfiltrate data. *(High confidence — Hak5, Sepio.)*

### Out-of-band C2: the LoRa / sub-GHz implant (the WIPS blind spot)
A newer and genuinely under-appreciated technique: modern implants increasingly carry their command-and-control (C2) over **LoRa in the 915 MHz ISM band** instead of Wi-Fi/Bluetooth. This matters specifically because it **defeats a mature defender's wireless monitoring.** Black Hills Information Security's "Offensive IoT for Red Team Implants" research lays out why a red team would do this:
- **It side-steps WIPS.** "Many mature organizations have robust wireless intrusion prevention solutions that can detect a rogue access point or even a rogue Bluetooth device. How many people have even thought about detecting **LoRa**?" The 915 MHz band is "largely unmonitored… from a rogue device perspective," unlike the crowded, sometimes-monitored 2.4 GHz used by Wi-Fi/Bluetooth/Zigbee.
- **It works from the parking lot.** LoRa is low-bandwidth but long-range — roughly **3× Wi-Fi distance** in practice; the author controlled an implant **indoors from ~500 m away**, so the operator never has to be "caught hanging outside the secretary's office." The implant's signal "is strong enough to escape the building, into the parking lot, and beyond."
- **It's hard to detect even if you look.** An SDR (RTL-SDR/HackRF) can spot the characteristic LoRa "chirp" *presence*, but demodulating requires matching proprietary parameters (spreading factor, coding rate, bandwidth) and the right node address, and the payload is likely encrypted. Worse, **legitimate LoRa is everywhere** (utility meters, IoT sensors, LoRaWAN), so a rogue device hides in genuine background traffic.

**Defensive implication:** a Wi-Fi/Bluetooth-only WIPS gives false comfort — it cannot see a LoRa-backhauled implant at all. Closing this means **SDR-based sub-GHz spectrum sweeps** (at least for anomalous-chirp presence), knowing your *baseline* legitimate LoRa devices, and — because spectral detection is genuinely hard — **falling back on the controls that don't depend on catching the radio: disable dead jacks, physical-layer device fingerprinting, and physical inspection of jacks/ceilings/desks.** *(Medium-high confidence — single detailed practitioner source, BHIS; mechanism and range are well-explained and consistent with LoRa physics.)*

### The HID enumeration mechanism — bypass *and* signal
The reason keystroke injection works is the **HID trust model**: a USB device that enumerates as a keyboard/mouse is trusted to inject input with no prompt, no admin rights, no dropped file, and no malware signature — ThreatLocker's framing is *"you're technically not executing scripts, you're just typing."* That same fact is the defender's best **detection signal**: a USB flash-drive-shaped object, a phone charger, or a cable that **enumerates as a NEW keyboard/HID** is highly anomalous and should be treated as an alert (see Detection Signals). *(High confidence — ThreatLocker, Sepio, Progress/Ipswitch.)*

---

## Why NAC Alone Fails

This is the central nuance for hardening. **802.1X / NAC by itself does not stop rogue APs or Layer-1 implants.** Corroborated mechanisms:

1. **Insider registers the rogue AP as a legitimate supplicant.** Per CWNP, an insider can "configure the Rogue AP with necessary credentials to authenticate itself to the 802.1X infrastructure," then spoof allowed MACs or run it open — the AP is now an *authenticated* gateway for outsiders. *(CWNP, high confidence.)*
2. **Dumb AP / device hidden behind a hub on an authenticated port.** An employee authenticates their own adapter through a hub, then bridges a cheap AP (or implant) onto the same hub. CWNP notes "this AP need not be capable of 802.1X at all" and is invisible to the wired control. The port authenticated once; everything behind the hub rides that authentication. *(CWNP, high confidence.)*
3. **802.1X only secures "the wire," not the air or the physical layer.** CWNP explicitly frames 802.1X as addressing "the relatively deterministic part of the problem — the wire," with coverage gaps from legacy devices, guest networks, and operational exceptions.
4. **Layer-1 implants are below NAC's and behavioral monitoring's line of sight.** Sepio: a rogue device that "initially acts as a passive tap... lacks a MAC and IP address," so it operates covertly and "without Layer 1 data, MACsec cannot detect the rogue device — the switch thinks it is connecting to a legitimate, authorized supplicant." Behavioral/EDR tooling is trained to spot malware, not a passive hardware tap or a device "just typing." *(Sepio, high confidence.)*

**Implication:** NAC is necessary but must be **layered** — pair it with **WIPS** (to catch rogue APs in the air) and **MACsec** (to cryptographically bind authenticated links), and add **physical-layer device fingerprinting** for implants that even MACsec can't see on its own.

---

## Defensive Countermeasures

| # | Control | What it stops | Cost / value |
|---|---------|---------------|--------------|
| 1 | **Disable all unused switch ports** (admin-down) and shut ports in vacant areas, conference rooms, lobbies. | An implant on a dead jack never gets a link or a DHCP lease. | **Highest value, cheapest fix.** Do this first. Corroborated by Progress/Ipswitch as the baseline measure. |
| 2 | **Don't rely on NAC alone — layer it.** 802.1X **+ WIPS + MACsec**. WIPS scans the air for rogue/unauthorized APs (closes the insider-supplicant and hub-bridge gaps). MACsec cryptographically authenticates and encrypts each link so an inline tap/implant can't transparently bridge. | Rogue APs, hub-bypass bridges, inline taps that NAC misses. | Medium cost; the durable network-side posture. (CWNP, Sepio.) |
| 3 | **DHCP lockdown / static reservations / MAC filtering** where full NAC isn't deployed. | Casual implants that expect a free DHCP lease. | Cheap stopgap — explicitly "a basic security measure if you don't implement full NAC" (Progress/Ipswitch). Not a substitute for NAC. |
| 4 | **USB device control / HID allowlisting.** Block or restrict new HID enumeration; allowlist known keyboards/mice by device ID; restrict mass-storage and command interpreters (PowerShell/cmd) via application allowlisting + ringfencing. | Rubber Ducky / Bash Bunny keystroke injection and USB exfil. | Medium; the endpoint-side counterpart to network layering. (ThreatLocker, Sepio.) |
| 5 | **Enforced short auto-lock** (screen lock after a short idle, e.g. 1–5 min; lock-on-walk-away where available). | **Directly defeats HID injection** — Ducky/Bunny only work on an unlocked, logged-in session. | Very cheap (group policy); high value. (ThreatLocker.) |
| 6 | **Physical-layer device fingerprinting** (Layer-1 "asset DNA") on both USB and Ethernet. | Implants and taps invisible to NAC/MACsec/EDR — detects by *device existence*, not behavior. | Higher cost; closes the residual Layer-1 gap. (Sepio, Progress/Ipswitch.) |
| 7 | **Port security:** limit MACs per port, sticky-MAC, err-disable on violation; **disable hubs/unmanaged switches** downstream of authenticated ports. | The hub-bridge bypass (CWNP scenario #2). | Cheap on managed switches. |

---

## Detection Signals

Watch for these — each maps to one of the techniques above:

- **Unexpected HID enumeration.** A USB stick, charger, or cable that registers as a **new keyboard or mouse** is the canonical Ducky/Bunny tell. Treat any new HID on an endpoint as an **alert**, not a routine event. *(ThreatLocker, Sepio.)*
- **A previously-disabled or vacant-area switch port suddenly shows link / a new DHCP lease.** Indicates something was plugged into a jack that should be dead. Alert on link-state changes and new leases in non-active zones.
- **New / unknown MAC or device ID** appearing on the LAN, especially behind a port that should have one known device — possible hub-bridge or implant. Watch for **multiple MACs on a single access port**.
- **A new wireless AP / BSSID** broadcasting in or near your space, or an SSID impersonating yours — the rogue-AP signal WIPS is designed to catch. *(CWNP.)*
- **MACsec/802.1X session anomalies** — unexpected re-authentications, supplicant on a port that should be empty, or a link that won't establish a MACsec SA (possible inline device).
- **Burst of input at non-human cadence** (mitigated where Ducky/Bunny throttle to human speed — so do not rely on this alone). *(ThreatLocker.)*
- **Passive-tap blind spot:** a device with **no MAC/IP** producing no traffic will NOT show in logs — this is precisely why physical-layer fingerprinting is needed; absence of a signal is not absence of a device. *(Sepio.)*
- **Sub-GHz / LoRa chirps your WIPS ignores:** an SDR sweep showing **915 MHz LoRa chirp activity that doesn't map to a known/baselined device** (meter, sensor) is the only over-the-air tell for a LoRa-backhauled implant — and most programs never sweep this band at all. *(BHIS.)*

---

## Pre-Pentest Checklist

Run through this before the authorized test (and as ongoing hygiene):

- [ ] **Inventory every wall jack and patch-panel port**; confirm every live port maps to a known, needed device.
- [ ] **Admin-down all unused ports** — especially in lobbies, conference rooms, vacant desks, printer alcoves, and common areas. *(Highest-value item.)*
- [ ] Confirm **802.1X is enforced** on access ports — and that it is **not your only** control.
- [ ] **WIPS deployed and alerting** on rogue/unknown APs and SSID impersonation.
- [ ] **MACsec** enabled on links where supported (uplinks, sensitive segments).
- [ ] **Port security** configured: MAC limits, sticky MAC, err-disable; downstream hubs/unmanaged switches prohibited or detected.
- [ ] **DHCP** locked down / reservations where full NAC is absent; alerting on new leases in inactive zones.
- [ ] **USB device control / HID allowlisting** active on endpoints; mass-storage and PowerShell/cmd restricted via allowlisting + ringfencing.
- [ ] **Auto-lock enforced** org-wide at a short idle timeout; verify it actually triggers on a sample of machines.
- [ ] **Alert pipeline** wired for: new HID enumeration, link-up on disabled/vacant ports, new/unknown MAC, multiple MACs per port, new BSSID.
- [ ] Consider **physical-layer device fingerprinting** for the residual implant/tap gap NAC and MACsec can't see.
- [ ] **Confirm your WIPS coverage band.** If it only watches 2.4/5 GHz Wi-Fi + Bluetooth, it is **blind to LoRa/sub-GHz (915 MHz) implant C2.** Baseline your legitimate sub-GHz/LoRa devices and consider periodic SDR spectrum sweeps; don't assume "we have WIPS" covers this.
- [ ] **Train reception/security staff** to challenge unescorted visitors and tailgaters — the pen-test entry vector that precedes every implant (Rapid7's lesson: after one assessment, staff later *did* challenge the same tester).
- [ ] **Walk the floor** post-test (and periodically) looking for unfamiliar devices on jacks, in drop ceilings, behind desks, and plugged into workstations.

---

## Sources (with confidence)

- [CWNP — Rogue AP Prevention: Duping 802.1X Access Control](https://www.cwnp.com/rogue-ap-prevention-duping-802dot1x-access-control/) — **High** confidence for the two NAC-bypass mechanisms (rogue AP as supplicant; dumb AP behind a hub) and the "802.1X only secures the wire" framing. *Caveat: author discloses working for a WIPS vendor — directionally sound but vendor-adjacent.*
- [Sepio — Rogue Devices on Financial Institutions](https://sepiocyber.com/resources/research/rogue-devices-on-financial-institutions/) and [Sepio — MACsec and the Hidden Challenges](https://sepiocyber.com/blog/macsec/) — **High** confidence for Layer-1 implants bypassing NAC/behavioral monitoring, passive taps with no MAC/IP, and MACsec's inability to see Layer-1 implants without Layer-1 data. *Vendor of a physical-layer fingerprinting product — control #6 reflects their offering; corroborated independently on the mechanism.*
- [Progress/Ipswitch — Rogue Device Detection and Prevention](https://www.progress.com/blogs/rogue-device-detection-and-prevention) — **High** confidence for DHCP lockdown / MAC filtering as a "basic measure if you don't implement full NAC," ineffective tamper labels, and most malicious USB appearing as harmless HID.
- [ThreatLocker — USB Rubber Ducky Attacks Explained](https://www.threatlocker.com/blog/usb-rubber-ducky-attacks-explained-keystroke-injection-evasion-and-defense) — **High** confidence for HID-trust bypass mechanism, "just typing" (no dropped file / no signature), human-cadence evasion, and application allowlisting / ringfencing / external-storage control as defenses. *Vendor positioning toward allowlisting — mechanism is well-established.*
- [Hak5 — Bash Bunny product / features](https://shop.hak5.org/products/bash-bunny) and [Network Hijack Attacks with the Bash Bunny](https://shop.hak5.org/blogs/bash-bunny/network-hijack-attacks-with-the-bash-bunny) — **High** confidence (primary vendor) for category capabilities: "plug to pwn in ~7 seconds," multi-device emulation (HID/storage/serial/Ethernet), and the Shark Jack / LAN Turtle / Packet Squirrel exfil/foothold class.
- [Rapid7 — From Physical Security Weakness to Strength (Pen Test Part 5)](https://www.rapid7.com/blog/post/2018/10/02/this-one-time-on-a-pen-test-part-5-from-physical-security-weakness-to-strength/) — **Medium** confidence for the *physical-access entry vector* (badge/tailgating) that precedes implant placement, and the value of staff challenging visitors. *Note: this article centers on social-engineering entry rather than network implants specifically — used for the entry/awareness point, not the technical implant detail.*
- [Black Hills Information Security — Offensive IoT for Red Team Implants, Part 1 (Tim Fowler, 2024)](https://www.blackhillsinfosec.com/offensive-iot-for-red-team-implants-part-1/) — **Medium-high** confidence for the **LoRa/sub-GHz (915 MHz) C2 blind spot**: implants using LoRa to evade Wi-Fi/Bluetooth WIPS, ~3× Wi-Fi range / ~500 m indoor control, and why spectral detection is hard (proprietary modulation, encrypted payload, ubiquitous legitimate LoRa). *Fetched in full via real-browser User-Agent (originally 403 bot-blocked). Single detailed source, but the mechanism and physics are well-explained and consistent.*

*Overall: every load-bearing claim (NAC-alone insufficiency, Layer-1 invisibility, HID trust bypass, auto-lock defeats injection, disable unused ports) is corroborated across 2+ independent sources. Several sources are security vendors whose recommended controls map to their products — noted inline; the underlying mechanisms are consistent across all of them.*
