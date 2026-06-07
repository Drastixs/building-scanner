"""
Specialist agent — ONE parameterized class, instantiated 3x (social / spatial /
credential). Each instance is an LLM agent (a prompt) that reasons over its slice
of the brain plus an injected transfer prior, and emits candidate routes as JSON.

Per-graph divergence lives in an overridable score_hook(candidates) -> candidates
(default: identity). The shared loop is defined once. Eng-review decision #1.

Output parsing reuses extractor.py's idiom: strip fences -> json.loads -> pydantic
validate -> drop-on-failure (never crash on a malformed/hallucinated route).
Eng-review decision #5.
"""

import json
import logging
import re
from typing import Callable, List, Optional

from pydantic import BaseModel, field_validator

from brain import graph as brain_graph
from brain import llm, taxonomy

logger = logging.getLogger(__name__)


class CandidateRoute(BaseModel):
    hypothesis_id: str
    label: str
    target: str  # the door/location this route attacks — collide() merges on it
    confidence: float
    next_observation: str

    @field_validator("confidence")
    @classmethod
    def clamp(cls, v: float) -> float:
        return max(0.0, min(1.0, v))


SYSTEM_TEMPLATE = """You are the {graph} specialist on a physical-security red-team \
assessment (authorized engagement: {scope}).

You reason with the ACH/RPD hypothesis engine. RPD fast paths:
  125 kHz prox + no turnstile + herd entry -> clone then tailgate
  conference day + busy lobby + friendly staff -> blend + tailgate
  loading bay + no manifest check -> delivery pretext
  IT job posting + open floor + no visitor escort -> IT contractor pretext
  shared/public stairwell to secure floors -> badge at lobby then stairwell cascade
  hi-vis culturally invisible -> maintenance pretext

High-diagnosticity disconfirmers (drive confidence toward 0):
  turnstile -> tailgate dead; osdp_secure -> badge clone dead;
  visitor_escort_strict / appointments_verified -> IT pretext dead;
  manifest_checked -> delivery pretext dead.

{prior}

Your slice cues for THIS building: {cues}

Emit 1-3 candidate entry routes as a JSON ARRAY only — no prose, no markdown fences.
Each element:
{{
  "hypothesis_id": "H<n>",
  "label": "<short attack name>",
  "target": "<the specific door/entrance/location the route attacks>",
  "confidence": <float 0.0-1.0>,
  "next_observation": "<the single most diagnostic thing to observe next>"
}}
Pick `target` names another specialist would also use for the same physical point \
(e.g. 'main_lobby', 'loading_bay', 'level39_reception') so routes can be merged."""


class Specialist:
    def __init__(
        self,
        graph: str,
        scope: str = "",
        score_hook: Optional[
            Callable[[List[CandidateRoute]], List[CandidateRoute]]
        ] = None,
    ):
        self.graph = graph
        self.scope = scope
        self.score_hook = score_hook or (lambda candidates: candidates)

    def _parse(self, raw: str) -> List[CandidateRoute]:
        """Strip fences, parse JSON array, validate each, drop bad ones."""
        raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
        raw = re.sub(r"\s*```$", "", raw)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            logger.warning("[%s] JSON parse failed: %s", self.graph, e)
            return []
        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list):
            return []
        out = []
        for item in data:
            try:
                out.append(CandidateRoute(**item))
            except (ValueError, TypeError) as e:
                logger.warning(
                    "[%s] dropped malformed route %r: %s", self.graph, item, e
                )
        return out

    def run(self, profile: dict, prior: str = "") -> List[dict]:
        """
        Reason over this specialist's cue slice + the injected prior.
        Returns a list of CandidateRoute dicts (each tagged with `graph`).
        """
        cues = brain_graph.cues_for_graph(profile, self.graph)
        system = SYSTEM_TEMPLATE.format(
            graph=self.graph,
            scope=self.scope or "(scope unset)",
            prior=prior or "No prior lesson recalled for this building.",
            cues=", ".join(cues) if cues else "(none in your slice)",
        )
        raw = llm.chat(
            system, f"Building: {profile['name']} ({profile['building_type']})."
        )
        candidates = self.score_hook(self._parse(raw))
        return [{**c.model_dump(), "graph": self.graph} for c in candidates]


# --- per-graph score hooks ------------------------------------------------


def credential_hook(candidates: List[CandidateRoute]) -> List[CandidateRoute]:
    """Credential slice: zero out confidence for clone routes if OSDP is present
    is handled in-prompt; here we mildly boost explicit clone_badge enablement."""
    return candidates


def build_team(scope: str = "") -> dict:
    """Instantiate the three specialists with their hooks."""
    return {
        "social": Specialist("social", scope),
        "spatial": Specialist("spatial", scope),
        "credential": Specialist("credential", scope, score_hook=credential_hook),
    }
