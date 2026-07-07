# Loop5 merged action list (applied)

## Changes applied
- Clarified proxy mapping $\pi$ construction from the pinned SmartPalate layout snapshot; duplicates resolved by first occurrence; unmapped channels retained separately.
- Replaced “proxy-grid reconstruction” with “proxy-grid projection” throughout.
- Clarified availability mask semantics for budgeted subsets and fixed-dropout evaluation.
- Added operational definitions for TopK/FPS-diverse TopK (occlusion score, Euclidean distance, twice-budget candidate pool, fill-by-importance).
- Distinguished SpecAugment-inspired masking (time/channel) vs proxy-grid spatial augmentation.
- Clarified RTF scope as forward-pass wall time excluding decoding/data loading.

## Remaining optional improvements
- Link split artifacts/manifests directly in text.
- Add a short deterministic description of fixed-dropout mask sampling/rounding (or link to the pinned script).
- If space allows, add extra structured-EPG citations (e.g., shadle1993depth, toutios2006learning, toutios2006on).
