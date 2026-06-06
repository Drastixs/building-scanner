import { describe, it, expect } from 'vitest';
import { hideReducer, initialHideState } from '@/lib/interaction';

describe('hideReducer', () => {
  it('hides a unit and tracks it for undo', () => {
    const s = hideReducer(initialHideState, { type: 'hide', id: 'a' });
    expect(s.hidden.has('a')).toBe(true);
    expect(s.undo).toEqual(['a']);
    expect(s.redo).toEqual([]);
  });

  it('is a no-op when hiding an already-hidden unit', () => {
    const s1 = hideReducer(initialHideState, { type: 'hide', id: 'a' });
    const s2 = hideReducer(s1, { type: 'hide', id: 'a' });
    expect(s2).toBe(s1);
  });

  it('undo restores and redo re-hides', () => {
    let s = hideReducer(initialHideState, { type: 'hide', id: 'a' });
    s = hideReducer(s, { type: 'hide', id: 'b' });
    s = hideReducer(s, { type: 'undo' });
    expect(s.hidden.has('b')).toBe(false);
    expect(s.redo).toEqual(['b']);
    s = hideReducer(s, { type: 'redo' });
    expect(s.hidden.has('b')).toBe(true);
    expect(s.redo).toEqual([]);
  });

  it('clears the redo stack on a fresh hide', () => {
    let s = hideReducer(initialHideState, { type: 'hide', id: 'a' });
    s = hideReducer(s, { type: 'undo' }); // redo = [a]
    s = hideReducer(s, { type: 'hide', id: 'c' });
    expect(s.redo).toEqual([]);
  });

  it('undo/redo on empty stacks are no-ops', () => {
    expect(hideReducer(initialHideState, { type: 'undo' })).toBe(initialHideState);
    expect(hideReducer(initialHideState, { type: 'redo' })).toBe(initialHideState);
  });

  it('reset clears everything', () => {
    let s = hideReducer(initialHideState, { type: 'hide', id: 'a' });
    s = hideReducer(s, { type: 'hide', id: 'b' });
    s = hideReducer(s, { type: 'reset' });
    expect(s.hidden.size).toBe(0);
    expect(s.undo).toEqual([]);
    expect(s.redo).toEqual([]);
  });
});
