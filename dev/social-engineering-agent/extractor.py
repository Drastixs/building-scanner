"""
Fact extraction: sentence → resolved entity + fact via Claude.
Entity dict is injected into the system prompt so Claude handles
pronouns, informal refs, and role aliases without a separate resolver.
"""

import json
import logging
import re
from typing import Optional

import anthropic
from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.7

SYSTEM_TEMPLATE = """You are a security audit fact extractor.

Known entities (JSON):
{entity_dict}

Role aliases:
{role_aliases}

Extract ONE security-relevant fact from the given sentence.
Respond with JSON only — no other text, no markdown fences.

Schema:
{{
  "resolved_entity_id": "<key from known entities, or null>",
  "fact": "<concise one-line actionable fact>",
  "confidence": <float 0.0-1.0>
}}

Rules:
- Resolve pronouns (he/she/they) and informal refs (the manager, the boss) to entity keys
- If the sentence is noise or contains no security-relevant fact, return confidence < 0.3
- If no entity matches, set resolved_entity_id to null
- Facts must be concrete: schedules, absences, access patterns, staffing gaps"""


class ExtractionResult(BaseModel):
    resolved_entity_id: Optional[str] = None
    fact: str
    confidence: float

    @field_validator("confidence")
    @classmethod
    def clamp(cls, v: float) -> float:
        return max(0.0, min(1.0, v))


def extract_fact(
    sentence: str,
    entity_dict: dict,
    role_aliases: dict,
    client: anthropic.Anthropic,
) -> Optional[ExtractionResult]:
    """
    Call Claude to extract a fact from one sentence.
    Returns None if confidence < CONFIDENCE_THRESHOLD or parsing fails.
    """
    system = SYSTEM_TEMPLATE.format(
        entity_dict=json.dumps(entity_dict, indent=2),
        role_aliases=json.dumps(role_aliases, indent=2),
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=256,
            system=system,
            messages=[{"role": "user", "content": sentence}],
        )
        raw = response.content[0].text.strip()

        # Strip markdown fences if model adds them
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        data = json.loads(raw)
        result = ExtractionResult(**data)
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.warning("Parse error for sentence %r: %s", sentence, e)
        return None

    if result.confidence < CONFIDENCE_THRESHOLD:
        logger.info(
            "Skipped (confidence %.2f < %.2f): %r",
            result.confidence,
            CONFIDENCE_THRESHOLD,
            sentence,
        )
        return None

    # Guard: resolved entity must exist in dict
    if result.resolved_entity_id and result.resolved_entity_id not in entity_dict:
        logger.warning(
            "Unknown entity_id %r returned by Claude — clearing",
            result.resolved_entity_id,
        )
        result.resolved_entity_id = None

    return result


def apply_fact(result: ExtractionResult, entity_dict: dict) -> None:
    """Write an extracted fact back into the in-memory entity dict."""
    if result.resolved_entity_id and result.resolved_entity_id in entity_dict:
        entity_dict[result.resolved_entity_id].setdefault("known_facts", []).append(
            result.fact
        )
