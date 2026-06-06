import { describe, it, expect } from 'vitest';
import {
  worldXZ,
  stairSteps,
  liftColumn,
  liftBuckets,
  wallSegTransform,
  partitionPlacement,
  doorGap,
  outerRing,
} from '@/lib/scene/geometry';
import { SCALE_XY, MIN_FOOT, LIFT_OVERRUN } from '@/lib/scene/constants';
import type { GraphNode, WallSeg } from '@/lib/types';

const node = (p: Partial<GraphNode>): GraphNode => ({
  id: 'n',
  label: '',
  type: 'office',
  floor: 0,
  x: 0,
  y: 0,
  z: 0,
  ...p,
});

describe('worldXZ', () => {
  it('scales normalised coords to world units', () => {
    expect(worldXZ({ x: 0.5, y: 0.25 })).toEqual([0.5 * SCALE_XY, 0.25 * SCALE_XY]);
  });
});

describe('outerRing', () => {
  // A unit square traced head-to-tail (already ordered, as in walls.json).
  const square: WallSeg[] = [
    [0, 0, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [0, 1, 0, 0],
  ];

  it('returns one scaled vertex per segment, in order, no closing dup', () => {
    expect(outerRing(square)).toEqual([
      [0, 0],
      [1 * SCALE_XY, 0],
      [1 * SCALE_XY, 1 * SCALE_XY],
      [0, 1 * SCALE_XY],
    ]);
  });

  it('chains unordered / reversed segments into the same ring', () => {
    const scrambled: WallSeg[] = [
      [0, 0, 1, 0],
      [0, 1, 0, 0], // reversed
      [1, 1, 0, 1],
      [1, 0, 1, 1],
    ];
    expect(outerRing(scrambled)).toEqual(outerRing(square));
  });

  it('handles empty and degenerate input', () => {
    expect(outerRing([])).toEqual([]);
    expect(outerRing([[0, 0, 1, 0]])).toEqual([[0, 0]]);
  });
});

describe('stairSteps', () => {
  it('returns nothing for a negligible rise', () => {
    expect(stairSteps({ x: 0, y: 0, z: 0 }, { x: 0, y: 0.005, z: 0 })).toEqual([]);
  });
  it('builds 12 treads + 12 risers + 1 landing = 25 boxes', () => {
    const boxes = stairSteps({ x: 0, y: 0, z: 0 }, { x: 0, y: 3.5, z: 0 });
    expect(boxes).toHaveLength(25);
    // every box has finite dims and positions
    for (const b of boxes) {
      expect(Number.isFinite(b.w + b.h + b.d + b.x + b.y + b.z)).toBe(true);
    }
  });
  it('orders treads upward (last tread above first)', () => {
    const boxes = stairSteps({ x: 0, y: 0, z: 0 }, { x: 0, y: 3.5, z: 0 });
    const treads = boxes.slice(0, 24).filter((_, i) => i % 2 === 0);
    expect(treads[treads.length - 1].y).toBeGreaterThan(treads[0].y);
  });
});

describe('liftColumn', () => {
  it('returns null when served height collapses', () => {
    // h = (y1 + OVERRUN) - y0; force negative
    expect(liftColumn(0, 0, 0, -LIFT_OVERRUN - 1)).toBeNull();
  });
  it('builds 4 walls + 4 posts', () => {
    const col = liftColumn(5, 5, 0, 10);
    expect(col).not.toBeNull();
    expect(col!.walls).toHaveLength(4);
    expect(col!.posts).toHaveLength(4);
    expect(col!.h).toBeCloseTo(10 + LIFT_OVERRUN);
  });
});

describe('liftBuckets', () => {
  it('groups same-position lift cores and drops single-floor shafts', () => {
    const nodes: GraphNode[] = [
      node({ id: 'a', type: 'core', label: 'Lift 1', x: 0.5, y: 0.5, z: 0 }),
      node({ id: 'b', type: 'core', label: 'Lift 1', x: 0.5, y: 0.5, z: 3.5 }),
      // a lone lift core on one floor → excluded (needs >= 2)
      node({ id: 'c', type: 'core', label: 'Lift 2', x: 0.1, y: 0.1, z: 0 }),
      // not a lift
      node({ id: 'd', type: 'core', label: 'Stair', x: 0.5, y: 0.5, z: 0 }),
      // not a core
      node({ id: 'e', type: 'office', label: 'Lift-ish', x: 0.5, y: 0.5, z: 0 }),
    ];
    const buckets = liftBuckets(nodes);
    expect(buckets).toHaveLength(1);
    expect(buckets[0].y0).toBe(0);
    expect(buckets[0].y1).toBe(3.5);
  });
});

describe('wallSegTransform', () => {
  it('returns null for a zero-length segment', () => {
    expect(wallSegTransform([0.5, 0.5, 0.5, 0.5], 0, 0.07)).toBeNull();
  });
  it('computes length and rotation for a horizontal segment', () => {
    const t = wallSegTransform([0, 0, 1, 0], 0, 0.07)!;
    expect(t.len).toBeCloseTo(SCALE_XY);
    expect(t.rotY).toBeCloseTo(0);
  });
});

describe('partitionPlacement', () => {
  it('runs the wall along Z when the interface is vertical (dx dominant)', () => {
    const a = node({ x: 0, y: 0.5, w: 0.2, h: 0.4 });
    const b = node({ x: 0.5, y: 0.5, w: 0.2, h: 0.4 });
    expect(partitionPlacement(a, b).orientation).toBe('z');
  });
  it('runs the wall along X when the interface is horizontal (dz dominant)', () => {
    const a = node({ x: 0.5, y: 0, w: 0.4, h: 0.2 });
    const b = node({ x: 0.5, y: 0.5, w: 0.4, h: 0.2 });
    expect(partitionPlacement(a, b).orientation).toBe('x');
  });
  it('falls back to a MIN_FOOT-derived length when overlap is too small', () => {
    const a = node({ x: 0, y: 0, w: 0.1, h: 0.05 });
    const b = node({ x: 0.5, y: 0.9, w: 0.1, h: 0.05 });
    const p = partitionPlacement(a, b);
    expect(p.len).toBeGreaterThan(0);
  });
});

describe('doorGap', () => {
  it('keeps short walls solid (no door)', () => {
    const g = doorGap(1.5);
    expect(g.solid).toBe(true);
    expect(g.door).toBeNull();
    expect(g.segments).toHaveLength(1);
  });
  it('splits long walls into two segments + a door', () => {
    const g = doorGap(5);
    expect(g.solid).toBe(false);
    expect(g.segments).toHaveLength(2);
    expect(g.door).not.toBeNull();
    // segments are symmetric about centre
    expect(g.segments[0].offset).toBeCloseTo(-g.segments[1].offset);
  });
});
