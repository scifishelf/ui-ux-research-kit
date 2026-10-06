// Integration example: implement this explicit fixture contract in a test build.
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { createHash } from 'node:crypto';
import { writeFile } from 'node:fs/promises';

test('UI state emits review evidence', async ({ page, browserName }, info) => {
  const expectedBuild = process.env.UI_AUDIT_BUILD;
  if (!expectedBuild) throw new Error('UI_AUDIT_BUILD missing');
  // App adapter must fix data, time, locale and permissions without live writes.
  await page.goto('/__ui_audit?task=B01&state=empty');
  await page.getByTestId('audit-ready').waitFor();
  await page.evaluate(() => document.fonts.ready);
  await expect(page.locator('html')).toHaveAttribute('data-build-id', expectedBuild);
  const scan = await new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
  expect(scan.violations).toEqual([]);
  await info.attach('axe-incomplete', { body: JSON.stringify(scan.incomplete), contentType: 'application/json' });
  // Compile/import probe into app and expose a read-only audited export.
  // Playwright page.evaluate cannot directly close over a Node-imported function.
  const probe = await page.evaluate(async () => {
    const w = window as typeof window & { __uiAuditProbe?: () => Promise<object> };
    if (!w.__uiAuditProbe) throw new Error('App probe adapter missing');
    return w.__uiAuditProbe();
  });
  const imagePath = info.outputPath('desktop.png');
  const bytes = await page.screenshot({ path: imagePath, animations: 'disabled' });
  const manifest = {
    ...probe, schemaVersion: '1', surface: 'desktop', captureKind: 'desktop-browser',
    runId: process.env.UI_AUDIT_RUN, fixtureId: 'B01-empty-v1', state: 'empty',
    theme: 'light', capturedAt: new Date().toISOString(),
    screenshot: { path: 'desktop.png', sha256: createHash('sha256').update(bytes).digest('hex') },
    runtime: { name: browserName, version: page.context().browser()?.version() },
  };
  await writeFile(info.outputPath('desktop.json'), JSON.stringify(manifest, null, 2));
  // This is one desktop state. iOS capture and full matrix remain mandatory.
});
