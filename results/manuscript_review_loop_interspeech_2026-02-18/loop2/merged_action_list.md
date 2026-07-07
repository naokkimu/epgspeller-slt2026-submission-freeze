# Loop2 merged action list (priority-ordered)

## P0 (must-fix for reviewability / reproducibility)
1. **Add missing definitions on first use**
   - Expand: CTC, CER, RTF, word-holdout, proxy layout/mapping, “spatial augmentation”, “fixed dropout”.
   - Keep digits out of `main.tex` (use macros or refer to tables/scripts).

2. **Define the proxy electrode-to-grid mapping more concretely and link it to pinned provenance**
   - Introduce mapping object (e.g., $\pi$) and clarify mapped/unmapped/duplicate handling.
   - Mention the pinned SmartPalate distribution evidence via `\EvSmartpalateDistribution` / `\ShaSmartpalateDistribution`.

3. **Make the protocol reproducible in prose (without new experiments)**
   - Clarify word-holdout: train/test disjoint by word identity; splits fixed across compared front-ends.
   - Clarify what is held constant vs varied across vector/spatial2d/rowcol.
   - Provide explicit “how to regenerate numbers” command in Artifacts section (facts generator + strict checker + paperjson audit renderers).

4. **Strengthen related work / positioning minimally but sufficiently**
   - Replace the current 2-sentence Related Work with a compact paragraph situating SSI and EPG.
   - Add citations from existing bib only (e.g., SSI overview, EPG background, EPG data-reduction).
   - Add explicit non-claims (no new hardware/geometry/objective) to avoid overclaiming.

5. **Make evidence linkage local to each result table**
   - Add “Evidence: `\Ev… (\Sha…)`” in each table caption for H11/H12/H13.

## P1 (should-fix for stronger score)
6. **Tighten abstract scope / avoid overclaiming**
   - Rephrase “open-vocabulary” as “lexicon-free (character-level) under word-holdout” and remove auditability sentence from abstract.

7. **Clarify TopK / FPS-diverse TopK procedures at a high level**
   - State TopK uses an importance ranking; FPS-diverse TopK enforces proxy-grid diversity (farthest-point sampling) from a bounded candidate pool.
   - Avoid hardcoding numeric constants in the paper; defer exact algorithm to scripts if needed.

8. **Define streaming RTF computation**
   - RTF = (total forward-pass wall time) / (total input duration from frames × hop).
   - Mention “lower is better” and that we report streaming-ready models only.

## Notes / conflicts
- Reviewer B’s “missing artifacts in packet” is addressed by making the Artifacts section self-contained (explicit commands + evidence IDs). The repo already contains `paper/paper.json`, `paper/facts_spec.yaml`, and `scripts/paper/*`.
