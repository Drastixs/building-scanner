"""
test_embedded_labels.py — the text-extraction filter is where #1's bugs live, so it
gets the coverage. Pure + deterministic: reads a real Arbor GA PDF, no OpenAI calls.

    pytest dev/schematic-scanning/tests/test_embedded_labels.py
"""

import sys
from pathlib import Path

import fitz
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from extract import (  # noqa: E402
    PDF_DIR,
    _looks_like_label,
    assign_text_labels,
    embedded_labels,
)

SHEET = PDF_DIR / "PA2001_LEVEL_1_GA.pdf"


@pytest.fixture(scope="module")
def labels():
    if not SHEET.exists():
        pytest.skip(f"{SHEET} not present")
    page = fitz.open(SHEET)[0]
    return embedded_labels(page)


# ── the pure classifier: keep room labels, drop notes + drawing codes ─────────
@pytest.mark.parametrize(
    "text", ["Office", "Plant", "Terrace", "Planting", "WC", "Plant Room"]
)
def test_keeps_room_labels(text):
    assert _looks_like_label(text) is True


@pytest.mark.parametrize(
    "text",
    [
        "PA2200",  # drawing register code
        "R.15",  # revision / grid code
        "N.B. All internal layouts are shown for indicative purposes",  # note
        "1:100",  # scale
        "",  # empty
        "(Class (g)(i))",  # planning-class fragment, lowercase start
    ],
)
def test_drops_boilerplate(text):
    assert _looks_like_label(text) is False


# ── end-to-end on the real sheet ──────────────────────────────────────────────
def test_real_sheet_has_room_labels(labels):
    texts = {lab["text"].lower() for lab in labels}
    assert any("office" in t for t in texts), f"no Office label found in {texts}"
    assert any("plant" in t for t in texts), f"no Plant label found in {texts}"


def test_real_sheet_excludes_codes_and_notes(labels):
    texts = [lab["text"] for lab in labels]
    assert "PA2200" not in texts
    assert not any(t.lower().startswith("n.b") for t in texts)


def test_labels_normalised_into_clip_frame(labels):
    # every kept label sits in the drawing area (0..1, title block already dropped)
    for lab in labels:
        assert 0.0 <= lab["x"] <= 1.0
        assert 0.0 <= lab["y"] <= 1.0


def test_rotated_multifloor_sheet_stays_in_frame():
    # REGRESSION: PA2002 is a 90°-rotated multi-floor sheet. Before the rotation_matrix
    # transform, get_text() bbox lived in mediabox space and normalised to y up to 1.34,
    # scrambling the point-in-box label override. Every label must land in 0..1.
    sheet = PDF_DIR / "PA2002_LEVEL_2-5_GA.pdf"
    if not sheet.exists():
        pytest.skip(f"{sheet} not present")
    labs = embedded_labels(fitz.open(sheet)[0])
    assert labs, "expected room labels on PA2002"
    for lab in labs:
        assert 0.0 <= lab["x"] <= 1.0, f"{lab} x out of frame"
        assert 0.0 <= lab["y"] <= 1.0, f"{lab} y out of frame (rotation regression)"
    # title-block / keyplan text (all at x>=0.91 in display space) must be gone
    assert not any(lab["text"].startswith("Context") for lab in labs)


# ── deterministic point-in-box override ───────────────────────────────────────
def test_assign_prefers_printed_label_inside_box():
    rooms = [
        {
            "approximate_bounds": {"x": 0.4, "y": 0.4, "w": 0.2, "h": 0.2},
            "label": "Room",
        }
    ]
    assign_text_labels(rooms, [{"text": "Terrace", "x": 0.5, "y": 0.5}])
    assert rooms[0]["label"] == "Terrace"
    assert rooms[0]["label_source"] == "text"


def test_assign_keeps_vision_label_when_no_text_inside():
    rooms = [
        {
            "approximate_bounds": {"x": 0.0, "y": 0.0, "w": 0.1, "h": 0.1},
            "label": "Lobby",
        }
    ]
    assign_text_labels(rooms, [{"text": "Terrace", "x": 0.9, "y": 0.9}])
    assert rooms[0]["label"] == "Lobby"
    assert rooms[0]["label_source"] == "vision"
