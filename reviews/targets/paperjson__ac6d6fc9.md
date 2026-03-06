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
  "paper_json_sha256": "ac6d6fc940cc4e0251654636b744c525505d26a4f1c047fc1b874ba6c83e9a5c",
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
    "bytes": 24351,
    "id": "ev_ed20260217_h11_spatial2d_vs_vector_p1_k32_k64_k96_k124_2026-02-17",
    "kind": "table",
    "path": "results/ed20260217/paperjson/h11_spatial2d_vs_vector_p1_k32_k64_k96_k124_2026-02-17.csv",
    "sha256": "2f2840f6dee5b8b9e17faf696f9fb8f5f86c2a952d6c239eee2c202b747f0b06"
  },
  {
    "bytes": 1750,
    "id": "ev_ed20260217_h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17",
    "kind": "table",
    "path": "results/ed20260217/paperjson/h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17.csv",
    "sha256": "0cd1fecedc166c732da45187356434c85c9316a546151dd6d5100e6caec19284"
  },
  {
    "bytes": 13847,
    "id": "ev_ed20260217_h13_rowcol_vs_vector_p1_k32_k64_2026-02-17",
    "kind": "table",
    "path": "results/ed20260217/paperjson/h13_rowcol_vs_vector_p1_k32_k64_2026-02-17.csv",
    "sha256": "a7fb56ec370de19333dc4ab1f059fbd473b9d0f4b40af525375c1c7d3877bb4b"
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
    "bytes": 659,
    "id": "ev_msx20260224_table_kshot_csv",
    "kind": "table",
    "path": "results/msx20260224/paper_tables/table_kshot.csv",
    "sha256": "67248482a1c901f1fc2a35b2a0c41ea27541ac3b172eb5e4cf73dd41cedc38bb"
  },
  {
    "bytes": 276,
    "id": "ev_msx20260224_table_main_csv",
    "kind": "table",
    "path": "results/msx20260224/paper_tables/table_main.csv",
    "sha256": "dff6b3436c265008bc53754745b6fd44b0cd6fcca7bd92a34fcf7d1f13ae9570"
  },
  {
    "bytes": 982,
    "id": "ev_msx20260224_table_p3ms_csv",
    "kind": "table",
    "path": "results/msx20260224/paper_tables/table_p3ms.csv",
    "sha256": "11097b4d1edb99125d487667697cbd39c9fd49b0230f2d9c635fb9f6493a24ad"
  },
  {
    "bytes": 832,
    "id": "ev_msx20260224_table_spatial_k124_csv",
    "kind": "table",
    "path": "results/msx20260224/paper_tables/table_spatial_k124.csv",
    "sha256": "74bd2da304d330f3230103baede46960f994dfcd55563d2f6021fddc1d87240e"
  },
  {
    "bytes": 1000,
    "id": "ev_msx20260224_table_spatial_k64_csv",
    "kind": "table",
    "path": "results/msx20260224/paper_tables/table_spatial_k64.csv",
    "sha256": "48c274f9ec2043d91f695560bf1833471f8495862469beb39bccc061d99159cf"
  },
  {
    "bytes": 8557,
    "id": "ev_positioning_analysis_epgspeller_2026_02_18_report_md",
    "kind": "document",
    "path": "results/positioning_analysis_epgspeller_2026-02-18/report.md",
    "sha256": "94f8a086cc48489bf7b1377903b996aca2e7617b25b933cd41c6af8c75ccf356"
  },
  {
    "bytes": 7298,
    "id": "ev_related_work_survey_epgspeller_2026-02-17_references_sanitized_ascii_bib",
    "kind": "bibtex",
    "path": "paper/bibliography/references_sanitized_ascii.bib",
    "sha256": "c3f3b22c7c62b881ffee68e3bd9589f23911f9c91accd1c18b84d4a169514e9b"
  },
  {
    "bytes": 10496,
    "id": "ev_related_work_survey_epgspeller_2026-02-17_report_md",
    "kind": "document",
    "path": "results/related_work_survey_epgspeller_2026-02-17/report.md",
    "sha256": "3ee6f36219209631bb14cf2b8639d6f70fe3b896a0e903be8164818edf14fe55"
  },
  {
    "bytes": 20650,
    "id": "ev_scripts_paper_export_msx_tables_for_paperjson_py",
    "kind": "data",
    "path": "scripts/paper/export_msx_tables_for_paperjson.py",
    "sha256": "2100f045c5b121e7167cbb5cb59136bc2e6d61f8b64b2663f8fc317e4d801e84"
  },
  {
    "bytes": 18515,
    "id": "ev_scripts_paper_export_uc20260226_tables_py",
    "kind": "data",
    "path": "scripts/paper/export_uc20260226_tables.py",
    "sha256": "936113afcbce65fbf7e4a2da7d66e8459d23e70188ad5f5db61492fdcbee0991"
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
    "bytes": 40812,
    "id": "ev_uc20260226_fig_p3ms_delta_vs_similarity_png",
    "kind": "figure",
    "path": "docs/report/figures/uc20260226/p3ms_delta_vs_similarity.png",
    "sha256": "389a51e53d54d08608c4ed1d359f81fd984a062e6d0114994b3dad1cc1f87cda"
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
    "bytes": 3623,
    "id": "ev_uc20260226_split_npz_manifest_to4_csv",
    "kind": "data",
    "path": "results/uc20260226/split_npz_manifest_to4.csv",
    "sha256": "8a00315026803e752c9fad58a43a002418ce52dbb338f14e8d46de630b65a766"
  },
  {
    "bytes": 725,
    "id": "ev_uc20260226_table_to4_generalization_csv",
    "kind": "table",
    "path": "results/uc20260226/paper_tables/table_to4_generalization.csv",
    "sha256": "12b0e0d2360897aeb3b66c61db48cbd3ae230298bd4eea88fcc2102b76fcef14"
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
Silent speech text entry with electropalatography requires models that generalize across word identities and participants while remaining auditable. We present an evidence-only study of open-vocabulary silent spelling from binary palate contact patterns, with protocols for word holdout, instance holdout, and cross participant transfer. Using four participants and deterministic artifact tracking, we evaluate a vector baseline and two layout aware front ends, and we analyze electrode reduction and low shot adaptation. Across our audited runs, the row and column front end tracks the vector baseline more closely than a convolutional grid front end, while the grid front end increases streaming latency. We release split manifests, checksums, and compact result tables as pinned repository artifacts.
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
Silent speech interfaces aim to enable communication without audible acoustics, using sensor measurements of articulation or physiology. Electropalatography provides a practical binary contact representation of tongue and palate interaction, but its discrete layout and device variability raise questions about inductive bias, robustness, and generalization.
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
Recent work on silent spelling has emphasized open-vocabulary text entry, where character level decoding can compose words beyond a fixed closed set. We study open-vocabulary spelling with a CTC style decoder and lexicon projection, and we compare vector and layout aware front ends under multiple generalization protocols.
```

Slot trace:
```json
{}
```

#### Block b_contrib (kind=bullets)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_msx20260224_split_npz_manifest_csv, ev_msx20260224_table_main_csv, ev_msx20260224_table_spatial_k124_csv, ev_msx20260224_table_k64_methods_csv, ev_scripts_rebuttal_gc_make_cmdlists_py, ev_scripts_rebuttal_gc_collect_metrics_py

Text:
```text
- We define evaluation protocols that separate word identity generalization and participant transfer, and we provide split archives with checksums.
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
Within our surveyed set, open-vocabulary silent spelling systems are represented by SilentSpeller and ReHEarSSE, while broader silent speech systems span constrained recognition and reconstruction settings. In the electropalatography literature, the spatial layout has been used for visualization, device characterization, and representation reduction, motivating tests of layout aware inductive bias in learned decoders.
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
We use four participant electropalatography datasets with word labels. Each sample is a variable length binary contact matrix, and the raw exports are treated as immutable evidence. We audit dataset statistics, label counts, and anomalies before constructing any train and test splits, and a small set of all-zero samples is excluded via a pinned index list.
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
We evaluate three primary protocols. The word holdout protocol uses disjoint vocabularies across train, test, and a competition partition. The instance holdout protocol evaluates held out instances of seen words by separating train and competition vocabularies while keeping the test vocabulary within their union. The cross participant protocol trains on a source participant and evaluates on a target participant under a shared vocabulary constraint. When a target participant has limited within word repetition, we configure the cross participant split generators to allow single instance target words while keeping source side constraints unchanged. All split archives used in this study are enumerated with sizes and checksums in manifest artifacts.
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
Labels are normalized by uppercasing and filtering to alphabet characters, then represented as a space separated character sequence for CTC training and greedy decoding. This normalization is applied consistently during split construction and dataset preparation to avoid vocabulary drift.
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
We report character error rate from greedy decoding and streaming speed using real time factor, defined as total inference time divided by total input duration. For open-vocabulary decoding we also report lexicon projection error rates using a training lexicon and a full lexicon.
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
Our baseline model encodes each frame as a vector of palate channels and applies a uni-directional recurrent decoder trained with a CTC objective. We compare two layout aware front ends: a row and column pooling front end that aggregates a proxy grid into one dimensional summaries, and a grid reconstruction front end that applies a convolutional spatial encoder. For the grid model we optionally enable a spatial augmentation that drops and shifts contiguous electrode blocks.
```

Slot trace:
```json
{}
```

### Section: Results (id=results)

#### Block b_results_1 (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_table_main_csv, ev_msx20260224_metrics_csv

Text:
```text
The baseline recap table summarizes baseline performance under word holdout, instance holdout, and cross participant transfer. Lexicon projection reduces error rates relative to greedy decoding across protocols, highlighting the importance of open-vocabulary post processing for spelling.
```

Slot trace:
```json
{}
```

#### Block tbl_main (kind=table)
- status: supported
- evidence_ids: ev_msx20260224_table_main_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_msx_tables_for_paperjson_py
- source_evidence_id: ev_msx20260224_table_main_csv

Text:
```text
[TABLE] label=tab:main source_evidence_id=ev_msx20260224_table_main_csv
Caption: Baseline recap across three evaluation protocols (mean and standard deviation over groups).
```

Slot trace:
```json
{}
```

#### Block b_results_to4 (kind=paragraph)
- status: supported
- evidence_ids: ev_uc20260226_table_to4_generalization_csv, ev_uc20260226_to4_metrics_csv, ev_uc20260226_split_npz_manifest_to4_csv

Text:
```text
We additionally evaluate cross participant generalization targeting participant four under both single source and multi source transfer. The to participant four generalization table summarizes direction level seed statistics, and the corresponding split archives are pinned by checksum in a dedicated manifest artifact.
```

Slot trace:
```json
{}
```

#### Block tbl_to4_generalization (kind=table)
- status: supported
- evidence_ids: ev_uc20260226_table_to4_generalization_csv, ev_uc20260226_to4_metrics_csv, ev_scripts_paper_export_uc20260226_tables_py
- source_evidence_id: ev_uc20260226_table_to4_generalization_csv

Text:
```text
[TABLE] label=tab:tofour source_evidence_id=ev_uc20260226_table_to4_generalization_csv
Caption: Cross participant generalization targeting participant four (direction wise mean and standard deviation over seeds, plus across direction aggregation).
```

Slot trace:
```json
{}
```

#### Block b_results_spatial (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_table_spatial_k124_csv, ev_ed20260217_h11_spatial2d_vs_vector_p1_k32_k64_k96_k124_2026-02-17, ev_ed20260217_h13_rowcol_vs_vector_p1_k32_k64_2026-02-17

Text:
```text
The spatial modeling table compares spatial inductive bias variants at full channels across protocols. The row and column front end tracks the vector baseline more closely than the convolutional grid front end, and the grid front end increases real time factor. This trend is consistent with our single participant spatial analysis.
```

Slot trace:
```json
{}
```

#### Block tbl_spatial_k124 (kind=table)
- status: supported
- evidence_ids: ev_msx20260224_table_spatial_k124_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_msx_tables_for_paperjson_py
- source_evidence_id: ev_msx20260224_table_spatial_k124_csv

Text:
```text
[TABLE] label=tab:spatial source_evidence_id=ev_msx20260224_table_spatial_k124_csv
Caption: Spatial modeling comparison at full channels (mean and standard deviation over groups).
```

Slot trace:
```json
{}
```

#### Block b_results_k64 (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_table_k64_methods_csv, ev_msx20260224_metrics_csv

Text:
```text
The electrode reduction table evaluates a reduced channel budget using several selection strategies. Across protocols, within participant selection and simple transfer selection yield similar performance, suggesting that a compact subset can preserve a large fraction of the vector baseline performance.
```

Slot trace:
```json
{}
```

#### Block tbl_k64_methods (kind=table)
- status: supported
- evidence_ids: ev_msx20260224_table_k64_methods_csv, ev_msx20260224_metrics_csv, ev_scripts_paper_export_msx_tables_for_paperjson_py
- source_evidence_id: ev_msx20260224_table_k64_methods_csv

Text:
```text
[TABLE] label=tab:k64 source_evidence_id=ev_msx20260224_table_k64_methods_csv
Caption: Electrode reduction methods under a reduced channel budget (mean and standard deviation over groups).
```

Slot trace:
```json
{}
```

### Section: Discussion (id=discussion)

#### Block b_discussion (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_metrics_csv, ev_msx20260224_table_spatial_k64_csv, ev_ed20260217_h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17, ev_msx20260224_table_p3ms_csv, ev_msx20260224_table_kshot_csv, ev_uc20260226_p3ms_conditions_csv, ev_uc20260226_fig_p3ms_delta_vs_similarity_png, ev_uc20260226_p3ms_conditions_md

Text:
```text
Our results suggest that an explicit convolutional grid encoder is not automatically beneficial for electropalatography, despite its intuitive spatial structure. Spatial augmentation can improve robustness to synthetic electrode dropout, but it does not close the gap in our multi-participant accuracy results. Additional analyses on multi-source cross participant transfer and low shot adaptation are provided as artifact tables, and they highlight that cross participant performance remains challenging. We also provide a conditions analysis of multi-source transfer deltas versus simple dataset similarity measures, which shows that the effect is conditional and does not present a single dominant monotonic trend within our evaluated group set.
```

Slot trace:
```json
{}
```

### Section: Artifacts and Auditability (id=artifacts)

#### Block b_artifacts (kind=paragraph)
- status: supported
- evidence_ids: ev_msx20260224_split_npz_manifest_csv, ev_msx20260224_metrics_csv, ev_msx20260224_table_main_csv, ev_msx20260224_table_spatial_k124_csv, ev_msx20260224_table_k64_methods_csv, ev_uc20260226_split_npz_manifest_to4_csv, ev_uc20260226_table_to4_generalization_csv, ev_uc20260226_p3ms_conditions_csv

Text:
```text
This repository uses a strict paper registry that pins every evidence file by checksum and rejects unsupported manuscript blocks. The split manifests, aggregated metrics, compact tables, and analysis summaries referenced in this paper are stored as deterministic artifacts, enabling audit and reproduction within our repository environment.
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
