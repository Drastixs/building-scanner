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
  DOOR_PANEL_COLOR,
  PARTITION_COLOR,
} from '@/lib/scene/constants';
import { partitionPlacement, doorGap } from '@/lib/scene/geometry';

// A door is drawn wherever two rooms on the same floor share a wall long enough for
// an opening (doorGap returns a non-solid split). The opening is the SAME gap the
// adjacency partitions cut, so the leaf always lands in a real doorway. We render it
// as its own layer (not inside Partitions) so doors also appear over the vector walls,
// which carry no opening data of their own.
//
// The leaf is a framed, slightly-hollow panel (stiles + rails + a recessed centre
// panel) rather than a solid slab, and the opening gets a deep jamb lining + sill so
// it reads as a real walk-through doorway, not just a hole.
const SWING = THREE.MathUtils.degToRad(34); // leaf left ajar, like a plan's door-swing arc
const LEAF_T = WALL_T * 1.6;
const FRAME_RAIL = 0.13; // stile / rail width on the leaf
const PANEL_T = LEAF_T * 0.4; // recessed inner panel → hollow look
const JAMB_T = WALL_T * 1.9;
const LINING_D = WALL_T * 3.0; // jamb/head lining depth — gives the opening a reveal
const SILL_H = 0.04; // threshold sill
const HEADER_H = Math.max(PARTITION_H - DOOR_H, 0.12); // lintel above the opening

// A framed, slightly-hollow door leaf in a local frame: hinge at local origin, the
// leaf extends +X from 0..w and 0..DOOR_H in Y, thin in Z. Two stiles, two rails and
// a recessed centre panel read as a real paneled door rather than a flat block.
function DoorLeaf({
  w,
  leafMat,
  panelMat,
}: {
  w: number;
  leafMat: THREE.Material;
  panelMat: THREE.Material;
}) {
  const fr = Math.min(FRAME_RAIL, w * 0.28);
  const innerW = Math.max(w - 2 * fr, 0.02);
  const innerH = Math.max(DOOR_H - 2 * fr, 0.02);
  return (
    <>
      {/* Stiles (left/right verticals) */}
      <mesh position={[fr / 2, DOOR_H / 2, 0]} material={leafMat}>
        <boxGeometry args={[fr, DOOR_H, LEAF_T]} />
      </mesh>
      <mesh position={[w - fr / 2, DOOR_H / 2, 0]} material={leafMat}>
        <boxGeometry args={[fr, DOOR_H, LEAF_T]} />
      </mesh>
      {/* Rails (top/bottom horizontals) */}
      <mesh position={[w / 2, fr / 2, 0]} material={leafMat}>
        <boxGeometry args={[innerW, fr, LEAF_T]} />
      </mesh>
      <mesh position={[w / 2, DOOR_H - fr / 2, 0]} material={leafMat}>
        <boxGeometry args={[innerW, fr, LEAF_T]} />
      </mesh>
      {/* Recessed centre panel — thinner, darker, reads as hollow */}
      <mesh position={[w / 2, DOOR_H / 2, 0]} material={panelMat}>
        <boxGeometry args={[innerW, innerH, PANEL_T]} />
      </mesh>
      {/* Handle */}
      <mesh position={[w - fr - 0.06, DOOR_H * 0.46, LEAF_T * 0.7]} material={leafMat}>
        <boxGeometry args={[0.05, 0.12, 0.05]} />
      </mesh>
    </>
  );
}

export function Doors({ graph, state, hidden, onHover, onHide }: GraphProps) {
  const leafMat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: DOOR_LEAF_COLOR,
        emissive: new THREE.Color(DOOR_LEAF_COLOR),
        emissiveIntensity: 0.1,
        roughness: 0.6,
        metalness: 0.05,
      }),
    [],
  );
  const panelMat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: DOOR_PANEL_COLOR,
        roughness: 0.75,
        metalness: 0.02,
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
        // x-orientation: wall runs along X, hinge at left jamb, no base rotation.
        // z-orientation: wall runs along Z → rotate the leaf frame -90° so its width
        // maps onto world Z, hinge at the -Z jamb.
        const isX = d.orientation === 'x';
        const baseRot = isX ? 0 : -Math.PI / 2;
        const hingeX = isX ? d.xc - half : d.xc;
        const hingeZ = isX ? d.zc : d.zc - half;
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
            {isX ? (
              <>
                {/* Lintel bridging the opening up to ceiling height */}
                <mesh position={[d.xc, headerY, d.zc]} material={headerMat}>
                  <boxGeometry args={[d.doorW, HEADER_H, WALL_T]} />
                </mesh>
                {/* Head lining under the lintel (reveal) */}
                <mesh position={[d.xc, d.baseY + DOOR_H + 0.02, d.zc]} material={frameMat}>
                  <boxGeometry args={[d.doorW + JAMB_T, 0.05, LINING_D]} />
                </mesh>
                {/* Jamb linings at each side — deep, so the opening has a reveal */}
                <mesh position={[d.xc - half, jambY, d.zc]} material={frameMat}>
                  <boxGeometry args={[JAMB_T, DOOR_H, LINING_D]} />
                </mesh>
                <mesh position={[d.xc + half, jambY, d.zc]} material={frameMat}>
                  <boxGeometry args={[JAMB_T, DOOR_H, LINING_D]} />
                </mesh>
                {/* Threshold sill */}
                <mesh position={[d.xc, d.baseY + SILL_H / 2, d.zc]} material={frameMat}>
                  <boxGeometry args={[d.doorW, SILL_H, LINING_D]} />
                </mesh>
              </>
            ) : (
              <>
                <mesh position={[d.xc, headerY, d.zc]} material={headerMat}>
                  <boxGeometry args={[WALL_T, HEADER_H, d.doorW]} />
                </mesh>
                <mesh position={[d.xc, d.baseY + DOOR_H + 0.02, d.zc]} material={frameMat}>
                  <boxGeometry args={[LINING_D, 0.05, d.doorW + JAMB_T]} />
                </mesh>
                <mesh position={[d.xc, jambY, d.zc - half]} material={frameMat}>
                  <boxGeometry args={[LINING_D, DOOR_H, JAMB_T]} />
                </mesh>
                <mesh position={[d.xc, jambY, d.zc + half]} material={frameMat}>
                  <boxGeometry args={[LINING_D, DOOR_H, JAMB_T]} />
                </mesh>
                <mesh position={[d.xc, d.baseY + SILL_H / 2, d.zc]} material={frameMat}>
                  <boxGeometry args={[LINING_D, SILL_H, d.doorW]} />
                </mesh>
              </>
            )}
            {/* Ajar hollow leaf, hinged at the jamb and swung into the room */}
            <group
              position={[hingeX, d.baseY, hingeZ]}
              rotation={[0, baseRot - SWING, 0]}
            >
              <DoorLeaf w={d.doorW} leafMat={leafMat} panelMat={panelMat} />
            </group>
          </SceneMesh>
        );
      })}
    </>
  );
}
