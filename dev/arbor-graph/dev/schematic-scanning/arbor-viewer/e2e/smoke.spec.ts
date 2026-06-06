import { test, expect } from '@playwright/test';

test('loads the viewer, renders the canvas, and filters a floor without errors', async ({
  page,
}) => {
  const errors: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  page.on('pageerror', (e) => errors.push(String(e)));

  await page.goto('/');

  // Header stats populate once graph.json loads (proves data + scene mounted).
  await expect(page.locator('#stats')).toContainText('rooms', { timeout: 20_000 });

  // The WebGL canvas exists and has real size.
  const canvas = page.locator('#canvas-container canvas');
  await expect(canvas).toBeVisible();
  const box = await canvas.boundingBox();
  expect(box?.width ?? 0).toBeGreaterThan(100);
  expect(box?.height ?? 0).toBeGreaterThan(100);

  // Floor buttons rendered; clicking one activates it (floor filter works).
  const allBtn = page.locator('.floor-btn.all');
  await expect(allBtn).toHaveClass(/active/);
  const firstLevel = page.locator('#floor-list .floor-btn').first();
  await firstLevel.click();
  await expect(firstLevel).toHaveClass(/active/);
  await expect(allBtn).not.toHaveClass(/active/);

  // Toggle a detail layer (no crash).
  await page.locator('#detail-filters input').first().click();

  expect(errors, `console errors:\n${errors.join('\n')}`).toEqual([]);
});
