# Component and token contract

Criteria DS-01–04 and UX-02. Shared source: tokens → CSS variables → components. Themes supply values; components supply semantics. Document slots, data states, validation, keyboard, focus, hover/touch, busy/disabled and motion per component. Give the agent small reference implementations and fixture/story URLs.

`tokens.json` is a small DTCG-format example; `tokens.css` is its readable CSS counterpart. Adapt examples to the existing system instead of treating them as a mandatory migration. [DTCG 2025.10](https://www.designtokens.org/tr/2025.10/format/) is a Final Community Group Report, not a W3C standard.

Lint in AST/CSS context: flag new color, spacing, radius and motion literals and arbitrary utility values. Permit justified zero, hairlines, percentages, grid ratios, measured image coordinates and safe-area formulas. Numeric regex matches do not measure design quality. Exceptions need an owner and purpose. Cover iframes, shadow DOM, dynamic CSS and Canvas separately where used.

Across sessions, retain versioned design contracts, tokens, state matrices, approved screens, motion budgets and actual decisions. Link them from project instructions and load only the relevant contracts for each task.
