# b_data_audit_2

- kind: `paragraph`
- status: `supported`
- section: Data and Protocols (data) ([data](../sections/data.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md) kind=`data` path=`results/dataset_audit_silentspeller_2026-02-24/exclusions/john_2328_exclude_indices.json` sha256=`8d7a0fcfb0107b812c88df69e66647af4c69f6a85b197783f5c07eff77a41188`
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md) kind=`document` path=`results/dataset_audit_silentspeller_2026-02-24/inputs_manifest.md` sha256=`32a33544de5bb7965809adfa4c62f7699d51e811d688f74e043feee0283169f5`
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md) kind=`document` path=`results/dataset_audit_silentspeller_2026-02-24/report.md` sha256=`143c09b739b8ee6dbfc81c41232cb5aca29d2cd1af52a9d2afb06eb823e8fb55`

## Statements

### st_b_data_audit_2_01
The audit pipeline records raw file checksums.

evidence_supports:
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md)
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md)
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md)

### st_b_data_audit_2_02
It validates schema consistency.

evidence_supports:
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md)
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md)
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md)

### st_b_data_audit_2_03
It summarizes label counts, sequence length summaries, and per channel activity statistics before any split construction.

evidence_supports:
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md)
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md)
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md)

### st_b_data_audit_2_04
The raw exports remain unchanged.

evidence_supports:
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md)
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md)
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md)

### st_b_data_audit_2_05
We apply any exclusions only through pinned index lists that are included in the audit artifacts.

evidence_supports:
- [ev_dataset_audit_silentspeller_2026_02_24_exclusions_json](../evidence/ev_dataset_audit_silentspeller_2026_02_24_exclusions_json.md)
- [ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md.md)
- [ev_dataset_audit_silentspeller_2026_02_24_report_md](../evidence/ev_dataset_audit_silentspeller_2026_02_24_report_md.md)
