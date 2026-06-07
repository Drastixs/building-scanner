"""
Company Brain — Mubit-shaped facade.

This is the ONLY surface the agents touch: init / recall / write_lesson. Internals
(graph, lesson store, embeddings) are swappable; if real mubit-sdk is ever
verified, this module is the seam to swap it behind.

`reflect` is a deferred interface stub (design "NOT in Scope") — declared so the
shape matches Mubit, intentionally not implemented in v1.
"""

from . import graph as _graph
from . import lesson_store as _lesson_store
from . import llm as _llm
from . import taxonomy as _taxonomy
from .recall import SIM_FLOOR, profile_embedding_text, recall

__all__ = [
    "init",
    "recall",
    "write_lesson",
    "build_lesson",
    "reflect",
    "SIM_FLOOR",
]


class Brain:
    """Per-building handle: holds the cue graph + the shared lesson store path."""

    def __init__(self, building_id: str, scope: str, store_path: str = None):
        self.building_id = building_id
        self.scope = scope
        self.store_path = store_path
        self.graph = None

    def attach_profile(self, profile: dict):
        _taxonomy.validate_cues(
            profile.get("cues", []), where=f"profile {profile['building_id']}"
        )
        self.graph = _graph.build_graph(profile)
        return self

    def recall(self, profile: dict, **kw):
        if self.store_path:
            kw.setdefault("path", self.store_path)
        return recall(profile, **kw)

    def write_lesson(self, lesson: dict):
        return (
            write_lesson(lesson, path=self.store_path)
            if self.store_path
            else write_lesson(lesson)
        )


def init(building_id: str, scope: str, store_path: str = None) -> Brain:
    """Create/load a per-building brain handle attached to the lesson store."""
    return Brain(building_id, scope, store_path)


def write_lesson(lesson: dict, path: str = None) -> None:
    """Append a fully-formed Lesson (must carry profile_embedding) to the store."""
    if path:
        _lesson_store.write_lesson(lesson, path=path)
    else:
        _lesson_store.write_lesson(lesson)


def build_lesson(profile: dict, hypotheses: list, key_lesson: str) -> dict:
    """
    Assemble a Lesson from a profile + its hypothesis outcomes + the one-line
    transferable lesson, embedding the profile so it is ready for write_lesson().
    """
    _taxonomy.validate_cues(
        profile.get("cues", []), where=f"lesson {profile['building_id']}"
    )
    return {
        "building_id": profile["building_id"],
        "name": profile["name"],
        "building_type": profile["building_type"],
        "cues": list(profile.get("cues", [])),
        "profile_embedding": list(_llm.embed(profile_embedding_text(profile))),
        "hypotheses": hypotheses,
        "key_lesson": key_lesson,
    }


def reflect(*args, **kwargs):
    """Deferred Mubit-shaped stub. Not implemented in v1 (see design NOT in Scope)."""
    raise NotImplementedError("reflect() is a deferred interface stub; not in v1 scope")
