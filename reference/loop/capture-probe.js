// Read-only page diagnostics. App must expose stable build and test contracts.
// Integrate only after application-specific review.
export async function captureProbe({ tokenNames, semantics }) {
  const standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  const controller = navigator.serviceWorker?.controller;
  const swBuildId = controller ? await new Promise(resolve => {
    const channel = new MessageChannel();
    const close = value => { clearTimeout(timer); channel.port1.close(); channel.port2.close(); resolve(value); };
    const timer = setTimeout(() => close(null), 2000);
    channel.port1.onmessage = e => close(e.data?.type === 'UI_AUDIT_BUILD' ? e.data.buildId : null);
    controller.postMessage({ type: 'UI_AUDIT_BUILD_REQUEST' }, [channel.port2]);
  }) : null;
  const css = getComputedStyle(document.documentElement);
  return {
    buildId: document.documentElement.dataset.buildId || null,
    tokenVersion: document.documentElement.dataset.tokenVersion || null,
    displayMode: standalone ? 'standalone' : 'browser', swBuildId,
    reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches,
    viewport: { width: innerWidth, height: innerHeight, dpr: devicePixelRatio,
      visualHeight: visualViewport?.height, visualOffsetTop: visualViewport?.offsetTop },
    tokens: Object.fromEntries(tokenNames.map(t => [t, css.getPropertyValue(t).trim()])),
    semantics, focused: document.activeElement?.getAttribute('data-testid') || null,
  };
}
// Companion SW handler uses the SW's own immutable build ID, never the page ID:
// self.addEventListener('message', e => {
//   if (e.data?.type === 'UI_AUDIT_BUILD_REQUEST')
//     e.ports[0]?.postMessage({ type: 'UI_AUDIT_BUILD', buildId: SW_BUILD_ID });
// });
