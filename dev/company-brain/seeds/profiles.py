"""
Canned seed data for the demo.

BUILDING_1 ships WITH its outcomes (pre-authored ground-truth) — its hypotheses
are not computed from a run; they are the lesson we want to transfer. After
building #1 runs, write_lesson() stores it.

BUILDING_2 (Arbor Bankside, the live building) starts with only OSINT cues; live
recon sentences add the rest. Its starting cues are chosen to clear SIM_FLOOR
against building #1 so the transfer whoa is guaranteed at rehearsal.

Edit cues here using ONLY tags from brain/taxonomy.py (validated at load).
"""

# --- building #1: canned, with pre-authored outcomes ----------------------

BUILDING_1 = {
    "building_id": "meridian-quay",
    "name": "Meridian Quay",
    "building_type": "multi-tenant-commercial",
    "scope": "ENG-2026-PTB-001 (authorized red-team, Pop The Bubble)",
    "cues": [
        "hid_maxiprox",
        "herd_entry",
        "no_turnstile",
        "conference_day",
        "open_floor",
        "no_visitor_escort",
        "it_job_posting",
    ],
    "osint_summary": (
        "19-storey multi-tenant tower, shared ground-floor lobby, single bank of "
        "speedless prox barriers, frequent tenant conferences draw unbadged guests, "
        "open-plan tenant floors, active IT-contractor job postings."
    ),
}

# Pre-authored ground-truth outcomes for building #1 (NOT computed from a run).
BUILDING_1_HYPOTHESES = [
    {
        "id": "H7",
        "label": "IT-contractor pretext to a tenant floor",
        "result": "disconfirmed",
        "notes": "Reception live-verified the appointment; pretext collapsed at desk.",
    },
    {
        "id": "H2",
        "label": "Blend + tailgate during the conference window",
        "result": "confirmed",
        "notes": "Walked in with a guest cluster at 09:05; no badge check at barrier.",
    },
]

BUILDING_1_LESSON = (
    "IT-contractor pretext gets verified at reception and fails here; "
    "tailgating during the morning conference window works."
)

# --- building #2: live building (Arbor Bankside) --------------------------

BUILDING_2 = {
    "building_id": "arbor-bankside",
    "name": "Arbor Bankside",
    "building_type": "multi-tenant-commercial",
    "scope": "ENG-2026-PTB-002 (authorized red-team, Pop The Bubble)",
    # OSINT-only at start; live recon adds herd_entry / no_turnstile / no_visitor_escort.
    "cues": [
        "hid_maxiprox",
        "conference_day",
        "open_floor",
    ],
    "osint_summary": (
        "Bankside Yards multi-tenant tower, 19 floors, shared lobby, HID prox "
        "readers, tenant conference scheduled, open-plan floors above reception."
    ),
}
