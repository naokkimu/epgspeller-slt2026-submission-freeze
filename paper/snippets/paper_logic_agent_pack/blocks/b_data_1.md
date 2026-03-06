# b_data_1

- kind: `paragraph`
- status: `supported`
- section: Data and Protocols (data) ([data](../sections/data.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md) kind=`data` path=`results/dataset_audit_silentspeller_2026-02-24/exclusions/john_2328_exclude_indices.json` sha256=`8d7a0fcfb0107b812c88df69e66647af4c69f6a85b197783f5c07eff77a41188`
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md) kind=`document` path=`results/dataset_audit_silentspeller_2026-02-24/inputs_manifest.md` sha256=`32a33544de5bb7965809adfa4c62f7699d51e811d688f74e043feee0283169f5`
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md) kind=`document` path=`results/dataset_audit_silentspeller_2026-02-24/report.md` sha256=`143c09b739b8ee6dbfc81c41232cb5aca29d2cd1af52a9d2afb06eb823e8fb55`

## Statements

### st_b_data_1_01
We use four participant electropalatography datasets with word labels.

evidence_supports:
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md)
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md)
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md)

### st_b_data_1_02
Each sample is a variable length binary contact matrix, and the raw exports are treated as immutable evidence.

evidence_supports:
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md)
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md)
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md)

### st_b_data_1_03
We refer to participants with anonymous labels in all tables and split archives.

evidence_supports:
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md)
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md)
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md)

### st_b_data_1_04
We audit dataset statistics, label counts, and anomalies before we construct any train and test splits.

evidence_supports:
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md)
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md)
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md)

### st_b_data_1_05
We exclude a small set of all-zero samples via a pinned index list.

evidence_supports:
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md)
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md)
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md)
