"""
Live Audit Intelligence — FastAPI backend.

Routes:
  GET  /health          Validate Mubit + OpenAI API keys
  POST /preload         Seed entity dict from OSINT data
  GET  /entities        Return current entity dict state
  POST /transcribe      WAV path → transcript via OpenAI Whisper
  POST /extract         Sentence list → extracted facts
  POST /dream-cycle     Run reflect() → inferences
  DELETE /session       Reset entity dict + start new session
"""

import copy
import json
import logging
import os
import time
from typing import Optional

import anthropic
import mubit
import mubit.learn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel

from extractor import ExtractionResult, apply_fact, extract_fact
from preload import OSINT_ENTITIES, ROLE_ALIASES

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)

# ── State ──────────────────────────────────────────────────────────────────────

entity_dict: dict = {}
session_id: str = f"audit:session:{int(time.time())}"

anthropic_client: Optional[anthropic.Anthropic] = None
mubit_client: Optional[mubit.Client] = None
openai_client: Optional[OpenAI] = None

# ── Startup ────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Live Audit Intelligence",
    description="Entity-linking brain for physical security audits.",
    version="0.1.0",
)


@app.on_event("startup")
def startup() -> None:
    global anthropic_client, mubit_client, openai_client

    mubit_api_key = os.environ.get("MUBIT_API_KEY", "")
    mubit_endpoint = os.environ.get("MUBIT_ENDPOINT", "https://api.mubit.ai")
    openai_api_key = os.environ.get("OPENAI_API_KEY", "")

    if not mubit_api_key:
        logger.warning("MUBIT_API_KEY not set — memory disabled")
    if not openai_api_key:
        logger.warning("OPENAI_API_KEY not set — transcription disabled")

    # Wrap Anthropic client so every LLM call is auto-captured by Mubit
    if mubit_api_key:
        mubit.learn.init(
            api_key=mubit_api_key,
            agent_id="audit-agent",
            auto_reflect=True,
        )
        mubit_client = mubit.Client(endpoint=mubit_endpoint)
        mubit_client.set_api_key(mubit_api_key)

    # Create AFTER mubit.learn.init so instrumentation wraps it
    anthropic_client = anthropic.Anthropic()
    openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None


# ── Request / Response models ──────────────────────────────────────────────────


class TranscribeRequest(BaseModel):
    audio_path: str


class ExtractRequest(BaseModel):
    sentences: list[str]


class ExtractResponse(BaseModel):
    results: list[dict]
    skipped: int


class DreamCycleResponse(BaseModel):
    session_id: str
    inferences: list[str]


# ── Routes ─────────────────────────────────────────────────────────────────────


@app.get("/health", summary="Validate API keys and connections")
def health() -> dict:
    """
    Checks both MUBIT_API_KEY and OPENAI_API_KEY are present.
    Does a minimal Anthropic ping to confirm the key works.
    Returns 503 if any required key is missing.
    """
    issues = []

    if not os.environ.get("MUBIT_API_KEY"):
        issues.append("MUBIT_API_KEY missing")
    if not os.environ.get("OPENAI_API_KEY"):
        issues.append("OPENAI_API_KEY missing")

    # Minimal Anthropic ping
    if anthropic_client:
        try:
            anthropic_client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1,
                messages=[{"role": "user", "content": "ping"}],
            )
        except Exception as e:
            issues.append(f"Anthropic API error: {e}")

    if issues:
        raise HTTPException(status_code=503, detail={"issues": issues})

    return {"status": "ok", "session_id": session_id}


@app.post("/preload", summary="Seed entity dict from OSINT data")
def preload() -> dict:
    """
    Loads the hardcoded OSINT entities from preload.py into the in-memory
    entity dict. Resets any facts accumulated in the current session.
    """
    global entity_dict
    entity_dict = copy.deepcopy(OSINT_ENTITIES)
    logger.info("Preloaded %d entities", len(entity_dict))
    return {"loaded": len(entity_dict), "entities": list(entity_dict.keys())}


@app.get("/entities", summary="Return current entity dict state")
def get_entities() -> dict:
    """Returns the full entity dict including any facts extracted this session."""
    return entity_dict


@app.post("/transcribe", summary="Transcribe a WAV file via OpenAI Whisper")
def transcribe(req: TranscribeRequest) -> dict:
    """
    Calls OpenAI Whisper API with the given WAV file path.
    Returns the full transcript text split into sentences.
    """
    if not openai_client:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY not configured")

    try:
        with open(req.audio_path, "rb") as f:
            result = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text",
            )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Audio file not found: {req.audio_path}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Whisper error: {e}")

    transcript = str(result).strip()
    # Split on sentence boundaries (naive but sufficient for demo)
    sentences = [
        s.strip() for s in transcript.replace(".", ".\n").splitlines() if s.strip()
    ]
    return {"transcript": transcript, "sentences": sentences}


@app.post(
    "/extract",
    summary="Extract facts from a list of sentences",
    response_model=ExtractResponse,
)
def extract(req: ExtractRequest) -> ExtractResponse:
    """
    For each sentence, calls Claude to extract a security-relevant fact and
    resolve the entity reference. Results with confidence < 0.7 are skipped.
    Extracted facts are written back into the entity dict.
    """
    if not anthropic_client:
        raise HTTPException(status_code=503, detail="Anthropic client not initialised")
    if not entity_dict:
        raise HTTPException(
            status_code=400, detail="Entity dict empty — call /preload first"
        )

    results = []
    skipped = 0

    for sentence in req.sentences:
        result: Optional[ExtractionResult] = extract_fact(
            sentence, entity_dict, ROLE_ALIASES, anthropic_client
        )
        if result is None:
            skipped += 1
            continue

        apply_fact(result, entity_dict)
        results.append(result.model_dump())
        logger.info(
            "Extracted [%s] → %r (confidence %.2f)",
            result.resolved_entity_id or "unlinked",
            result.fact,
            result.confidence,
        )

    return ExtractResponse(results=results, skipped=skipped)


@app.post(
    "/dream-cycle",
    summary="Run reflection pass to surface inferences",
    response_model=DreamCycleResponse,
)
def dream_cycle() -> DreamCycleResponse:
    """
    Calls mubit.Client.reflect() on the current session to synthesise
    cross-fact inferences from everything captured this session.
    Returns the inferences as a list of strings.
    """
    if not mubit_client:
        raise HTTPException(status_code=503, detail="MUBIT_API_KEY not configured")

    try:
        reflection = mubit_client.reflect(session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mubit reflect error: {e}")

    # reflect() returns a dict or list depending on SDK version — normalise
    inferences: list[str] = []
    if isinstance(reflection, dict):
        raw = reflection.get("lessons") or reflection.get("inferences") or []
        inferences = [str(item) for item in raw]
    elif isinstance(reflection, list):
        inferences = [str(item) for item in reflection]
    else:
        inferences = [str(reflection)] if reflection else []

    logger.info("Dream cycle: %d inferences", len(inferences))
    return DreamCycleResponse(session_id=session_id, inferences=inferences)


@app.delete("/session", summary="Reset session and entity dict")
def reset_session() -> dict:
    """Clears the entity dict and starts a new session ID."""
    global entity_dict, session_id
    entity_dict = {}
    session_id = f"audit:session:{int(time.time())}"
    return {"session_id": session_id}
