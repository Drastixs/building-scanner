# Building Access Scripts

Standardized talking points for authorized security assessments. Tailor the script based on building type, entry point, and time of day. Scripts are tested, iterated, and ranked by effectiveness.

---

## Script Framework

Each script has:
- **Building type** — office, venue, hospital, university, etc.
- **Entry point** — main entrance, service entrance, delivery, parking
- **Cover story** — attendee, vendor, security audit, contractor
- **Opening line** — how to initiate contact
- **Objection handlers** — responses if challenged
- **Success rate** — % effectiveness from past assessments (updated from feedback)

---

## Templates

### Template 1: "Event Attendee" (High Success)
**Building type:** Venue, theater, conference center  
**Entry point:** Main entrance  
**Success rate:** 85% (based on feedback)

**Opening:**
> "Hi, I'm here for the [EVENT NAME]. I think I'm a bit early / running a bit late — could you point me to where [AREA] is?"

**If challenged:**
- "I have my ticket here" (show phone/printed)
- "A friend said to meet them in [COMMON AREA] — do you know where that is?"
- "Is there a reception desk I should check in at?"

**Why it works:**
- Assumes legitimacy (you belong there)
- Ask for help rather than permission
- Creates social obligation to assist
- Works best 30–90 min before/after event start

---

### Template 2: "Lost Delivery/Contractor" (Medium Success)
**Building type:** Office, medical facility  
**Entry point:** Service/loading entrance  
**Success rate:** 62% (based on feedback)

**Opening:**
> "Hi, I'm here with a delivery/to fix the [SYSTEM]. I think I might be at the wrong entrance — am I in the right place?"

**If challenged:**
- "I have a work order" (generic doc, vague reference number)
- "Your building manager's office — is that up these stairs?"
- "I was told it's on Floor [X] — do you know the access code?"

**Why it works:**
- Service staff expect vendors
- Uncertainty invites help
- Less scrutiny on loading areas during business hours

**When to avoid:**
- After 6pm (building mostly empty)
- If security desk is actively checking credentials

---

### Template 3: "Tenant/Contractor Lookup" (Lower Success)
**Building type:** Office (multi-tenant)  
**Entry point:** Main lobby  
**Success rate:** 41% (based on feedback)

**Opening:**
> "Hi, I'm here to see [COMPANY NAME] in [SUITE NUMBER]. Do I need to sign in?"

**If challenged:**
- Look for wall directory, read a company name plausibly
- "I should have a visitor pass — did someone call down?"
- "Is there a visitor book I should use?"

**Why it works:**
- Directs interaction toward admin procedures (your cover)
- Implies legitimate booking

**When to avoid:**
- Large corporate buildings with strict visitor procedures
- After hours

---

### Template 4: "Facilities/Building Systems" (Specialist)
**Building type:** Any (requires more prep)  
**Entry point:** Service areas  
**Success rate:** 33% (based on feedback)

**Opening:**
> "Hi, I'm here to check the [SYSTEM: HVAC/Fire panels/Network/etc.]. Which floor is your mechanical room?"

**Requires:**
- Shirt/uniform from vendor (optional, risky)
- Knowledge of building systems
- Confident demeanor
- Building-specific intel

**Why risky:**
- Highest scrutiny
- Facilities staff may know all vendors
- Requires specific knowledge to maintain cover

---

## Usage Notes

**When selecting a script:**
1. **Building type** → narrows choice
2. **Time of day** → Event Attendee works 30–90 min around event; Contractor works 9–17:30 weekdays only
3. **Your appearance** → Event Attendee = casual/smart casual; Contractor = work-appropriate
4. **Confidence level** → Event Attendee is lowest-stakes; Facilities requires acting skill

**Documentation:**
- Record which script you used *before* entering
- Note the building, entry point, time
- Rate success/failure and collect reasons in `assessments/` after each attempt

---

## Iteration Notes

Scripts are ranked by success rate (last updated from real assessments). As you test and report back:
- New data updates the success rates
- Failing scripts get refined or marked for testing in different conditions
- New scripts can be added based on emerging patterns

See `feedback-system.md` for how to submit assessment results.
