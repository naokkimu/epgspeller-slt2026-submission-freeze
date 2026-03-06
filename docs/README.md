# Rebuttal Runbook (epg_speller_base)

Use these steps to reproduce rebuttal numbers (one command at a time).

## Recent maintenance
- `paper/submission/interspeech2026_review_manual.tex` now imports `float` (`\usepackage{float}`).
- Reason: tables using `[H]` require the `float` package; without it, LaTeX reports `Unknown float option 'H'`.

## 0) Sanity after prepare
- After dataset pickle is created, ensure target IDs are within A–Z: built-in assertion (`max_id <= 26`) will stop if violated.

## 1) Make word-holdout split (seed example)
```
python scripts/rebuttal/make_word_holdout_split.py \
  --raw_npz raw/silentspeller_dataset/p1_2328_old_dataset.npz \
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
  --n_classes 26

python scripts/train.py \
  --dataset_path data/rebuttal_pca32_seed0 \
  --model_name rebuttal_seed0_pca32_specaug \
  --n_units 1024 --n_layers 5 --n_batch 10000 --seed 0 \
  --enable_online_specaug true \
  --n_classes 26
```

## Protocol-S (seen-word / instance holdout)

Protocol-S keeps the **vocabulary seen** in training while holding out **one instance per word** for test.
This repo assumes the SilentSpeller raw datasets have **exactly 2 renditions per word** (2328 samples = 1164 words × 2).

### 1) Make instance-holdout split (subject1/subject2)
```
python scripts/rebuttal/make_instance_holdout_split.py \
  --raw_npz raw/silentspeller_dataset/p1_2328_old_dataset.npz \
  --seed 0 --n_competition_words 50 \
  --out_npz raw_dataset/protocolS_split_seed0_subj1_ds1.npz

python scripts/rebuttal/make_instance_holdout_split.py \
  --raw_npz raw/silentspeller_dataset/thad_2328_old_dataset.npz \
  --seed 0 --n_competition_words 50 \
  --out_npz raw_dataset/protocolS_split_seed0_subj2_ds1.npz
```

### 2) Prepare PCA32 dataset from Protocol-S split
```
python scripts/prepare_silentspeller_dataset.py \
  --split_path raw_dataset/protocolS_split_seed0_subj1_ds1.npz \
  --n_components 32 \
  --output_path data/protocolS_seed0_subj1_ds1_pca32
```

### 3) Train (noaug first)
Note: `--enable_online_specaug` is a **flag**. Omit it for no-aug.
```
CUDA_VISIBLE_DEVICES=0 python scripts/train.py \
  --dataset_path data/protocolS_seed0_subj2_ds1_pca32 \
  --model_name protocolS_s0_subj2_ds1_noaug \
  --n_classes 26 --seed 0 \
  --n_units 1024 --n_layers 5 --n_batch 10000
```

### 4) Evaluate (test is the main Protocol-S metric)
```
python scripts/rebuttal/eval_greedy_clean.py \
  --model_path logs/<...protocolS_s0_subj2_ds1_noaug...> \
  --partition test --device cuda \
  --out_json logs/<...>/protocolS_eval_greedy_test.json

python scripts/rebuttal/eval_greedy_clean.py \
  --model_path logs/<...protocolS_s0_subj2_ds1_noaug...> \
  --partition competition --device cuda \
  --out_json logs/<...>/protocolS_eval_greedy_comp.json

python scripts/rebuttal/eval_lexicon_project.py \
  --pred_json logs/<...>/protocolS_eval_greedy_test.json \
  --lexicon_source train \
  --out_json logs/<...>/protocolS_eval_lex_train.json
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

Notes for lexicon projection:
- Lexicon words are normalized to **uppercase** internally to match greedy outputs.
- With word-holdout splits, `lexicon_source=train` does not contain test vocabulary; expect WER=1.0 but CER < 1.0 after projection.
- `lexicon_source=all` is an **oracle vocabulary (upper bound)**; use only as a sanity/upper bound, not for conclusions.

Label mapping used in aggregation:
- A = SpecAug **OFF** greedy (seed0, test; competition optionally logged)
- D = SpecAug **ON** greedy (seed0, test; competition optionally logged)
- E = alias of A (SpecAug OFF, seed0)
- C_train = lexicon projection with train vocabulary (seed0 test)
- C_all = lexicon projection with oracle/all vocabulary (seed0 test, upper bound)
- CV = mean±std over SpecAug OFF greedy test runs (seeds 0/1/2)

## 6) Repeat seeds 1,2 for CV
- Run steps 1–5 with `--seed 1` and `--seed 2` for split creation and training seeds.

## 7) Aggregate to rebuttal_numbers
```
python scripts/rebuttal/aggregate_rebuttal_numbers.py \
  --inputs logs/**/rebuttal_eval_*.json logs/**/protocolS_eval_*.json \
  --out_yaml rebuttal_numbers.yaml \
  --out_md rebuttal_numbers.md
```

## Rebuttal response draft
- A repo-local rebuttal draft is maintained at `rebuttal_response.md` (copy-paste into the submission form).

Notes:
- SpecAug is **online only** via `--enable_online_specaug`; dataset prep stays fixed (PCA32).
- Aggregator writes both test and competition numbers; CV uses SpecAug-OFF greedy runs.
- Validation/checkpointing uses the **competition** partition by default; report numbers on **test**.
- If KenLM is used, train the LM **only on training transcripts (seed0)** and state this; otherwise omit B.

