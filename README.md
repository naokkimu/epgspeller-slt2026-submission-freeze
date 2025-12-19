
## Rebuttal Quickstart (this repo only)

This replaces old instructions. Focus is on reproducible rebuttal numbers (A/B/C/D/E/CV).

### Prereqs
- Data: `raw/silentspeller_dataset/p1_2328_old_dataset.npz`
- Set env when running Python: `PYTHONPATH=src`
- GPU recommended; CPU is slow. Default validation split = `competition`, report on `test`.

### Pipeline (seed0, one command at a time)
1) Split (word-holdout, seed0)
```
python scripts/rebuttal/make_word_holdout_split.py \
  --raw_npz raw/silentspeller_dataset/p1_2328_old_dataset.npz \
  --n_competition_words 50 --n_test_words 50 --seed 0 \
  --out_npz raw_dataset/train_test_competition_split_seed0.npz
```
2) Prepare PCA32 (no offline aug)
```
python scripts/prepare_silentspeller_dataset.py \
  --split_path raw_dataset/train_test_competition_split_seed0.npz \
  --n_components 32 \
  --output_path data/rebuttal_seed0_pca32
```
3) Train SpecAug OFF (E/A)
```
PYTHONPATH=src python scripts/train.py \
  --dataset_path data/rebuttal_seed0_pca32 \
  --model_name rebuttal_s0_pca32_noaug \
  --n_units 1024 --n_layers 5 --n_batch 10000 --seed 0 \
  --n_classes 26 --val_split competition
```
4) Greedy eval (A/E)
```
PYTHONPATH=src python scripts/rebuttal/eval_greedy_clean.py \
  --model_path logs/<...rebuttal_s0_pca32_noaug> \
  --partition test --device cuda \
  --out_json logs/<...>/rebuttal_eval_greedy_test.json

PYTHONPATH=src python scripts/rebuttal/eval_greedy_clean.py \
  --model_path logs/<...rebuttal_s0_pca32_noaug> \
  --partition competition --device cuda \
  --out_json logs/<...>/rebuttal_eval_greedy_competition.json
```
5) Lexicon baselines (C_train, C_all)
```
PYTHONPATH=src python scripts/rebuttal/eval_lexicon_project.py \
  --pred_json logs/<...>/rebuttal_eval_greedy_test.json \
  --lexicon_source train \
  --out_json logs/<...>/rebuttal_eval_lexicon_train.json

PYTHONPATH=src python scripts/rebuttal/eval_lexicon_project.py \
  --pred_json logs/<...>/rebuttal_eval_greedy_test.json \
  --lexicon_source all \
  --out_json logs/<...>/rebuttal_eval_lexicon_all.json
```
6) SpecAug ON (D)
```
PYTHONPATH=src python scripts/train.py \
  --dataset_path data/rebuttal_seed0_pca32 \
  --model_name rebuttal_s0_pca32_specaug \
  --n_units 1024 --n_layers 5 --n_batch 10000 --seed 0 \
  --n_classes 26 --val_split competition --enable_online_specaug

PYTHONPATH=src python scripts/rebuttal/eval_greedy_clean.py \
  --model_path logs/<...rebuttal_s0_pca32_specaug> \
  --partition test --device cuda \
  --out_json logs/<...>/rebuttal_eval_greedy_test_specaug.json
```
7) Seeds 1/2 (CV): repeat steps 1–5 with `--seed 1` and `--seed 2`, SpecAug OFF greedy (test) only for mean±std.
8) Aggregate
```
PYTHONPATH=src python scripts/rebuttal/aggregate_rebuttal_numbers.py \
  --inputs "logs/**/rebuttal_eval_*.json" \
  --out_yaml rebuttal_numbers.yaml \
  --out_md rebuttal_numbers.md
```

### KenLM (B) leakage policy
- Only if you train an LM on **training transcripts (seed0) only**; otherwise omit B. State this explicitly in text.

### Sanity
- `prepare_silentspeller_dataset.py` asserts target IDs `<=26` (A–Z). Fails fast if mapping is wrong.
