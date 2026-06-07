"""
Transfer agent — runs first at every building. THIS is the on-stage magic.

Calls brain.recall(profile); for each recalled prior it renders a DETERMINISTIC
announcement line (not free LLM text), so the whoa is reproducible every rehearsal
and can never ramble or hallucinate a cue. The combined prior is then prepended to
each specialist's prompt as context — that prepend is the whole "injection".

Eng-review decision #8: the announcement line is asserted exact-string in tests.
"""

from typing import List, Tuple


def announce(lesson: dict) -> str:
    """The exact, reproducible announcement line for one recalled prior."""
    overlap = ", ".join(lesson.get("why", []))
    return f"From {lesson['name']} (shared cues: {overlap}), expect: {lesson['key_lesson']}"


COLD_LINE = "No strong analog in memory — proceeding cold."


def transfer_prior(profile: dict, brain) -> Tuple[List[str], str]:
    """
    Run recall and build the prior to inject.
    Returns (announcement_lines, prior_block_for_prompt).
    On cold start, lines == [COLD_LINE] and the prior block tells specialists so.
    """
    lessons = brain.recall(profile)
    if not lessons:
        return [COLD_LINE], "PRIOR: " + COLD_LINE

    lines = [announce(lesson) for lesson in lessons]
    prior_block = (
        "PRIOR LESSONS RECALLED (bias your reasoning before any local recon):\n"
        + "\n".join(f"- {line}" for line in lines)
    )
    return lines, prior_block
