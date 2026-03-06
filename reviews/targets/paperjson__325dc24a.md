# paper.json review target bundle

## Input
```json
{
  "format": {
    "name": "paper-json",
    "version": "1.0.0"
  },
  "manuscript": {
    "language": "en",
    "paper_type": "regular",
    "stage": "review",
    "title": "EPGSpeller: Lexicon-Free Silent Spelling Recognition with Electropalatography",
    "venue": "interspeech"
  },
  "paper_json": "paper/paper.json",
  "paper_json_sha256": "325dc24abd4f2ac0c8515a9408dd36568bae6d0e4d9a272d5ec7ebd3cd9b2b6a",
  "policy": {
    "allowlist_block_kinds": [
      "paragraph",
      "bullets",
      "table",
      "figure",
      "equation"
    ],
    "banned_token_re": "\\b(TBD|TODO|placeholder|mock)\\b",
    "forbid_digits_in_templates": false,
    "strict_evidence_for_manuscript": true
  }
}
```

## Lint (CI gate)
```json
{
  "command": [
    "python3",
    "$CODEX_HOME/skills/paperjson-init/assets/toolkit/paper_json_lint.py",
    "--paper-json",
    "paper/paper.json",
    "--root",
    ".",
    "--ci",
    "--expected-version",
    "1.0.0"
  ],
  "errors": [],
  "implementation": "bundled",
  "returncode": 0,
  "warnings": []
}
```

## Evidence (referenced by manuscript)
```json
[
  {
    "bytes": 202,
    "id": "ev_ai_disclosure_2026_03_04_md",
    "kind": "document",
    "path": "results/ai_disclosure_2026-03-04.md",
    "sha256": "9bd5402079858ef56448e0221c86bde0eccf388265a088f13b4823ac4d7dc0d8"
  },
  {
    "bytes": 215,
    "id": "ev_dataset_audit_silentspeller_2026_02_24_exclusions_json",
    "kind": "data",
    "path": "results/dataset_audit_silentspeller_2026-02-24/exclusions/john_2328_exclude_indices.json",
    "sha256": "8d7a0fcfb0107b812c88df69e66647af4c69f6a85b197783f5c07eff77a41188"
  },
  {
    "bytes": 18195,
    "id": "ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md",
    "kind": "document",
    "path": "results/dataset_audit_silentspeller_2026-02-24/inputs_manifest.md",
    "sha256": "32a33544de5bb7965809adfa4c62f7699d51e811d688f74e043feee0283169f5"
  },
  {
    "bytes": 25260,
    "id": "ev_dataset_audit_silentspeller_2026_02_24_report_md",
    "kind": "document",
    "path": "results/dataset_audit_silentspeller_2026-02-24/report.md",
    "sha256": "143c09b739b8ee6dbfc81c41232cb5aca29d2cd1af52a9d2afb06eb823e8fb55"
  },
  {
    "bytes": 20654,
    "id": "ev_docs_report_figures_ed20260217_cer_rtf_vs_k_pdf",
    "kind": "figure",
    "path": "docs/report/figures/ed20260217/cer_rtf_vs_k.pdf",
    "sha256": "53bc574b546de3d04b2a6cadf59d55679e5e3a06131436fb164fbbb6e1164fa2"
  },
  {
    "bytes": 1750,
    "id": "ev_ed20260217_h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17",
    "kind": "table",
    "path": "results/ed20260217/paperjson/h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17.csv",
    "sha256": "0cd1fecedc166c732da45187356434c85c9316a546151dd6d5100e6caec19284"
  },
  {
    "bytes": 928072,
    "id": "ev_msx20260224_metrics_csv",
    "kind": "data",
    "path": "sweeps/msx20260224/results/msx_all_metrics.csv",
    "sha256": "5a0cff21afab9ccb14d2d3cbc15bb9257cca6d765ed8b26232d2e47b10e3f706"
  },
  {
    "bytes": 10683,
    "id": "ev_msx20260224_split_npz_manifest_csv",
    "kind": "data",
    "path": "results/msx20260224/split_npz_manifest.csv",
    "sha256": "8eef0bb574044a4d527c4a3d16a1fa17c31c3b61f83fc7c25a9f8462c5c33363"
  },
  {
    "bytes": 963,
    "id": "ev_msx20260224_table_k64_methods_csv",
    "kind": "table",
    "path": "results/msx20260224/paper_tables/table_k64_methods.csv",
    "sha256": "4deb9957f723e91475a974b20ff5e6a105ffed8d40646901d7df8cae18b93573"
  },
  {
    "bytes": 832,
    "id": "ev_msx20260224_table_spatial_k124_csv",
    "kind": "table",
    "path": "results/msx20260224/paper_tables/table_spatial_k124.csv",
    "sha256": "74bd2da304d330f3230103baede46960f994dfcd55563d2f6021fddc1d87240e"
  },
  {
    "bytes": 126,
    "id": "ev_paper_layout_2026_03_03_table_dataset_summary_csv",
    "kind": "table",
    "path": "results/paper_layout_2026-03-03/table_dataset_summary.csv",
    "sha256": "0003d67eaefbb1eaa49702c94f3f5b7d73b137754a7d346cdc458723580e2bef"
  },
  {
    "bytes": 472,
    "id": "ev_paper_layout_2026_03_03_table_k64_all_csv",
    "kind": "table",
    "path": "results/paper_layout_2026-03-03/table_k64_all.csv",
    "sha256": "9a69bc1ea1c313dcf85238842a8d31a786e62490f10294f10e23acf6ad9c0975"
  },
  {
    "bytes": 353,
    "id": "ev_paper_layout_2026_03_03_table_kshot_compact_csv",
    "kind": "table",
    "path": "results/paper_layout_2026-03-03/table_kshot_compact.csv",
    "sha256": "b479ae3875206eef2a242f0b946474d35efdb3b22d74dcf208e82dd3249c8b5f"
  },
  {
    "bytes": 116,
    "id": "ev_paper_layout_2026_03_03_table_main_compact_csv",
    "kind": "table",
    "path": "results/paper_layout_2026-03-03/table_main_compact.csv",
    "sha256": "6dd26a458542b1cabbd03b1df56816de18a27dff0c76eb2b6bcde3cdc3d266d6"
  },
  {
    "bytes": 542,
    "id": "ev_paper_layout_2026_03_03_table_p3ms_compact_csv",
    "kind": "table",
    "path": "results/paper_layout_2026-03-03/table_p3ms_compact.csv",
    "sha256": "e662c605c765183c5fd7fc5314934242e0c9cf3877edff192864180dd72fed1f"
  },
  {
    "bytes": 689,
    "id": "ev_paper_layout_2026_03_03_table_spatial_all_csv",
    "kind": "table",
    "path": "results/paper_layout_2026-03-03/table_spatial_all.csv",
    "sha256": "ff8592aec427fb489d9f278894b5dedbc7489f273a8a200d8dcc8d02c46a907c"
  },
  {
    "bytes": 2454,
    "id": "ev_paper_layout_2026_03_03_table_stats_compact_csv",
    "kind": "table",
    "path": "results/paper_layout_2026-03-03/table_stats_compact.csv",
    "sha256": "c5f846b805626bb0dc75c7ad2c2686ca5f13975b12f750775de95e66269df012"
  },
  {
    "bytes": 366,
    "id": "ev_paper_layout_2026_03_03_table_to4_compact_csv",
    "kind": "table",
    "path": "results/paper_layout_2026-03-03/table_to4_compact.csv",
    "sha256": "81b08893439527b346bcbf828270dace69d5e3bacfaaf16b5ece081cee6bcc9d"
  },
  {
    "bytes": 8557,
    "id": "ev_positioning_analysis_epgspeller_2026_02_18_report_md",
    "kind": "document",
    "path": "results/positioning_analysis_epgspeller_2026-02-18/report.md",
    "sha256": "94f8a086cc48489bf7b1377903b996aca2e7617b25b933cd41c6af8c75ccf356"
  },
  {
    "bytes": 5147,
    "id": "ev_references_sanitized_ascii_cited_bib",
    "kind": "bibtex",
    "path": "paper/bibliography/references_sanitized_ascii_cited.bib",
    "sha256": "0e5d05c87e7a6d9c75385e1719ac9d621d593a7d644298d521e9a1c51003125f"
  },
  {
    "bytes": 10496,
    "id": "ev_related_work_survey_epgspeller_2026-02-17_report_md",
    "kind": "document",
    "path": "results/related_work_survey_epgspeller_2026-02-17/report.md",
    "sha256": "3ee6f36219209631bb14cf2b8639d6f70fe3b896a0e903be8164818edf14fe55"
  },
  {
    "bytes": 16947,
    "id": "ev_scripts_paper_export_layout_tables_for_paperjson_py",
    "kind": "data",
    "path": "scripts/paper/export_layout_tables_for_paperjson.py",
    "sha256": "0ba9e5c602e58596ac80f759c6b59baa1402a36433e31ebbf4012f3f77c23e8e"
  },
  {
    "bytes": 21164,
    "id": "ev_scripts_paper_export_stats_table_for_paperjson_py",
    "kind": "data",
    "path": "scripts/paper/export_stats_table_for_paperjson.py",
    "sha256": "ca8f529ef532e16b626264a2be592d347b04e3cfd4f4ee33a1ca38f73fce44ff"
  },
  {
    "bytes": 24653,
    "id": "ev_scripts_prepare_silentspeller_dataset_py",
    "kind": "data",
    "path": "scripts/prepare_silentspeller_dataset.py",
    "sha256": "0c13a2f8d7bb7f470851d1928acd1bf51633b42d532c4dc1cbd746f4fb9d69aa"
  },
  {
    "bytes": 8058,
    "id": "ev_scripts_rebuttal_eval_greedy_clean_py",
    "kind": "data",
    "path": "scripts/rebuttal/eval_greedy_clean.py",
    "sha256": "a341ada9fb1e2b0d0a0754edf3e1c122bb9d253c627511256abf39441bfeb0fb"
  },
  {
    "bytes": 10012,
    "id": "ev_scripts_rebuttal_gc_collect_metrics_py",
    "kind": "data",
    "path": "scripts/rebuttal/gc_collect_metrics.py",
    "sha256": "13570f95d81749e176dfb80fdca6f90fa67f7aef83af032e7a57480883e19307"
  },
  {
    "bytes": 12310,
    "id": "ev_scripts_rebuttal_gc_make_cmdlists_py",
    "kind": "data",
    "path": "scripts/rebuttal/gc_make_cmdlists.py",
    "sha256": "b7f5786fc095cdb40def676d32c0ba08e52b5654dee446494ba48581192a459f"
  },
  {
    "bytes": 14377,
    "id": "ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py",
    "kind": "data",
    "path": "scripts/rebuttal/make_cross_subject_instance_holdout_split.py",
    "sha256": "7c41255d135ad856637c39c7ac3162041a18d71a53b043a2c97c226157e0b87c"
  },
  {
    "bytes": 10763,
    "id": "ev_scripts_rebuttal_make_instance_holdout_split_py",
    "kind": "data",
    "path": "scripts/rebuttal/make_instance_holdout_split.py",
    "sha256": "07041c24ac0120a854ca55921017f9e628510b7e0b783e8bf74b55f3b6c783e2"
  },
  {
    "bytes": 10303,
    "id": "ev_scripts_rebuttal_make_kshot_instance_holdout_split_py",
    "kind": "data",
    "path": "scripts/rebuttal/make_kshot_instance_holdout_split.py",
    "sha256": "246e41e934eb225d74fc6a738d880c2f16336112b7f8ccb4450bc4c09ff1c763"
  },
  {
    "bytes": 16396,
    "id": "ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py",
    "kind": "data",
    "path": "scripts/rebuttal/make_multi_source_cross_subject_instance_holdout_split.py",
    "sha256": "4b831294d8fab58c02d485c6197ce3fdce4ab8104f7d771417b876dbc7254b34"
  },
  {
    "bytes": 5817,
    "id": "ev_scripts_rebuttal_make_word_holdout_split_py",
    "kind": "data",
    "path": "scripts/rebuttal/make_word_holdout_split.py",
    "sha256": "29765a348234ddafcd7c0bb3aeedc3dad1813fa863da921039dcf2b5e4be5065"
  },
  {
    "bytes": 802,
    "id": "ev_scripts_smartpalate_distribution_csv",
    "kind": "data",
    "path": "scripts/smartpalate_distribution.csv",
    "sha256": "d21d93c9ec3c0ecd6676908c8d8bc58ea2019533260b883c3d0a3b86213c0b84"
  },
  {
    "bytes": 10256,
    "id": "ev_scripts_train_py",
    "kind": "data",
    "path": "scripts/train.py",
    "sha256": "9fe71a8eff17ed9d4e8f249a55c2d805e2b011b3068ae75ab47eedb9d3593853"
  },
  {
    "bytes": 36552,
    "id": "ev_src_neural_decoder_model_py",
    "kind": "data",
    "path": "src/neural_decoder/model.py",
    "sha256": "738e9282960ff03c3d378c3c9f5862ba2d9bde7570822a57e764b42069aed5ed"
  },
  {
    "bytes": 2454,
    "id": "ev_supplementary_table_stats_compact_csv",
    "kind": "data",
    "path": "paper/supplementary/table_stats_compact.csv",
    "sha256": "c5f846b805626bb0dc75c7ad2c2686ca5f13975b12f750775de95e66269df012"
  },
  {
    "bytes": 522136,
    "id": "ev_sweeps_ed20260217_results_ed20260217_vector_full_with_random_csv",
    "kind": "data",
    "path": "sweeps/ed20260217/results/ed20260217.vector_full_with_random.csv",
    "sha256": "c151b5e1941318c9f88855979afdce5a29198c521adf6c752073e020ccffdec9"
  },
  {
    "bytes": 1876,
    "id": "ev_uc20260226_p3ms_conditions_csv",
    "kind": "data",
    "path": "results/uc20260226/p3ms_conditions.csv",
    "sha256": "a87d7100db6592493c49161fa0b33195b76fed13157544539bba251173616a7a"
  },
  {
    "bytes": 1341,
    "id": "ev_uc20260226_p3ms_conditions_md",
    "kind": "document",
    "path": "docs/report/p3ms_conditions_2026-02-26.md",
    "sha256": "59fac410e5e864470cd6950109ef23be3b9e5fa0d76e3d3f846444b44dfeeeca"
  },
  {
    "bytes": 155374,
    "id": "ev_uc20260226_spatial2d_patchpool_metrics_csv",
    "kind": "data",
    "path": "sweeps/uc20260226/results/uc_spatial2d_patchpool_metrics.csv",
    "sha256": "c9734dbae7608ebcb578bf2f3b435fdc4cb19fc6b6878fcb7cb8e94ac5a5b4f7"
  },
  {
    "bytes": 3623,
    "id": "ev_uc20260226_split_npz_manifest_to4_csv",
    "kind": "data",
    "path": "results/uc20260226/split_npz_manifest_to4.csv",
    "sha256": "8a00315026803e752c9fad58a43a002418ce52dbb338f14e8d46de630b65a766"
  },
  {
    "bytes": 31771,
    "id": "ev_uc20260226_to4_metrics_csv",
    "kind": "data",
    "path": "sweeps/uc20260226/results/uc_to4_metrics.csv",
    "sha256": "2b0bf8251a917034ba20e90dd537fa0b67c56033de103b6aaf51d09a624e9ed2"
  }
]
```

## Manuscript (resolved; block_id-anchored)

### Section: Abstract (id=abstract)

#### Block b_abs (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_dataset_audit_silentspeller_2026_02_24_report_md, ev_msx20260224_split_npz_manifest_csv, ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_paper_layout_2026_03_03_table_to4_compact_csv, ev_uc20260226_to4_metrics_csv

Text:
```text
We show that lexicon-free electropalatography (EPG) silent spelling can reach low error in audited within-participant settings (CER 0.180+/-0.084 in P1 and 0.145+/-0.063 in P2). Protocol mixing still obscures progress when word holdout, instance holdout, and cross-participant transfer are reported together. We present EPGSpeller, an auditable benchmark with deterministic splits, checksum-pinned artifacts, and a shared CER/LEX/RTF harness for protocol-matched comparison. In 652 audited runs, P3 remains much harder (CER 0.691+/-0.133), marking transfer mismatch as the main bottleneck. Rowcol stays closest to vec, while grid variants are usually higher in CER and RTF. For p4 target transfer, paired-source aggregation improves the all-direction aggregate (CER 0.686+/-0.114 to 0.582+/-0.064; LEX 0.659+/-0.073 to 0.554+/-0.034), but effects remain mixed by direction. We therefore treat deployment claims as protocol-specific and limit conclusions to audited datasets and definitions.
```

Slot trace:
```json
{}
```

### Section: Introduction (id=intro)

#### Block b_intro_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_related_work_survey_epgspeller_2026-02-17_report_md
- citations: denby2010silent, freitas2017an, gonzalez2020silent, lee2021biosignal, hardcastle1989new, hardcastle1990electropalatography, verhoeven2019visualisation, woo2021design

Text:
```text
Silent speech interfaces (SSI) infer linguistic intent from non-acoustic signals, including articulatory sensing and other biosignals. For silent spelling with electropalatography (EPG), a practical failure remains: many evaluations mix word-identity holdout, repeated-instance holdout, and cross-participant transfer, so reported gains can reflect protocol differences rather than decoder differences.
```

Slot trace:
```json
{}
```

#### Block b_intro_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_related_work_survey_epgspeller_2026-02-17_report_md, ev_positioning_analysis_epgspeller_2026_02_18_report_md
- citations: denby2010silent, dong2024rehearsse, gilbert2010isolated, graves2006connectionist, kimura2022silentspeller, hueber2010development, hardcastle1991epg, carreira1998dimensionality, shadle1993depth, toutios2006learning, toutios2006on

Text:
```text
Recent systems such as SilentSpeller and ReHEarSSE show lexicon-scale character-level spelling beyond small command sets. However, these lines of work do not provide a unified, auditable protocol stack that isolates each generalization regime under a shared artifact trace. In parallel, prior EPG studies motivate structured representations and spatial inductive bias, but their evaluation settings are heterogeneous across datasets and tasks.
```

Slot trace:
```json
{}
```

#### Block b_intro_3 (kind=paragraph)
- status: supported
- evidence_ids: ev_related_work_survey_epgspeller_2026-02-17_report_md, ev_positioning_analysis_epgspeller_2026_02_18_report_md, ev_msx20260224_metrics_csv, ev_msx20260224_split_npz_manifest_csv
- citations: hardcastle1991epg, carreira1998dimensionality, shadle1993depth, toutios2006learning, toutios2006on

Text:
```text
To address this gap, we introduce EPGSpeller, an evidence-tracked evaluation framework for EPG silent spelling. EPGSpeller fixes deterministic split generation, pinned split manifests, and a common metric harness for greedy decoding, lexicon projection, and streaming cost. It explicitly separates word holdout, instance holdout, and cross-participant transfer so model comparisons remain protocol-specific and reproducible. We validate EPGSpeller with four participant datasets and compare a vector baseline with row-column and grid-based front ends under matched settings. We also evaluate electrode reduction and low-shot adaptation under the same audit rules. Across our audited runs, row-column pooling tracks the vector baseline more consistently than grid variants, while cross-participant transfer remains the dominant bottleneck.
```

Slot trace:
```json
{}
```

#### Block b_intro_claim (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_msx20260224_split_npz_manifest_csv

Text:
```text
Within these audited datasets and protocol definitions, protocol-level auditability is necessary for interpretable benchmarking.
```

Slot trace:
```json
{}
```

#### Block b_contrib (kind=bullets)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_msx20260224_split_npz_manifest_csv, ev_msx20260224_table_spatial_k124_csv, ev_msx20260224_table_k64_methods_csv, ev_scripts_rebuttal_gc_make_cmdlists_py, ev_scripts_rebuttal_gc_collect_metrics_py

Text:
```text
- We define deterministic protocol families that isolate word-identity, instance-level, and cross-participant generalization.
- We provide checksum-pinned split archives and manifests so each reported result is reproducible from audited artifacts.
- We benchmark vector, row-column, and grid front ends under a shared evaluation harness with accuracy and streaming metrics.
- We report electrode-reduction and low-shot analyses under the same protocol constraints.
```

Slot trace:
```json
{
  "0": {},
  "1": {},
  "2": {},
  "3": {}
}
```

### Section: Data and Protocols (id=data)

#### Block b_data_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_dataset_audit_silentspeller_2026_02_24_report_md, ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md, ev_dataset_audit_silentspeller_2026_02_24_exclusions_json

Text:
```text
We use four participant electropalatography datasets with word labels. Each sample is a variable length binary contact matrix, and the raw exports are treated as immutable evidence. We refer to participants with anonymous labels in all tables and split archives. We audit dataset statistics, label counts, and anomalies before we construct any train and test splits. We exclude a small set of all-zero samples via a pinned index list.
```

Slot trace:
```json
{}
```

#### Block b_data_audit_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_dataset_audit_silentspeller_2026_02_24_report_md, ev_dataset_audit_silentspeller_2026_02_24_inputs_manifest_md, ev_dataset_audit_silentspeller_2026_02_24_exclusions_json

Text:
```text
The audit pipeline records raw file checksums. It validates schema consistency. It summarizes label counts, sequence length summaries, and per channel activity statistics before any split construction. The raw exports remain unchanged. We apply any exclusions only through pinned index lists that are included in the audit artifacts.
```

Slot trace:
```json
{}
```

#### Block b_data_summary (kind=paragraph)
- status: supported
- evidence_ids: ev_dataset_audit_silentspeller_2026_02_24_report_md, ev_paper_layout_2026_03_03_table_dataset_summary_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Table~\ref{tab:dataset} reports sample count, vocabulary size, median sequence length, mean contact rate, and all-zero count for each participant dataset. The id labels are anonymous participant codes used throughout the protocol manifests.
```

Slot trace:
```json
{}
```

#### Block tbl_dataset_summary (kind=table)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_dataset_summary_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py
- source_evidence_id: ev_paper_layout_2026_03_03_table_dataset_summary_csv

Text:
```text
[TABLE] label=tab:dataset source_evidence_id=ev_paper_layout_2026_03_03_table_dataset_summary_csv
Caption: Raw dataset summary for each participant dataset; id is an anonymous participant label, N is sample count, V is vocabulary size, Tmed is median sequence length in frames, contact is mean contact rate, and zero is the count of all-zero samples.
```

Slot trace:
```json
{}
```

#### Block b_protocols_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_split_npz_manifest_csv, ev_uc20260226_split_npz_manifest_to4_csv, ev_scripts_rebuttal_make_word_holdout_split_py, ev_scripts_rebuttal_make_instance_holdout_split_py, ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py, ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py, ev_scripts_rebuttal_make_kshot_instance_holdout_split_py

Text:
```text
We evaluate three primary protocols. The word holdout protocol uses disjoint vocabularies across train, test, and a competition partition. The instance holdout protocol tests held out instances of seen words. It separates train and competition vocabularies while keeping the test vocabulary within their union. The cross participant protocol trains on a source participant and tests on a target participant under a shared vocabulary constraint. We also define a paired source cross participant variant and a low shot adaptation variant to isolate source aggregation and limited supervision effects under the same audit rules. When a target participant has limited within word repetition, we configure the cross participant split generators to allow single instance target words. We keep the source side constraints unchanged. All split archives used in this study are enumerated with sizes and checksums in manifest artifacts.
```

Slot trace:
```json
{}
```

#### Block b_protocols_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_dataset_audit_silentspeller_2026_02_24_report_md, ev_msx20260224_split_npz_manifest_csv, ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py, ev_scripts_rebuttal_make_instance_holdout_split_py, ev_scripts_rebuttal_make_kshot_instance_holdout_split_py, ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py, ev_scripts_rebuttal_make_word_holdout_split_py, ev_uc20260226_split_npz_manifest_to4_csv

Text:
```text
All split archives are generated deterministically from audited exports with fixed seeds. Each train, test, and competition partition is stored as an immutable archive with a checksum in the manifests to enable reuse and later verification. The manifests show the word-holdout protocol uses all four participant datasets. They show the instance-holdout protocol uses three participant datasets. They also show the fourth participant is target-only (not used as a source) in the cross-participant splits. The audited label histogram for the fourth participant is dominated by single-instance labels, so we restrict that participant to target-only use in cross-participant evaluation. This separation explains why the dataset summary includes all participant datasets even when a protocol uses only a subset.
```

Slot trace:
```json
{}
```

#### Block b_labels_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_scripts_prepare_silentspeller_dataset_py, ev_scripts_rebuttal_make_word_holdout_split_py, ev_scripts_rebuttal_make_instance_holdout_split_py

Text:
```text
We normalize labels by uppercasing and filtering to alphabet characters, then represent each label as a space separated character sequence for CTC training and greedy decoding. We apply this step consistently during split construction and dataset preparation to avoid vocabulary drift.
```

Slot trace:
```json
{}
```

#### Block b_labels_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_scripts_prepare_silentspeller_dataset_py, ev_scripts_rebuttal_make_word_holdout_split_py, ev_scripts_rebuttal_make_instance_holdout_split_py

Text:
```text
We keep the label normalization step consistent across all splits and dataset preparation steps. This aligns the decoder vocabulary with the audited labels and reduces drift between training and artifacts used to evaluate.
```

Slot trace:
```json
{}
```

#### Block b_metrics_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_scripts_rebuttal_eval_greedy_clean_py, ev_scripts_rebuttal_gc_collect_metrics_py

Text:
```text
We report character error rate from greedy decoding and streaming speed using real time factor. We define real time factor as total inference time divided by total input duration. For character-level decoding we also report lexicon projection error rates using a training lexicon and a full lexicon.
```

Slot trace:
```json
{}
```

#### Block b_metrics_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py, ev_scripts_rebuttal_eval_greedy_clean_py, ev_scripts_rebuttal_gc_collect_metrics_py, ev_supplementary_table_stats_compact_csv

Text:
```text
Greedy decoding reports unconstrained character sequences. Lexicon projection maps outputs to finite word sets derived from the training vocabulary or the full audited lexicon. This allows us to separate decoding quality from lexicon constraints. We compute real time factor by dividing inference time by input duration under the same test harness. Tables summarize results over four split seeds as mean and standard deviation. We compute two sided t distribution confidence intervals for the primary accuracy metric and paired t tests with Holm correction; the compact statistical summary table is provided in the supplementary archive.
```

Slot trace:
```json
{}
```

### Section: Models (id=models)

#### Block b_models_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_src_neural_decoder_model_py, ev_scripts_train_py, ev_scripts_prepare_silentspeller_dataset_py
- citations: graves2006connectionist, park2019specaugment

Text:
```text
Our baseline model encodes each frame as a vector of palate channels and applies a uni-directional recurrent decoder trained with a CTC objective. We compare two layout aware front ends. One is a row and column pooling front end that aggregates a proxy grid into one dimensional summaries. The other is a grid front end that reconstructs a proxy grid and applies a convolutional spatial encoder. For the grid model we optionally enable a spatial augmentation that drops and shifts contiguous electrode blocks.
```

Slot trace:
```json
{}
```

#### Block b_models_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_src_neural_decoder_model_py, ev_scripts_train_py, ev_scripts_prepare_silentspeller_dataset_py, ev_scripts_smartpalate_distribution_csv

Text:
```text
The proxy grid is constructed from the palate channel layout. It supports row and column pooling or convolutional feature extraction. We use a fixed layout file for the mapping so that row and column indices are consistent across splits. We augment spatially by perturbing contiguous electrode blocks to emulate missing contacts and minor spatial shifts.
```

Slot trace:
```json
{}
```

#### Block b_training_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv

Text:
```text
We fix core training hyperparameters across runs and record how we configure them in the metrics registry for auditability.
```

Slot trace:
```json
{}
```

### Section: Results (id=results)

#### Block b_results_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_dataset_audit_silentspeller_2026_02_24_report_md, ev_msx20260224_metrics_csv, ev_msx20260224_split_npz_manifest_csv, ev_paper_layout_2026_03_03_table_k64_all_csv, ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_scripts_rebuttal_eval_greedy_clean_py

Text:
```text
We report greedy decoding error, lexicon-projected error, and streaming cost under a shared evaluation harness for all protocols. The fourth participant is target-only in cross-participant evaluation due to single-instance label dominance. All metrics are derived from the same audited registry of 652 runs (P1=176, P2=132, P3=264, P3MS=48, P2K=32).
```

Slot trace:
```json
{}
```

#### Block b_results_main (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_main_compact_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Table~\ref{tab:main} summarizes baseline performance across the three evaluation protocols.
```

Slot trace:
```json
{}
```

#### Block tbl_main (kind=table)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_main_compact_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py
- source_evidence_id: ev_paper_layout_2026_03_03_table_main_compact_csv

Text:
```text
[TABLE] label=tab:main source_evidence_id=ev_paper_layout_2026_03_03_table_main_compact_csv
Caption: Baseline recap across protocols; P1 means word holdout, P2 means instance holdout, and P3 means cross-participant transfer. n is the number of split-seed aggregates. CER is character error rate and LEX is lexicon-projected error rate.
```

Slot trace:
```json
{}
```

#### Block b_results_main_post (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_main_compact_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Table~\ref{tab:main} shows a clear protocol ordering: CER is 0.145 to 0.180 for within-participant protocols (P2 and P1) and 0.691 for cross-participant P3, while LEX rises from 0.075 to 0.102 up to 0.644. Transfer difficulty, not within-participant decoding, drives the largest residual error.
```

Slot trace:
```json
{}
```

#### Block b_results_main_lexgap (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_main_compact_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Table~\ref{tab:main} also shows that lexicon projection helps more in within-participant settings than in transfer: CER to LEX changes are 0.180 to 0.102 for P1 and 0.145 to 0.075 for P2, versus 0.691 to 0.644 for P3. Lexicon constraints reduce local decoding variance, but they do not remove cross-participant mismatch.
```

Slot trace:
```json
{}
```

#### Block b_results_spatial (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_uc20260226_spatial2d_patchpool_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Table~\ref{tab:spatial_all} compares vector, row/col, and grid-based front ends at full channels across protocols.
```

Slot trace:
```json
{}
```

#### Block tbl_spatial_k124 (kind=table)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_uc20260226_spatial2d_patchpool_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py
- source_evidence_id: ev_paper_layout_2026_03_03_table_spatial_all_csv

Text:
```text
[TABLE] label=tab:spatial_all source_evidence_id=ev_paper_layout_2026_03_03_table_spatial_all_csv
Caption: Spatial modeling at full channels across P1, P2, and P3; P1 means word holdout, P2 means instance holdout, and P3 means cross-participant transfer. CER is character error rate and RTF is real time factor.
```

Slot trace:
```json
{}
```

#### Block b_results_spatial_p1_post (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_uc20260226_spatial2d_patchpool_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
From Table~\ref{tab:spatial_all}, rowcol tracks vec across protocols (P1: 0.20 vs 0.18, P2: 0.16 vs 0.15, P3: 0.68 vs 0.69 CER). Grid and grid_aug are usually higher in CER and RTF, and patch variants only partially close this gap. The compact statistical summary in supplementary material shows broad interval overlap, so we treat these as directional trends rather than universal winners.
```

Slot trace:
```json
{}
```

#### Block b_results_spatial_latency (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_uc20260226_spatial2d_patchpool_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Latency shows a similarly stable tradeoff. In P1, vec runs at RTF 0.0006 while rowcol is 0.0024 and grid-family variants are 0.0034 to 0.0039; in P3, all variants remain below 0.001 but grid-family models are still slower than vec and rowcol. Under this audit setting, the expensive spatial front ends do not produce a consistent accuracy return.
```

Slot trace:
```json
{}
```

#### Block b_results_to4 (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_to4_compact_csv, ev_uc20260226_to4_metrics_csv, ev_uc20260226_split_npz_manifest_to4_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Table~\ref{tab:tofour} evaluates cross-participant transfer with participant p4 as target under single-source and paired-source settings.
```

Slot trace:
```json
{}
```

#### Block tbl_to4_generalization (kind=table)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_to4_compact_csv, ev_uc20260226_to4_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py
- source_evidence_id: ev_paper_layout_2026_03_03_table_to4_compact_csv

Text:
```text
[TABLE] label=tab:tofour source_evidence_id=ev_paper_layout_2026_03_03_table_to4_compact_csv
Caption: Cross-participant transfer targeting participant p4. Proto marks P3 single-source transfer or P3MS paired-source transfer. Lvl marks direction rows or all-direction aggregates. Group encodes source-to-target participant IDs p1 to p4. CER is character error rate and LEX is lexicon-projected error rate.
```

Slot trace:
```json
{}
```

#### Block b_results_to4_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_to4_compact_csv, ev_uc20260226_to4_metrics_csv

Text:
```text
Table~\ref{tab:tofour} shows an aggregate gain: CER drops from 0.686±0.114 in P3 all->p4 to 0.582±0.064 in P3MS all->p4, and LEX drops from 0.659±0.073 to 0.554±0.034. Direction rows remain heterogeneous, so source-pair selection stays condition dependent.
```

Slot trace:
```json
{}
```

#### Block b_results_to4_3 (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_to4_compact_csv, ev_uc20260226_to4_metrics_csv

Text:
```text
Direction rows in Table~\ref{tab:tofour} show where the aggregate gain comes from: p13->p4 reaches 0.536±0.009 CER versus 0.809±0.021 for p2->p4, and p23->p4 reaches 0.555±0.005 versus 0.666±0.024 for p1->p4. The remaining direction goes the other way (p12->p4 0.655±0.016 versus p3->p4 0.584±0.018), so source aggregation helps on average but not for every source-target match.
```

Slot trace:
```json
{}
```

#### Block b_results_kshot (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_kshot_compact_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Table~\ref{tab:kshot} evaluates low-shot adaptation by varying the number of training instances per word for a new participant.
```

Slot trace:
```json
{}
```

#### Block tbl_kshot_compact (kind=table)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_kshot_compact_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py
- source_evidence_id: ev_paper_layout_2026_03_03_table_kshot_compact_csv

Text:
```text
[TABLE] label=tab:kshot source_evidence_id=ev_paper_layout_2026_03_03_table_kshot_compact_csv
Caption: Low-shot adaptation for participant p3 with k1 or k2 training instances per word. vec is vector baseline, rowcol is row-column pooling, grid is a convolutional grid encoder, and grid_aug adds spatial augmentation. CER is character error rate and RTF is real time factor.
```

Slot trace:
```json
{}
```

#### Block b_results_kshot_post (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_kshot_compact_csv, ev_msx20260224_metrics_csv

Text:
```text
From Table~\ref{tab:kshot}, increasing from k1 to k2 improves vec (0.350->0.246) and rowcol (0.334->0.278), but worsens grid (0.515->0.616) and grid_aug (0.611->0.689). Low-shot gain is architecture dependent, not automatic.
```

Slot trace:
```json
{}
```

#### Block b_results_k64 (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_k64_all_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Table~\ref{tab:k64_all} evaluates reduced-channel subsets across protocols using within-participant, transfer, and random selection strategies.
```

Slot trace:
```json
{}
```

#### Block tbl_k64_methods (kind=table)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_k64_all_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py
- source_evidence_id: ev_paper_layout_2026_03_03_table_k64_all_csv

Text:
```text
[TABLE] label=tab:k64_all source_evidence_id=ev_paper_layout_2026_03_03_table_k64_all_csv
Caption: Electrode-reduction methods at K=64 across P1, P2, and P3; P1 means word holdout, P2 means instance holdout, and P3 means cross-participant transfer. topk and fps2k are within-participant selections, xfer transfers a source ranking, and rand is a fixed random subset. CER is character error rate and RTF is real time factor.
```

Slot trace:
```json
{}
```

#### Block b_results_k64_p12_post (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_k64_all_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Table~\ref{tab:k64_all} shows small method deltas at K=64: P1 CER ranges 0.191-0.205, P2 ranges 0.154-0.158, and P3 ranges 0.644-0.657. Because these ranges overlap strongly, we avoid a universal ranking among topk, fps2k, xfer, and rand.
```

Slot trace:
```json
{}
```

#### Block b_results_kcurve (kind=paragraph)
- status: supported
- evidence_ids: ev_docs_report_figures_ed20260217_cer_rtf_vs_k_pdf, ev_sweeps_ed20260217_results_ed20260217_vector_full_with_random_csv

Text:
```text
Fig.~\ref{fig:kcurve} visualizes how accuracy and streaming cost vary with electrode budget for the word holdout protocol.
```

Slot trace:
```json
{}
```

#### Block fig_kcurve (kind=figure)
- status: supported
- evidence_ids: ev_docs_report_figures_ed20260217_cer_rtf_vs_k_pdf, ev_sweeps_ed20260217_results_ed20260217_vector_full_with_random_csv
- source_evidence_id: ev_docs_report_figures_ed20260217_cer_rtf_vs_k_pdf

Text:
```text
[FIGURE] label=fig:kcurve source_evidence_id=ev_docs_report_figures_ed20260217_cer_rtf_vs_k_pdf
Caption: Electrode-budget trends for P1 word holdout; topk uses within-participant importance ranking, diversity corresponds to fps2k, and random is a fixed random subset. CER is character error rate and RTF is real time factor.
```

Slot trace:
```json
{}
```

#### Block b_results_k64_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_docs_report_figures_ed20260217_cer_rtf_vs_k_pdf, ev_sweeps_ed20260217_results_ed20260217_vector_full_with_random_csv

Text:
```text
Fig.~\ref{fig:kcurve} shows CER improving as K increases toward full channels, while RTF changes less steeply. Random subsets are generally above within-participant selections in CER, although the gap narrows at larger budgets.
```

Slot trace:
```json
{}
```

#### Block b_results_kcurve_budget (kind=paragraph)
- status: supported
- evidence_ids: ev_docs_report_figures_ed20260217_cer_rtf_vs_k_pdf, ev_sweeps_ed20260217_results_ed20260217_vector_full_with_random_csv

Text:
```text
Fig.~\ref{fig:kcurve} also shows where electrode-budget sensitivity is concentrated. At K=16, CER is 0.210 for random versus 0.192 for topk and 0.166 for fps2k; by K=64, these values narrow to 0.130, 0.129, and 0.119. Around K=80, all three are near 0.121, indicating a practical regime where selection strategy matters less than at sparse budgets.
```

Slot trace:
```json
{}
```

#### Block b_results_p3ms (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_p3ms_compact_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py

Text:
```text
Table~\ref{tab:p3ms} evaluates paired-source cross-participant transfer under the same target and protocol constraints.
```

Slot trace:
```json
{}
```

#### Block tbl_p3ms_compact (kind=table)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_p3ms_compact_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py
- source_evidence_id: ev_paper_layout_2026_03_03_table_p3ms_compact_csv

Text:
```text
[TABLE] label=tab:p3ms source_evidence_id=ev_paper_layout_2026_03_03_table_p3ms_compact_csv
Caption: Paired-source cross-participant results by source pair; group denotes source participants to target participant with participant IDs p1 to p4. vec is vector baseline, rowcol is row-column pooling, grid is a convolutional grid encoder, and grid_aug adds spatial augmentation. CER is character error rate and RTF is real time factor.
```

Slot trace:
```json
{}
```

#### Block b_results_p3ms_post (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_p3ms_compact_csv, ev_msx20260224_metrics_csv

Text:
```text
Table~\ref{tab:p3ms} is target dependent: for p23->p1, vec 0.473 and rowcol 0.476 outperform grid 0.602 and grid_aug 0.691, while for p12->p3, grid 0.736 outperforms vec 0.838 and rowcol 0.790. Multi-source benefit is therefore conditional rather than universal.
```

Slot trace:
```json
{}
```

#### Block b_results_p3ms_post_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_p3ms_compact_csv, ev_msx20260224_metrics_csv

Text:
```text
Table~\ref{tab:p3ms} also contains an intermediate regime where methods are close: for p13->p2, CER is 0.520 for vec, 0.504 for rowcol, and 0.511 for both grid variants. This narrow band contrasts with p23->p1 and p12->p3, reinforcing that source-target compatibility, not model family alone, governs paired-source behavior.
```

Slot trace:
```json
{}
```

### Section: Discussion (id=discussion)

#### Block b_discussion (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_uc20260226_spatial2d_patchpool_metrics_csv, ev_paper_layout_2026_03_03_table_k64_all_csv, ev_ed20260217_h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17, ev_paper_layout_2026_03_03_table_p3ms_compact_csv, ev_paper_layout_2026_03_03_table_kshot_compact_csv, ev_paper_layout_2026_03_03_table_to4_compact_csv, ev_uc20260226_p3ms_conditions_csv, ev_uc20260226_p3ms_conditions_md

Text:
```text
The dominant and most stable signal is the protocol gap: P3 CER is 0.691±0.133, versus 0.180±0.084 for P1 and 0.145±0.063 for P2. This ordering persists under front-end swaps, channel reduction, and low-shot settings, so cross-participant mismatch remains the primary error source in this audited setup.

Layout-aware bias alone is insufficient. Rowcol remains close to vec across P1-P3, while grid variants often increase CER and RTF; patch pooling narrows some gaps but does not create a consistent winner. Spatial encoders therefore need protocol-specific validation against explicit latency constraints.

Source aggregation helps at the p4 aggregate level (CER 0.686 to 0.582), but direction-level outcomes remain heterogeneous. Together with k-shot behavior (vec and rowcol improve from k1 to k2 while grid variants worsen), this indicates that transfer benefit depends on source-target compatibility and model family.

Our practical rule is protocol-specific selection under matched audited splits and manifests. We limit all claims to these datasets, this normalization pipeline, and these protocol definitions, and we do not extrapolate to unaudited populations or sensing setups.
```

Slot trace:
```json
{}
```

### Section: Conclusion (id=conclusion)

#### Block b_conclusion (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_msx20260224_split_npz_manifest_csv, ev_paper_layout_2026_03_03_table_main_compact_csv, ev_paper_layout_2026_03_03_table_to4_compact_csv

Text:
```text
EPGSpeller provides a reproducible benchmark for lexicon-free silent spelling under deterministic audited protocols. Within this audited setting, cross-participant transfer remains the hardest regime (P3 CER 0.691±0.133), and paired-source aggregation can reduce aggregate p4 error (0.686 to 0.582) without removing direction dependence. Deployment claims should therefore be validated per protocol, per target, and per latency constraint.
```

Slot trace:
```json
{}
```

### Section: Artifacts and Auditability (id=artifacts)

#### Block b_artifacts (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_msx20260224_split_npz_manifest_csv, ev_paper_layout_2026_03_03_table_k64_all_csv, ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_paper_layout_2026_03_03_table_stats_compact_csv, ev_paper_layout_2026_03_03_table_to4_compact_csv, ev_scripts_paper_export_stats_table_for_paperjson_py, ev_supplementary_table_stats_compact_csv, ev_uc20260226_p3ms_conditions_csv, ev_uc20260226_split_npz_manifest_to4_csv

Text:
```text
This repository uses a strict paper registry that pins every evidence file by checksum and rejects unsupported manuscript blocks. The split manifests, aggregated metrics, compact tables, statistical summaries, and analysis reports referenced in this paper are stored as deterministic artifacts, enabling audit and reproduction within our repository environment. A supplementary archive includes the compact statistical summary table for reviewers.
```

Slot trace:
```json
{}
```

### Section: Ethics and Disclosure (id=ethics)

#### Block b_ethics (kind=paragraph)
- status: supported
- evidence_ids: ev_dataset_audit_silentspeller_2026_02_24_report_md, ev_msx20260224_metrics_csv, ev_ai_disclosure_2026_03_04_md

Text:
```text
We report results only for audited artifacts and do not claim broader demographic coverage. The datasets and splits used in this study are derived from participant recordings, and we focus on methodological clarity and artifact traceability rather than deployment claims. We used generative AI tools for language polishing and verified technical claims against audited artifacts.
```

Slot trace:
```json
{}
```

## Runs (raw; sorted by id)
```json
[
  {
    "command": {
      "argv": [
        ".venv/bin/python",
        "scripts/rebuttal/ed_export_paperjson_evidence.py",
        "--export",
        "h11_spatial2d_vs_vector",
        "--out_csv",
        "results/ed20260217/paperjson/h11_spatial2d_vs_vector_p1_k32_k64_k96_k124_2026-02-17.csv",
        "--snapshot_date",
        "2026-02-17"
      ],
      "cwd": "."
    },
    "id": "run_ed20260217_snapshot_h11_spatial2d_vs_vector_2026-02-17",
    "notes": "Produces paper.json evidence snapshot for H11 (spatial2d vs vector).",
    "outputs": [
      {
        "path": "results/ed20260217/paperjson/h11_spatial2d_vs_vector_p1_k32_k64_k96_k124_2026-02-17.csv"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        ".venv/bin/python",
        "scripts/rebuttal/ed_export_paperjson_evidence.py",
        "--export",
        "h12_spatial_aug_dropout_summary",
        "--out_csv",
        "results/ed20260217/paperjson/h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17.csv",
        "--snapshot_date",
        "2026-02-17"
      ],
      "cwd": "."
    },
    "id": "run_ed20260217_snapshot_h12_spatial_aug_dropout_summary_2026-02-17",
    "notes": "Produces paper.json evidence snapshot for H12 (spatial aug fixed-dropout summary).",
    "outputs": [
      {
        "path": "results/ed20260217/paperjson/h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17.csv"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        ".venv/bin/python",
        "scripts/rebuttal/ed_export_paperjson_evidence.py",
        "--out_csv",
        "results/ed20260217/paperjson/h13_rowcol_vs_vector_p1_k32_k64_2026-02-17.csv",
        "--snapshot_date",
        "2026-02-17"
      ],
      "cwd": "."
    },
    "id": "run_ed20260217_snapshot_h13_rowcol_vs_vector_2026-02-17",
    "notes": "Produces paper.json evidence snapshot for H13 (rowcol vs vector).",
    "outputs": [
      {
        "path": "results/ed20260217/paperjson/h13_rowcol_vs_vector_p1_k32_k64_2026-02-17.csv"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        "python3",
        "scripts/paper/export_msx_tables_for_paperjson.py",
        "--metrics_csv",
        "sweeps/msx20260224/results/msx_all_metrics.csv",
        "--out_dir",
        "results/msx20260224/paper_tables"
      ],
      "cwd": "."
    },
    "id": "run_msx20260224_export_paper_tables_2026-02-26",
    "notes": "Export compact msx tables for paperjson manuscript blocks.",
    "outputs": [
      {
        "path": "results/msx20260224/paper_tables/table_main.csv"
      },
      {
        "path": "results/msx20260224/paper_tables/table_spatial_k124.csv"
      },
      {
        "path": "results/msx20260224/paper_tables/table_k64_methods.csv"
      },
      {
        "path": "results/msx20260224/paper_tables/table_spatial_k64.csv"
      },
      {
        "path": "results/msx20260224/paper_tables/table_p3ms.csv"
      },
      {
        "path": "results/msx20260224/paper_tables/table_kshot.csv"
      },
      {
        "path": "results/msx20260224/paperjson_evidence_items.json"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        ".venv/bin/python",
        "scripts/rebuttal/msx_export_split_npz_manifest.py",
        "--metrics_csv",
        "sweeps/msx20260224/results/msx_all_metrics.csv",
        "--out_csv",
        "results/msx20260224/split_npz_manifest.csv"
      ],
      "cwd": "."
    },
    "id": "run_msx20260224_export_split_npz_manifest_2026-02-26",
    "notes": "Export a sha256 manifest for split NPZ archives referenced by msx metrics.",
    "outputs": [
      {
        "path": "results/msx20260224/split_npz_manifest.csv"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        ".venv/bin/python",
        "scripts/rebuttal/pa_positioning_apply_taxonomy.py",
        "--raw_csv",
        "results/positioning_analysis_epgspeller_2026-02-18/prior_work_raw.csv",
        "--rubric_md",
        "results/positioning_analysis_epgspeller_2026-02-18/taxonomy_rubric.md",
        "--rules_json",
        "results/positioning_analysis_epgspeller_2026-02-18/taxonomy_rules.json"
      ],
      "cwd": "."
    },
    "id": "run_positioning_analysis_2026-02-18_apply_taxonomy",
    "notes": "Applies explicit (non-heuristic) taxonomy labels to the frozen survey export.",
    "outputs": [
      {
        "path": "results/positioning_analysis_epgspeller_2026-02-18/prior_work_taxonomy.csv"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        "manual",
        "authored results/positioning_analysis_epgspeller_2026-02-18/{inputs_manifest.md,taxonomy_rubric.md,taxonomy_rules.json}"
      ],
      "cwd": "."
    },
    "id": "run_positioning_analysis_2026-02-18_author_static_inputs",
    "notes": "Static inputs for positioning analysis were authored by hand (no heuristic inference).",
    "outputs": [
      {
        "path": "results/positioning_analysis_epgspeller_2026-02-18/inputs_manifest.md"
      },
      {
        "path": "results/positioning_analysis_epgspeller_2026-02-18/taxonomy_rubric.md"
      },
      {
        "path": "results/positioning_analysis_epgspeller_2026-02-18/taxonomy_rules.json"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        ".venv/bin/python",
        "scripts/rebuttal/pa_positioning_extract_ours_spatial.py",
        "--h11_csv",
        "results/ed20260217/paperjson/h11_spatial2d_vs_vector_p1_k32_k64_k96_k124_2026-02-17.csv",
        "--h12_csv",
        "results/ed20260217/paperjson/h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17.csv",
        "--h13_csv",
        "results/ed20260217/paperjson/h13_rowcol_vs_vector_p1_k32_k64_2026-02-17.csv",
        "--out_csv",
        "results/positioning_analysis_epgspeller_2026-02-18/ours_spatial_findings.csv"
      ],
      "cwd": "."
    },
    "id": "run_positioning_analysis_2026-02-18_extract_ours_spatial",
    "notes": "Normalizes H11–H13 evidence snapshots into a tidy findings CSV (aggregated across seeds when applicable).",
    "outputs": [
      {
        "path": "results/positioning_analysis_epgspeller_2026-02-18/ours_spatial_findings.csv"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        ".venv/bin/python",
        "scripts/rebuttal/pa_positioning_extract_priorwork.py",
        "--survey_dir",
        "results/related_work_survey_epgspeller_2026-02-17/results",
        "--out_csv",
        "results/positioning_analysis_epgspeller_2026-02-18/prior_work_raw.csv"
      ],
      "cwd": "."
    },
    "id": "run_positioning_analysis_2026-02-18_extract_priorwork",
    "notes": "Extracts frozen related-work survey JSON (required fields) into a flat CSV for taxonomy/plots.",
    "outputs": [
      {
        "path": "results/positioning_analysis_epgspeller_2026-02-18/prior_work_raw.csv"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        ".venv/bin/python",
        "scripts/rebuttal/pa_positioning_make_plots.py",
        "--prior_tax_csv",
        "results/positioning_analysis_epgspeller_2026-02-18/prior_work_taxonomy.csv",
        "--ours_csv",
        "results/positioning_analysis_epgspeller_2026-02-18/ours_spatial_findings.csv",
        "--out_dir",
        "results/positioning_analysis_epgspeller_2026-02-18/figures"
      ],
      "cwd": "."
    },
    "id": "run_positioning_analysis_2026-02-18_make_plots",
    "notes": "Generates positioning plots (systems space / representation space / W-matrix).",
    "outputs": [
      {
        "path": "results/positioning_analysis_epgspeller_2026-02-18/figures/positioning_space_systems.png"
      },
      {
        "path": "results/positioning_analysis_epgspeller_2026-02-18/figures/positioning_space_representation.png"
      },
      {
        "path": "results/positioning_analysis_epgspeller_2026-02-18/figures/w_matrix_evidence_map.png"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        ".venv/bin/python",
        "scripts/rebuttal/pa_positioning_write_report.py",
        "--prior_tax_csv",
        "results/positioning_analysis_epgspeller_2026-02-18/prior_work_taxonomy.csv",
        "--ours_csv",
        "results/positioning_analysis_epgspeller_2026-02-18/ours_spatial_findings.csv",
        "--review_weakness_md",
        "docs/report/icassp2026_review_weaknesses_and_rebuttal_actions.md",
        "--related_work_md",
        "results/related_work_survey_epgspeller_2026-02-17/report.md",
        "--out_md",
        "results/positioning_analysis_epgspeller_2026-02-18/report.md",
        "--fig_dir",
        "results/positioning_analysis_epgspeller_2026-02-18/figures"
      ],
      "cwd": "."
    },
    "id": "run_positioning_analysis_2026-02-18_write_report",
    "notes": "Writes the paper-ready English positioning report with strict H11–H13 assertions and explicit evidence references.",
    "outputs": [
      {
        "path": "results/positioning_analysis_epgspeller_2026-02-18/report.md"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        "python3",
        "~/.claude/skills/research/citation_export.py",
        "--outline",
        "results/related_work_survey_epgspeller_2026-02-17/outline.yaml",
        "--scope",
        "papers",
        "--verify-doi",
        "true",
        "--verify-url",
        "true"
      ],
      "cwd": "."
    },
    "id": "run_related_work_survey_epgspeller_2026-02-17_export_bib",
    "notes": "BibTeX export and DOI audit run (executed on a workstation with ~/.claude/skills/research tooling available).",
    "outputs": [
      {
        "path": "results/related_work_survey_epgspeller_2026-02-17/references.bib"
      },
      {
        "path": "results/related_work_survey_epgspeller_2026-02-17/references.json"
      },
      {
        "path": "results/related_work_survey_epgspeller_2026-02-17/references_audit.md"
      },
      {
        "path": "results/related_work_survey_epgspeller_2026-02-17/doi_cache.json"
      }
    ],
    "status": "succeeded"
  },
  {
    "command": {
      "argv": [
        "manual"
      ],
      "cwd": "."
    },
    "id": "run_related_work_survey_epgspeller_2026-02-17_generate_report",
    "notes": "Report and coverage matrix authored based on results/*.json and exported citekeys; no automated generator script was vendored in this repo for this step.",
    "outputs": [
      {
        "path": "results/related_work_survey_epgspeller_2026-02-17/report.md"
      },
      {
        "path": "results/related_work_survey_epgspeller_2026-02-17/coverage_matrix.csv"
      },
      {
        "path": "results/related_work_survey_epgspeller_2026-02-17/search_log.md"
      }
    ],
    "status": "succeeded"
  }
]
```

## Experiments (raw; sorted by id)
```json
[
  {
    "claim_ids": [
      "cl_ed20260217_h11_spatial2d_vs_vector_p1"
    ],
    "id": "exp_ed20260217_h11_spatial2d_vs_vector_p1",
    "notes": "Snapshot-based comparison; underlying model runs are referenced by run_id inside the evidence CSV.",
    "run_ids": [
      "run_ed20260217_snapshot_h11_spatial2d_vs_vector_2026-02-17"
    ],
    "title": "H11: 16×16 reconstruction + 2D Conv frontend vs vector (P1, K=32/64/96/124)"
  },
  {
    "claim_ids": [
      "cl_ed20260217_h12_spatial_aug_improves_dropout_robustness_p1"
    ],
    "id": "exp_ed20260217_h12_spatial_aug_dropout_robustness_p1",
    "notes": "Summary table derived from sweeps/ed20260217/results/dropout_summary_spatial2d.csv, which aggregates eval_dropout_q*.json artifacts under logs/<run_id>/.",
    "run_ids": [
      "run_ed20260217_snapshot_h12_spatial_aug_dropout_summary_2026-02-17"
    ],
    "title": "H12: spatial augmentation improves fixed-dropout robustness (P1, spatial2d, K=64 topk)"
  },
  {
    "claim_ids": [
      "cl_ed20260217_h13_rowcol_vs_vector_p1"
    ],
    "id": "exp_ed20260217_h13_rowcol_vs_vector_p1",
    "notes": "Snapshot-based comparison; underlying model runs are referenced by run_id inside the evidence CSV.",
    "run_ids": [
      "run_ed20260217_snapshot_h13_rowcol_vs_vector_2026-02-17"
    ],
    "title": "H13: row/col compression vs vector frontend (P1, K=32/64)"
  },
  {
    "claim_ids": [
      "cl_related_work_survey_epgspeller_2026-02-17_completed"
    ],
    "id": "exp_related_work_survey_epgspeller_2026-02-17",
    "notes": "Survey artifacts are stored under results/related_work_survey_epgspeller_2026-02-17/.",
    "run_ids": [
      "run_related_work_survey_epgspeller_2026-02-17_generate_report",
      "run_related_work_survey_epgspeller_2026-02-17_export_bib"
    ],
    "title": "Related Work survey (EPG-centered) up to 2026-02-17"
  }
]
```
