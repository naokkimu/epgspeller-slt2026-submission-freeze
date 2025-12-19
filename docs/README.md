# Rebuttal Runbook (epg_speller_base)

Use these steps to reproduce rebuttal numbers (one command at a time).

## 0) Sanity after prepare
- After dataset pickle is created, ensure target IDs are within A–Z: built-in assertion (`max_id <= 26`) will stop if violated.

## 1) Make word-holdout split (seed example)
```
python scripts/rebuttal/make_word_holdout_split.py \
  --raw_npz raw_dataset/p1_2328_old_dataset.npz \
  --n_competition_words 50 --n_test_words 50 --seed 0 \
  --out_npz raw_dataset/train_test_competition_split_seed0.npz
```

## 2) Prepare PCA32 dataset (no offline aug; split swap supported)
```
python scripts/prepare_silentspeller_dataset.py \
  --split_path raw_dataset/train_test_competition_split_seed0.npz \
  --n_components 32 \
  --output_path data/rebuttal_pca32_seed0
```

## 3) Train (SpecAug OFF = E, ON = D)
```
python scripts/train.py \
  --dataset_path data/rebuttal_pca32_seed0 \
  --model_name rebuttal_seed0_pca32_noaug \
  --n_units 1024 --n_layers 5 --n_batch 10000 --seed 0 \
  --enable_online_specaug false \
  --n_classes 26

python scripts/train.py \
  --dataset_path data/rebuttal_pca32_seed0 \
  --model_name rebuttal_seed0_pca32_specaug \
  --n_units 1024 --n_layers 5 --n_batch 10000 --seed 0 \
  --enable_online_specaug true \
  --n_classes 26
```

## 4) Greedy eval (A/E) both partitions
```
python scripts/rebuttal/eval_greedy_clean.py \
  --model_path logs/<...> --partition test --device cuda \
  --out_json logs/<...>/rebuttal_eval_greedy_test.json

python scripts/rebuttal/eval_greedy_clean.py \
  --model_path logs/<...> --partition competition --device cuda \
  --out_json logs/<...>/rebuttal_eval_greedy_competition.json
```

## 5) Lexicon projection (C)
```
python scripts/rebuttal/eval_lexicon_project.py \
  --pred_json logs/<...>/rebuttal_eval_greedy_test.json \
  --lexicon_source train \
  --out_json logs/<...>/rebuttal_eval_lexicon_train.json

python scripts/rebuttal/eval_lexicon_project.py \
  --pred_json logs/<...>/rebuttal_eval_greedy_test.json \
  --lexicon_source all \
  --out_json logs/<...>/rebuttal_eval_lexicon_all.json
```

## 6) Repeat seeds 1,2 for CV
- Run steps 1–5 with `--seed 1` and `--seed 2` for split creation and training seeds.

## 7) Aggregate to rebuttal_numbers
```
python scripts/rebuttal/aggregate_rebuttal_numbers.py \
  --inputs logs/**/rebuttal_eval_*.json \
  --out_yaml rebuttal_numbers.yaml \
  --out_md rebuttal_numbers.md
```

Notes:
- SpecAug is **online only** via `--enable_online_specaug`; dataset prep stays fixed (PCA32).
- Aggregator writes both test and competition numbers; CV uses SpecAug-OFF greedy runs.
- Validation/checkpointing uses the **competition** partition by default; report numbers on **test**.
- If KenLM is used, train the LM **only on training transcripts (seed0)** and state this; otherwise omit B.

