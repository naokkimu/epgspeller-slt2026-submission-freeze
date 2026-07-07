**Unreproducible Claims List**
- `main.tex:23` “All reported numbers are generated…” is not auditable from the manuscript alone: missing the exact regeneration command(s), required environment (versions/deps), and a trace from each `\input{...}` / macro in `facts.tex` to specific `paper.json` evidence IDs + sha256.
- `main.tex:28` Grid layout proxy + mapped/unmapped channel counts: missing the exact grid-map definition (how indices map to (row,col)), the referenced “pinned distribution CSV” identifier/path, and how unmapped channels are handled downstream.
- `main.tex:32` Recurrent CTC decoder spec is incomplete/ambiguous (“kernel length/stride” for a recurrent model): missing RNN type, layer counts, hidden sizes, dropout, normalization, and where kernel/stride apply.
- `main.tex:39` 2D reconstruction + conv stack: missing scatter rules (fill value, collisions), treatment of missing electrodes, and full conv stack details (layers/kernels/strides/padding/channels).
- `main.tex:42` Row/column compression: missing pooling operator(s) (mean/max/sum), any weighting/masking, concatenation/projection details.
- `main.tex:45` “Within-subject protocol” is not reproducible without: subject/session definition, exact split construction algorithm, leakage controls, what “random splits” randomize, and how `SeedListPone` maps to concrete splits.
- `main.tex:46` Training protocol incomplete: missing optimizer/LR schedule/batch size/regularization/checkpoint selection, and full SpecAugment-style masking parameters (what is masked, widths, probabilities, axis definitions for EPG).
- `main.tex:48` TopK and FPS-diverse TopK are undefined: missing “importance” scoring definition, data split used to compute it, FPS distance metric on the grid, tie-breaking, and whether selection is per-subject/per-split/global.
- `main.tex:53`–`main.tex:54` (and the `\input` at `main.tex:60`): claims about “worse” CER and “slower” streaming RTF require metric/protocol definitions not given (CER text normalization; greedy decoding details; streaming/RTF measurement procedure, hardware, what is timed).
- `main.tex:64` (and the `\input` at `main.tex:71`): same missing CER/RTF protocol issues.
- `main.tex:75`–`main.tex:77` (and the `\input` at `main.tex:83`): “fixed electrode dropout masks” and “spatial augmentation” are not defined (mask generation/seed, fixed across what, applied to which electrode set, and the exact augmentation operation during training).
- `main.tex:87`–`main.tex:88` Evidence registry is asserted, but the manuscript provides no explicit mapping from sections/tables to `paper.json` claim IDs/evidence IDs (evidence-linking gap).
- `main.tex:91` Bibliography depends on a date-stamped `results/...` path: missing guarantee it’s vendored or deterministically generated as part of the paper build.

**Manual Numeric Facts Violations**
- None in the experimental narrative/results (all quantitative content appears via macros/`\input{...}`).
- Potential “strict numeric literal” policy/claim mismatch: handwritten digits exist in `main.tex:1`, `main.tex:29`, `main.tex:46`, `main.tex:91` (not facts, but they contradict the literal reading of the claim at `main.tex:88` unless exceptions are documented).

**Required Fixes (Top Priority)**
- Add a complete, implementation-level protocol for splits/training/decoding/metrics/RTF measurement, using macros (not handwritten numbers) where needed.
- Add auto-generated traceability in the PDF: for each table/fact, print the corresponding `paper.json` claim/evidence IDs + sha256 (or a single generated appendix that links every `\input{...}` to pinned evidence).
- Document exact regeneration commands for `facts.tex` and the tables (entrypoint, args, expected outputs) plus the deterministic environment requirements.
- Fully define electrode layout mapping + selection (TopK/FPS) and robustness setup (dropout masks + “spatial augmentation”).
- Clarify the numeric-literal checker claim/scope (or adjust wording) to avoid a manuscript-internal contradiction.

**Verdict**
- Reviewable (evidence-only, from provided text): No.
- Score (Reproducibility/Auditability): 4/10.
MD'