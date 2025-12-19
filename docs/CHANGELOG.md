# Changelog

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

