# tbl_k64_all

- kind: `table`
- status: `supported`
- section: Results (results) ([results](../sections/results.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md) kind=`data` path=`sweeps/msx20260224/results/msx_all_metrics.csv` sha256=`5a0cff21afab9ccb14d2d3cbc15bb9257cca6d765ed8b26232d2e47b10e3f706`
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md) kind=`table` path=`results/paper_layout_2026-03-03/table_k64_all.csv` sha256=`9a69bc1ea1c313dcf85238842a8d31a786e62490f10294f10e23acf6ad9c0975`
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md) kind=`data` path=`scripts/paper/export_layout_tables_for_paperjson.py` sha256=`0ba9e5c602e58596ac80f759c6b59baa1402a36433e31ebbf4012f3f77c23e8e`

## Statements

### st_tbl_k64_all_01
[TABLE] label=tab:k64_all source_evidence_id=ev_paper_layout_2026_03_03_table_k64_all_csv Caption: Electrode reduction methods across protocols; protocol labels denote word holdout, instance holdout, and cross participant transfer, topk is within participant top ranked selection, fps two k is farthest point sampling, xfer is transfer selection, rand is random selection, CER is character error rate, and RTF is real time factor.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
