"""
extract.py — Rasterise Arbor GA PDFs and extract room graph data via OpenAI vision,
grounded on the PDF's own embedded text.

Two data sources are fused per sheet:
  1. The rasterised image (what o3 "sees").
  2. The PDF's embedded text lines (the architect's actual labels), pulled with
     PyMuPDF and normalised into the SAME 0..1 clip frame the image uses.

The text is authoritative: it is injected into the prompt as the real label set, and
a deterministic point-in-box pass overrides each room's label with the printed string
that sits inside it (label_source="text"). Vision only fills spaces that carry no text.

Usage:
    pip install openai pymupdf
    export OPENAI_API_KEY=...
    python dev/schematic-scanning/extract.py                    # all floors
    python dev/schematic-scanning/extract.py PA2001_LEVEL_1_GA  # single floor by stem
"""

import base64
import json
import re
import sys
from pathlib import Path

import fitz  # pymupdf
import openai

PDF_DIR = (
    Path(__file__).parent.parent.parent.parent.parent / "buildings" / "Arbor-22-AP-2295"
)
FLOORS_DIR = Path(__file__).parent / "floors"
FLOORS_DIR.mkdir(exist_ok=True)

TITLE_FRAC = (
    0.85  # drop right ~15% (title block); matches the image clip + vector_extract
)
# Arbor GA sheets also carry a keyplan / general-notes / title strip across the TOP
# (place names, "FOR PLANNING", project/client codes cluster at y_norm < ~0.13). The
# plan area sits below it, so drop that band. Template-specific to this drawing set.
TOP_NOTE_BAND = 0.13

FLOOR_MAP = {
    "PA1997_BASEMENT": [-2],
    "PA1998_BASEMENT_B1": [-1],
    "PA1999_GROUND_FLOOR_LOWER": ["L0a"],
    "PA2000_GROUND_FLOOR_UPPER": ["L0b"],
    "PA2001_LEVEL_1_GA": [1],
    "PA2002_LEVEL_2-5_GA": [2, 3, 4, 5],
    "PA2006_LEVEL_6-9_GA": [6, 7, 8, 9],
    "PA2010_LEVEL_10-13_GA": [10, 11, 12, 13],
    "PA2014_LEVEL_14-17_GA": [14, 15, 16, 17],
    "PA2018_ROOF_GA": [18],
}

# ── Embedded-text extraction (#1: text as a second data source) ───────────────
#
#   PDF text lines           normalise to clip 0..1        filter boilerplate
#   "Office"  (pts)   ──►     "Office" (0.42, 0.30)   ──►   keep room labels,
#   "N.B. All ..."           "N.B. ..."  (0.05, 0.92)       drop notes + codes
#   "PA2200"                 "PA2200"   (0.71, 0.55)
#
# Room words we always keep even if the generic heuristic would drop them.
ROOM_VOCAB = {
    "office",
    "plant",
    "planting",
    "terrace",
    "balcony",
    "roof",
    "wc",
    "toilet",
    "lift",
    "stair",
    "stairs",
    "reception",
    "lobby",
    "foyer",
    "core",
    "riser",
    "store",
    "storage",
    "comms",
    "cycle",
    "bin",
    "substation",
    "switchroom",
    "tank",
    "lounge",
    "kitchen",
    "meeting",
    "boardroom",
    "void",
    "atrium",
    "entrance",
    "corridor",
    "circulation",
    "retail",
    "residential",
    "apartment",
    "plantroom",
    "amenity",
    "gym",
    "studio",
    "pool",
    "void over",
    "loading",
}
# Drawing-register / dimension / revision codes, e.g. PA2200, R.15, B1, A1.
_CODE_RE = re.compile(r"^[A-Z]{1,3}[.\-]?\d")
# Words that mark title-block notes rather than room labels.
_NOTE_WORDS = (
    "n.b.",
    "refer",
    "drawing",
    "scale",
    "drawn",
    "checked",
    "approved",
    "pursuant",
    "condition",
    "boundary",
    "indicative",
    "rev ",
    "issue",
)


def _looks_like_label(text: str) -> bool:
    """True if a text line reads like a room label, not a note or a code."""
    low = text.lower()
    if low in ROOM_VOCAB or any(w in low.split() for w in ROOM_VOCAB):
        return True
    words = text.split()
    if len(words) > 4 or len(text) > 28:
        return False
    if _CODE_RE.match(text):
        return False
    if any(nw in low for nw in _NOTE_WORDS):
        return False
    stripped = text.replace(" ", "")
    if not stripped:
        return False
    if sum(c.isdigit() for c in stripped) > 0.3 * len(stripped):
        return False
    if not text[0].isupper():
        return False
    if sum(c.isalpha() for c in stripped) < 0.6 * len(stripped):
        return False
    return True


def embedded_labels(page) -> list[dict]:
    """
    Text lines inside the drawing area, normalised to the clip's 0..1 frame.
    Returns [{"text", "x", "y"}] in the same coordinate space the model sees.
    """
    # These sheets are rotated 90°. get_text() returns bbox in the UNROTATED mediabox
    # space, but the image o3 sees comes from get_pixmap() in the ROTATED display space
    # (page.rect). Transform text points through rotation_matrix so labels live in the
    # same 0..1 frame as the image and as o3's room bounds.
    mat = page.rotation_matrix
    clipx = page.rect.width * TITLE_FRAC
    clipy = page.rect.height
    out = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line["spans"]).strip()
            if not text:
                continue
            x0, y0, x1, y1 = line["bbox"]
            p0 = fitz.Point(x0, y0) * mat
            p1 = fitz.Point(x1, y1) * mat
            cx, cy = (p0.x + p1.x) / 2, (p0.y + p1.y) / 2
            if cx >= clipx:  # right-hand title block → drop
                continue
            if cy / clipy < TOP_NOTE_BAND:  # top keyplan/notes strip → drop
                continue
            if len(text.replace(" ", "")) < 2:  # stray grid refs like "A" → drop
                continue
            if not _looks_like_label(text):
                continue
            out.append(
                {"text": text, "x": round(cx / clipx, 4), "y": round(cy / clipy, 4)}
            )
    return out


def assign_text_labels(rooms: list[dict], labels: list[dict]) -> None:
    """
    Deterministic override: a printed label whose centroid falls inside a room's
    bounds becomes that room's label (text is ground truth). Spaces with no
    printed label keep the model's inference and are tagged label_source="vision".
    """
    for room in rooms:
        b = room.get("approximate_bounds", {})
        x, y = b.get("x", 0.0), b.get("y", 0.0)
        w, h = b.get("w", 0.0), b.get("h", 0.0)
        inside = [
            lab for lab in labels if x <= lab["x"] <= x + w and y <= lab["y"] <= y + h
        ]
        if inside:
            cx, cy = x + w / 2, y + h / 2
            best = min(
                inside, key=lambda lab: (lab["x"] - cx) ** 2 + (lab["y"] - cy) ** 2
            )
            room["label"] = best["text"]
            room["label_source"] = "text"
        else:
            room.setdefault("label_source", "vision")


# ── Prompt (#2: text injection + visual-cue classification) ───────────────────
PROMPT = """This is an architectural floor plan (General Arrangement drawing) for Bankside Yards Building 1 (Arbor), floor level {level}.

Extract every enclosed space as JSON. Return ONLY valid JSON, no commentary.

You are given the EXACT text labels printed on this drawing, with their normalised
(x, y) positions in the drawing area (0.0–1.0, origin top-left). These are authoritative:
use these strings verbatim for the `label` of the space each one sits in, and set
"label_source": "text". Do NOT invent or reword a printed label. If a space carries no
printed label, infer it from the visual cues below and set "label_source": "vision".

EMBEDDED TEXT LABELS:
{labels}

Visual cues — use these to set `type`, `function`, `environment`, `fixtures`:
- Toilet / urinal / basin glyphs in small cubicles with door swings -> WC (type: amenity, fixtures: ["wc","basin"], environment: indoor)
- A larger WC cubicle with a wheelchair / DDA symbol, a corner pan and grab rails -> Accessible WC (type: amenity, function: "Accessible WC", fixtures: ["wc","basin","grab-rail"], environment: indoor)
- A room sectioned off with a large table ringed by chairs          -> meeting room / boardroom (type: office)
- Regular tile / brick HATCH fill, usually labelled "Terrace"        -> terrace (type: external, environment: outdoor, fixtures: ["tile-hatch"])
- Dashed circles (tree canopies), usually labelled "Planting"        -> landscaping (type: external, environment: outdoor, fixtures: ["tree"])
- "Plant" (NOT "Planting")                                           -> mechanical plant room (type: plant, environment: indoor)
- A rectangle crossed by a dashed diagonal X                         -> void / shaft / open-below (type: core)
- Stair treads / lift car squares                                    -> type: core (also list under core_elements)

{{
  "floor_level": {level},
  "rooms": [
    {{
      "room_id": "string (e.g. L{level}-01)",
      "label": "the printed text label if one sits in this space, else inferred",
      "label_source": "text | vision",
      "type": "one of: office|residential|plant|circulation|core|amenity|external|unknown",
      "function": "short human description (e.g. 'Male WC', 'Boardroom', 'Terrace', 'Plant Room')",
      "environment": "indoor | outdoor | covered",
      "fixtures": ["visual items you used to classify, e.g. wc, basin, desk, tree, tile-hatch"],
      "confidence": 0.0,
      "approximate_bounds": {{"x": 0.0, "y": 0.0, "w": 0.0, "h": 0.0}},
      "neighbours": ["room_ids sharing a wall or door opening on this floor"]
    }}
  ],
  "core_elements": [
    {{
      "id": "string (e.g. LIFT-01)",
      "type": "lift|stair|corridor",
      "position": {{"x": 0.0, "y": 0.0}}
    }}
  ]
}}

Bounds are normalised 0.0–1.0 relative to the drawing area (not the full page).
Identify lifts, staircases, and corridors as core_elements — these connect floors vertically."""


def rasterise(page, target_long_px: int = 4096) -> bytes:
    """Render the drawing area (title block cropped) to a PNG."""
    clip = fitz.Rect(0, 0, page.rect.width * TITLE_FRAC, page.rect.height)
    # Scale so the longest edge = target_long_px (OpenAI tiles after scaling to 2048,
    # so 4096 gives 2× coverage per tile → labels readable at ~10px)
    scale = target_long_px / max(clip.width, clip.height)
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=clip)
    return pix.tobytes("png")


def _format_labels(labels: list[dict]) -> str:
    if not labels:
        return "(no embedded text found — classify from visual cues only)"
    return "\n".join(f'- "{lab["text"]}" at ({lab["x"]}, {lab["y"]})' for lab in labels)


def _call_o3(client, png_b64, prompt, stem, attempts=3):
    """
    Call o3 vision and parse its JSON, retrying on the empty / unparseable response
    o3 occasionally returns (reasoning ate the token budget, or a transient). Returns
    the parsed dict, or None if every attempt failed. The last raw body is saved for
    debugging.
    """
    for attempt in range(1, attempts + 1):
        try:
            response = client.chat.completions.create(
                model="o3",
                max_completion_tokens=8192,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{png_b64}",
                                    "detail": "high",
                                },
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            )
            raw_text = response.choices[0].message.content or ""
            (FLOORS_DIR / f"{stem}_raw.txt").write_text(raw_text)  # debug

            text = raw_text.strip()
            if text.startswith("```"):
                text = "\n".join(text.split("\n")[1:])
            if text.endswith("```"):
                text = "\n".join(text.split("\n")[:-1])
            if not text:
                raise ValueError("empty response")
            return json.loads(text)
        except (json.JSONDecodeError, ValueError) as e:
            print(
                f"  WARN: parse failed for {stem} (attempt {attempt}/{attempts}): {e}"
            )
        except Exception as e:
            print(
                f"  WARN: API call failed for {stem} (attempt {attempt}/{attempts}): {e}"
            )
    print(
        f"  ERROR: giving up on {stem}; raw saved to {FLOORS_DIR / f'{stem}_raw.txt'}"
    )
    return None


def extract_floor(pdf_stem: str, client: openai.OpenAI) -> list[dict]:
    levels = FLOOR_MAP[pdf_stem]
    pdf_path = PDF_DIR / f"{pdf_stem}.pdf"
    if not pdf_path.exists():
        print(f"  WARN: {pdf_path} not found, skipping")
        return []

    page = fitz.open(pdf_path)[0]

    print(f"  Rasterising {pdf_stem}...")
    png_bytes = rasterise(page)
    png_b64 = base64.standard_b64encode(png_bytes).decode()
    (FLOORS_DIR / f"{pdf_stem}.png").write_bytes(png_bytes)  # debug

    labels = embedded_labels(page)
    (FLOORS_DIR / f"{pdf_stem}_labels.json").write_text(json.dumps(labels, indent=2))
    print(
        f"  Embedded labels kept: {len(labels)} ({', '.join(l['text'] for l in labels[:8])}{'...' if len(labels) > 8 else ''})"
    )

    level_str = str(levels[0]) if len(levels) == 1 else f"{levels[0]}-{levels[-1]}"
    prompt = PROMPT.format(level=level_str, labels=_format_labels(labels))

    print(f"  Calling o3 vision for {pdf_stem}...")
    data = _call_o3(client, png_b64, prompt, pdf_stem)
    if data is None:
        return []

    # #1: deterministic text override — printed labels win where they sit in a room.
    assign_text_labels(data.get("rooms", []), labels)

    # If PDF covers multiple floors, replicate the room set for each
    results = []
    if len(levels) == 1:
        data["floor_level"] = levels[0]
        out = FLOORS_DIR / f"{pdf_stem}.json"
        out.write_text(json.dumps(data, indent=2))
        print(f"  Wrote {out}")
        results.append(data)
    else:
        for lvl in levels:
            floor_data = json.loads(json.dumps(data))  # deep copy
            floor_data["floor_level"] = lvl
            for room in floor_data["rooms"]:
                room["room_id"] = room["room_id"].replace(str(levels[0]), str(lvl))
            for core in floor_data.get("core_elements", []):
                core["id"] = f"{core['id']}-L{lvl}"
            out = FLOORS_DIR / f"{pdf_stem}_L{lvl}.json"
            out.write_text(json.dumps(floor_data, indent=2))
            print(f"  Wrote {out}")
            results.append(floor_data)

    return results


def main():
    client = openai.OpenAI()
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(FLOOR_MAP.keys())

    for stem in targets:
        if stem not in FLOOR_MAP:
            print(f"Unknown stem: {stem}. Valid: {list(FLOOR_MAP.keys())}")
            continue
        print(f"\n--- {stem} ---")
        extract_floor(stem, client)

    print("\nDone. Run graph_builder.py next.")


if __name__ == "__main__":
    main()
