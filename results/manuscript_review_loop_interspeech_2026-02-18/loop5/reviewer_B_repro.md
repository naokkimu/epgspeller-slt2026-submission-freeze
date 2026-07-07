**Reviewable?** yes (score: 8/10)

**Remaining manuscript-side reproducibility blockers (not packaging-side)**
- Word-holdout word identity still underspecified if “normalization” is claimed; prefer defining word identity as the target-word string used for evaluation (applied).
- Splits are not explicitly artifact-linked in-text; consider naming/citing split files or a manifest.
- Fixed-dropout mask construction could be more explicit (sampling distribution, rounding rule for number masked, replicate definition).
- RTF measurement context could be pinned more tightly (batching/device/sync policy), though scope is now stated as forward-pass only.

**Numeric-handwriting violations**
- None observed; numbers appear via generated macros/tables.
