"""
Live ingestion adapter — recon observation sentence -> taxonomy cue tag.

Reuses extractor.py's idiom (fence-strip -> json -> pydantic -> drop-on-failure)
but maps a free-text observation onto the CONTROLLED cue vocabulary in
taxonomy.py, so a live sentence like "everyone just streamed in behind the guy
with the badge, no gate" becomes the cue tag `herd_entry` (+ `no_turnstile`).

Cues not in the taxonomy are dropped (never invented), keeping the `why`
explanation honest.
"""

import json
import logging
import re
from typing import List, Optional

from pydantic import BaseModel, field_validator

from brain import llm, taxonomy

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.6

SYSTEM = """You convert one physical-security recon observation into cue TAGS from a \
fixed vocabulary. Respond with JSON only — no prose, no markdown fences.

Allowed cue tags (use ONLY these, exact spelling):
{vocab}

Schema:
{{"cues": ["<tag>", ...], "confidence": <float 0.0-1.0>}}

Rules:
- Only emit tags that the observation directly supports. Empty list if none.
- "no gate / no barrier / walked straight in" -> no_turnstile (+ herd_entry if a crowd)
- "turnstile / speedgate / mantrap" -> turnstile
- "prox reader / 125kHz / HID" -> hid_maxiprox ; "OSDP" -> osdp_secure
- "loading bay / goods in" -> loading_bay ; deliveries unchecked -> no_manifest_check
- "conference / event / lots of visitors" -> conference_day
- visitors escorted -> visitor_escort_strict ; visitors roam -> no_visitor_escort
- If the observation is noise, return {{"cues": [], "confidence": 0.0}}"""


class ReconCues(BaseModel):
    cues: List[str]
    confidence: float

    @field_validator("confidence")
    @classmethod
    def clamp(cls, v: float) -> float:
        return max(0.0, min(1.0, v))


def extract_cues(sentence: str) -> Optional[ReconCues]:
    """One observation -> validated cue tags, or None on low confidence / parse fail."""
    system = SYSTEM.format(vocab=", ".join(sorted(taxonomy.CUES)))
    raw = llm.chat(system, sentence, max_tokens=128)
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw)
    try:
        result = ReconCues(**json.loads(raw))
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        logger.warning("recon parse error for %r: %s", sentence, e)
        return None
    if result.confidence < CONFIDENCE_THRESHOLD:
        return None
    # drop any tag the model invented despite instructions
    result.cues = [c for c in result.cues if c in taxonomy.CUES]
    return result


def ingest_recon(sentences: List[str], profile: dict) -> List[str]:
    """
    Run each observation through extract_cues and merge new cues into the live
    building profile (in place). Returns the list of newly-added cue tags.
    """
    added = []
    have = set(profile.setdefault("cues", []))
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        result = extract_cues(s)
        if not result:
            continue
        for cue in result.cues:
            if cue not in have:
                profile["cues"].append(cue)
                have.add(cue)
                added.append(cue)
    return added
