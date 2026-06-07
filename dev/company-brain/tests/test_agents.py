"""
CI-gating tests for specialist parsing, score_hook, transfer template, and the
stubbed-specialist wiring E2E (decision #9 — catches a write->recall break).
No live LLM.
"""

import pytest

import brain
import brain.llm as brain_llm
from agents import specialist, transfer


# --- specialist parsing (reuses extractor fence/pydantic/drop idiom) -------


def test_specialist_parses_plain_json():
    s = specialist.Specialist("social")
    out = s._parse(
        '[{"hypothesis_id":"H2","label":"tailgate","target":"lobby",'
        '"confidence":0.8,"next_observation":"watch 9am"}]'
    )
    assert len(out) == 1 and out[0].target == "lobby"


def test_specialist_parses_fenced_json():
    s = specialist.Specialist("social")
    raw = (
        '```json\n[{"hypothesis_id":"H2","label":"t","target":"lobby",'
        '"confidence":0.8,"next_observation":"x"}]\n```'
    )
    assert len(s._parse(raw)) == 1


def test_specialist_drops_malformed_without_crash():
    s = specialist.Specialist("social")
    raw = (
        '[{"hypothesis_id":"H2","label":"ok","target":"lobby","confidence":0.8,'
        '"next_observation":"x"}, {"garbage":true}]'
    )
    out = s._parse(raw)
    assert len(out) == 1  # the bad one dropped, the good one kept


def test_specialist_total_garbage_returns_empty():
    s = specialist.Specialist("social")
    assert s._parse("not json at all") == []


def test_specialist_confidence_clamped():
    s = specialist.Specialist("social")
    out = s._parse(
        '[{"hypothesis_id":"H2","label":"t","target":"l",'
        '"confidence":5.0,"next_observation":"x"}]'
    )
    assert out[0].confidence == 1.0


def test_score_hook_override_applied(monkeypatch):
    # hook that drops everything
    s = specialist.Specialist("social", score_hook=lambda cands: [])
    monkeypatch.setattr(
        specialist.llm,
        "chat",
        lambda sys, usr, **k: (
            '[{"hypothesis_id":"H2","label":"t","target":"l",'
            '"confidence":0.8,"next_observation":"x"}]'
        ),
    )
    prof = {"name": "B", "building_type": "x", "cues": ["herd_entry"]}
    assert s.run(prof) == []  # hook emptied it


# --- transfer template (exact string) -------------------------------------


def test_transfer_announce_exact_string():
    lesson = {
        "name": "Meridian Quay",
        "why": ["hid_maxiprox", "conference_day"],
        "key_lesson": "tailgating during the conference window works",
    }
    assert transfer.announce(lesson) == (
        "From Meridian Quay (shared cues: hid_maxiprox, conference_day), "
        "expect: tailgating during the conference window works"
    )


def test_transfer_cold_path():
    class _Brain:
        def recall(self, profile):
            return []

    lines, prior = transfer.transfer_prior({"cues": []}, _Brain())
    assert lines == [transfer.COLD_LINE]
    assert transfer.COLD_LINE in prior


# --- stubbed-specialist wiring E2E (CI-gating) ----------------------------


def test_wiring_building1_write_then_building2_recall(tmp_path, monkeypatch):
    """A break between building#1 write_lesson and building#2 recall is caught here."""
    store = str(tmp_path / "lessons.jsonl")
    # deterministic embedding: identical vector so #2 recalls #1 above floor
    monkeypatch.setattr(brain_llm, "embed", lambda text: (1.0, 0.0, 0.0))

    b1 = {
        "building_id": "b1",
        "name": "B1",
        "building_type": "multi-tenant-commercial",
        "scope": "s",
        "cues": ["hid_maxiprox", "conference_day"],
        "osint_summary": "",
    }
    br1 = brain.init("b1", "s", store_path=store).attach_profile(b1)
    lesson = brain.build_lesson(
        b1,
        [{"id": "H2", "label": "tailgate", "result": "confirmed", "notes": ""}],
        "tailgating works",
    )
    br1.write_lesson(lesson)

    b2 = {
        "building_id": "b2",
        "name": "B2",
        "building_type": "multi-tenant-commercial",
        "scope": "s",
        "cues": ["hid_maxiprox", "open_floor"],
        "osint_summary": "",
    }
    br2 = brain.init("b2", "s", store_path=store).attach_profile(b2)
    lines, prior = transfer.transfer_prior(b2, br2)

    assert lines and lines[0] != transfer.COLD_LINE
    assert "B1" in lines[0]
    assert "hid_maxiprox" in lines[0]  # shared cue in the why
