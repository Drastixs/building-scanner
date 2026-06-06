'use client';
// Draws the active route through the building as a thin green guide line along the
// path's node positions, with fixed start/goal markers.
//
// Always visible by design: it's an overlay, not a hideable unit, so floor isolation
// never hides it. depthTest is also disabled (RENDER_ORDER on top) so the line draws
// THROUGH hidden floors and occluding walls — it keeps guiding even when the floor it
// runs along isn't rendered.
import { useMemo } from 'react';
import { Line } from '@react-three/drei';
import * as THREE from 'three';
import type { Building } from '@/lib/types';
import { SCALE_XY, SCALE_Z } from '@/lib/scene/constants';

const PATH_COLOR = '#22ff88'; // green guide line
const START_COLOR = '#00ff9c';
const GOAL_COLOR = '#ff5a5a';
const Y_LIFT = 0.6; // float the line above the floor slabs
const RENDER_ORDER = 999; // draw last → on top of everything

interface Props {
  building: Building;
  path: string[];
}

export function PathOverlay({ building, path }: Props) {
  const points = useMemo(() => {
    const byId = new Map(building.nodes.map((n) => [n.id, n] as const));
    const pts: THREE.Vector3[] = [];
    for (const id of path) {
      const n = byId.get(id);
      if (!n) continue;
      pts.push(
        new THREE.Vector3(n.x * SCALE_XY, (n.z || 0) * SCALE_Z + Y_LIFT, n.y * SCALE_XY),
      );
    }
    return pts;
  }, [building, path]);

  if (points.length < 2) return null;
  const start = points[0];
  const goal = points[points.length - 1];

  return (
    <group>
      <Line
        points={points}
        color={PATH_COLOR}
        lineWidth={1}
        transparent
        opacity={0.95}
        depthTest={false}
        renderOrder={RENDER_ORDER}
      />

      <mesh position={start} renderOrder={RENDER_ORDER}>
        <sphereGeometry args={[0.55, 16, 16]} />
        <meshStandardMaterial
          color={START_COLOR}
          emissive={START_COLOR}
          emissiveIntensity={0.9}
          depthTest={false}
          transparent
        />
      </mesh>
      <mesh position={goal} renderOrder={RENDER_ORDER}>
        <sphereGeometry args={[0.55, 16, 16]} />
        <meshStandardMaterial
          color={GOAL_COLOR}
          emissive={GOAL_COLOR}
          emissiveIntensity={0.9}
          depthTest={false}
          transparent
        />
      </mesh>
    </group>
  );
}
