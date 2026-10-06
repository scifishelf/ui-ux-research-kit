'use client';
import { MotionConfig, motion, useReducedMotion } from 'motion/react';
import type { ReactNode } from 'react';
export function MotionRoot({ children }: { children: ReactNode }) {
  return <MotionConfig reducedMotion="user">{children}</MotionConfig>;
}
export function DragExample() {
  const reduce = useReducedMotion();
  return <motion.div drag="x" dragConstraints={{ left: 0, right: 120 }}
    dragElastic={0} dragMomentum={!reduce}
    dragTransition={reduce ? { power: 0, timeConstant: 1 } : { bounceStiffness: 380, bounceDamping: 38 }}
    style={{ touchAction: 'pan-y' }}
    aria-label="Draggable preview; alternative move buttons required">
    Preview
  </motion.div>;
}
// Product must add equivalent buttons and keyboard handling. This visual fragment
// alone does not pass ACC-04. MotionConfig does not disable direct pointer movement
// or every inertia path; reduced mode here removes momentum, and runtime must verify.
