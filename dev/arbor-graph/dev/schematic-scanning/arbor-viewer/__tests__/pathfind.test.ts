import { describe, it, expect } from 'vitest';
import {
  DEFAULT_CONSTRAINTS,
  findRouteOptions,
  listSpaces,
  type RouteConstraints,
} from '@/lib/pathfind';
import type { Building } from '@/lib/types';

// Minimal two-floor building: rooms A0/B0 on floor 0, A1 on floor 1.
// A0 -door- B0 ; both A0/B0 reach a STAIR and a LIFT shaft up to A1.
const building: Building = {
  floors: [],
  nodes: [
    { id: 'A0', kind: 'space', type: 'office', floor: '0', x: 0.1, y: 0.1, z: 0 },
    { id: 'B0', kind: 'space', type: 'amenity', floor: '0', x: 0.3, y: 0.1, z: 0 },
    { id: 'A1', kind: 'space', type: 'amenity', floor: '1', x: 0.1, y: 0.1, z: 3.5 },
    { id: 'D0', kind: 'portal', portal_kind: 'door', floor: '0', x: 0.2, y: 0.1, z: 0 },
    { id: 'S0', kind: 'portal', portal_kind: 'stair', floor: '0', x: 0.3, y: 0.3, z: 0, core_id: 'STAIR-1' },
    { id: 'S1', kind: 'portal', portal_kind: 'stair', floor: '1', x: 0.3, y: 0.3, z: 3.5, core_id: 'STAIR-1' },
    { id: 'L0', kind: 'portal', portal_kind: 'lift', floor: '0', x: 0.1, y: 0.3, z: 0, core_id: 'LIFT-1' },
    { id: 'L1', kind: 'portal', portal_kind: 'lift', floor: '1', x: 0.1, y: 0.3, z: 3.5, core_id: 'LIFT-1' },
  ],
  edges: [
    { source: 'A0', target: 'D0', type: 'intra' },
    { source: 'D0', target: 'B0', type: 'intra' },
    { source: 'B0', target: 'S0', type: 'intra' },
    { source: 'A0', target: 'L0', type: 'intra' },
    { source: 'S0', target: 'S1', type: 'inter' },
    { source: 'L0', target: 'L1', type: 'inter' },
    { source: 'S1', target: 'A1', type: 'intra' },
    { source: 'L1', target: 'A1', type: 'intra' },
  ],
};

const c = (over: Partial<RouteConstraints> = {}): RouteConstraints => ({
  ...DEFAULT_CONSTRAINTS,
  ...over,
});

describe('listSpaces', () => {
  it('returns only spaces, sorted by floor then label', () => {
    const s = listSpaces(building);
    expect(s.map((x) => x.id).sort()).toEqual(['A0', 'A1', 'B0']);
  });
});

describe('findRouteOptions', () => {
  it('finds a route across floors and reports floor changes', () => {
    const [best] = findRouteOptions(building, 'A0', 'A1', c());
    expect(best.path[0]).toBe('A0');
    expect(best.path.at(-1)).toBe('A1');
    expect(best.stats.floorChanges).toBe(1);
  });

  it('offers lift and stair as alternatives', () => {
    const opts = findRouteOptions(building, 'B0', 'A1', c());
    const usesLift = opts.some((o) => o.stats.usesLift);
    const usesStair = opts.some((o) => o.stats.usesStair);
    expect(usesLift && usesStair).toBe(true);
  });

  it('no elevator → never routes through a lift', () => {
    const opts = findRouteOptions(building, 'A0', 'A1', c({ noLift: true }));
    expect(opts.length).toBeGreaterThan(0);
    expect(opts.every((o) => !o.stats.usesLift)).toBe(true);
  });

  it('step-free → never routes through stairs', () => {
    const opts = findRouteOptions(building, 'A0', 'A1', c({ stepFree: true }));
    expect(opts.every((o) => !o.stats.usesStair)).toBe(true);
  });

  it('avoid office routes around an office that is a pass-through', () => {
    // Goal B0 is reachable from A1 via stairs without entering office A0.
    const opts = findRouteOptions(building, 'A1', 'B0', c({ avoidOffice: true }));
    expect(opts.length).toBeGreaterThan(0);
    expect(opts[0].path.includes('A0')).toBe(false);
  });

  it('returns nothing when both vertical cores are banned', () => {
    const opts = findRouteOptions(
      building,
      'A0',
      'A1',
      c({ noLift: true, stepFree: true }),
    );
    expect(opts).toEqual([]);
  });
});
