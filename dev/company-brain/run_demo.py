"""
Company Brain demo — cross-building learning, on stage.

Flow:
  Building #1 (canned, pre-authored outcomes): run the team, then write_lesson().
  Building #2 (live): transfer agent fires FIRST and announces the recalled prior
  with the overlapping cues that justify it — BEFORE any local recon. Then live
  recon sentences add cues, the team reasons, collide() ranks the entry routes.

Usage:
  python run_demo.py                      # canned recon for building #2
  python run_demo.py --recon seeds/arbor_recon.txt
  python run_demo.py --rehearsal          # hard-assert building #2 clears SIM_FLOOR

The --rehearsal flag makes a silent no-fire of the transfer whoa impossible on
stage: if building #2 does not recall building #1 above SIM_FLOOR, it crashes
loudly at rehearsal time (eng-review decision #4).
"""

import argparse
import os
import sys

# make `brain` / `agents` importable when run from this dir
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import brain
from agents import specialist, transfer
from brain import collide
from brain.ingest import extractor_adapter
from seeds import profiles

DEFAULT_STORE = os.path.join(os.path.dirname(__file__), "lessons.run.jsonl")

CANNED_RECON = [
    "At 9am a whole cluster of people just streamed in together behind one badge holder.",
    "There's no turnstile or speedgate in the lobby, just an open walkway past the desk.",
    "Visitors I watched went up in the lifts on their own, nobody escorted them.",
]


def banner(profile):
    print("=" * 72)
    print(f"  BUILDING: {profile['name']}  [{profile['building_type']}]")
    print(f"  AUTHORIZATION SCOPE: {profile['scope'] or '(UNSET — banner only)'}")
    print("=" * 72)


def run_team(profile, scope, prior=""):
    team = specialist.build_team(scope)
    lists = [s.run(profile, prior=prior) for s in team.values()]
    return collide.collide(lists)


def print_routes(routes):
    if not routes:
        print("  (no routes returned)")
        return
    for i, r in enumerate(routes, 1):
        attacks = " + ".join(f"{a['label']}[{a['graph']}]" for a in r["attacks"])
        print(
            f"  {i}. target={r['target']}  score={r['score']}  ({r['n_graphs']} graphs)"
        )
        print(f"     attacks: {attacks}")
        print(f"     next test: {r['next_observation']}")


def read_recon_file(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                out.append(line)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--recon", help="file of live recon observation sentences for building #2"
    )
    ap.add_argument("--store", default=DEFAULT_STORE, help="lesson store path")
    ap.add_argument(
        "--rehearsal",
        action="store_true",
        help="hard-assert building #2 clears SIM_FLOOR before recon",
    )
    ap.add_argument(
        "--keep", action="store_true", help="do not reset the lesson store first"
    )
    args = ap.parse_args()

    if not args.keep and os.path.exists(args.store):
        os.remove(args.store)  # fresh store so #2 recalls exactly #1

    # ---- BUILDING #1: canned, produce the lesson -------------------------
    b1 = profiles.BUILDING_1
    banner(b1)
    brain1 = brain.init(
        b1["building_id"], b1["scope"], store_path=args.store
    ).attach_profile(b1)
    print("\n  Running specialist team (no prior — first building)...")
    routes1 = run_team(b1, b1["scope"])
    print_routes(routes1)

    lesson = brain.build_lesson(
        b1, profiles.BUILDING_1_HYPOTHESES, profiles.BUILDING_1_LESSON
    )
    brain1.write_lesson(lesson)
    print(f'\n  write_lesson() -> {b1["name"]}: "{profiles.BUILDING_1_LESSON}"')

    # ---- BUILDING #2: live, transfer fires first -------------------------
    b2 = profiles.BUILDING_2
    print("\n")
    banner(b2)
    brain2 = brain.init(
        b2["building_id"], b2["scope"], store_path=args.store
    ).attach_profile(b2)

    print("\n  >>> TRANSFER AGENT (before any local recon) <<<")
    lines, prior = transfer.transfer_prior(b2, brain2)
    for line in lines:
        print(f"     ★ {line}")

    if args.rehearsal:
        assert lines and lines[0] != transfer.COLD_LINE, (
            f"REHEARSAL FAIL: building #2 did not recall any prior above "
            f"SIM_FLOOR={brain.SIM_FLOOR}. The transfer whoa would no-fire on stage."
        )
        print(f"\n  [rehearsal] transfer cleared SIM_FLOOR={brain.SIM_FLOOR} ✓")

    # ---- live recon -> new cues ------------------------------------------
    sentences = read_recon_file(args.recon) if args.recon else CANNED_RECON
    print(f"\n  Ingesting {len(sentences)} live recon observations...")
    added = extractor_adapter.ingest_recon(sentences, b2)
    print(f"  new cues from recon: {added or '(none)'}")
    brain2.attach_profile(b2)  # rebuild graph with the new cues

    print("\n  Running specialist team WITH transferred prior + live cues...")
    routes2 = run_team(b2, b2["scope"], prior=prior)
    print("\n  RANKED ENTRY ROUTES:")
    print_routes(routes2)
    print()


if __name__ == "__main__":
    main()
