# Loop3 merged action list (priority-ordered)

## P0 (must-fix)
1. Clarify how the SmartPalate distribution snapshot defines the proxy mapping $\pi$ (operationally: grid cells contain channel indices).
2. Remove ambiguity about unmapped channels: explicitly state they are retained as non-grid features for layout-aware front-ends (and reflect this consistently in both Spatial2D and RowCol descriptions).
3. Tighten TopK/FPS-diverse TopK definitions (occlusion-based importance = performance drop when masking; FPS-diverse = farthest-point sampling from a high-scoring candidate pool).
4. Rename “streaming RTF” to “forward-pass RTF” (or similar) to avoid implying online constraints; keep the precise definition.
5. Align robustness wording: clarify that fixed dropout masks mean the same masked channels for all samples in an evaluation run.

## P1 (should-fix)
6. Add SSI-related work anchor `lee2021biosignal` and optionally cite EPG2S (`a8287fa9`) to avoid “single prior” optics.
7. Add a short parenthetical tying title “Open-Vocabulary” to lexicon-free greedy CTC decoding under word-holdout.
8. In Results scope, add one sentence scoping findings to proxy-layout inductive bias (not true geometric tongue structure).
9. Replace “worse/slower/close” with metric-direction language (higher CER/RTF; similar CER within the reported table values).
