# Schematic → HTML: how the conversion actually works

The "HTML file" (`index.html`) is **not generated per floor plan**. It is a fixed Three.js
renderer. The real work is turning each architectural drawing into JSON that the renderer
loads. Source drawing → JSON → 3D in the browser. There are two independent extraction
routes feeding three JSON outputs.

```
buildings/Arbor-22-AP-2295/*.pdf  (architect's GA drawings, one per floor band)
        │
        ├──[A] vision route: extract.py ────────────► floors/*.json   (rooms + cores)
        │                                                   │
        │                                            graph_builder.py ─► graph.json
        │                                       security_graph_builder.py ─► building.json
        │
        └──[B] vector route: vector_extract.py ─────► walls.json       (wall geometry)
                                                            │
                                              index.html (Three.js) ◄── fetch all 3 JSON
                                                            │
                                                   3D building in browser
```

## Route A — Vision extraction (`extract.py`)
1. **Rasterise.** PyMuPDF opens the PDF, crops off the right ~15% (the title block), and
   renders the page to a PNG at 4096px on the long edge — high enough that ~10px room
   labels survive OpenAI's internal 2048px tiling.
2. **Ask a vision model.** The PNG is base64'd and sent to OpenAI `o3` with a strict prompt:
   "return ONLY JSON — list every enclosed space with id, label, type, normalised bounds
   (0–1), neighbours, plus lifts/stairs/corridors as core_elements."
3. **Parse + fan out.** The model's JSON is cleaned (strip ``` fences) and saved. A drawing
   like "Level 2–5 GA" represents four identical floors, so the room set is deep-copied and
   re-IDed per level → `floors/PA2002_..._L2.json … _L5.json`.

## Route B — Vector extraction (`vector_extract.py`) — no AI
1. **Read native lines.** Instead of an image, it reads the PDF's actual vector strokes
   (`get_drawings`) and keeps only wall-weight segments (stroke width ≥ 0.5; thin clutter is
   dropped).
2. **Find the plan.** A GA sheet may hold a plan plus a legend/section. Segment midpoints are
   bucketed into a 48×48 occupancy grid; the largest connected blob (8-neighbour BFS) is the
   real floor plan. Everything outside its bbox is cropped away.
3. **Normalise to a shared frame.** All coords are uniformly scaled to 0–1 (aspect preserved,
   centred, y-flipped to bottom-left origin). Same recipe every floor, so identical footprints
   stack perfectly. *All* geometry math lives here — the viewer stays dumb.
4. **Split envelope vs partitions.** A Shapely concave hull traces the building footprint,
   simplified (Douglas–Peucker) into a few smooth `outer` segments. Segments whose midpoints
   sit well inside become `inner` partitions → `walls.json`.

## Graph builders
- `graph_builder.py` merges the per-floor room JSON into a NetworkX graph: each room is a node
  carrying x/y/w/h and a z height (`level × 3.5m`), neighbours become edges → `graph.json`.
- `security_graph_builder.py` builds the portal graph: doors, lifts, stairs are **nodes**, a
  door is `roomA — portal — roomB`, external entrances link to one room, and stair/lift portals
  sharing a `core_id` on adjacent floors get explicit inter-floor edges → `building.json`.

## The HTML
`index.html` is a static Three.js page. On load it does three `fetch`es —
`graph.json`, `walls.json`, `building.json` — then extrudes the normalised 0–1 geometry into 3D:
floor slabs, inner partitions, the outer glass envelope, and glowing lift/stair cores, with
hover readouts and per-floor toggles. Because all the math was done upstream, the renderer just
does `coordinate × SCALE`. Serve it with `python -m http.server 8181` and the same HTML
visualises any building whose JSON you drop next to it.

**One line:** the schematic isn't "converted to HTML" — it's parsed (by vision and/or vector
analysis) into a normalised room+wall+portal graph in JSON, and a fixed Three.js HTML page
renders that JSON as a 3D model.
