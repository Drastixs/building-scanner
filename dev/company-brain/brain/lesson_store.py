"""
Cross-building lesson store — JSONL append, one Lesson per line.

A Lesson carries its own precomputed profile_embedding so recall() never has to
re-embed historical lessons; it just loads the floats and does cosine in-process.
"""

import json
import os
from typing import List

DEFAULT_STORE = os.path.join(os.path.dirname(__file__), "..", "lessons.jsonl")


def write_lesson(lesson: dict, path: str = DEFAULT_STORE) -> None:
    """Append one Lesson (must already contain profile_embedding) to the store."""
    if "profile_embedding" not in lesson or not lesson["profile_embedding"]:
        raise ValueError("lesson missing profile_embedding; embed before writing")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(lesson) + "\n")


def load_lessons(path: str = DEFAULT_STORE) -> List[dict]:
    """Load all lessons. Missing store -> empty list (cold start)."""
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out
