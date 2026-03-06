# b_results_kshot

- kind: `paragraph`
- status: `supported`
- section: Results (results) ([results](../sections/results.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md) kind=`data` path=`sweeps/msx20260224/results/msx_all_metrics.csv` sha256=`5a0cff21afab9ccb14d2d3cbc15bb9257cca6d765ed8b26232d2e47b10e3f706`
- [ev_paper_layout_2026_03_03_table_kshot_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_kshot_compact_csv.md) kind=`table` path=`results/paper_layout_2026-03-03/table_kshot_compact.csv` sha256=`b479ae3875206eef2a242f0b946474d35efdb3b22d74dcf208e82dd3249c8b5f`
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md) kind=`data` path=`scripts/paper/export_layout_tables_for_paperjson.py` sha256=`0ba9e5c602e58596ac80f759c6b59baa1402a36433e31ebbf4012f3f77c23e8e`

## Statements

### st_b_results_kshot_01
We evaluate how models adapt in low shot settings for a new participant by varying the number of training instances per word.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_paper_layout_2026_03_03_table_kshot_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_kshot_compact_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)

### st_b_results_kshot_02
For the vector baseline, two shot improves over one shot, and the table reports layout aware variants.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_paper_layout_2026_03_03_table_kshot_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_kshot_compact_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)

### st_b_results_kshot_03
This isolates adaptation behavior when only a small amount of labeled target data is available.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_paper_layout_2026_03_03_table_kshot_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_kshot_compact_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
