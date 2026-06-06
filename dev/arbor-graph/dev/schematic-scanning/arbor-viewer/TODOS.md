# TODOs

## Perf: bulk geometry — PARTIALLY DONE (2026-06-06)
DONE: walls.json segments now merge into one BufferGeometry per floor
(lib/scene/mergeWalls.ts + components/scene/VectorWalls.tsx). 13,605 wall meshes → ~44.
Labels (127 troika SDF Text) no longer mount until the labels toggle is on.
dpr capped at 1.5. Total scene objects ~14,800 → ~1,200.

REMAINING optional levers, only if it still janks on the demo machine:
- components/scene/Rooms.tsx — 127 slabs + 127 EdgesGeometry outlines are still
  per-mesh. Switch slabs to drei <Instances> and drop/merge the outlines for another
  ~250 → ~2 draw calls.
- components/scene/Stairs.tsx — 27 stair runs × ~25 boxes = ~675 meshes; could merge
  per run (~675 → ~27).
- Transparency: nearly every material is transparent (intentional "exposed structure"
  look). If still fragment-bound, consider opaque cores/walls or dropping FogExp2.
- Render loop: useFrame (entrance pulse) forces frameloop="always". If idle cost matters,
  gate the pulse and switch to frameloop="demand" + invalidate() on OrbitControls change.
