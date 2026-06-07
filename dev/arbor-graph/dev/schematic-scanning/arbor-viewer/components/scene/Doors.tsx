'use client';
import { useMemo } from 'react';
import * as THREE from 'three';
import type { GraphNode } from '@/lib/types';
import type { GraphProps } from '@/components/contracts';
import { SceneMesh } from '@/components/SceneMesh';
import {
  PARTITION_H,
  WALL_T,
  DOOR_H,
  DOOR_LEAF_COLOR,
  DOOR_FRAME_COLOR,
  PARTITION_COLOR,
} from '@/lib/scene/constants';
import { partitionPlacement, doorGap } from '@/lib/scene/geometry';

// A door is drawn wherever two rooms on the same floor share a wall long enough for
// an opening (doorGap returns a non-solid split). The opening is the SAME gap the
// adjacency partitions cut, so the leaf always lands in a real doorway. We render it
// as its own layer (not inside Partitions) so doors also appear over the vector walls,
// which carry no opening data of their own.
const SWING = THREE.MathUtils.degToRad(34); // leaf left ajar, like a plan's door-swing arc
const LEAF_T = WALL_T * 1.6;
const JAMB_T = WALL_T * 1.9;
const HEADER_H = Math.max(PARTITION_H - DOOR_H, 0.12); // lintel above the opening

export function Doors({ graph, state, hidden, onHover, onHide }: GraphProps) {
  const leafMat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: DOOR_LEAF_COLOR,
        emissive: new THREE.Color(DOOR_LEAF_COLOR),
        emissiveIntensity: 0.12,
        roughness: 0.6,
        metalness: 0.05,
        transparent: true,
        opacity: 0.95,
      }),
    [],
  );
  const frameMat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: DOOR_FRAME_COLOR,
        roughness: 0.7,
      }),
    [],
  );
  const headerMat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: PARTITION_COLOR,
        transparent: true,
        opacity: 0.5,
        roughness: 0.7,
        side: THREE.DoubleSide,
      }),
    [],
  );

  const nodeById = useMemo(() => {
    const map = new Map<string, GraphNode>();
    for (const node of graph.nodes) map.set(node.id, node);
    return map;
  }, [graph.nodes]);

  const doors = useMemo(() => {
    const out: {
      id: string;
      floor: string;
      label: string;
      orientation: 'x' | 'z';
      xc: number;
      zc: number;
      baseY: number;
      doorW: number;
    }[] = [];
    graph.edges.forEach((e, index) => {
      if (e.type !== 'intra') return;
      const a = nodeById.get(e.source);
      const b = nodeById.get(e.target);
      if (!a || !b || String(a.floor) !== String(b.floor)) return;
      const p = partitionPlacement(a, b);
      const g = doorGap(p.len);
      if (g.solid || !g.door) return; // wall too short for an opening
      out.push({
        id: `door-${index}`,
        floor: String(a.floor),
        label: `Door · ${a.label} ↔ ${b.label}`,
        orientation: p.orientation,
        xc: p.xc,
        zc: p.zc,
        baseY: p.baseY,
        doorW: g.door.width,
      });
    });
    return out;
  }, [graph.edges, nodeById]);

  return (
    <>
      {doors.map((d) => {
        const half = d.doorW / 2;
        const headerY = d.baseY + DOOR_H + HEADER_H / 2;
        const jambY = d.baseY + DOOR_H / 2;
        const meta = {
          id: d.id,
          kind: 'door' as const,
          isPartition: true, // shares the Partitions toggle
          floorLevel: d.floor,
          label: d.label,
        };

        return (
          <SceneMesh
            key={d.id}
            meta={meta}
            state={state}
            hidden={hidden}
            onHover={onHover}
            onHide={onHide}
            pickable
          >
            {d.orientation === 'x' ? (
              <>
                {/* Lintel bridging the opening up to ceiling height */}
                <mesh position={[d.xc, headerY, d.zc]} material={headerMat}>
                  <boxGeometry args={[d.doorW, HEADER_H, WALL_T]} />
                </mesh>
                {/* Jambs at each side of the opening */}
                <mesh position={[d.xc - half, jambY, d.zc]} material={frameMat}>
                  <boxGeometry args={[JAMB_T, DOOR_H, WALL_T * 1.2]} />
                </mesh>
                <mesh position={[d.xc + half, jambY, d.zc]} material={frameMat}>
                  <boxGeometry args={[JAMB_T, DOOR_H, WALL_T * 1.2]} />
                </mesh>
                {/* Leaf, hinged at the left jamb and swung into the room */}
                <group position={[d.xc - half, d.baseY, d.zc]} rotation={[0, -SWING, 0]}>
                  <mesh position={[half, DOOR_H / 2, 0]} material={leafMat}>
                    <boxGeometry args={[d.doorW, DOOR_H, LEAF_T]} />
                  </mesh>
                </group>
              </>
            ) : (
              <>
                <mesh position={[d.xc, headerY, d.zc]} material={headerMat}>
                  <boxGeometry args={[WALL_T, HEADER_H, d.doorW]} />
                </mesh>
                <mesh position={[d.xc, jambY, d.zc - half]} material={frameMat}>
                  <boxGeometry args={[WALL_T * 1.2, DOOR_H, JAMB_T]} />
                </mesh>
                <mesh position={[d.xc, jambY, d.zc + half]} material={frameMat}>
                  <boxGeometry args={[WALL_T * 1.2, DOOR_H, JAMB_T]} />
                </mesh>
                <group position={[d.xc, d.baseY, d.zc - half]} rotation={[0, SWING, 0]}>
                  <mesh position={[0, DOOR_H / 2, half]} material={leafMat}>
                    <boxGeometry args={[LEAF_T, DOOR_H, d.doorW]} />
                  </mesh>
                </group>
              </>
            )}
          </SceneMesh>
        );
      })}
    </>
  );
}
