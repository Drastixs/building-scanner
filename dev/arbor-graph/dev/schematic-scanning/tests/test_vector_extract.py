"""M1 unit tests for vector_extract pure functions (decision 4A)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import vector_extract as ve


def test_normalise_preserves_aspect():
    # A wide region (2:1) must NOT shear into a square: the longer axis spans the
    # full 0..1 and the shorter axis stays proportionally shorter (uniform scale).
    region = (0.0, 0.0, 200.0, 100.0)  # w=200, h=100
    segs = [
        (0.0, 0.0, 200.0, 0.0),  # full-width horizontal
        (0.0, 0.0, 0.0, 100.0),
    ]  # full-height vertical
    out = ve.normalise(segs, region)
    width_span = abs(out[0][2] - out[0][0])  # normalised x extent of wide seg
    height_span = abs(out[1][3] - out[1][1])  # normalised y extent of tall seg
    assert abs(width_span - 1.0) < 1e-6, f"long axis should fill 0..1, got {width_span}"
    # height is half the width in the source → must stay ~0.5 after uniform scale
    assert abs(height_span - 0.5) < 1e-6, f"aspect not preserved: {height_span}"


def test_normalise_centres_shorter_axis():
    # 2:1 region → shorter (y) axis centred: 0.25 margin top and bottom.
    region = (0.0, 0.0, 200.0, 100.0)
    segs = [(0.0, 0.0, 0.0, 100.0)]  # full-height line at left edge
    out = ve.normalise(segs, region)
    ys = sorted([out[0][1], out[0][3]])
    assert abs(ys[0] - 0.25) < 1e-6, f"bottom margin should be 0.25, got {ys[0]}"
    assert abs(ys[1] - 0.75) < 1e-6, f"top margin should be 0.75, got {ys[1]}"


def test_normalise_coords_in_range():
    # Segments fully inside the region normalise into [0,1].
    region = (10.0, 10.0, 110.0, 110.0)
    segs = [(10.0, 10.0, 110.0, 110.0)]
    out = ve.normalise(segs, region)
    for v in (out[0][0], out[0][1], out[0][2], out[0][3]):
        assert -1e-6 <= v <= 1.0 + 1e-6, f"coord out of range: {v}"


def test_normalise_flips_y():
    # PDF y grows downward; model y grows upward. Top-of-PDF maps to top-of-model (~1).
    region = (0.0, 0.0, 100.0, 100.0)
    segs = [(50.0, 0.0, 50.0, 100.0)]  # y=0 is PDF-top, y=100 is PDF-bottom
    out = ve.normalise(segs, region)
    y_at_pdf_top = out[0][1]  # corresponds to source y=0
    y_at_pdf_bottom = out[0][3]  # corresponds to source y=100
    assert y_at_pdf_top > y_at_pdf_bottom, "y axis not flipped"
    assert abs(y_at_pdf_top - 1.0) < 1e-6 and abs(y_at_pdf_bottom - 0.0) < 1e-6


def test_main_plan_region_picks_largest_cluster():
    # Two blocks: a big dense plan (left) + a tiny key diagram (far right).
    # Region detection must return a bbox around the BIG block, not the small one.
    plan = []
    for i in range(20):
        for j in range(20):
            x = 10 + i * 2
            y = 10 + j * 2
            plan.append((x, y, x + 1, y + 1))  # dense grid of short segs
    key = [(300, 10, 301, 11), (300, 12, 301, 13)]  # tiny far-right cluster
    region = ve.main_plan_region(plan + key)
    rx0, ry0, rx1, ry1 = region
    assert rx1 < 200, f"region should exclude the far-right key block, got x1={rx1}"
    assert rx0 < 20 and ry0 < 20, "region should start near the dense plan block"


def test_split_outer_inner_separates_envelope():
    # A square ring of perimeter segments + one interior segment in the middle.
    # The outer outline should be a small set of boundary edges; the interior
    # segment should land in inner, not outer.
    ring = [
        (0.1, 0.1, 0.9, 0.1),
        (0.9, 0.1, 0.9, 0.9),
        (0.9, 0.9, 0.1, 0.9),
        (0.1, 0.9, 0.1, 0.1),
    ]
    # densify the ring a little so the hull has points to work with
    dense = ring + [
        (0.3, 0.1, 0.5, 0.1),
        (0.9, 0.3, 0.9, 0.5),
        (0.5, 0.9, 0.7, 0.9),
        (0.1, 0.5, 0.1, 0.7),
    ]
    interior = (0.45, 0.45, 0.55, 0.55)
    outer, inner = ve.split_outer_inner(dense + [interior])
    assert len(outer) >= 3, "outer envelope should have boundary segments"
    assert list(interior) in inner, "interior segment must be classified as inner"
    # the smoothed outer should be far fewer segments than the dense perimeter input
    assert len(outer) <= len(dense), "outer outline should be simplified, not denser"


def test_clip_to_region_drops_outside():
    region = (0.0, 0.0, 100.0, 100.0)
    inside = (10.0, 10.0, 20.0, 20.0)
    outside = (500.0, 500.0, 510.0, 510.0)
    out = ve.clip_to_region([inside, outside], region)
    assert inside in out and outside not in out
