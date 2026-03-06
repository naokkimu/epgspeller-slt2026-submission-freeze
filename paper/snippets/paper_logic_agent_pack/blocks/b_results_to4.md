# b_results_to4

- kind: `paragraph`
- status: `supported`
- section: Results (results) ([results](../sections/results.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md) kind=`table` path=`results/paper_layout_2026-03-03/table_to4_compact.csv` sha256=`81b08893439527b346bcbf828270dace69d5e3bacfaaf16b5ece081cee6bcc9d`
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md) kind=`data` path=`scripts/paper/export_layout_tables_for_paperjson.py` sha256=`0ba9e5c602e58596ac80f759c6b59baa1402a36433e31ebbf4012f3f77c23e8e`
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md) kind=`data` path=`results/uc20260226/split_npz_manifest_to4.csv` sha256=`8a00315026803e752c9fad58a43a002418ce52dbb338f14e8d46de630b65a766`
- [ev_uc20260226_to4_metrics_csv](../evidence/ev_uc20260226_to4_metrics_csv.md) kind=`data` path=`sweeps/uc20260226/results/uc_to4_metrics.csv` sha256=`2b0bf8251a917034ba20e90dd537fa0b67c56033de103b6aaf51d09a624e9ed2`

## Statements

### st_b_results_to4_01
We evaluate cross participant transfer with the fourth participant as target under single source and paired source settings.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)
- [ev_uc20260226_to4_metrics_csv](../evidence/ev_uc20260226_to4_metrics_csv.md)

### st_b_results_to4_02
The table uses protocol labels for single source cross participant transfer and multi source transfer.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)
- [ev_uc20260226_to4_metrics_csv](../evidence/ev_uc20260226_to4_metrics_csv.md)

### st_b_results_to4_03
The lvl field marks direction level rows and an across direction aggregate.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)
- [ev_uc20260226_to4_metrics_csv](../evidence/ev_uc20260226_to4_metrics_csv.md)

### st_b_results_to4_04
Group labels join source participant identifiers with an arrow to the target.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)
- [ev_uc20260226_to4_metrics_csv](../evidence/ev_uc20260226_to4_metrics_csv.md)

### st_b_results_to4_05
The split archives that define these targets are pinned by checksum in the manifest.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)
- [ev_uc20260226_to4_metrics_csv](../evidence/ev_uc20260226_to4_metrics_csv.md)

### st_b_results_to4_06
In our audited splits, the multi source aggregate reduces CER relative to the single source aggregate for the same target.

evidence_supports:
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md)
- [ev_scripts_paper_export_layout_tables_for_paperjson_py](../evidence/ev_scripts_paper_export_layout_tables_for_paperjson_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)
- [ev_uc20260226_to4_metrics_csv](../evidence/ev_uc20260226_to4_metrics_csv.md)
