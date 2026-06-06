'use client';
// 3D scene contents (rendered inside <Canvas>): lights, fog, controls, and every
// geometry layer. Chooses real vector walls (walls.json) over adjacency partitions.
import { memo } from 'react';
import { OrbitControls } from '@react-three/drei';
import type { UnitHandlers } from '@/components/contracts';
import type { LoadedData } from '@/lib/types';
import { BG_COLOR } from '@/lib/scene/constants';
import { FloorPlates } from './FloorPlates';
import { Rooms } from './Rooms';
import { CoreMarkers } from './CoreMarkers';
import { Labels } from './Labels';
import { VectorWalls } from './VectorWalls';
import { Partitions } from './Partitions';
import { Stairs } from './Stairs';
import { Lifts } from './Lifts';
import { Entrances } from './Entrances';
import { PathOverlay } from './PathOverlay';

interface Props extends UnitHandlers {
  data: LoadedData;
  routePath?: string[] | null;
}

export const Scene = memo(function Scene({ data, routePath, ...h }: Props) {
  const { graph, walls, building } = data;
  return (
    <>
      <color attach="background" args={[BG_COLOR]} />
      <fogExp2 attach="fog" args={[BG_COLOR, 0.0045]} />

      <ambientLight intensity={0.55} />
      <directionalLight intensity={0.8} position={[30, 90, 30]} />
      <directionalLight color={0x6688cc} intensity={0.35} position={[-40, 30, -30]} />

      <OrbitControls
        makeDefault
        enableDamping
        dampingFactor={0.06}
        minDistance={5}
        maxDistance={280}
        target={[11, 24, 11]}
      />

      <FloorPlates graph={graph} walls={walls} {...h} />
      <Rooms graph={graph} {...h} />
      <CoreMarkers graph={graph} {...h} />
      {/* 127 troika SDF text meshes — only mount them when labels are actually on. */}
      {h.state.labelsEnabled && <Labels graph={graph} {...h} />}

      {walls ? (
        <VectorWalls graph={graph} walls={walls} {...h} />
      ) : (
        <Partitions graph={graph} {...h} />
      )}

      <Stairs graph={graph} {...h} />
      <Lifts graph={graph} {...h} />

      {building && <Entrances building={building} {...h} />}
      {building && routePath && routePath.length > 1 && (
        <PathOverlay building={building} path={routePath} />
      )}
    </>
  );
});
