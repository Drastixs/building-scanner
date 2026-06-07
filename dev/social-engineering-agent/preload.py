"""
OSINT seed data for Arbor Bankside demo.
Edit this file to target a different building/company.
"""

OSINT_ENTITIES: dict = {
    "dave_anderson": {
        "name": "Dave Anderson",
        "role": "site_manager",
        "employer": "Arbor Bankside",
        "location": "Floor 12, Arbor Bankside",
        "known_facts": [],
    },
    "sarah": {
        "name": "Sarah",
        "role": "front_desk",
        "employer": "Arbor Bankside",
        "location": "Ground floor reception",
        "known_facts": [],
    },
    "arbor_bankside": {
        "name": "Arbor Bankside",
        "role": "building",
        "address": "Bankside Yards, SE1",
        "floors": 19,
        "known_facts": [],
    },
}

# Role aliases used as hints to the LLM extractor
# (Claude resolves via context, but these help in the system prompt)
ROLE_ALIASES: dict = {
    "site_manager": [
        "manager",
        "site manager",
        "building manager",
        "facilities manager",
    ],
    "front_desk": ["receptionist", "front desk", "reception", "front of house"],
}
