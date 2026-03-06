# Changelog

## 2026-03-05
- Fix LaTeX float placement error in `paper/submission/interspeech2026_review_manual.tex` by adding `\usepackage{float}` so table blocks using `[H]` compile correctly.

## 2025-12-19
- Normalize lexicon words to uppercase in `scripts/rebuttal/eval_lexicon_project.py` so projections align with greedy outputs (fixes false CER/WER=1.0 when vocab casing differed).
- Fix `scripts/rebuttal/aggregate_rebuttal_numbers.py` selection:
  - A/E = SpecAug OFF, seed0 greedy; D = SpecAug ON, seed0 greedy; CV = SpecAug OFF seeds.
  - Split lexicon results into `C_train` and oracle `C_all`.

## 2025-12-22
- Add Protocol-S (seen-word / instance holdout) split generator `scripts/rebuttal/make_instance_holdout_split.py`.
- Make `src/` importable in `scripts/train.py`, `scripts/rebuttal/eval_greedy_clean.py`, and `scripts/rebuttal/eval_lexicon_project.py` for fresh checkouts (no editable install).
- Document Protocol-S commands and correct SpecAug CLI usage in `docs/README.md`.
- Extend `scripts/rebuttal/aggregate_rebuttal_numbers.py` with Protocol-S (multi-subject) aggregation and ensure legacy A/C/D/E/CV metrics only use `rebuttal_eval_*` inputs.
- Add `rebuttal_response.md` as a repo-local rebuttal draft for copy-paste submission.

## 2025-12-18
- Add rebuttal utilities:
  - `scripts/rebuttal/make_word_holdout_split.py` for seeded word-holdout splits.
  - `scripts/rebuttal/eval_greedy_clean.py` for clean greedy CTC CER/WER.
  - `scripts/rebuttal/eval_lexicon_project.py` for lexicon projection baseline.
  - `scripts/rebuttal/aggregate_rebuttal_numbers.py` for YAML/MD aggregation.
- Extend `scripts/prepare_silentspeller_dataset.py` with `--split_path`/`--output_path`.
- Extend `scripts/train.py` with rebuttal knobs (n_units/layers/batch/seed/n_classes, online SpecAug toggle) and param_count logging.
- Add target-ID sanity assert (max<=26) in dataset prep.
- Validation now defaults to competition split; report on test.
- README documents sanities, lexicon sources, and KenLM train-only note.

