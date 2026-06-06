import { describe, it, expect, vi } from 'vitest';
import { loadData } from '@/lib/loader';

const res = (ok: boolean, body: unknown): Response =>
  ({ ok, status: ok ? 200 : 404, json: async () => body }) as unknown as Response;

describe('loadData', () => {
  it('returns all three when every file is present', async () => {
    const fetcher = vi.fn(async (url: string) => {
      if (url.includes('graph')) return res(true, { nodes: [], edges: [], floors: [] });
      if (url.includes('walls')) return res(true, { floors: {} });
      return res(true, { nodes: [], edges: [] });
    }) as unknown as typeof fetch;
    const out = await loadData('', fetcher);
    expect(out.graph).toBeTruthy();
    expect(out.walls).toBeTruthy();
    expect(out.building).toBeTruthy();
  });

  it('falls back to null when walls.json and building.json are absent', async () => {
    const fetcher = vi.fn(async (url: string) => {
      if (url.includes('graph')) return res(true, { nodes: [], edges: [], floors: [] });
      return res(false, null);
    }) as unknown as typeof fetch;
    const out = await loadData('', fetcher);
    expect(out.graph).toBeTruthy();
    expect(out.walls).toBeNull();
    expect(out.building).toBeNull();
  });

  it('swallows network errors on the optional files', async () => {
    const fetcher = vi.fn(async (url: string) => {
      if (url.includes('graph')) return res(true, { nodes: [], edges: [], floors: [] });
      throw new Error('network down');
    }) as unknown as typeof fetch;
    const out = await loadData('', fetcher);
    expect(out.walls).toBeNull();
    expect(out.building).toBeNull();
  });

  it('throws when graph.json fails (required)', async () => {
    const fetcher = vi.fn(async () => res(false, null)) as unknown as typeof fetch;
    await expect(loadData('', fetcher)).rejects.toThrow(/graph\.json/);
  });
});
