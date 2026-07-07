# Loop1 merged action list (priority order)

## P0: Reproducibility / auditability (must fix)
1. Replace the ambiguous "within-subject" wording with a protocol definition that matches repo evidence (word-holdout / unseen-word test) and explicitly scope all claims to this protocol.
2. Define the proxy electrode layout mapping precisely:
   - channel index order is the canonical order for layout-agnostic models;
   - proxy grid is derived from the pinned SmartPalate distribution artifact;
   - mapped/unmapped/duplicated channels are defined and handled deterministically.
3. Clarify model description so that "kernel length" / "stride" are not misleading for a recurrent decoder; explicitly state what is shared across conditions and which component changes.
4. Define the evaluation metrics/procedures used in the tables:
   - greedy decoding for CER;
   - what streaming RTF represents (speed metric) and how it is computed/compared;
   - fixed-dropout evaluation protocol at a high level (rate values are in the generated table).
5. Make evidence linkage explicit in-paper without handwritten identifiers:
   - generate a small `paper/generated/provenance.tex` that lists the pinned evidence IDs used by the manuscript;
   - reference those macros in the "Artifacts and auditability" section.
6. Clarify the "no handwritten numeric facts" claim so it matches the actual checker policy (numeric facts in the manuscript body, not all digits in every context).

## P1: Clarity / definitions
7. Add one "Related work and positioning" section using existing bib entries (at least SilentSpeller) and scope novelty claims accordingly.
8. Rename "unordered channel vector" to "layout-agnostic channel vector (canonical index order)".
9. Define TopK and FPS-diverse TopK as simple heuristics/baselines; do not imply novelty.

## P2: Presentation
10. Fix table overfull boxes by wrapping `\input{...}` tables in `\resizebox{\columnwidth}{!}{...}`.

## Deferred (explicitly not doing in this loop)
- Add new experiments or add new external citations beyond the existing `references.bib`.
- Handwrite any numeric facts (metrics, dataset sizes, hyperparameters).
MD'