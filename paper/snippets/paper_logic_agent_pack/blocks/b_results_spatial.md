# b_results_spatial

- kind: `paragraph`
- status: `supported`
- section: Results (results) ([results](../sections/results.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md) kind=`table` path=`results/paper_layout_2026-03-03/table_spatial_all.csv` sha256=`ff8592aec427fb489d9f278894b5dedbc7489f273a8a200d8dcc8d02c46a907c`
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md) kind=`data` path=`scripts/paper/export_layout_tables_for_paperjson.py` sha256=`0ba9e5c602e58596ac80f759c6b59baa1402a36433e31ebbf4012f3f77c23e8e`
- [ev_uc20260226_spatial2d_patchpool_metrics_csv](../evidence/ev_uc20260226_spatial2d_patchpool_metrics_csv.md) kind=`data` path=`sweeps/uc20260226/results/uc_spatial2d_patchpool_metrics.csv` sha256=`c9734dbae7608ebcb578bf2f3b435fdc4cb19fc6b6878fcb7cb8e94ac5a5b4f7`

## Statements

### st_b_results_spatial_01
The spatial modeling table compares spatial inductive bias variants at full channels across protocols.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_spatial2d_patchpool_metrics_csv](../evidence/ev_uc20260226_spatial2d_patchpool_metrics_csv.md)

### st_b_results_spatial_02
We include a patchpool grid encoder as a minimal way to implement a rescue for the grid encoder.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_spatial2d_patchpool_metrics_csv](../evidence/ev_uc20260226_spatial2d_patchpool_metrics_csv.md)

### st_b_results_spatial_03
The patchpool variant keeps a coarser spatial map before recurrent decoding.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_spatial2d_patchpool_metrics_csv](../evidence/ev_uc20260226_spatial2d_patchpool_metrics_csv.md)

### st_b_results_spatial_04
The variant labels are vec, rowcol, grid, grid_aug, patch, and patch_aug.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_spatial2d_patchpool_metrics_csv](../evidence/ev_uc20260226_spatial2d_patchpool_metrics_csv.md)

### st_b_results_spatial_05
The row and column front end tracks the vector baseline more closely than the convolutional grid front end under within participant protocols.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_spatial2d_patchpool_metrics_csv](../evidence/ev_uc20260226_spatial2d_patchpool_metrics_csv.md)

### st_b_results_spatial_06
Patchpool reduces the gap under cross participant transfer.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_spatial2d_patchpool_metrics_csv](../evidence/ev_uc20260226_spatial2d_patchpool_metrics_csv.md)

### st_b_results_spatial_07
Across protocols, grid variants tend to increase real time factor relative to the vector baseline.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_spatial2d_patchpool_metrics_csv](../evidence/ev_uc20260226_spatial2d_patchpool_metrics_csv.md)

### st_b_results_spatial_08
We do not observe a consistent accuracy gain over the vector baseline in any protocol.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_spatial2d_patchpool_metrics_csv](../evidence/ev_uc20260226_spatial2d_patchpool_metrics_csv.md)
