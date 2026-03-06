# b_results_1

- kind: `paragraph`
- status: `supported`
- section: Results (results) ([results](../sections/results.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md) kind=`data` path=`sweeps/msx20260224/results/msx_all_metrics.csv` sha256=`5a0cff21afab9ccb14d2d3cbc15bb9257cca6d765ed8b26232d2e47b10e3f706`
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md) kind=`data` path=`results/msx20260224/split_npz_manifest.csv` sha256=`8eef0bb574044a4d527c4a3d16a1fa17c31c3b61f83fc7c25a9f8462c5c33363`
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md) kind=`table` path=`results/paper_layout_2026-03-03/table_k64_all.csv` sha256=`9a69bc1ea1c313dcf85238842a8d31a786e62490f10294f10e23acf6ad9c0975`
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md) kind=`table` path=`results/paper_layout_2026-03-03/table_spatial_all.csv` sha256=`ff8592aec427fb489d9f278894b5dedbc7489f273a8a200d8dcc8d02c46a907c`
- [ev_scripts_rebuttal_eval_greedy_clean_py](../evidence/ev_scripts_rebuttal_eval_greedy_clean_py.md) kind=`data` path=`scripts/rebuttal/eval_greedy_clean.py` sha256=`a341ada9fb1e2b0d0a0754edf3e1c122bb9d253c627511256abf39441bfeb0fb`

## Statements

### st_b_results_1_01
Baseline performance across protocols is derived from the same metrics registry as the remaining tables.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md)
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_rebuttal_eval_greedy_clean_py](../evidence/ev_scripts_rebuttal_eval_greedy_clean_py.md)

### st_b_results_1_02
We report greedy decoding error and lexicon-projected error to separate open vocabulary decoding quality from lexicon constraints.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md)
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_rebuttal_eval_greedy_clean_py](../evidence/ev_scripts_rebuttal_eval_greedy_clean_py.md)

### st_b_results_1_03
The vector baseline rows in the spatial modeling and electrode reduction tables serve as the reference for protocol comparisons.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md)
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_rebuttal_eval_greedy_clean_py](../evidence/ev_scripts_rebuttal_eval_greedy_clean_py.md)

### st_b_results_1_04
We use the same split manifests and deterministic evaluation scripts across all protocols.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md)
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_rebuttal_eval_greedy_clean_py](../evidence/ev_scripts_rebuttal_eval_greedy_clean_py.md)
