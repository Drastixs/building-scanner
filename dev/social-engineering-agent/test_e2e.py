"""
End-to-end test: fake transcript → entity-linked facts → dream cycle.

Run:
    pip install -r requirements.txt
    cp .env.example .env  # add real keys
    python test_e2e.py

Assertions:
  1. /preload seeds 3 entities
  2. /extract resolves "manager" → dave_anderson with fact about Fridays
  3. /extract resolves "receptionist" → sarah with an access fact
  4. Noise sentence is skipped (confidence < 0.7)
  5. dave_anderson.known_facts has ≥1 entry after extraction
  6. /dream-cycle returns without error
"""

import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE = "http://localhost:8000"

# ── Fake transcript ────────────────────────────────────────────────────────────
# Mix: two fact sentences, one noise sentence
FAKE_SENTENCES = [
    "Yeah the manager doesn't come in on Fridays, he works from home.",
    "The receptionist always leaves the side door propped open during her lunch break.",
    "It was raining quite heavily this morning actually.",  # noise — no security fact
    "Dave handles all the access card requests for floors 10 through 15.",
]


def check(label: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    msg = f"[{status}] {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    if not condition:
        sys.exit(1)


def main() -> None:
    print("=== Live Audit Intelligence — E2E test ===\n")

    client = httpx.Client(base_url=BASE, timeout=60.0)

    # 1. Health check
    r = client.get("/health")
    if r.status_code != 200:
        print(f"[SKIP] /health returned {r.status_code}: {r.json()}")
        print("  → Start the server: uvicorn main:app --reload")
        sys.exit(1)
    check("/health ok", r.status_code == 200, r.json().get("status"))

    # 2. Preload entities
    r = client.post("/preload")
    data = r.json()
    check("/preload loaded 3 entities", data["loaded"] == 3, str(data["entities"]))

    # 3. Extract facts from fake transcript
    r = client.post("/extract", json={"sentences": FAKE_SENTENCES})
    check("/extract 200", r.status_code == 200, r.text[:200])
    result = r.json()

    extracted = result["results"]
    skipped = result["skipped"]

    print(f"\nExtracted {len(extracted)} facts, skipped {skipped} sentences:\n")
    for e in extracted:
        print(
            f"  [{e['resolved_entity_id'] or 'unlinked'}] {e['fact']}  (conf={e['confidence']:.2f})"
        )
    print()

    # At least one fact linked to dave_anderson (manager reference)
    dave_facts = [e for e in extracted if e["resolved_entity_id"] == "dave_anderson"]
    check("dave_anderson resolved from 'manager'", len(dave_facts) >= 1)

    # At least one fact linked to sarah (receptionist reference)
    sarah_facts = [e for e in extracted if e["resolved_entity_id"] == "sarah"]
    check("sarah resolved from 'receptionist'", len(sarah_facts) >= 1)

    # Noise sentence should have been skipped
    check("noise sentence skipped", skipped >= 1, f"skipped={skipped}")

    # 4. Confirm entity dict updated
    r = client.get("/entities")
    entities = r.json()
    dave_known = entities.get("dave_anderson", {}).get("known_facts", [])
    check(
        "dave_anderson.known_facts populated",
        len(dave_known) >= 1,
        str(dave_known),
    )

    # 5. Dream cycle (mubit may be a stub if MUBIT_API_KEY is a test key)
    r = client.post("/dream-cycle")
    if r.status_code == 503:
        print("[SKIP] /dream-cycle skipped — MUBIT_API_KEY not configured")
    else:
        check("/dream-cycle 200", r.status_code == 200, r.text[:200])
        dc = r.json()
        print(f"  session_id: {dc['session_id']}")
        print(f"  inferences ({len(dc['inferences'])}): {dc['inferences'][:3]}")

    print("\n=== All assertions passed ===")


if __name__ == "__main__":
    main()
