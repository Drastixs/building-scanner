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
  WC_CERAMIC_COLOR,
  WC_METAL_COLOR,
  WC_MALE_COLOR,
  WC_FEMALE_COLOR,
  WC_ACCESSIBLE_COLOR,
} from '@/lib/scene/constants';
import { worldXZ } from '@/lib/scene/geometry';

// A WC is an amenity space whose label/function/fixtures name a toilet. We render
// real sanitaryware inside its footprint so a bathroom reads as a bathroom — and an
// Accessible (DDA / disabled) WC reads differently from a standard cubicle.
const WC_RE = /\b(wc|toilet|lavatory|washroom|restroom|bathroom|sanitary)\b/i;
const ACCESSIBLE_RE = /accessible|disabled|ambulant|wheelchair|\bdda\b/i;

interface Wc {
  node: GraphNode;
  accessible: boolean;
  marker: number; // gender / DDA marker colour
}

function classifyWc(node: GraphNode): Wc | null {
  if (node.type !== 'amenity') return null;
  const text = `${node.label ?? ''} ${node.function ?? ''}`.toLowerCase();
  const fixtures = node.fixtures ?? [];
  const isWc = WC_RE.test(text) || fixtures.includes('wc');
  if (!isWc) return null;
  const accessible = ACCESSIBLE_RE.test(text);
  const marker = accessible
    ? WC_ACCESSIBLE_COLOR
    : /\bfemale\b/.test(text)
      ? WC_FEMALE_COLOR
      : /\bmale\b/.test(text)
        ? WC_MALE_COLOR
        : WC_ACCESSIBLE_COLOR;
  return { node, accessible, marker };
}

export function Toilets({ graph, state, hidden, onHover, onHide }: GraphProps) {
  const ceramicMat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: WC_CERAMIC_COLOR,
        roughness: 0.25,
        metalness: 0.05,
      }),
    [],
  );
  const metalMat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: WC_METAL_COLOR,
        roughness: 0.35,
        metalness: 0.6,
      }),
    [],
  );
  // One emissive marker material per colour (male / female / accessible).
  const markerMats = useMemo(() => {
    const make = (c: number) =>
      new THREE.MeshStandardMaterial({
        color: c,
        emissive: new THREE.Color(c),
        emissiveIntensity: 0.55,
        roughness: 0.4,
      });
    return new Map<number, THREE.MeshStandardMaterial>([
      [WC_MALE_COLOR, make(WC_MALE_COLOR)],
      [WC_FEMALE_COLOR, make(WC_FEMALE_COLOR)],
      [WC_ACCESSIBLE_COLOR, make(WC_ACCESSIBLE_COLOR)],
    ]);
  }, []);

  const wcs = useMemo(
    () => graph.nodes.map(classifyWc).filter((w): w is Wc => w !== null),
    [graph.nodes],
  );

  return (
    <>
      {wcs.map(({ node, accessible, marker }) => {
        const [cx, cz] = worldXZ(node);
        const floorY = node.z * SCALE_Z + SLAB_H; // sanitaryware sits on the room slab
        const wWorld = Math.max((node.w ?? 0) * SCALE_XY, MIN_FOOT);
        const dWorld = Math.max((node.h ?? 0) * SCALE_XY, MIN_FOOT);
        // Scale fixtures down in a tight cubicle so nothing pokes through the walls.
        const sc = Math.min(1, Math.min(wWorld, dWorld) / 1.3);

        const panW = 0.36 * sc;
        const panD = 0.6 * sc;
        const panH = 0.4 * sc;
        const cisternH = 0.5 * sc;
        const basinW = 0.5 * sc;
        const basinH = 0.82 * sc;

        const markerMat = markerMats.get(marker)!;
        const meta = {
          id: `wc-${node.id}`,
          kind: 'fixture' as const,
          type: 'amenity',
          floorLevel: String(node.floor),
          label: accessible ? `Accessible WC · ${node.label}` : `WC · ${node.label}`,
        };

        // Back wall is -Z, side wall is -X (in the room's local footprint).
        const backZ = cz - dWorld / 2;
        const leftX = cx - wWorld / 2;
        const rightX = cx + wWorld / 2;

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
            {accessible ? (
              // ── Accessible / disabled WC: centred pan with clear floor + grab rails ──
              <>
                {/* Pan, set off the back wall for transfer space */}
                <mesh position={[cx, floorY + panH / 2, backZ + panD / 2 + 0.12]} material={ceramicMat}>
                  <boxGeometry args={[panW * 1.15, panH, panD]} />
                </mesh>
                <mesh position={[cx, floorY + panH + cisternH / 2, backZ + 0.1]} material={ceramicMat}>
                  <boxGeometry args={[panW * 1.3, cisternH, 0.18 * sc]} />
                </mesh>
                {/* Corner basin */}
                <mesh position={[rightX - 0.22 * sc, floorY + basinH, backZ + 0.18 * sc]} material={ceramicMat}>
                  <boxGeometry args={[basinW, 0.12 * sc, 0.34 * sc]} />
                </mesh>
                {/* Drop-down + fixed grab rails beside the pan */}
                <mesh position={[cx + panW * 0.9, floorY + 0.78 * sc, backZ + panD / 2 + 0.12]} material={metalMat}>
                  <boxGeometry args={[0.05, 0.05, panD * 1.1]} />
                </mesh>
                <mesh position={[cx + panW * 0.55, floorY + 0.95 * sc, backZ + 0.06]} material={metalMat}>
                  <boxGeometry args={[panW * 1.4, 0.05, 0.05]} />
                </mesh>
                {/* Blue floor disc — the international accessibility marker */}
                <mesh position={[cx, floorY + 0.015, cz + dWorld * 0.18]} material={markerMat}>
                  <cylinderGeometry args={[Math.min(wWorld, dWorld) * 0.28, Math.min(wWorld, dWorld) * 0.28, 0.03, 20]} />
                </mesh>
              </>
            ) : (
              // ── Standard WC: pan + cistern in the corner, basin on the side wall ──
              <>
                <mesh position={[leftX + panW / 2 + 0.1, floorY + panH / 2, backZ + panD / 2 + 0.08]} material={ceramicMat}>
                  <boxGeometry args={[panW, panH, panD]} />
                </mesh>
                <mesh position={[leftX + panW / 2 + 0.1, floorY + panH + cisternH / 2, backZ + 0.1]} material={ceramicMat}>
                  <boxGeometry args={[panW * 1.1, cisternH, 0.16 * sc]} />
                </mesh>
                <mesh position={[rightX - 0.2 * sc, floorY + basinH, backZ + 0.2 * sc]} material={ceramicMat}>
                  <boxGeometry args={[basinW * 0.7, 0.12 * sc, 0.3 * sc]} />
                </mesh>
                {/* Gender marker disc on the floor */}
                <mesh position={[cx, floorY + 0.015, cz + dWorld * 0.22]} material={markerMat}>
                  <cylinderGeometry args={[Math.min(wWorld, dWorld) * 0.2, Math.min(wWorld, dWorld) * 0.2, 0.03, 18]} />
                </mesh>
              </>
            )}
          </SceneMesh>
        );
      })}
    </>
  );
}
