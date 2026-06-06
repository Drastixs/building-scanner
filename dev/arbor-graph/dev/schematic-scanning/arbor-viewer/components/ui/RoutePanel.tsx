'use client';
// Route demo controls: pick Start + Goal, toggle constraints, pick a metric, and
// see the constrained shortest path re-solve live. Lists alternative routes (e.g.
// stairs vs lift) and pushes the selected path up to the viewer for rendering.
import { useEffect, useMemo, useState } from 'react';
import type { Building } from '@/lib/types';
import {
  DEFAULT_CONSTRAINTS,
  findRouteOptions,
  listSpaces,
  type RouteConstraints,
  type RouteMetric,
  type RouteOption,
} from '@/lib/pathfind';

interface Props {
  building: Building;
  onPath: (path: string[] | null) => void;
}

const METRICS: { key: RouteMetric; label: string }[] = [
  { key: 'shortest', label: 'Shortest' },
  { key: 'fewestDoors', label: 'Fewest doors' },
  { key: 'fewestFloors', label: 'Fewest floors' },
];

export function RoutePanel({ building, onPath }: Props) {
  const spaces = useMemo(() => listSpaces(building), [building]);
  const [start, setStart] = useState(spaces[0]?.id ?? '');
  const [goal, setGoal] = useState(spaces[spaces.length - 1]?.id ?? '');
  const [c, setC] = useState<RouteConstraints>(DEFAULT_CONSTRAINTS);
  const [sel, setSel] = useState(0);

  const options = useMemo<RouteOption[]>(
    () =>
      start && goal && start !== goal ? findRouteOptions(building, start, goal, c) : [],
    [building, start, goal, c],
  );

  const active = options[Math.min(sel, Math.max(0, options.length - 1))] ?? null;

  // Push the selected path to the 3D overlay whenever it changes.
  useEffect(() => {
    onPath(active ? active.path : null);
  }, [active, onPath]);

  const setFlag = (k: keyof RouteConstraints, v: boolean) =>
    setC((prev) => ({ ...prev, [k]: v }));

  return (
    <div id="route-panel">
      <h3>Route</h3>

      <label className="rp-field">
        <span>Start</span>
        <select value={start} onChange={(e) => setStart(e.target.value)}>
          {spaces.map((s) => (
            <option key={s.id} value={s.id}>
              {s.floor} · {s.label}
            </option>
          ))}
        </select>
      </label>

      <label className="rp-field">
        <span>Goal</span>
        <select value={goal} onChange={(e) => setGoal(e.target.value)}>
          {spaces.map((s) => (
            <option key={s.id} value={s.id}>
              {s.floor} · {s.label}
            </option>
          ))}
        </select>
      </label>

      <h3 className="sep">Constraints</h3>
      <label className="chk">
        <input
          type="checkbox"
          checked={c.noLift}
          onChange={(e) => setFlag('noLift', e.target.checked)}
        />{' '}
        No elevator
      </label>
      <label className="chk">
        <input
          type="checkbox"
          checked={c.stepFree}
          onChange={(e) => setFlag('stepFree', e.target.checked)}
        />{' '}
        Step-free (no stairs)
      </label>
      <label className="chk">
        <input
          type="checkbox"
          checked={c.avoidOffice}
          onChange={(e) => setFlag('avoidOffice', e.target.checked)}
        />{' '}
        Avoid office
      </label>

      <h3 className="sep">Optimise for</h3>
      <div id="rp-metrics">
        {METRICS.map((m) => (
          <button
            key={m.key}
            className={`floor-btn${c.metric === m.key ? ' active' : ''}`}
            onClick={() => setC((prev) => ({ ...prev, metric: m.key }))}
          >
            {m.label}
          </button>
        ))}
      </div>

      <h3 className="sep">
        {options.length ? `Routes (${options.length})` : 'Routes'}
      </h3>
      {options.length === 0 ? (
        <div className="rp-empty">
          {start === goal ? 'Pick two different rooms.' : 'No route — constraints too strict.'}
        </div>
      ) : (
        <div id="rp-routes">
          {options.map((o, i) => (
            <button
              key={o.label + i}
              className={`rp-route${i === sel ? ' active' : ''}`}
              onClick={() => setSel(i)}
            >
              <div className="rp-route-label">{o.label}</div>
              <div className="rp-route-stats">
                {o.stats.doors} doors · {o.stats.floorChanges} floor
                {o.stats.floorChanges === 1 ? '' : 's'}
                {o.stats.usesLift ? ' · lift' : ''}
                {o.stats.usesStair ? ' · stairs' : ''}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
