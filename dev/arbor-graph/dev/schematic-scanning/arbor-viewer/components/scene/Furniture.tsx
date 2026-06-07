'use client';
import { useMemo } from 'react';
import * as THREE from 'three';
import type { GraphNode } from '@/lib/types';
import type { GraphProps } from '@/components/contracts';
import { SceneMesh } from '@/components/SceneMesh';
import {
  SCALE_XY,
  SCALE_Z,
  SLAB_H,
  MIN_FOOT,
  FURN_WOOD_COLOR,
  FURN_FABRIC_COLOR,
  FURN_METAL_COLOR,
  FURN_SCREEN_COLOR,
} from '@/lib/scene/constants';
import { worldXZ } from '@/lib/scene/geometry';

// "Other items should have a 3D model where possible." Each room gets simple,
// representative furniture keyed off its label so an office reads as desks, a
// meeting room as a table + chairs, a store as shelving, plant/comms as equipment
// racks, etc. WC rooms are handled by Toilets.tsx and skipped here.
//
// Models are emitted in a LOCAL footprint frame centred on the room (x∈[-w/2,w/2],
// z∈[-d/2,d/2], y = box-centre height above the floor) and then translated to world.

type MatKey = 'wood' | 'fabric' | 'metal' | 'screen';
interface Item {
  m: MatKey;
  s: [number, number, number]; // size
  p: [number, number, number]; // centre (y above floor)
}

const WC_RE = /\b(wc|toilet|lavatory|washroom|restroom|bathroom|sanitary)\b/i;

type Kind =
  | 'office'
  | 'meeting'
  | 'reception'
  | 'breakout'
  | 'store'
  | 'changing'
  | 'vending'
  | 'equipment'
  | 'retail'
  | 'bench'
  | null;

function classify(node: GraphNode): Kind {
  const t = (node.label || '').toLowerCase();
  if (WC_RE.test(t)) return null; // Toilets.tsx owns these
  if (/\bmeeting\b|\bboardroom\b/.test(t)) return 'meeting';
  if (/reception|event space|lobby/.test(t)) return 'reception';
  if (/breakout|lounge/.test(t)) return 'breakout';
  if (/changing|drying|locker/.test(t)) return 'changing';
  if (/vending/.test(t)) return 'vending';
  if (/retail|shop/.test(t)) return 'retail';
  if (/store|storage|cycle|cleaner/.test(t)) return 'store';
  if (/comms|server|power|plumbing|plant|switch|comm\b|data/.test(t)) return 'equipment';
  if (/injury|bench|wash room|lab/.test(t)) return 'bench';
  if (node.type === 'office' || /office|open plan|workplace/.test(t)) return 'office';
  return null;
}

const clamp = (v: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, v));

// A desk + chair pair centred at (x,z).
function desk(x: number, z: number): Item[] {
  return [
    { m: 'wood', s: [1.3, 0.05, 0.65], p: [x, 0.72, z] },
    { m: 'metal', s: [0.06, 0.72, 0.06], p: [x - 0.55, 0.36, z] },
    { m: 'metal', s: [0.06, 0.72, 0.06], p: [x + 0.55, 0.36, z] },
    { m: 'fabric', s: [0.45, 0.05, 0.45], p: [x, 0.45, z + 0.5] }, // seat
    { m: 'fabric', s: [0.45, 0.5, 0.05], p: [x, 0.68, z + 0.72] }, // back
  ];
}

function buildModels(kind: Kind, w: number, d: number): Item[] {
  const items: Item[] = [];
  const mx = w / 2 - 0.4; // usable half-extents (leave a margin)
  const mz = d / 2 - 0.4;
  if (mx <= 0.2 || mz <= 0.2) return items;

  switch (kind) {
    case 'office': {
      const cols = clamp(Math.floor(w / 1.7), 1, 4);
      const rows = clamp(Math.floor(d / 1.8), 1, 3);
      const dxStep = (2 * mx) / cols;
      const dzStep = (2 * mz) / rows;
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const x = -mx + dxStep * (c + 0.5);
          const z = -mz + dzStep * (r + 0.5);
          items.push(...desk(x, z));
        }
      }
      break;
    }
    case 'meeting': {
      const tw = clamp(w * 0.45, 1.0, 2.6);
      const td = clamp(d * 0.4, 0.8, 1.4);
      items.push({ m: 'wood', s: [tw, 0.05, td], p: [0, 0.74, 0] });
      items.push({ m: 'metal', s: [tw * 0.5, 0.74, td * 0.4], p: [0, 0.37, 0] });
      const seats = 6;
      for (let i = 0; i < seats; i++) {
        const side = i < seats / 2 ? -1 : 1;
        const k = i % (seats / 2);
        const x = -tw / 2 + (tw / (seats / 2)) * (k + 0.5);
        const z = side * (td / 2 + 0.35);
        items.push({ m: 'fabric', s: [0.45, 0.05, 0.45], p: [x, 0.45, z] });
        items.push({ m: 'fabric', s: [0.45, 0.45, 0.05], p: [x, 0.68, z + side * 0.22] });
      }
      break;
    }
    case 'reception': {
      // L-shaped counter near the front-left + a couple of waiting seats.
      items.push({ m: 'wood', s: [clamp(w * 0.5, 1.2, 2.8), 1.1, 0.55], p: [-mx * 0.2, 0.55, -mz * 0.5] });
      items.push({ m: 'wood', s: [0.55, 1.1, clamp(d * 0.3, 0.8, 1.4)], p: [-mx * 0.2 - clamp(w * 0.25, 0.6, 1.4), 0.55, -mz * 0.2] });
      for (let i = 0; i < 2; i++) {
        const x = mx * (0.2 + i * 0.5);
        items.push({ m: 'fabric', s: [0.6, 0.4, 0.6], p: [x, 0.2, mz * 0.4] });
        items.push({ m: 'fabric', s: [0.6, 0.4, 0.12], p: [x, 0.55, mz * 0.4 + 0.24] });
      }
      break;
    }
    case 'breakout': {
      items.push({ m: 'fabric', s: [clamp(w * 0.5, 1.0, 2.2), 0.45, 0.7], p: [-mx * 0.2, 0.22, -mz * 0.3] });
      items.push({ m: 'fabric', s: [clamp(w * 0.5, 1.0, 2.2), 0.4, 0.15], p: [-mx * 0.2, 0.55, -mz * 0.3 - 0.42] });
      items.push({ m: 'wood', s: [0.7, 0.4, 0.5], p: [-mx * 0.2, 0.2, mz * 0.1] }); // coffee table
      break;
    }
    case 'store':
    case 'retail': {
      // Shelving banks against the back wall (stacked thin slabs).
      const banks = clamp(Math.floor(w / 1.2), 1, 4);
      const bw = (2 * mx) / banks - 0.1;
      for (let b = 0; b < banks; b++) {
        const x = -mx + ((2 * mx) / banks) * (b + 0.5);
        for (let lvl = 0; lvl < 3; lvl++) {
          items.push({ m: 'metal', s: [bw, 0.04, Math.min(0.5, d * 0.4)], p: [x, 0.5 + lvl * 0.55, -mz + 0.3] });
        }
        items.push({ m: 'metal', s: [0.05, 1.7, Math.min(0.5, d * 0.4)], p: [x - bw / 2, 0.85, -mz + 0.3] });
        items.push({ m: 'metal', s: [0.05, 1.7, Math.min(0.5, d * 0.4)], p: [x + bw / 2, 0.85, -mz + 0.3] });
      }
      if (kind === 'retail') {
        items.push({ m: 'wood', s: [clamp(w * 0.4, 1.0, 2.2), 1.0, 0.5], p: [0, 0.5, mz * 0.5] });
      }
      break;
    }
    case 'changing': {
      // Locker bank along the back + a bench down the middle.
      items.push({ m: 'metal', s: [clamp(w * 0.8, 1.0, 3.0), 1.8, 0.4], p: [0, 0.9, -mz + 0.25] });
      items.push({ m: 'wood', s: [clamp(w * 0.6, 0.8, 2.4), 0.42, 0.35], p: [0, 0.21, 0] });
      items.push({ m: 'metal', s: [0.05, 0.42, 0.35], p: [-clamp(w * 0.28, 0.4, 1.1), 0.21, 0] });
      items.push({ m: 'metal', s: [0.05, 0.42, 0.35], p: [clamp(w * 0.28, 0.4, 1.1), 0.21, 0] });
      break;
    }
    case 'vending': {
      const n = clamp(Math.floor(w / 0.9), 1, 3);
      for (let i = 0; i < n; i++) {
        const x = -mx + ((2 * mx) / n) * (i + 0.5);
        items.push({ m: 'metal', s: [0.7, 1.8, 0.6], p: [x, 0.9, -mz + 0.35] });
        items.push({ m: 'screen', s: [0.5, 1.2, 0.04], p: [x, 1.0, -mz + 0.06] });
      }
      break;
    }
    case 'equipment': {
      // Equipment / server racks in a row.
      const n = clamp(Math.floor(w / 0.8), 1, 5);
      for (let i = 0; i < n; i++) {
        const x = -mx + ((2 * mx) / n) * (i + 0.5);
        items.push({ m: 'screen', s: [0.6, 1.9, Math.min(0.8, d * 0.5)], p: [x, 0.95, -mz + 0.45] });
      }
      break;
    }
    case 'bench': {
      items.push({ m: 'wood', s: [clamp(w * 0.7, 0.8, 2.4), 0.85, 0.55], p: [0, 0.42, -mz + 0.35] });
      break;
    }
    default:
      break;
  }
  return items;
}

export function Furniture({ graph, state, hidden, onHover, onHide }: GraphProps) {
  const mats = useMemo(() => {
    const make = (c: number, rough: number, metal: number) =>
      new THREE.MeshStandardMaterial({ color: c, roughness: rough, metalness: metal });
    return {
      wood: make(FURN_WOOD_COLOR, 0.6, 0.05),
      fabric: make(FURN_FABRIC_COLOR, 0.85, 0.0),
      metal: make(FURN_METAL_COLOR, 0.4, 0.6),
      screen: new THREE.MeshStandardMaterial({
        color: FURN_SCREEN_COLOR,
        emissive: new THREE.Color(0x1c6e7a),
        emissiveIntensity: 0.25,
        roughness: 0.5,
        metalness: 0.3,
      }),
    } as Record<MatKey, THREE.MeshStandardMaterial>;
  }, []);

  const furnished = useMemo(() => {
    const out: { node: GraphNode; kind: Kind; items: Item[] }[] = [];
    for (const node of graph.nodes) {
      if (node.type === 'core') continue;
      const kind = classify(node);
      if (!kind) continue;
      const w = Math.max((node.w ?? 0) * SCALE_XY, MIN_FOOT);
      const d = Math.max((node.h ?? 0) * SCALE_XY, MIN_FOOT);
      const items = buildModels(kind, w, d);
      if (items.length) out.push({ node, kind, items });
    }
    return out;
  }, [graph.nodes]);

  return (
    <>
      {furnished.map(({ node, kind, items }) => {
        const [cx, cz] = worldXZ(node);
        const floorY = node.z * SCALE_Z + SLAB_H;
        const meta = {
          id: `furn-${node.id}`,
          kind: 'fixture' as const,
          type: node.type, // follows the room's category toggle
          floorLevel: String(node.floor),
          label: `${kind} fit-out · ${node.label}`,
        };
        return (
          <SceneMesh
            key={meta.id}
            meta={meta}
            state={state}
            hidden={hidden}
            onHover={onHover}
            onHide={onHide}
            pickable
          >
            {items.map((it, i) => (
              <mesh
                key={i}
                position={[cx + it.p[0], floorY + it.p[1], cz + it.p[2]]}
                material={mats[it.m]}
              >
                <boxGeometry args={it.s} />
              </mesh>
            ))}
          </SceneMesh>
        );
      })}
    </>
  );
}
