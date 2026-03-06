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
    "title": "EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for Open-Vocabulary Silent Spelling",
    "venue": "interspeech"
  },
  "paper_json": "paper/paper.json",
  "paper_json_sha256": "5c6b395a024489e6bf0b2216f7e24b58cb9f2e47cc930dd84242c9fe508c1723",
  "policy": {
    "allowlist_block_kinds": [
      "paragraph",
      "bullets",
      "table",
      "figure",
      "equation"
    ],
    "banned_token_re": "\\b(TBD|TODO|placeholder|mock)\\b",
    "forbid_digits_in_templates": true,
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
    "bytes": 3575,
    "id": "ev_config_outline_yaml",
    "kind": "config_snapshot",
    "path": "results/related_work_survey_epgspeller_2026-02-17/outline.yaml",
    "sha256": "90e6a179b29cca1331e7613fce62e3c1529fca96c12bc7dbd81112fc1f642fa8"
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
    "bytes": 4827,
    "id": "ev_references_sanitized_ascii_cited_bib",
    "kind": "bibtex",
    "path": "paper/bibliography/references_sanitized_ascii_cited.bib",
    "sha256": "46f42262e35b3ca42676b8e147b7e13a838d423126f5e2be8fe2254378361f8c"
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
- evidence_ids: ev_msx20260224_metrics_csv, ev_dataset_audit_silentspeller_2026_02_24_report_md, ev_msx20260224_split_npz_manifest_csv

Text:
```text
Silent speech text entry with electropalatography requires models that generalize across word identities and participants while remaining auditable. We present an evidence-only study of open-vocabulary silent spelling from binary palate contact patterns. We define protocols for word holdout, instance holdout, and cross participant transfer. Using participant labeled datasets and deterministic artifact tracking, we evaluate a vector baseline and two layout aware front ends. We also analyze electrode reduction and how models adapt in low shot settings. Across our audited runs, the row and column front end tracks the vector baseline more closely than a convolutional grid front end. The grid front end increases streaming latency. We release split manifests, checksums, and compact result tables as pinned repository artifacts.
```

Slot trace:
```json
{}
```

### Section: Introduction (id=intro)

#### Block b_intro_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_related_work_survey_epgspeller_2026-02-17_report_md
- citations: denby2010silent, freitas2017an, gonzalez2020silent, lee2021biosignal

Text:
```text
Silent speech interfaces aim to enable communication without audible acoustics. They use sensor measures of articulation or physiology. Electropalatography provides a practical binary contact form for tongue and palate interaction. Its discrete layout and device variability raise questions about inductive bias, robustness, and how models generalize.
```

Slot trace:
```json
{}
```

#### Block b_intro_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_positioning_analysis_epgspeller_2026_02_18_report_md
- citations: kimura2022silentspeller, dong2024rehearsse, graves2006connectionist

Text:
```text
Recent work on silent spelling has emphasized open-vocabulary text entry, where character level decoding can compose words beyond a fixed closed set. We study open-vocabulary spelling with a CTC style decoder and lexicon projection. We compare vector and layout aware front ends under multiple protocols that test how models generalize across words.
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
- We define protocols to evaluate word identity generalization and participant transfer, and we provide split archives with checksums.
- We run multi-participant experiments with open-vocabulary decoding and lexicon projection, tracked by a strict evidence registry.
- We compare a vector baseline with two layout aware front ends, and we report both accuracy and streaming speed metrics.
- We provide deterministic scripts that export compact tables and manifests used by this manuscript.
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

### Section: Related Work (id=related)

#### Block b_related_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_related_work_survey_epgspeller_2026-02-17_report_md, ev_positioning_analysis_epgspeller_2026_02_18_report_md
- citations: kimura2022silentspeller, dong2024rehearsse, denby2010silent, gonzalez2020silent, hardcastle1989new, hardcastle1990electropalatography, hardcastle1991epg, carreira1998dimensionality, verhoeven2019visualisation, woo2021design, shadle1993depth, hueber2010development, toutios2006on, toutios2006learning

Text:
```text
Within our surveyed set, SilentSpeller and ReHEarSSE represent open-vocabulary silent spelling systems. Broader silent speech systems span constrained recognition and reconstruction settings. In the electropalatography literature, the spatial layout is used to visualize contacts, characterize devices, and reduce how contacts are represented. This motivates tests of layout aware inductive bias in learned decoders.
```

Slot trace:
```json
{}
```

#### Block b_related_positioning (kind=paragraph)
- status: supported
- evidence_ids: ev_positioning_analysis_epgspeller_2026_02_18_report_md

Text:
```text
We summarize the positioning of prior work using survey tags. These tags map systems by how they represent data and by system scope. We describe where open vocabulary silent spelling and electropalatography studies sit in the space.
```

Slot trace:
```json
{}
```

#### Block b_related_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_related_work_survey_epgspeller_2026-02-17_report_md, ev_positioning_analysis_epgspeller_2026_02_18_report_md

Text:
```text
Prior electropalatography studies emphasize that contact patterns are structured by the palate layout. This motivates a proxy grid form and spatially structured modeling in learned decoders. Our work situates these ideas within open vocabulary silent spelling by making protocol definitions and artifact traceability explicit.
```

Slot trace:
```json
{}
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
The dataset summary table reports id, sample count, vocabulary size, median sequence length, mean contact rate, and the count of all-zero samples for each participant dataset. The id labels are anonymous participant codes used throughout the protocol manifests.
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
- evidence_ids: ev_msx20260224_split_npz_manifest_csv, ev_uc20260226_split_npz_manifest_to4_csv, ev_scripts_rebuttal_make_word_holdout_split_py, ev_scripts_rebuttal_make_instance_holdout_split_py, ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py, ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py, ev_scripts_rebuttal_make_kshot_instance_holdout_split_py

Text:
```text
All split archives are generated deterministically from audited exports with fixed seeds. Each train, test, and competition partition is stored as an immutable archive with a checksum in the manifests to enable reuse and later verification. The manifests show the word-holdout protocol uses all four participant datasets. They show the instance-holdout protocol uses three participant datasets. They also show the fourth participant appears only as a target in the cross-participant splits. This separation explains why the dataset summary includes all participant datasets even when a protocol uses only a subset.
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
We report character error rate from greedy decoding and streaming speed using real time factor. We define real time factor as total inference time divided by total input duration. For open-vocabulary decoding we also report lexicon projection error rates using a training lexicon and a full lexicon.
```

Slot trace:
```json
{}
```

#### Block b_metrics_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_scripts_rebuttal_eval_greedy_clean_py, ev_scripts_rebuttal_gc_collect_metrics_py

Text:
```text
Greedy decoding reports unconstrained character sequences. Lexicon projection maps outputs to finite word sets derived from the training vocabulary or the full audited lexicon. This allows us to separate decoding quality from lexicon constraints. We compute real time factor by dividing inference time by input duration under the same test harness.
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
- evidence_ids: ev_msx20260224_metrics_csv, ev_msx20260224_split_npz_manifest_csv, ev_scripts_rebuttal_eval_greedy_clean_py, ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_paper_layout_2026_03_03_table_k64_all_csv

Text:
```text
Baseline performance across protocols is derived from the same metrics registry as the remaining tables. We report greedy decoding error and lexicon-projected error to separate open vocabulary decoding quality from lexicon constraints. The vector baseline rows in the spatial modeling and electrode reduction tables serve as the reference for protocol comparisons. We use the same split manifests and deterministic evaluation scripts across all protocols.
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
We evaluate cross participant transfer with the fourth participant as target under single source and paired source settings. The table uses protocol labels for single source cross participant transfer and multi source transfer. The lvl field marks direction level rows and an across direction aggregate. Group labels join source participant identifiers with an arrow to the target. The split archives that define these targets are pinned by checksum in the manifest. In our audited splits, the multi source aggregate reduces CER relative to the single source aggregate for the same target.
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
Caption: Cross participant generalization targeting the fourth participant; proto distinguishes single source cross participant transfer and multi source transfer, lvl marks direction level rows versus an across direction aggregate, group encodes source to target participant labels, CER is character error rate, and lex is lexicon projected error rate.
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
The cross participant results for the fourth participant include both single source and paired source settings. This provides a direct comparison of transfer with and without source aggregation under the same audited protocol constraints. This helps isolate source aggregation effects without changing the target data or evaluation pipeline.
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
The spatial modeling table compares spatial inductive bias variants at full channels across protocols. We include a patchpool grid encoder as a minimal way to implement a rescue for the grid encoder. The patchpool variant keeps a coarser spatial map before recurrent decoding. The variant labels are vec, rowcol, grid, grid_aug, patch, and patch_aug. The row and column front end tracks the vector baseline more closely than the convolutional grid front end under within participant protocols. Patchpool reduces the gap under cross participant transfer. Across protocols, grid variants tend to increase real time factor relative to the vector baseline. We do not observe a consistent accuracy gain over the vector baseline in any protocol.
```

Slot trace:
```json
{}
```

#### Block tbl_spatial_all (kind=table)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_uc20260226_spatial2d_patchpool_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py
- source_evidence_id: ev_paper_layout_2026_03_03_table_spatial_all_csv

Text:
```text
[TABLE] label=tab:spatial_all source_evidence_id=ev_paper_layout_2026_03_03_table_spatial_all_csv
Caption: Spatial modeling at full channels across protocols; protocol labels denote word holdout, instance holdout, and cross participant transfer, vec is vector baseline, rowcol is row and column pooling, grid is convolutional grid encoder, grid aug is grid with spatial augmentation, patch is patchpool grid encoder, patch aug is patchpool with augmentation, CER is character error rate, and RTF is real time factor.
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
The electrode reduction table evaluates a reduced channel budget using several selection strategies. The method labels are topk, fps two k, xfer, and rand. The table reports both accuracy and streaming speed so reduction effects can be compared under the same evaluation harness. Across protocols, within participant selection and simple transfer selection yield similar performance. This suggests that a compact subset can preserve a large fraction of the vector baseline performance. Random selection and simple transfer remain slightly worse than within participant selection in the audited results.
```

Slot trace:
```json
{}
```

#### Block tbl_k64_all (kind=table)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_k64_all_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_layout_tables_for_paperjson_py
- source_evidence_id: ev_paper_layout_2026_03_03_table_k64_all_csv

Text:
```text
[TABLE] label=tab:k64_all source_evidence_id=ev_paper_layout_2026_03_03_table_k64_all_csv
Caption: Electrode reduction methods across protocols; protocol labels denote word holdout, instance holdout, and cross participant transfer, topk is within participant top ranked selection, fps two k is farthest point sampling, xfer is transfer selection, rand is random selection, CER is character error rate, and RTF is real time factor.
```

Slot trace:
```json
{}
```

#### Block b_results_k64_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_k64_all_csv, ev_paper_layout_2026_03_03_table_p3ms_compact_csv, ev_paper_layout_2026_03_03_table_kshot_compact_csv, ev_msx20260224_metrics_csv

Text:
```text
The reduction results complement the protocol tables. They show that compact selections preserve much of the vector baseline under within participant tests. Cross participant transfer remains more challenging, so we report paired source and low shot analyses in the subsequent tables.
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
We evaluate multi source cross participant transfer using paired source participants. The group labels concatenate the two source identifiers and use an arrow to the target identifier. The multi source table reports direction level results for vector and layout aware front ends. This isolates whether combining sources helps under the same target and protocol constraints.
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
Caption: Multi source cross participant results by source pair; group concatenates source participant labels with an arrow to the target, vec is vector baseline, rowcol is row and column pooling, grid is convolutional grid encoder, grid aug is grid with spatial augmentation, CER is character error rate, and RTF is real time factor.
```

Slot trace:
```json
{}
```

#### Block b_results_p3ms_conditions (kind=paragraph)
- status: supported
- evidence_ids: ev_uc20260226_p3ms_conditions_csv, ev_uc20260226_p3ms_conditions_md

Text:
```text
We further analyze multi source transfer deltas against simple similarity measures. Delta_cer is negative for all audited groups, and corr_src_tgt_mean varies within a narrow range across groups. We report these measures to describe conditions rather than to assert a universal rule.
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
We evaluate how models adapt in low shot settings for a new participant by varying the number of training instances per word. For the vector baseline, two shot improves over one shot, and the table reports layout aware variants. This isolates adaptation behavior when only a small amount of labeled target data is available.
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
Caption: Low shot adaptation results for a new participant; group uses the participant label and k one or k two for the number of training instances per word, vec is vector baseline, rowcol is row and column pooling, grid is convolutional grid encoder, grid aug is grid with spatial augmentation, CER is character error rate, and RTF is real time factor.
```

Slot trace:
```json
{}
```

### Section: Discussion (id=discussion)

#### Block b_discussion (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_ed20260217_h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17, ev_paper_layout_2026_03_03_table_p3ms_compact_csv, ev_paper_layout_2026_03_03_table_kshot_compact_csv, ev_uc20260226_p3ms_conditions_csv, ev_uc20260226_p3ms_conditions_md

Text:
```text
Our results suggest that an explicit convolutional grid encoder is not automatically beneficial for electropalatography under within participant tests, despite its intuitive spatial structure. A patchpool grid variant reduces the underperformance of the grid encoder under cross participant transfer. This indicates that spatial encoder design choices can materially affect outcomes. The patchpool variant does not yield consistent gains over the vector baseline across protocols. Spatial augmentation can improve robustness to synthetic electrode dropout, but it does not close the accuracy gap for the convolutional grid variants in our multi participant results. We analyze multi source cross participant transfer and how models adapt in low shot settings, and we provide the results as artifact tables. They highlight that cross participant performance remains challenging. We also analyze conditions for multi source transfer deltas against simple dataset similarity measures. The effect is conditional and does not present a single dominant monotonic trend within our evaluated group set. These observations are limited to our audited multi participant dataset collection and protocols.
```

Slot trace:
```json
{}
```

#### Block b_discussion_2 (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_paper_layout_2026_03_03_table_to4_compact_csv

Text:
```text
Across the audited protocols, within participant performance remains stronger than cross participant transfer. This emphasizes the difficulty of generalization under limited participant coverage. The target participant results reinforce this gap even when source aggregation is enabled. We report these trends as artifact grounded observations rather than broad claims. We expect additional participant data to be necessary for stronger transfer conclusions.
```

Slot trace:
```json
{}
```

### Section: Artifacts and Auditability (id=artifacts)

#### Block b_artifacts (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_split_npz_manifest_csv, ev_msx20260224_metrics_csv, ev_paper_layout_2026_03_03_table_spatial_all_csv, ev_paper_layout_2026_03_03_table_k64_all_csv, ev_uc20260226_split_npz_manifest_to4_csv, ev_paper_layout_2026_03_03_table_to4_compact_csv, ev_uc20260226_p3ms_conditions_csv

Text:
```text
This repository uses a strict paper registry that pins every evidence file by checksum and rejects unsupported manuscript blocks. The split manifests, aggregated metrics, compact tables, and analysis summaries referenced in this paper are stored as deterministic artifacts, enabling audit and reproduction within our repository environment. The same artifacts are reused to build the manuscript tables and to support verification in the audit views.
```

Slot trace:
```json
{}
```

### Section: Ethics and Disclosure (id=ethics)

#### Block b_ethics (kind=paragraph)
- status: supported
- evidence_ids: ev_dataset_audit_silentspeller_2026_02_24_report_md, ev_msx20260224_metrics_csv

Text:
```text
We report results only for audited artifacts and do not claim broader demographic coverage. The datasets and splits used in this study are derived from participant recordings, and we focus on methodological clarity and artifact traceability rather than deployment claims.
```

Slot trace:
```json
{}
```

### Section: Logic Checks (id=logic_checks)

#### Block cl_table_main_has_header (kind=paragraph)
- status: supported
- evidence_ids: ev_paper_layout_2026_03_03_table_main_compact_csv, ev_config_outline_yaml

Text:
```text
The baseline table includes protocol and aggregate metrics fields.
```

Slot trace:
```json
{}
```

Assertions:
```json
[
  {
    "cast_spec": null,
    "cast_used": "string",
    "id": "a_table_main_header",
    "left": {
      "evidence_id": "ev_paper_layout_2026_03_03_table_main_compact_csv",
      "group": 1,
      "kind": "regex",
      "pattern": "(protocol,n,cer,lex)"
    },
    "left_value": "protocol,n,cer,lex",
    "ok": true,
    "op": "==",
    "right": "protocol,n,cer,lex",
    "right_value": "protocol,n,cer,lex"
  }
]
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
