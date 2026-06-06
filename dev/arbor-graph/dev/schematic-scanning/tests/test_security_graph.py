"""CRITICAL tests for the security portal graph (eng-review test plan).

1. Cross-extractor inter-floor match (regression guard): a 2-floor graph where
   the floors came from DIFFERENT extractors, stairs at the same normalized pos,
   must produce a CORRECT inter-floor edge — not just `inter_edge_count > 0`
   (Codex: the old 0.08 matcher passed that bar on garbage). We assert the edge
   joins the two stair portals that share a core_id, and joins nothing else.
2. normalize() with a zero-width / zero-height bbox must not divide by zero.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import portal_schema as ps
import security_graph_builder as sgb


def _floor(level, *, with_entrance=False):
    """A minimal valid floor: one space + one stair portal (core STAIR-A).
    Both stairs sit at the SAME normalized pos so a position matcher *could*
    link them — but we link by core_id, which must be exact regardless."""
    portals = [
        {
            "id": f"P{level}-01",
            "a": f"S{level}-01",
            "b": ps.UNKNOWN,
            "kind": "stair",
            "is_external": False,
            "pos": [0.5, 0.5],
            "core_id": "STAIR-A",
        },
    ]
    if with_entrance:
        portals.append(
            {
                "id": f"P{level}-09",
                "a": ps.OUTSIDE,
                "b": f"S{level}-01",
                "kind": "door",
                "is_external": True,
                "pos": [0.1, 0.1],
            }
        )
    return ps.validate_floor(
        {
            "floor": level,
            "perimeter": [],
            "spaces": [
                {
                    "id": f"S{level}-01",
                    "label": "Room",
                    "type": "office",
                    "bounds": {"x": 0.4, "y": 0.4, "w": 0.2, "h": 0.2},
                }
            ],
            "portals": portals,
        }
    )


def test_cross_extractor_inter_floor_match_is_correct():
    # floor 0 (imagine vector path) + floor 1 (imagine vision path), same schema.
    floor_a = _floor(0, with_entrance=True)
    floor_b = _floor(1)
    G = sgb.build_graph([floor_a, floor_b])

    inter = [(u, v) for u, v, d in G.edges(data=True) if d.get("type") == "inter"]
    # exactly one inter-floor edge, and it joins the two STAIR-A portals
    assert len(inter) == 1, f"expected 1 inter edge, got {inter}"
    assert set(inter[0]) == {"P0-01", "P1-01"}, f"wrong endpoints: {inter[0]}"
    assert G.edges["P0-01", "P1-01"]["core_id"] == "STAIR-A"


def test_inter_floor_does_not_link_distinct_cores():
    # same pos, DIFFERENT core_id => no inter edge (guards the 0.08-on-position bug)
    floor_a = _floor(0, with_entrance=True)
    floor_b = _floor(1)
    floor_b["portals"][0]["core_id"] = "STAIR-B"  # different shaft, identical pos
    G = sgb.build_graph([floor_a, floor_b])
    inter = [d for _, _, d in G.edges(data=True) if d.get("type") == "inter"]
    assert inter == [], f"distinct cores must not link by position: {inter}"


def test_entrance_depth_reaches_upper_floor():
    # the entrance on floor 0 must make floor 1's space reachable via the stair
    G = sgb.build_graph([_floor(0, with_entrance=True), _floor(1)])
    assert G.nodes["S0-01"]["entrance_depth"] is not None
    assert G.nodes["S1-01"]["entrance_depth"] is not None  # reached across floors


def test_unreachable_space_has_null_depth():
    # no entrance anywhere => every space depth is None, no crash
    G = sgb.build_graph([_floor(0), _floor(1)])
    assert G.nodes["S0-01"]["entrance_depth"] is None
    assert G.nodes["S1-01"]["entrance_depth"] is None


def test_normalize_zero_width_bbox_no_div_by_zero():
    # degenerate drawing area must not raise
    assert ps.normalize((5.0, 7.0), (5.0, 0.0, 5.0, 10.0)) == [0.0, 0.7]


def test_normalize_zero_height_bbox_no_div_by_zero():
    assert ps.normalize((3.0, 4.0), (0.0, 4.0, 10.0, 4.0)) == [0.3, 0.0]


def test_normalize_corners_map_to_unit():
    bbox = (10.0, 20.0, 110.0, 220.0)
    assert ps.normalize((10.0, 20.0), bbox) == [0.0, 0.0]
    assert ps.normalize((110.0, 220.0), bbox) == [1.0, 1.0]
