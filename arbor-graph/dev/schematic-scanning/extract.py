"""
extract.py — Rasterise Arbor GA PDFs and extract room graph data via OpenAI vision.

Usage:
    pip install openai pymupdf
    export OPENAI_API_KEY=...
    python dev/schematic-scanning/extract.py                    # all floors
    python dev/schematic-scanning/extract.py PA2001_LEVEL_1_GA  # single floor by stem
"""

import json
import sys
from pathlib import Path
import fitz  # pymupdf
import openai
import base64

PDF_DIR = Path(__file__).parent.parent.parent.parent / "Arbor-22-AP-2295"
FLOORS_DIR = Path(__file__).parent / "floors"
FLOORS_DIR.mkdir(exist_ok=True)

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

PROMPT = """This is an architectural floor plan (General Arrangement drawing) for Bankside Yards Building 1 (Arbor), floor level {level}.

Extract all enclosed spaces as JSON. Return ONLY valid JSON, no commentary.

{{
  "floor_level": {level},
  "rooms": [
    {{
      "room_id": "string (e.g. L{level}-01)",
      "label": "text label visible in or near the space (e.g. Office, Plant, WC, Lift, Stair)",
      "type": "one of: office|residential|plant|circulation|core|amenity|external|unknown",
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


def rasterise(pdf_path: Path, dpi: int = 200) -> bytes:
    doc = fitz.open(pdf_path)
    page = doc[0]
    # Crop title block (right ~15% of page)
    clip = fitz.Rect(0, 0, page.rect.width * 0.85, page.rect.height)
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=clip)
    return pix.tobytes("png")


def extract_floor(pdf_stem: str, client: openai.OpenAI) -> list[dict]:
    levels = FLOOR_MAP[pdf_stem]
    pdf_path = PDF_DIR / f"{pdf_stem}.pdf"
    if not pdf_path.exists():
        print(f"  WARN: {pdf_path} not found, skipping")
        return []

    print(f"  Rasterising {pdf_stem}...")
    png_bytes = rasterise(pdf_path)
    png_b64 = base64.standard_b64encode(png_bytes).decode()

    # Save raw PNG for debugging
    raw_png = FLOORS_DIR / f"{pdf_stem}.png"
    raw_png.write_bytes(png_bytes)

    level_str = str(levels[0]) if len(levels) == 1 else f"{levels[0]}-{levels[-1]}"
    prompt = PROMPT.format(level=level_str)

    print(f"  Calling GPT-4o vision for {pdf_stem}...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=4096,
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
        raw_text = response.choices[0].message.content

        # Save raw response for debugging
        raw_out = FLOORS_DIR / f"{pdf_stem}_raw.txt"
        raw_out.write_text(raw_text)

        # Strip markdown code fences if present
        text = raw_text.strip()
        if text.startswith("```"):
            text = "\n".join(text.split("\n")[1:])
        if text.endswith("```"):
            text = "\n".join(text.split("\n")[:-1])

        data = json.loads(text)

    except json.JSONDecodeError as e:
        print(f"  ERROR: JSON parse failed for {pdf_stem}: {e}")
        print(f"  Raw saved to {FLOORS_DIR / f'{pdf_stem}_raw.txt'}")
        return []
    except Exception as e:
        print(f"  ERROR: API call failed for {pdf_stem}: {e}")
        return []

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
            # Re-id rooms per level
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
