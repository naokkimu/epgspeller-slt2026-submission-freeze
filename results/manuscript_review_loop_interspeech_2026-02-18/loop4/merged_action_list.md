# Loop4 merged action list (priority-ordered)

## P0 (must-fix)
1. Make proxy mapping definition self-consistent with how duplicates are handled (first occurrence for duplicated channel indices; no “multiple channels in one cell” claim).
2. Replace “proxy-grid reconstruction” phrasing with “proxy-grid projection” to avoid implying learned imputation.
3. Add explicit budget linkage: for each $K$, the same selected channels are fed to all compared front-ends.
4. Make negative directions explicit: “higher (worse) CER/RTF” in abstract/results sentences.
5. Expand Related Work to directly motivate the spatial/representation question using EPG representation/reduction/design citations, and connect robustness to masking-style augmentation.

## P1 (should-fix)
6. Clarify “word identity” definition (normalized target-word string) to reduce leakage ambiguity.
7. Optionally clarify RTF timing scope (forward pass only) and add a pointer for SpecAugment/dropout mask details.
