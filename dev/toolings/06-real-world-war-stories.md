# Real-World Physical-Pentest War Stories: Defensive Lessons

> **Audience:** Building head of security preparing to harden against an AUTHORIZED physical penetration test.
> **Purpose:** Threat-awareness, not a how-to. Each vignette extracts the *defensive lesson* and the *recurring defender mistake* the tester exploited. The point is to recognize these patterns in your own building before a tester (or a real adversary) does.

---

## Summary

Across a decade-plus of published physical-pentest war stories from multiple firms (Rapid7, Triaxiom, Raxis, TrustedSec, Bishop Fox, RedTeam/CyberCrowd, Black Hills, the "We Hack People" blog, and the DEF CON Physical Security Village), the same handful of failures show up again and again. Testers almost never defeat a *technical* control to get in. They defeat **people and habits**: a held door, a polite "good morning," a hi-vis vest, an "I'm from IT" line at a reception desk, an unlocked screen, an open network jack. The strong recurring finding is that **physical-entry success is overwhelmingly a social-engineering and culture problem, not a hardware problem.**

The flip side is equally consistent: when testers *do* get caught or stopped, it is almost always a **human** who does it — an alert assistant who stands her ground and calls security, a help-desk employee who refuses to grant access and says "even I don't have that," a guard who refuses after-hours entry without point-of-contact sign-off, a receptionist enforcing a sign-in policy. Locked screens, encrypted credentials, network segmentation, and verified vendor appointments turn a full compromise into a contained incident. **Trained, empowered, slightly suspicious staff are the single most effective physical control** — far more than cameras (frequently unmonitored) or badge readers (which verify a credential but cannot count how many people walked through the door).

A specific reality worth internalizing: **badge/prox cloning requires the attacker to get within roughly 4–7 inches of the badge.** Long-range cloning is largely aspirational. That proximity requirement is a *detectable human signature* — someone getting unusually close, or asking "can I see your badge?", is the tell.

---

## War-Story Vignettes

### 1. The fake badge, the held door, and the help desk that said "no" — *(Rapid7)*
**What the tester did (high level):** Watched employees in the parking lot and a nearby Starbucks to learn what badges looked like and the building's rhythm, fabricated a lookalike badge, then blended into the ~4:30 p.m. exit crowd, holding doors and riding an employee's badge scan up the elevator. Later he approached the help desk posing as "a new employee on the security team," stuck working late, asking for a phone charger — using small talk to probe for server-room access.
**Why it worked (and where it stopped):** The door-tailgating worked because no one challenged an unfamiliar face and holding a door creates a reciprocity reflex. But the help desk **stopped him cold** — the employee asked why he needed access and said *even they* didn't have it. He spent ~30 minutes trying to get challenged into more access and never did.
**Lesson:** A polite "no, and I can't help with that" from a single junior employee defeated a sophisticated multi-step intrusion. Seven months later the same firm returned and the *guard refused elevator access*, citing the prior fake-badge incident and a new policy requiring point-of-contact sign-off for after-hours access. **Training + a clear escalation policy is what converted this weakness into a strength.** (Confidence: high — primary source.)

### 2. "Can I see that badge?" — the proximity clone — *(We Hack People)*
**What the tester did:** Struck up friendly lobby small talk with a guard about the badge system, then asked to see the guard's badge "to compare the model for another location." Holding it in both hands over a concealed cloner, he captured the credential in seconds while pretending to examine the back. The clone later opened restricted elevators and floors.
**Why it worked:** Rapport plus a plausible business reason; the guard was distracted on his phone and had no training that *handing over a badge* is itself a compromise.
**Lesson:** Staff — *especially guards* — must NEVER hand a badge, key, or fob to any "employee" or "contractor," however legitimate they look. And note the signature: **the tester had to physically take the badge into his hands.** Any request to *see, hold, or compare* a badge, or anyone leaning unusually close to a badge-wearer, is the human tell of a clone attempt. (Confidence: high — primary source, corroborated by the proximity facts in Vignette 9.)

### 3. The hospital "I'm from IT" walk-in — *(Raxis)*
**What the tester did:** Wore ordinary clothes (in one case "a cheap pair of scrubs" with a blank lanyard card), told a hospital receptionist he was "from IT to fix a computer." In a variant, he said automatic security updates were failing and he needed to manually install them from a USB drive. The receptionist let him into the locked area "without another word." He roamed multiple floors with access to computers, patient files, and medical records, unquestioned.
**Why it worked:** The "IT/help" pretext exploits the instinct to be helpful and the assumption that anyone past the front desk has been vetted. Scrubs/uniform = instant belonging.
**Lesson:** *Help-vs-policy* is a core failure mode — staff default to helping over verifying. Reception must verify IT/vendor visits against a **pre-arranged, named appointment**, not a story. "I'm from IT" with a USB stick should trigger escalation, not a door opening. (Confidence: high — multiple Raxis stories corroborate.)

### 4. The big box and the phone call — *(Triaxiom, electrical co-op)*
**What the tester did:** Recon'd during lunch, then loitered outside carrying a large box while faking a phone call, and asked a departing employee to hold the door. "Perfect, I am in."
**Why it worked:** Hands-full + on-the-phone is a near-universal tailgating prop; people hold doors for someone who looks burdened and occupied.
**Lesson:** Train employees that **holding a door for anyone — however legitimate or burdened they appear — is the breach.** Each person should badge in individually. A box and a phone are not credentials. (Confidence: high; this "box + phone + held door" pattern recurs across Triaxiom, Raxis, and CyberCrowd.)

### 5. The substation under the fence — *(Triaxiom, electrical substation)*
**What the tester did:** Inspected the perimeter, noted cameras were present but **unmonitored**, found the fence sat on gravel with erosion at the base, scraped away washed-out gravel, crawled under, found the control shed unlocked, and reached unprotected SCADA gear and the security DVR.
**Why it worked:** Cameras that no one watches are theater. The fence wasn't anchored below grade; the critical building wasn't locked.
**Lesson:** Perimeter barriers must be anchored below ground; critical-infrastructure buildings must be locked; **camera feeds must be actively monitored or they deter nothing**; and the DVR/NVR itself must be secured (an intruder who reaches it can erase the evidence). (Confidence: high — primary source.)

### 6. The two-tester split: one caught, one walks out clean — *(CyberCrowd / RedTeam-style)*
**What the tester did:** OSINT from Google Maps, LinkedIn, and social media to learn layout and routines. Tester A ran a *vishing* call to pre-arrange an expected (fabricated) visit, then arrived to a receptionist who was already expecting "someone." Tester B simply tailgated an employee who held the door with a friendly "good morning." Inside, an IT staffer *typed his own password into the tester's laptop*, assuming he was a new contractor. Day two, they planted keyloggers, drop boxes, and Ethernet implants.
**Why it worked / how one got caught:** Tester A was eventually caught — he **lacked sign-in credentials** and the sign-in check exposed him. Tester B, who never hit a verification checkpoint, roamed undetected, scanned the (unsegmented) network, then dismantled his kit and walked out.
**Lesson:** A *sign-in/visitor-verification checkpoint is what caught the one tester* — proof that the control works when enforced. The catastrophic detail is the IT staffer entering a password for a stranger: a clean process failure. And **flat networks turn one unlocked jack into total compromise** — segment, and the blast radius shrinks. (Confidence: high; tailgating + "good morning" + flat-network escalation corroborated across Raxis and Triaxiom.)

### 7. The assistant who stood her ground — *(Raxis)*
**What the tester did:** Got deep into an executive area and tried to snap a covert photo of a sensitive paper.
**Why it stopped:** A senior manager's assistant immediately said she was **calling security**, stood her ground, and demanded credentials before letting anything proceed. The intrusion ended there.
**Lesson:** This is the model defender — alert, unintimidated by apparent authority/seniority, willing to challenge and escalate. **One empowered, suspicious employee is worth more than a wall of cameras.** Make challenging explicitly safe and expected; never punish a staffer for politely challenging a real executive or real vendor. (Confidence: high — primary source.)

### 8. The blend-in: scrubs, off-hours, and the cleaning crew — *(Raxis)*
**What the tester did:** Used the "lost my badge, could you let me in?" line on a coworker; in another, simply waited inside an office into the evening when "the building was deserted except for the cleaning crew," exploiting the assumption that anyone still inside must be authorized.
**Why it worked:** Uniform/role camouflage plus the false premise that *secured access = everyone present is vetted*. Cleaning/vendor crews often prop doors.
**Lesson:** Late-hour presence and "lost my badge" should both trigger verification, not sympathy. Brief janitorial/vendor crews specifically on not propping doors and not letting people in. **Belonging is assumed, not verified — that assumption is the vulnerability.** (Confidence: high.)

### 9. The badge cloner that wasn't long-range — *(TrustedSec, plus HID/Black Hills proximity data)*
**What the tester did:** Built a covert long-range RFID cloner hoping to harvest badges from a couple of feet away — and found that even a powered MaxiProx-class reader still needed the card in **extremely close proximity** to the antenna in practice.
**Why it matters defensively:** This is the load-bearing reality for your threat model. Common 125 kHz HID prox cards read at roughly **4 inches (10 cm)** at a door reader; concealed handheld cloners ($10–30 on Amazon/eBay) need near-contact. Long-range readers (MaxiProx 5375, ~1–2 m) exist but are bulky, power-hungry, and unreliable to conceal. So in practice an attacker must get to **~4–7 inches of the badge** — meaning either tailgating tight, brushing past in an elevator/queue, or socially engineering the badge into their hands ("can I see that?").
**Lesson:** Because cloning needs that close approach, it carries a **detectable human signature**: someone crowding a badge-wearer, lingering close in a lift, or asking to handle a badge. Defenses: shielded badge sleeves/holders, move to higher-security encrypted credentials (e.g., iCLASS SE / SEOS rather than legacy 125 kHz prox), don't display badges externally in public, and pair badges with PIN or biometric (multi-factor) so a clone alone is useless. (Confidence: high — TrustedSec primary + corroborating HID/vendor range data.)

### 10. The Iowa courthouse arrests — when authorization is the failure — *(Coalfire / TrustedSec coverage)*
**What the testers did:** Two Coalfire consultants ran an *authorized* physical pentest of the Dallas County, Iowa courthouse for the Iowa State Judicial Branch, and deliberately tripped the alarm to measure law-enforcement response time.
**How it went wrong:** They were arrested and charged with felonies. The county argued the *state branch had no authority to authorize a test of county property*. Charges were later reduced and ultimately dropped, but the consultants were detained and legally exposed.
**Lesson (operational, for the engagement itself):** Scope and authorization must be airtight before anyone touches a door. Verify that the party signing off **actually owns the authority** over that facility (state vs. county vs. landlord vs. tenant), carry a signed **get-out-of-jail / authorization letter**, and **pre-brief local law enforcement and your own guard force** so a real response doesn't escalate into arrests. From the building owner's side: know exactly who on your team will be in the loop, and ensure your guards/police liaison can confirm an authorized test is underway without blowing it. (Confidence: high — widely documented incident.)

### 11. The "unmatched" building that fell to wetware — *(Black Hills InfoSec, Sally Vandeven)* — **READ THIS ONE; it is your building**
**What the tester did:** This is the single most on-profile case for you. The target had **RFID on all exterior and many interior doors, "No Tailgating" signs at every door, a guard/receptionist watching a bank of camera monitors at the one open front door, a "Visitors Must Sign In" sheet, badge-controlled elevators, and badge-locked stairwells and cube farms** — what the author calls a building that "to some sounds like bulletproof security." Recon was done from an **outdoor employee picnic table**, close enough to photograph badges and recreate convincing *lookalike* (non-RFID) badges purely to blend in. Entry was by **tailgating the morning crowd**: lookalike badge on a lanyard, arms full of books/papers and coffee, phone to the ear, smiling eye contact, approach timed from the parking lot — "the door was graciously held open." Inside, they opened a quiet **unalarmed back door** to admit the second tester, "hitchhiked" the badge-controlled **elevator** by riding with a legitimate employee (the elevator can't tell that no floor LED was lit for the rider), and when they couldn't find the unmarked data center, they **asked a back-office receptionist** — "we're supposed to meet someone at the data center but can't find it" — and she walked them right to it. They were only stopped when, pushing "right to the edge," repeated attempts to get someone to open the data-center door finally made staff **call security**.
**Why it worked:** Every *technical* control held — and was bypassed by people. The front guard was trained to be suspicious; the *interior* receptionist was trained to be **helpful**, so the testers simply moved past the suspicious human to the helpful one. The "make anyone who doesn't hold the door feel rude" setup beat the no-tailgating signs. No turnstile meant the door couldn't enforce one-body-one-badge; the elevator couldn't count riders.
**Lessons (several, all directly applicable):**
- **A pile of strong technical controls does not add up to security if the human layer is untrained.** This building had *more* controls than most and still fell in minutes.
- **Your most dangerous door is the helpful person behind the suspicious one.** Train *interior* staff (back-office receptionists, assistants, anyone past the lobby) to verify too — attackers route around the hardened front line to the soft inside.
- **Badge-controlled elevators don't stop hitchhiking** — riders without a lit floor request are the tell; this is impossible to catch without awareness or destination-dispatch that ties each floor call to a credential.
- **Secondary/unalarmed doors are an internal-accomplice tool**, not just an entry point — alarm them.
- **"No Tailgating" signs are not a control.** Turnstiles/mantraps enforce one-body-one-badge; signs delegate enforcement to the exact social reflex the attacker is exploiting.
- The author's own recap names the gaps: *no turnstiles, a single guard who can't simultaneously watch the door + check badges + manage sign-in + watch monitors, and elevators that can't count bodies.* (Confidence: high — primary source, fetched in full.)

---

## What Got Testers Caught (the controls that actually worked)

- **A human who challenged them.** The assistant who said "I'm calling security" (V7); the help-desk employee who refused access and said "even I don't have that" (V1); the guard who refused after-hours entry without point-of-contact sign-off (V1, return visit).
- **A sign-in / visitor-verification checkpoint, enforced.** It exposed the tester who lacked credentials in the two-tester engagement (V6).
- **Locked screens & encrypted credentials.** Where workstations auto-lock and creds aren't reusable/plaintext, a planted device or a roamed desk yields far less. (Recurring theme; the V6 IT-password failure is the counterexample.)
- **Network segmentation.** Caught nothing directly, but it's what *limits* a tester who's already inside — the flat networks in V5/V6 are why one jack became total compromise.
- **Verified vendor/IT appointments.** A receptionist checking "I'm from IT" against a named, pre-arranged appointment (rather than a story) stops the single most effective pretext (V3).
- **Active camera monitoring + secured DVR.** Unmonitored cameras stopped no one (V5); the value is in someone watching and in the footage surviving.

---

## Recurring Defender Mistakes (the patterns testers count on)

1. **Holding the door / tailgating tolerance.** The #1 entry vector. Box + phone call, "good morning," "lost my badge" — all exploit the reciprocity reflex. (V1, V4, V6, V8)
2. **Tailgating at smoking doors and back/side exits.** Propped or briefly-open secondary doors and smoking areas bypass the guarded front entrance entirely. (Recurring across Triaxiom/Raxis.)
3. **Unchallenged hi-vis vest, scrubs, uniform, or clipboard.** Visible "role costume" = assumed belonging; nobody questions someone who looks like they work there. (V3, V8)
4. **Help-vs-policy.** Staff default to being helpful (especially to "IT") over verifying. (V1 help desk was the exception that *worked*; V3 reception was the rule that failed.)
5. **Badges worn visibly in public.** Lets a tester photograph the design to forge a lookalike (V1) and aids the "can I see that?" clone setup (V2). Don't display badges outside the building.
6. **Reception/help-desk social engineering with no appointment verification.** "I'm from IT," "I'm new on the security team," "I have a delivery" — accepted on the strength of a story. (V1, V3)
7. **Open / live network jacks in lobbies, conference rooms, and empty desks.** Plug-and-pivot, especially on a flat network. (V6; Triaxiom's "notify IT of unused ports.")
8. **Unmonitored cameras and exposed DVR/NVR.** Deterrence theater; the intruder can even wipe the recorder (V5).
9. **Assuming badge readers prevent tailgating.** A reader verifies a credential; it cannot confirm only one person walked through. Turnstiles address tailgating but not piggybacking, and neither helps without staff awareness. (DEF CON Physical Security Village.)
10. **Authorization/scope ambiguity (engagement-side).** Wrong authority signs off, no get-out-of-jail letter, no law-enforcement pre-brief → arrests. (V10)
11. **The "everyone inside is vetted" assumption.** Off-hours presence, cleaning crews, and "I'm already inside" all ride on this false premise. (V8)

---

## Sources (with confidence)

- **Rapid7 — "This One Time on a Pen Test, Part 5: From Physical Security Weakness to Strength"** — https://www.rapid7.com/blog/post/2018/10/02/this-one-time-on-a-pen-test-part-5-from-physical-security-weakness-to-strength/ — *High.* Primary source for V1 (fake badge, held door, help desk refusal, 7-months-later guard refusal).
- **We Hack People — "War Story: 'Can I see that?'"** — https://wehackpeople.wordpress.com/2022/08/18/war-story-can-i-see-that/ — *High.* Primary source for V2 (proximity badge clone via guard).
- **Triaxiom Security — "Physical Penetration Test War Stories"** — https://www.triaxiomsecurity.com/physical-penetration-test-war-stories/ — *High.* Primary source for V4 (box + phone, electrical co-op) and V5 (under-the-fence substation).
- **Triaxiom Security — "Physical Penetration Test Examples: Tailgating"** — https://www.triaxiomsecurity.com/blog/physical-penetration-test-examples/ — *High.* Corroborates tailgating tactics and "badge worn visibly / challenge unfamiliar people" lessons.
- **Raxis — "Tailgating & Other Physical SE (Social Engineering Part 3)"** — https://raxis.com/blog/se-part-3-physical/ — *High.* Primary source for V3 (hospital "I'm from IT" / USB), V7 (assistant who called security), V8 (scrubs, "lost my badge," off-hours/cleaning crew).
- **Raxis — "PSE & Red Team Series: Physical Entry Bypass"** — https://raxis.com/blog/pse-red-team-series-physical-entry-bypass/ — *Medium.* Confirms PSE methodology and latch-bypass tradecraft (limited war-story detail retrieved).
- **CyberCrowd — "Inside the Action: A Red Team Physical Penetration Test in Action"** — https://www.cybercrowd.co.uk/news/inside-the-action-a-red-team-physical-penetration-test-in-action/ — *High.* Primary source for V6 (two-tester split, sign-in catch, IT staffer types password, flat-network escalation).
- **TrustedSec — "Let's Clone a Cloner… To Meet My Needs"** — https://trustedsec.com/blog/lets-clone-a-cloner-to-meet-my-needs — *High.* Primary source for V9 (long-range cloning is aspirational; close proximity still required).
- **TrustedSec — "A Message of Support: Coalfire Consultants Charged"** — https://trustedsec.com/blog/a-message-of-support-coalfire-consultants-charged — *High.* Primary source for V10 (Iowa courthouse arrests, authorization/scope failure).
- **HID 125 kHz / prox cloning range data** (AtlasRFIDStore, Kisi, SecurityInfoWatch, Dangerous Things) — e.g. https://www.getkisi.com/blog/copy-clone-prox-hid-id-card and https://www.atlasrfidstore.com/hid-proxcard-ii-lf-125-khz/ — *High.* Corroborate the ~4-inch (10 cm) reader range, cheap handheld cloners, and shielded-sleeve / higher-security-credential defenses underpinning V9.
- **DEF CON Physical Security Village (formerly Lock Bypass Village)** — https://physsec.org/ and https://forum.defcon.org/node/227890 — *Medium.* Source for "badge readers don't stop tailgating," piggybacking-vs-tailgating distinction, and unprotected-latch/egress-bypass and alarm/camera-defeat lessons.
- **Bishop Fox — "Breaking & Entering" pocket guide** — https://bishopfox.com/resources/breaking-and-entering-guide (PDF: assets.bishopfox.com/.../Bishop-Fox-Breaking-and-Entering.pdf) — *Fetched in full (real-UA download).* Turned out to be a **network/red-team command pocket-reference** (SOCKS proxies, DNS, git, recon/ISR phases, incident response) — a CTF/remote-admin cheat sheet, **not** a physical-entry case-study collection. Not load-bearing for any physical vignette; noted here so the record is accurate.
- **Black Hills Information Security — "Let's Get Physical, Part 1: Defeating Wetware Access Controls"** (Sally Vandeven, 2016) — https://www.blackhillsinfosec.com/lets-get-physical-part-1-defeating-wetware-access-controls/ — *High. Fetched in full via real-browser User-Agent (originally 403 bot-blocked).* Primary source for **Vignette 11** — the on-profile "mature building defeated by wetware" story.

> **Verification note:** Every vignette is drawn from a source I fetched directly. The two sources originally blocked were recovered with a real-browser User-Agent: the **Black Hills "wetware" piece is now a primary source (Vignette 11)**, and the **Bishop Fox PDF was retrieved but proved to be a network-pentest pocket reference, not physical case studies** (corrected above). Every recurring theme (tailgating/held doors, hi-vis/IT pretext, help-vs-policy, badges worn visibly, open jacks, unmonitored cameras, badge-clone proximity) is corroborated across **2 or more** independent sources.
