// Constrained shortest-path over the portal graph (building.json).
//
// The "best algorithm" here is plain weighted Dijkstra over a CONSTRAINT-FILTERED
// view of the graph — no exotic search needed. Every constraint is one of:
//   hard avoid  → drop the node from the traversal  (no lift, step-free, avoid office)
//   preference  → tweak edge weights                (shortest / fewest doors / fewest floors)
// Start and goal are never dropped, so an impossible filter yields null, not a crash.
//
// Substrate is building.json (spaces + door/stair/lift PORTALS as nodes), because
// rooms are real pass-throughs there — "avoid the office" can actually bend a route.
// The collapsed routes.json can't express that (rooms are leaves).
import type { Building, BuildingNode, EdgeType } from '@/lib/types';

export type RouteMetric = 'shortest' | 'fewestDoors' | 'fewestFloors';

export interface RouteConstraints {
  noLift: boolean;
  stepFree: boolean; // exclude stairs
  avoidOffice: boolean;
  avoidIds?: string[]; // arbitrary extra nodes to route around
  metric: RouteMetric;
}

export const DEFAULT_CONSTRAINTS: RouteConstraints = {
  noLift: false,
  stepFree: false,
  avoidOffice: false,
  metric: 'shortest',
};

export interface RouteStats {
  doors: number;
  floorChanges: number;
  usesLift: boolean;
  usesStair: boolean;
  floors: string[];
  cost: number;
}

export interface RouteOption {
  label: string; // e.g. "via STAIR-01", or "same floor"
  path: string[]; // ordered building-node ids
  stats: RouteStats;
}

export interface SpaceRef {
  id: string;
  label: string;
  floor: string;
  type: string;
}

interface Index {
  nodeById: Map<string, BuildingNode>;
  adj: Map<string, { to: string; type: EdgeType }[]>;
}

function buildIndex(building: Building): Index {
  const nodeById = new Map<string, BuildingNode>();
  for (const n of building.nodes) nodeById.set(n.id, n);
  const adj = new Map<string, { to: string; type: EdgeType }[]>();
  const push = (a: string, b: string, type: EdgeType) => {
    if (!adj.has(a)) adj.set(a, []);
    adj.get(a)!.push({ to: b, type });
  };
  for (const e of building.edges) {
    push(e.source, e.target, e.type);
    push(e.target, e.source, e.type);
  }
  return { nodeById, adj };
}

/** Selectable rooms for the Start / Goal pickers, grouped readably by floor. */
export function listSpaces(building: Building): SpaceRef[] {
  return building.nodes
    .filter((n) => n.kind === 'space')
    .map((n) => ({
      id: n.id,
      label: n.label ?? n.id,
      floor: String(n.floor),
      type: n.type ?? 'unknown',
    }))
    .sort((a, b) => a.floor.localeCompare(b.floor) || a.label.localeCompare(b.label));
}

function isBlocked(n: BuildingNode, c: RouteConstraints): boolean {
  if (n.kind === 'portal') {
    if (c.noLift && n.portal_kind === 'lift') return true;
    if (c.stepFree && n.portal_kind === 'stair') return true;
  }
  if (n.kind === 'space' && c.avoidOffice && n.type === 'office') return true;
  if (c.avoidIds?.includes(n.id)) return true;
  return false;
}

// A floor change (inter edge) costs more than a door, so the optimiser doesn't
// hop floors gratuitously. The metric just re-weights that vertical cost.
function edgeCost(type: EdgeType, c: RouteConstraints): number {
  if (type === 'inter') {
    if (c.metric === 'fewestDoors') return 0.25; // floors are cheap → minimise doors
    if (c.metric === 'fewestFloors') return 25; // floors are dear → minimise changes
    return 4; // balanced
  }
  return 1; // intra: space↔portal (a door crossing is space-portal-space = 2)
}

function dijkstra(
  index: Index,
  start: string,
  goal: string,
  c: RouteConstraints,
  banned?: ReadonlySet<string>,
): string[] | null {
  const { nodeById, adj } = index;
  if (!nodeById.has(start) || !nodeById.has(goal)) return null;

  const allow = (id: string): boolean => {
    if (id === start || id === goal) return true;
    if (banned?.has(id)) return false;
    const n = nodeById.get(id);
    return n ? !isBlocked(n, c) : false;
  };

  const dist = new Map<string, number>([[start, 0]]);
  const prev = new Map<string, string>();
  const done = new Set<string>();

  // Graph is tiny (tens of nodes) → linear-scan min is fine; no heap needed.
  for (;;) {
    let u: string | null = null;
    let best = Infinity;
    for (const [id, d] of dist) {
      if (!done.has(id) && d < best) {
        best = d;
        u = id;
      }
    }
    if (u === null || u === goal) break;
    done.add(u);
    for (const { to, type } of adj.get(u) ?? []) {
      if (done.has(to) || !allow(to)) continue;
      const nd = best + edgeCost(type, c);
      if (nd < (dist.get(to) ?? Infinity)) {
        dist.set(to, nd);
        prev.set(to, u);
      }
    }
  }

  if (!dist.has(goal)) return null;
  const path: string[] = [];
  let cur: string | undefined = goal;
  while (cur !== undefined) {
    path.unshift(cur);
    cur = prev.get(cur);
  }
  return path[0] === start ? path : null;
}

export function routeStats(
  index: Index,
  path: string[],
  c: RouteConstraints,
): RouteStats {
  const { nodeById } = index;
  let doors = 0;
  let floorChanges = 0;
  let cost = 0;
  let usesLift = false;
  let usesStair = false;
  const floors = new Set<string>();

  for (let i = 0; i < path.length; i++) {
    const n = nodeById.get(path[i])!;
    floors.add(String(n.floor));
    if (n.kind === 'portal') {
      if (n.portal_kind === 'door' || n.portal_kind === 'opening') doors++;
      if (n.portal_kind === 'lift') usesLift = true;
      if (n.portal_kind === 'stair') usesStair = true;
    }
    if (i > 0) {
      const prev = nodeById.get(path[i - 1])!;
      const type: EdgeType =
        String(prev.floor) !== String(n.floor) ? 'inter' : 'intra';
      if (type === 'inter') floorChanges++;
      cost += edgeCost(type, c);
    }
  }
  return { doors, floorChanges, usesLift, usesStair, floors: [...floors], cost };
}

// Vertical cores (stair/lift shafts) a path rides — used to label routes and to
// generate alternatives by banning one shaft at a time.
function verticalCores(index: Index, path: string[]): string[] {
  const s = new Set<string>();
  for (const id of path) {
    const n = index.nodeById.get(id)!;
    if ((n.portal_kind === 'stair' || n.portal_kind === 'lift') && n.core_id) {
      s.add(n.core_id);
    }
  }
  return [...s];
}

function labelFor(index: Index, path: string[]): string {
  const cores = verticalCores(index, path);
  return cores.length ? `via ${cores.join(' + ')}` : 'same floor';
}

/**
 * Best constrained route + up to k-1 alternatives. Alternatives are produced by
 * banning each vertical shaft the primary route uses and re-solving — which yields
 * naturally meaningful options ("take the stairs instead of the lift") for a demo.
 */
export function findRouteOptions(
  building: Building,
  start: string,
  goal: string,
  c: RouteConstraints,
  k = 3,
): RouteOption[] {
  const index = buildIndex(building);
  const primary = dijkstra(index, start, goal, c);
  if (!primary) return [];

  const options: RouteOption[] = [
    { label: labelFor(index, primary), path: primary, stats: routeStats(index, primary, c) },
  ];
  const seen = new Set([primary.join('>')]);

  for (const core of verticalCores(index, primary)) {
    if (options.length >= k) break;
    const banned = new Set<string>();
    for (const n of building.nodes) if (n.core_id === core) banned.add(n.id);
    const alt = dijkstra(index, start, goal, c, banned);
    if (alt && !seen.has(alt.join('>'))) {
      seen.add(alt.join('>'));
      options.push({ label: labelFor(index, alt), path: alt, stats: routeStats(index, alt, c) });
    }
  }
  return options;
}
