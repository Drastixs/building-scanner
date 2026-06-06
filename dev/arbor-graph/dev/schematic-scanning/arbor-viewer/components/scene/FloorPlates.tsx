'use client';
import { useMemo } from 'react';
import * as THREE from 'three';
import { Text } from '@react-three/drei';
import type { GraphProps } from '@/components/contracts';
import type { UnitMeta } from '@/lib/types';
import { SceneMesh } from '@/components/SceneMesh';
import { FLOOR_W, PLATE_H, SCALE_Z } from '@/lib/scene/constants';

// Build the shared box geometry once at module level so it is never recreated.
const plateBoxGeom = new THREE.BoxGeometry(FLOOR_W, PLATE_H, FLOOR_W);

export function FloorPlates({
  graph,
  state,
  hidden,
  onHover,
  onHide,
}: GraphProps) {
  // Memoise the per-floor meta objects so identity is stable across re-renders.
  const floorMetas = useMemo<UnitMeta[]>(
    () =>
      graph.floors.map((fl) => ({
        id: `plate-${fl.level}`,
        kind: 'plate',
        floorLevel: String(fl.level),
        label: fl.label,
      })),
    [graph.floors],
  );

  return (
    <>
      {graph.floors.map((fl, i) => {
        const y = fl.z * SCALE_Z;
        const px = FLOOR_W / 2;
        const py = y - PLATE_H;
        const pz = FLOOR_W / 2;
        const meta = floorMetas[i];

        return (
          <group key={fl.level}>
            {/* Reference plate (hideable via SceneMesh) */}
            <SceneMesh
              meta={meta}
              state={state}
              hidden={hidden}
              onHover={onHover}
              onHide={onHide}
              pickable
            >
              {/* Filled slab */}
              <mesh position={[px, py, pz]}>
                <boxGeometry args={[FLOOR_W, PLATE_H, FLOOR_W]} />
                <meshStandardMaterial
                  color={0x1a1a2e}
                  transparent
                  opacity={0.06}
                  roughness={0.9}
                />
              </mesh>

              {/* Edge outline */}
              <lineSegments position={[px, py, pz]}>
                <edgesGeometry args={[plateBoxGeom]} />
                <lineBasicMaterial
                  color={0x33334d}
                  transparent
                  opacity={0.35}
                />
              </lineSegments>
            </SceneMesh>

            {/* Floor label — always visible, not floor-filtered */}
            <Text
              position={[-1.5, y, FLOOR_W + 0.5]}
              fontSize={0.55}
              color="#666677"
              anchorX="left"
              anchorY="middle"
              renderOrder={1}
              depthOffset={-1}
            >
              {fl.label}
            </Text>
          </group>
        );
      })}
    </>
  );
}
