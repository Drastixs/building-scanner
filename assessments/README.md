# Building Access Assessment System

End-to-end system for authorized building security assessments: pre-visit script selection, post-visit feedback collection, and continuous script improvement.

---

## Workflow

### 1. Before You Go

**Choose your script** from `access-scripts.md`:
- Match the building type (office, venue, hospital, etc.)
- Match the time of day (pre-event, during business hours, etc.)
- Decide your cover story and entry point
- Read the script's opening line, objection handlers, and success rate

**Make a note:**
- Which script you're using
- Date and time
- Building name and address
- Entry point you'll attempt

This prevents you from forgetting details while in the building.

---

### 2. During the Visit

- Follow the script you chose
- Observe security barriers, guard behavior, busiest/quietest times
- Note any floor-plan details, access points, or vulnerabilities
- **Do not take risks** — if challenged and uncomfortable, stop

---

### 3. After You Leave

**Fill out `feedback-template.md`:**
1. Save a copy and name it: `assessments/results/[BUILDING-SLUG]_[DATE].md`
2. Complete all sections honestly and in detail
3. Be specific about what phrases worked, what barriers you hit, recommendations

**Key sections:**
- **What Worked:** exact words/actions that got you in or further
- **Barriers:** where you got stuck and why
- **Recommendations:** how to improve the script for next time
- **Building Intel:** security setup, access controls, floor plan notes

**Submit immediately after the visit** — memory fades fast.

---

### 4. Script Improvement (Automated)

Run the script iterator to analyze all feedback and rank scripts:

```bash
python assessments/script-iterator.py
```

This generates:
- `assessments/script-effectiveness-report.md` — success rates, what works, improvements
- Console output of improvement suggestions

**Update `access-scripts.md`:**
1. Adjust success rates based on real data
2. Highlight key phrases that consistently worked
3. Add new scripts or variations based on recommendations
4. Remove or archive scripts with consistently low success

---

## File Structure

```
assessments/
├── README.md                          (this file)
├── access-scripts.md                  (script templates, ranked by success)
├── feedback-template.md               (fill out after each visit)
├── script-iterator.py                 (auto-analyze feedback, suggest improvements)
├── script-effectiveness-report.md     (generated: ranked scripts, patterns)
└── results/
    ├── emirates-stadium_2026-06-06.md
    ├── barbican-hall_2026-06-15.md
    └── ... (one file per assessment)
```

---

## Process Flow

```
[Choose Script]
      ↓
[Visit Building]
      ↓
[Fill Feedback Form]
      ↓
[script-iterator.py reads all feedback]
      ↓
[Generate Effectiveness Report]
      ↓
[Update access-scripts.md with learned patterns]
      ↓
[Next visit uses better scripts]
```

---

## Key Principles

### Feedback Quality

- **Specific, not vague.** Instead of "it worked," write the exact phrase that worked
- **Honest, not flattering.** If a script failed, say so and explain why
- **Timely.** Fill out feedback while memories are fresh (within 1 hour of leaving)
- **Complete.** All sections matter; empty sections = lost learning

### Script Development

- Scripts improve iteratively — early success rates may be low; that's normal
- New variations of struggling scripts are added based on feedback
- High-success scripts get refined and locked in
- Scripts are building-type-specific; patterns transfer (e.g., "Event Attendee" works at all venues)

### Security Discipline

- Never take unnecessary risks; de-escalate if challenged
- Document incidents honestly (they teach more than successes)
- If a building's security is too tight, mark it and move on
- Always have a genuine reason to be present (the "cover" must be real enough to hold under questioning)

---

## Example Workflow

**Visit 1:** Use "Event Attendee" script at a theater.
- ✅ Success — got into main lobby
- Key phrase: "I think I'm running a bit late, is the box office this way?"
- Filled out feedback, noted that uncertainty + polite asking = most effective

**Visit 2:** Use "Event Attendee" script at a different theater.
- ⚠️ Partial — got to elevator, stopped by security
- Script needed refinement: "I have my ticket, just looking for the restroom"
- Feedback: suggest adding a "lost" element (less confrontational than "here for event")

**After 5+ visits:** Run `script-iterator.py`
- Report shows "Event Attendee" at 78% success
- Most effective phrases: uncertainty, politeness, specific location asks
- Barriers: strict ID checks, security desks
- New variation added: "Event Attendee (Lost)" for venues with tighter security

**Update scripts**
- "Event Attendee" bumped to 85% success with refined language
- New variant added for high-security venues
- Scripts now reflect real-world patterns

---

## Running the Iterator

```bash
# Generate effectiveness report and suggestions
python assessments/script-iterator.py

# View the report
cat assessments/script-effectiveness-report.md

# Update scripts based on report
# (manual step — edit access-scripts.md with insights)
```

---

## Tips for Success

1. **Build a library of scripts, not one perfect script.** Different buildings, times, and circumstances need different approaches.

2. **Test one variable at a time.** If you change the script *and* the entry point *and* the time of day, you can't tell which mattered.

3. **Track what you're measuring.** Success is different for different buildings:
   - Office: getting to a restricted floor
   - Venue: getting past the main entrance
   - Hospital: accessing non-public areas
   - Define it clearly in feedback

4. **Learn from failures more than successes.** A failed attempt teaches you exactly what *doesn't* work. Successes can be lucky.

5. **Respect consent and authorization.** These assessments are only valid when you have explicit written permission from the building owner/manager. Document the engagement (date, scope, authorization).

---

## Next Steps

1. **Copy `feedback-template.md`** for your first visit
2. **Choose a script** from `access-scripts.md` 
3. **Visit a building** (you have 30+ events scheduled)
4. **Fill out feedback**
5. **After 5+ visits, run the iterator** to see patterns emerge
6. **Update scripts** based on what you learned

---

**Questions?** Refer back to the assessment system design in this README, or check the feedback template for guidance on each field.
