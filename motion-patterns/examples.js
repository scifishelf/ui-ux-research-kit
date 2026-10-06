// Synchronous DOM commit only. For React/Next route changes, use a commit-aware
// router integration rather than assuming router.push() has rendered the target.
export async function transitionCommit(commit) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !document.startViewTransition) { commit(); return; }
  const t = document.startViewTransition(() => commit());
  // updateCallbackDone means target DOM is committed; do not wait for animation.
  try { await t.updateCallbackDone; } finally { await t.finished.catch(() => {}); }
}
export function showReviewDialog(dialog) { if (!dialog.open) dialog.showModal(); }
export function replay(element) {
  const animations = element.getAnimations();
  for (const animation of animations) { animation.cancel(); animation.play(); }
}
