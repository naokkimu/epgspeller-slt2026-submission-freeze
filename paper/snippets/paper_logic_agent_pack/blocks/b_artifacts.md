# b_artifacts

- kind: `paragraph`
- status: `supported`
- section: Artifacts and Auditability (artifacts) ([artifacts](../sections/artifacts.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md) kind=`data` path=`sweeps/msx20260224/results/msx_all_metrics.csv` sha256=`5a0cff21afab9ccb14d2d3cbc15bb9257cca6d765ed8b26232d2e47b10e3f706`
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md) kind=`data` path=`results/msx20260224/split_npz_manifest.csv` sha256=`8eef0bb574044a4d527c4a3d16a1fa17c31c3b61f83fc7c25a9f8462c5c33363`
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md) kind=`table` path=`results/paper_layout_2026-03-03/table_k64_all.csv` sha256=`9a69bc1ea1c313dcf85238842a8d31a786e62490f10294f10e23acf6ad9c0975`
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md) kind=`table` path=`results/paper_layout_2026-03-03/table_spatial_all.csv` sha256=`ff8592aec427fb489d9f278894b5dedbc7489f273a8a200d8dcc8d02c46a907c`
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md) kind=`table` path=`results/paper_layout_2026-03-03/table_to4_compact.csv` sha256=`81b08893439527b346bcbf828270dace69d5e3bacfaaf16b5ece081cee6bcc9d`
- [ev_uc20260226_p3ms_conditions_csv](../evidence/ev_uc20260226_p3ms_conditions_csv.md) kind=`data` path=`results/uc20260226/p3ms_conditions.csv` sha256=`a87d7100db6592493c49161fa0b33195b76fed13157544539bba251173616a7a`
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md) kind=`data` path=`results/uc20260226/split_npz_manifest_to4.csv` sha256=`8a00315026803e752c9fad58a43a002418ce52dbb338f14e8d46de630b65a766`

## Statements

### st_b_artifacts_01
This repository uses a strict paper registry that pins every evidence file by checksum and rejects unsupported manuscript blocks.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md)
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md)
- [ev_uc20260226_p3ms_conditions_csv](../evidence/ev_uc20260226_p3ms_conditions_csv.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)

### st_b_artifacts_02
The split manifests, aggregated metrics, compact tables, and analysis summaries referenced in this paper are stored as deterministic artifacts, enabling audit and reproduction within our repository environment.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md)
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md)
- [ev_uc20260226_p3ms_conditions_csv](../evidence/ev_uc20260226_p3ms_conditions_csv.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)

### st_b_artifacts_03
The same artifacts are reused to build the manuscript tables and to support verification in the audit views.

evidence_supports:
- [ev_msx20260224_metrics_csv](../evidence/ev_msx20260224_metrics_csv.md)
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_paper_layout_2026_03_03_table_k64_all_csv](../evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md)
- [ev_paper_layout_2026_03_03_table_spatial_all_csv](../evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- [ev_paper_layout_2026_03_03_table_to4_compact_csv](../evidence/ev_paper_layout_2026_03_03_table_to4_compact_csv.md)
- [ev_uc20260226_p3ms_conditions_csv](../evidence/ev_uc20260226_p3ms_conditions_csv.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)
