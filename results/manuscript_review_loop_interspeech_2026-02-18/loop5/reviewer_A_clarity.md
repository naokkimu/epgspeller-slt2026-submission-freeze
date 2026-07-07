Reviewable? **Yes**. Score: **Weak Accept** (clarity/definitions).

## Major issues
1) Duplicate handling inconsistency between proxy mapping definition and model description (resolved in final draft: duplicates resolved by first occurrence; no aggregation claim).
2) Mask channel semantics ambiguity under budgeted subsets and fixed-dropout eval (resolved in final draft: availability mask for selected subset; fixed-dropout zeros values while mask unchanged).
3) Word identity definition ambiguity (mitigated by defining word identity as target-word string used for evaluation).
4) Occlusion importance + FPS-diverse TopK needed sharper operational definitions (resolved in final draft: occlusion score = ΔCER under channel zeroing; FPS uses Euclidean distance; twice-budget candidate pool; fill by importance).
5) SpecAugment vs spatial augmentation needed clearer separation (resolved in final draft: SpecAug = time/channel masking for all; spatial aug = proxy-grid perturbations for proxy-grid conv only).

## TeX-ready suggestions
- Keep negative direction explicit (“higher (worse)”).
- Keep proxy-grid projection terminology (avoid “reconstruction”).
