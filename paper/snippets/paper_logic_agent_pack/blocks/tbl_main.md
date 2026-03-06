# tbl_main

- kind: `table`
- status: `supported`
- section: Results (results) ([results](../sections/results.md))
- generated_utc: 2026-03-02T08:36:31+00:00

## Evidence (ids)
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md) kind=`data` path=`sweeps/msx20260224/results/msx_all_metrics.csv` sha256=`5a0cff21afab9ccb14d2d3cbc15bb9257cca6d765ed8b26232d2e47b10e3f706`
- [ev_msx20260224_table_main_csv](../evidence/ev_msx20260224_table_main_csv.md) kind=`table` path=`results/msx20260224/paper_tables/table_main.csv` sha256=`dff6b3436c265008bc53754745b6fd44b0cd6fcca7bd92a34fcf7d1f13ae9570`
- [ev_scripts_paper_export_msx_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_msx_tables_for_paperjson_py.md) kind=`data` path=`scripts/paper/export_msx_tables_for_paperjson.py` sha256=`2100f045c5b121e7167cbb5cb59136bc2e6d61f8b64b2663f8fc317e4d801e84`

## Statements

### st_tbl_main_01
[TABLE] label=tab:main source_evidence_id=ev_msx20260224_table_main_csv Caption: Baseline recap across three evaluation protocols (mean and standard deviation over groups).

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_msx20260224_table_main_csv](../evidence/ev_msx20260224_table_main_csv.md)
- [ev_scripts_paper_export_msx_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_msx_tables_for_paperjson_py.md)
