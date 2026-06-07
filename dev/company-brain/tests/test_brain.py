"""
CI-gating unit tests. No live LLM — llm.embed / llm.chat are stubbed.
"""

import json

import pytest

import sys

import brain  # noqa: F401  (ensures brain.recall submodule is loaded)
import brain.llm as brain_llm
from brain import collide, lesson_store, taxonomy

# brain.__init__ rebinds the name `brain.recall` to the recall() function, so the
# submodule must be fetched from sys.modules rather than via attribute access.
recall_mod = sys.modules["brain.recall"]


# --- taxonomy -------------------------------------------------------------


def test_taxonomy_unknown_cue_raises():
    with pytest.raises(taxonomy.UnknownCueError):
        taxonomy.validate_cues(["hid_maxiprox", "totally_made_up_cue"])


def test_taxonomy_known_cues_pass():
    assert taxonomy.validate_cues(["hid_maxiprox", "turnstile"]) == [
        "hid_maxiprox",
        "turnstile",
    ]


# --- recall ---------------------------------------------------------------


def _write_lesson(path, name, cues, emb, key="k"):
    lesson_store.write_lesson(
        {
            "building_id": name,
            "name": name,
            "building_type": "multi-tenant-commercial",
            "cues": cues,
            "profile_embedding": emb,
            "hypotheses": [],
            "key_lesson": key,
        },
        path=str(path),
    )


def test_recall_hit_returns_lessons_with_why(tmp_path, monkeypatch):
    store = tmp_path / "lessons.jsonl"
    _write_lesson(store, "A", ["hid_maxiprox", "conference_day"], [1.0, 0.0, 0.0])
    monkeypatch.setattr(brain_llm, "embed", lambda text: (1.0, 0.0, 0.0))
    prof = {
        "building_type": "multi-tenant-commercial",
        "cues": ["hid_maxiprox", "open_floor"],
        "osint_summary": "",
    }
    hits = recall_mod.recall(prof, path=str(store))
    assert len(hits) == 1
    assert hits[0]["why"] == ["hid_maxiprox"]  # set intersection, non-empty
    assert hits[0]["similarity"] >= recall_mod.SIM_FLOOR


def test_recall_all_below_floor_returns_empty(tmp_path, monkeypatch):
    store = tmp_path / "lessons.jsonl"
    _write_lesson(store, "A", ["hid_maxiprox"], [0.0, 1.0, 0.0])  # orthogonal
    monkeypatch.setattr(brain_llm, "embed", lambda text: (1.0, 0.0, 0.0))
    prof = {"building_type": "x", "cues": ["hid_maxiprox"], "osint_summary": ""}
    assert recall_mod.recall(prof, path=str(store)) == []


def test_recall_topk_ordering(tmp_path, monkeypatch):
    store = tmp_path / "lessons.jsonl"
    _write_lesson(store, "near", ["hid_maxiprox"], [1.0, 0.0, 0.0])  # cos 1.0
    _write_lesson(store, "mid", ["hid_maxiprox"], [0.9, 0.2, 0.0])  # cos ~0.976
    monkeypatch.setattr(brain_llm, "embed", lambda text: (1.0, 0.0, 0.0))
    prof = {"building_type": "x", "cues": ["hid_maxiprox"], "osint_summary": ""}
    hits = recall_mod.recall(prof, path=str(store))
    assert [h["building_id"] for h in hits] == ["near", "mid"]


def test_recall_cold_start_empty_store(tmp_path, monkeypatch):
    monkeypatch.setattr(brain_llm, "embed", lambda text: (1.0, 0.0, 0.0))
    prof = {"building_type": "x", "cues": [], "osint_summary": ""}
    assert recall_mod.recall(prof, path=str(tmp_path / "missing.jsonl")) == []


# --- lesson_store ---------------------------------------------------------


def test_write_lesson_appends_jsonl_with_embedding(tmp_path):
    store = tmp_path / "lessons.jsonl"
    _write_lesson(store, "A", ["hid_maxiprox"], [0.1, 0.2])
    lines = store.read_text().strip().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["profile_embedding"] == [0.1, 0.2]


def test_write_lesson_rejects_missing_embedding(tmp_path):
    with pytest.raises(ValueError):
        lesson_store.write_lesson({"building_id": "x"}, path=str(tmp_path / "l.jsonl"))


# --- collide --------------------------------------------------------------


def _c(hid, target, conf, graph):
    return {
        "hypothesis_id": hid,
        "label": hid,
        "target": target,
        "confidence": conf,
        "next_observation": "look",
        "graph": graph,
    }


def test_collide_shared_target_merges_and_ranks():
    social = [_c("H2", "main_lobby", 0.8, "social")]
    spatial = [_c("H1", "main_lobby", 0.5, "spatial")]
    credential = [_c("H3", "main_lobby", 0.9, "credential")]
    routes = collide.collide([social, spatial, credential])
    assert len(routes) == 1
    r = routes[0]
    assert r["target"] == "main_lobby"
    assert r["n_graphs"] == 3
    assert r["score"] == pytest.approx(0.8 * 0.5 * 0.9)


def test_collide_unique_targets_independent():
    social = [_c("H2", "lobby", 0.8, "social")]
    spatial = [_c("H1", "loading_bay", 0.6, "spatial")]
    routes = collide.collide([social, spatial])
    assert len(routes) == 2
    assert {r["target"] for r in routes} == {"lobby", "loading_bay"}


def test_collide_ranks_more_graphs_first():
    a = [_c("H2", "lobby", 0.4, "social")]
    b = [_c("H1", "lobby", 0.4, "spatial")]
    c = [_c("H9", "bay", 0.99, "credential")]
    routes = collide.collide([a, b, c])
    # lobby has 2 graphs -> ranks above single-graph bay despite lower score
    assert routes[0]["target"] == "lobby"
