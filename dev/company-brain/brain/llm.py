"""
Thin OpenAI wrapper — the one place that talks to a hosted model.

The project's .env carries OPENAI_API_KEY only (ANTHROPIC was intentionally
removed), so both the specialist chat calls and the recall embeddings go through
OpenAI here. Swapping providers later means editing only this file.

Embeddings are cached in-process by text, so re-embedding the same profile in a
demo run is free and (after a rehearsal warm-up) off the live critical path.
"""

import os
from functools import lru_cache

from openai import OpenAI

CHAT_MODEL = os.environ.get("BRAIN_CHAT_MODEL", "gpt-4o-mini")
EMBED_MODEL = os.environ.get("BRAIN_EMBED_MODEL", "text-embedding-3-small")

_client = None


def client() -> OpenAI:
    """Lazily build the OpenAI client so import never needs a key."""
    global _client
    if _client is None:
        _client = OpenAI()  # reads OPENAI_API_KEY from env
    return _client


@lru_cache(maxsize=512)
def embed(text: str) -> tuple:
    """Embed one string. Returns a tuple (hashable/cacheable)."""
    resp = client().embeddings.create(model=EMBED_MODEL, input=text)
    return tuple(resp.data[0].embedding)


def chat(system: str, user: str, max_tokens: int = 512) -> str:
    """Single-turn chat completion. Returns raw assistant text."""
    resp = client().chat.completions.create(
        model=CHAT_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content.strip()
