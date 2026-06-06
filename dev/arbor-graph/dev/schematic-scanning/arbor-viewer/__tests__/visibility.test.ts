import { describe, it, expect } from 'vitest';
import { isVisible } from '@/lib/scene/visibility';
import { DEFAULT_VIEWER_STATE } from '@/lib/scene/constants';
import type { UnitMeta, ViewerState } from '@/lib/types';

const state = (over: Partial<ViewerState> = {}): ViewerState => ({
  ...DEFAULT_VIEWER_STATE,
  categoryEnabled: { ...DEFAULT_VIEWER_STATE.categoryEnabled, ...over.categoryEnabled },
  ...over,
});

const meta = (over: Partial<UnitMeta>): UnitMeta => ({
  id: 'u',
  kind: 'floor',
  floorLevel: '0',
  label: '',
  type: 'office',
  ...over,
});

const NONE = new Set<string>();

describe('isVisible', () => {
  it('hides anything in the hidden set', () => {
    expect(isVisible(meta({ id: 'x' }), state(), new Set(['x']))).toBe(false);
  });

  it('shows office rooms by default but hides plant', () => {
    expect(isVisible(meta({ type: 'office' }), state(), NONE)).toBe(true);
    expect(isVisible(meta({ type: 'plant' }), state(), NONE)).toBe(false);
  });

  it('applies the floor filter to rooms but NOT to vertical circulation', () => {
    const onL5 = meta({ floorLevel: '5' });
    expect(isVisible(onL5, state({ activeFloor: '3' }), NONE)).toBe(false);
    expect(isVisible(onL5, state({ activeFloor: '5' }), NONE)).toBe(true);

    const stair = meta({ kind: 'stair', isCore: true, floorLevel: '5' });
    expect(isVisible(stair, state({ activeFloor: '3' }), NONE)).toBe(true);
  });

  it('respects per-layer toggles', () => {
    expect(isVisible(meta({ kind: 'stair', isCore: true }), state({ stairsEnabled: false }), NONE)).toBe(false);
    expect(isVisible(meta({ kind: 'lift', isCore: true }), state({ liftsEnabled: false }), NONE)).toBe(false);
    expect(isVisible(meta({ isPartition: true }), state({ partitionsEnabled: false }), NONE)).toBe(false);
    expect(isVisible(meta({ isOuterWall: true }), state({ outerWallsEnabled: false }), NONE)).toBe(false);
    expect(isVisible(meta({ isEntrance: true }), state({ entrancesEnabled: false }), NONE)).toBe(false);
    expect(isVisible(meta({ isLabel: true }), state({ labelsEnabled: false }), NONE)).toBe(false);
    // labels off by default
    expect(isVisible(meta({ isLabel: true }), state(), NONE)).toBe(false);
  });

  it('always shows reference plates on the active floor', () => {
    expect(isVisible(meta({ kind: 'plate' }), state(), NONE)).toBe(true);
  });
});
