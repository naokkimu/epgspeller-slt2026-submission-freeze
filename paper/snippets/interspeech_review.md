# Interspeech-style review (evidence-only; paper.json target bundle)

## Summary
This paper presents an evidence-only, protocol-explicit evaluation of open-vocabulary EPG silent spelling with audited artifacts and multi-participant splits.

## Scores (self-assessed from the target bundle)
- Depth: 3/5
- Originality: 2/5
- Correctness: 4/5
- Clarity: 3/5
- References: 3/5
- Impact: 3/5

## Strengths
- Strong auditability posture: dataset audits, pinned exclusions, and split manifests are explicitly referenced as artifacts. [CITE block=b_data_1,b_data_audit_2,b_artifacts evidence=ev_dataset_audit_silentspeller_2026_02_24_report_md,ev_dataset_audit_silentspeller_2026_02_24_exclusions_json,ev_msx20260224_split_npz_manifest_csv]
- Multi-protocol results are consolidated into compact tables spanning spatial variants, electrode reduction, cross-participant transfer, and low-shot adaptation. [CITE block=tbl_spatial_all,tbl_k64_all,tbl_to4_generalization,tbl_p3ms_compact,tbl_kshot_compact evidence=ev_paper_layout_2026_03_03_table_spatial_all_csv,ev_paper_layout_2026_03_03_table_k64_all_csv,ev_paper_layout_2026_03_03_table_to4_compact_csv,ev_paper_layout_2026_03_03_table_p3ms_compact_csv,ev_paper_layout_2026_03_03_table_kshot_compact_csv]
- The protocol definitions and deterministic split generation are clearly documented, including how participant four is used as a target-only case. [CITE block=b_protocols_1,b_protocols_2 evidence=ev_msx20260224_split_npz_manifest_csv,ev_uc20260226_split_npz_manifest_to4_csv]

## Weaknesses
- Quantitative comparisons are limited to internal variants; no external baselines appear in the results tables. [CITE block=tbl_spatial_all,tbl_k64_all evidence=ev_paper_layout_2026_03_03_table_spatial_all_csv,ev_paper_layout_2026_03_03_table_k64_all_csv]
- Cross-participant error remains substantially higher than within-participant protocols, and the discussion highlights the difficulty of transfer. [CITE block=tbl_spatial_all,b_discussion evidence=ev_paper_layout_2026_03_03_table_spatial_all_csv,ev_msx20260224_metrics_csv]
- Grid-based variants increase RTF and underperform relative to vector or row/column baselines across protocols. [CITE block=b_results_spatial,tbl_spatial_all evidence=ev_paper_layout_2026_03_03_table_spatial_all_csv,ev_uc20260226_spatial2d_patchpool_metrics_csv]

## Questions
- What are the sizes and construction sources of the training lexicon and full lexicon used for lexicon projection? [CITE block=b_metrics_1 evidence=ev_msx20260224_metrics_csv]
- For target participants with single-instance allowances, how many labels are retained and how does this affect comparability across protocols? [CITE block=b_protocols_1,b_protocols_2 evidence=ev_uc20260226_split_npz_manifest_to4_csv,ev_msx20260224_split_npz_manifest_csv]
- Are there cases where patchpool narrows the cross-participant gap without increasing RTF, and how stable is this across directions? [CITE block=b_results_spatial,tbl_spatial_all evidence=ev_uc20260226_spatial2d_patchpool_metrics_csv,ev_paper_layout_2026_03_03_table_spatial_all_csv]

## Required Fixes
- Add a short positioning sentence that clarifies why external quantitative baselines are not included, to avoid misinterpretation of the contribution scope. [CITE block=b_related_1 evidence=ev_related_work_survey_epgspeller_2026-02-17_report_md]
- Clarify lexicon projection setup (lexicon source and size) in the metrics description so readers can interpret lexicon-based CER. [CITE block=b_metrics_1 evidence=ev_msx20260224_metrics_csv]
