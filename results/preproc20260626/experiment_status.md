# P1 6-8 Completion Status

## Scope

- Priority 6: train-only normalization ablation
- Priority 7: contact-rate matching / per-channel marginal normalization
- Priority 8: raw vs standardized vs PCA/no-PCA aggregation

## Completion

- Status: complete
- Matrix rows: 120 (6 directions x 4 seeds x 5 preprocessing conditions)
- Required eval artifacts:
  - `eval_greedy_test.json`: 120
  - `eval_lex_train.json`: 120
  - `eval_lex_all.json`: 120

## Artifacts

- Matrix:
  - `sweeps/preproc20260626/matrices/preproc20260626_to4_preproc.csv`
- Collected metrics (all rows complete):
  - `sweeps/preproc20260626/results/preproc20260626_to4_metrics.csv`
- Paper tables:
  - `results/preproc20260626/paper_tables/table_preproc_protocol_condition.csv`
  - `results/preproc20260626/paper_tables/table_preproc_direction_condition.csv`
- Summary report:
  - `results/preproc20260626/preproc_ablation_report.md`

## Conditions

- `raw_std`
- `raw_none`
- `raw_contact_match`
- `raw_target_marginal`
- `pca32_std`

## Headline CER (protocol-level, mean +- std)

- P3:
  - `raw_std`: 0.6893 +- 0.0951
  - `raw_none`: 0.6527 +- 0.0545
  - `raw_contact_match`: 0.6773 +- 0.0973
  - `raw_target_marginal`: 0.6426 +- 0.0811
  - `pca32_std`: 0.6960 +- 0.0836
- P3MS:
  - `raw_std`: 0.5818 +- 0.0535
  - `raw_none`: 0.5848 +- 0.0304
  - `raw_contact_match`: 0.5747 +- 0.0657
  - `raw_target_marginal`: 0.5692 +- 0.0544
  - `pca32_std`: 0.5919 +- 0.0523
