"""
Cross-building recall — the transfer engine.

embed(profile) -> brute-force cosine over the lesson pool (<10 lessons; a numpy
array beats any vector DB) -> top-k above SIM_FLOOR. For each hit, `why` is the
SET INTERSECTION of the query profile's cues with the matched lesson's cues, so
the transfer is explained, not a black box.

Empty/low recall -> []  (caller says "no strong analog; proceeding cold").
"""

from typing import List

import numpy as np

from . import llm, lesson_store

# Similarity floor for a lesson to count as a transferable analog.
# Tuned at rehearsal; seeded buildings are chosen to clear it for the demo pair.
SIM_FLOOR = 0.75


def profile_embedding_text(profile: dict) -> str:
    """The exact text we embed for a building profile."""
    return (
        profile["building_type"]
        + " "
        + ", ".join(profile.get("cues", []))
        + " "
        + profile.get("osint_summary", "")
    )


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1.0
    return float(np.dot(a, b) / denom)


def recall(
    profile: dict, path: str = None, top_k: int = 3, floor: float = SIM_FLOOR
) -> List[dict]:
    """
    Return up to top_k lessons whose profile embedding is within `floor` cosine of
    this profile, each annotated with `similarity` and `why` (shared cue tags),
    sorted most-similar first. Returns [] on cold start or all-below-floor.
    """
    lessons = lesson_store.load_lessons(path) if path else lesson_store.load_lessons()
    if not lessons:
        return []

    q = np.array(llm.embed(profile_embedding_text(profile)), dtype=float)
    q_cues = set(profile.get("cues", []))

    scored = []
    for lesson in lessons:
        emb = lesson.get("profile_embedding")
        if not emb:
            continue
        sim = _cosine(q, np.array(emb, dtype=float))
        if sim < floor:
            continue
        why = sorted(q_cues & set(lesson.get("cues", [])))
        scored.append({**lesson, "similarity": sim, "why": why})

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]
