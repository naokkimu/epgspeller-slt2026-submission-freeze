# paper-logic agent pack (narrative)

**Title:** EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for Open-Vocabulary Silent Spelling
**Venue:** interspeech
**Type:** regular
**Stage:** review
**Generated (UTC):** 2026-03-04T11:22:19+00:00

Notes:
- Figures and paper-only formatting (2-column layout, \ref) are treated as noise and omitted/stripped.
- Claims-first verification lives in `claims.md`; this file is context/flow only.
- Follow links to block files for supports (evidence/slices/needs) and to evidence files for excerpts.

## Abstract (abstract)

### [b_abs](blocks/b_abs.md) (paragraph)
Silent speech text entry with electropalatography requires models that generalize across word identities and participants while remaining auditable. We present an evidence-only study of open-vocabulary silent spelling from binary palate contact patterns. We define protocols for word holdout, instance holdout, and cross participant transfer. Using participant labeled datasets and deterministic artifact tracking, we evaluate a vector baseline and two layout aware front ends. We also analyze electrode reduction and how models adapt in low shot settings. Across our audited runs, the row and column front end tracks the vector baseline more closely than a convolutional grid front end. The grid front end increases streaming latency. We release split manifests, checksums, and compact result tables as pinned repository artifacts.

## Introduction (intro)

### [b_intro_1](blocks/b_intro_1.md) (paragraph)
Silent speech interfaces aim to enable communication without audible acoustics. They use sensor measures of articulation or physiology. Electropalatography provides a practical binary contact form for tongue and palate interaction. Its discrete layout and device variability raise questions about inductive bias, robustness, and how models generalize. ~\\cite{denby2010silent,freitas2017an,gonzalez2020silent,lee2021biosignal}

### [b_intro_2](blocks/b_intro_2.md) (paragraph)
Recent work on silent spelling has emphasized open-vocabulary text entry, where character level decoding can compose words beyond a fixed closed set. We study open-vocabulary spelling with a CTC style decoder and lexicon projection. We compare vector and layout aware front ends under multiple protocols that test how models generalize across words. ~\\cite{dong2024rehearsse,graves2006connectionist,kimura2022silentspeller}

### [b_contrib](blocks/b_contrib.md) (bullets)
- We define protocols to evaluate word identity generalization and participant transfer, and we provide split archives with checksums.
- We run multi-participant experiments with open-vocabulary decoding and lexicon projection, tracked by a strict evidence registry.
- We compare a vector baseline with two layout aware front ends, and we report both accuracy and streaming speed metrics.
- We provide deterministic scripts that export compact tables and manifests used by this manuscript.

## Related Work (related)

### [b_related_1](blocks/b_related_1.md) (paragraph)
Within our surveyed set, SilentSpeller and ReHEarSSE represent open-vocabulary silent spelling systems. Broader silent speech systems span constrained recognition and reconstruction settings. In the electropalatography literature, the spatial layout is used to visualize contacts, characterize devices, and reduce how contacts are represented. This motivates tests of layout aware inductive bias in learned decoders. ~\\cite{carreira1998dimensionality,denby2010silent,dong2024rehearsse,gonzalez2020silent,hardcastle1989new,hardcastle1990electropalatography,hardcastle1991epg,hueber2010development,kimura2022silentspeller,shadle1993depth,toutios2006learning,toutios2006on,verhoeven2019visualisation,woo2021design}

### [b_related_positioning](blocks/b_related_positioning.md) (paragraph)
We summarize the positioning of prior work using survey tags. These tags map systems by how they represent data and by system scope. We describe where open vocabulary silent spelling and electropalatography studies sit in the space.

### [b_related_2](blocks/b_related_2.md) (paragraph)
Prior electropalatography studies emphasize that contact patterns are structured by the palate layout. This motivates a proxy grid form and spatially structured modeling in learned decoders. Our work situates these ideas within open vocabulary silent spelling by making protocol definitions and artifact traceability explicit.

## Data and Protocols (data)

### [b_data_1](blocks/b_data_1.md) (paragraph)
We use four participant electropalatography datasets with word labels. Each sample is a variable length binary contact matrix, and the raw exports are treated as immutable evidence. We refer to participants with anonymous labels in all tables and split archives. We audit dataset statistics, label counts, and anomalies before we construct any train and test splits. We exclude a small set of all-zero samples via a pinned index list.

### [b_data_audit_2](blocks/b_data_audit_2.md) (paragraph)
The audit pipeline records raw file checksums. It validates schema consistency. It summarizes label counts, sequence length summaries, and per channel activity statistics before any split construction. The raw exports remain unchanged. We apply any exclusions only through pinned index lists that are included in the audit artifacts.

### [b_data_summary](blocks/b_data_summary.md) (paragraph)
The dataset summary table reports id, sample count, vocabulary size, median sequence length, mean contact rate, and the count of all-zero samples for each participant dataset. The id labels are anonymous participant codes used throughout the protocol manifests.

### [tbl_dataset_summary](blocks/tbl_dataset_summary.md) (table)
Table: Raw dataset summary for each participant dataset; id is an anonymous participant label, N is sample count, V is vocabulary size, Tmed is median sequence length in frames, contact is mean contact rate, and zero is the count of all-zero samples. (source: `ev_paper_layout_2026_03_03_table_dataset_summary_csv`) path=`results/paper_layout_2026-03-03/table_dataset_summary.csv`

### [b_protocols_1](blocks/b_protocols_1.md) (paragraph)
We evaluate three primary protocols. The word holdout protocol uses disjoint vocabularies across train, test, and a competition partition. The instance holdout protocol tests held out instances of seen words. It separates train and competition vocabularies while keeping the test vocabulary within their union. The cross participant protocol trains on a source participant and tests on a target participant under a shared vocabulary constraint. We also define a paired source cross participant variant and a low shot adaptation variant to isolate source aggregation and limited supervision effects under the same audit rules. When a target participant has limited within word repetition, we configure the cross participant split generators to allow single instance target words. We keep the source side constraints unchanged. All split archives used in this study are enumerated with sizes and checksums in manifest artifacts.

### [b_protocols_2](blocks/b_protocols_2.md) (paragraph)
All split archives are generated deterministically from audited exports with fixed seeds. Each train, test, and competition partition is stored as an immutable archive with a checksum in the manifests to enable reuse and later verification. The manifests show the word-holdout protocol uses all four participant datasets. They show the instance-holdout protocol uses three participant datasets. They also show the fourth participant appears only as a target in the cross-participant splits. This separation explains why the dataset summary includes all participant datasets even when a protocol uses only a subset.

### [b_labels_1](blocks/b_labels_1.md) (paragraph)
We normalize labels by uppercasing and filtering to alphabet characters, then represent each label as a space separated character sequence for CTC training and greedy decoding. We apply this step consistently during split construction and dataset preparation to avoid vocabulary drift.

### [b_labels_2](blocks/b_labels_2.md) (paragraph)
We keep the label normalization step consistent across all splits and dataset preparation steps. This aligns the decoder vocabulary with the audited labels and reduces drift between training and artifacts used to evaluate.

### [b_metrics_1](blocks/b_metrics_1.md) (paragraph)
We report character error rate from greedy decoding and streaming speed using real time factor. We define real time factor as total inference time divided by total input duration. For open-vocabulary decoding we also report lexicon projection error rates using a training lexicon and a full lexicon.

### [b_metrics_2](blocks/b_metrics_2.md) (paragraph)
Greedy decoding reports unconstrained character sequences. Lexicon projection maps outputs to finite word sets derived from the training vocabulary or the full audited lexicon. This allows us to separate decoding quality from lexicon constraints. We compute real time factor by dividing inference time by input duration under the same test harness.

## Models (models)

### [b_models_1](blocks/b_models_1.md) (paragraph)
Our baseline model encodes each frame as a vector of palate channels and applies a uni-directional recurrent decoder trained with a CTC objective. We compare two layout aware front ends. One is a row and column pooling front end that aggregates a proxy grid into one dimensional summaries. The other is a grid front end that reconstructs a proxy grid and applies a convolutional spatial encoder. For the grid model we optionally enable a spatial augmentation that drops and shifts contiguous electrode blocks. ~\\cite{graves2006connectionist,park2019specaugment}

### [b_models_2](blocks/b_models_2.md) (paragraph)
The proxy grid is constructed from the palate channel layout. It supports row and column pooling or convolutional feature extraction. We use a fixed layout file for the mapping so that row and column indices are consistent across splits. We augment spatially by perturbing contiguous electrode blocks to emulate missing contacts and minor spatial shifts.

### [b_training_1](blocks/b_training_1.md) (paragraph)
We fix core training hyperparameters across runs and record how we configure them in the metrics registry for auditability.

## Results (results)

### [b_results_1](blocks/b_results_1.md) (paragraph)
Baseline performance across protocols is derived from the same metrics registry as the remaining tables. We report greedy decoding error and lexicon-projected error to separate open vocabulary decoding quality from lexicon constraints. The vector baseline rows in the spatial modeling and electrode reduction tables serve as the reference for protocol comparisons. We use the same split manifests and deterministic evaluation scripts across all protocols.

### [b_results_to4](blocks/b_results_to4.md) (paragraph)
We evaluate cross participant transfer with the fourth participant as target under single source and paired source settings. The table uses protocol labels for single source cross participant transfer and multi source transfer. The lvl field marks direction level rows and an across direction aggregate. Group labels join source participant identifiers with an arrow to the target. The split archives that define these targets are pinned by checksum in the manifest. In our audited splits, the multi source aggregate reduces CER relative to the single source aggregate for the same target.

### [tbl_to4_generalization](blocks/tbl_to4_generalization.md) (table)
Table: Cross participant generalization targeting the fourth participant; proto distinguishes single source cross participant transfer and multi source transfer, lvl marks direction level rows versus an across direction aggregate, group encodes source to target participant labels, CER is character error rate, and lex is lexicon projected error rate. (source: `ev_paper_layout_2026_03_03_table_to4_compact_csv`) path=`results/paper_layout_2026-03-03/table_to4_compact.csv`

### [b_results_to4_2](blocks/b_results_to4_2.md) (paragraph)
The cross participant results for the fourth participant include both single source and paired source settings. This provides a direct comparison of transfer with and without source aggregation under the same audited protocol constraints. This helps isolate source aggregation effects without changing the target data or evaluation pipeline.

### [b_results_spatial](blocks/b_results_spatial.md) (paragraph)
The spatial modeling table compares spatial inductive bias variants at full channels across protocols. We include a patchpool grid encoder as a minimal way to implement a rescue for the grid encoder. The patchpool variant keeps a coarser spatial map before recurrent decoding. The variant labels are vec, rowcol, grid, grid_aug, patch, and patch_aug. The row and column front end tracks the vector baseline more closely than the convolutional grid front end under within participant protocols. Patchpool reduces the gap under cross participant transfer. Across protocols, grid variants tend to increase real time factor relative to the vector baseline. We do not observe a consistent accuracy gain over the vector baseline in any protocol.

### [tbl_spatial_all](blocks/tbl_spatial_all.md) (table)
Table: Spatial modeling at full channels across protocols; protocol labels denote word holdout, instance holdout, and cross participant transfer, vec is vector baseline, rowcol is row and column pooling, grid is convolutional grid encoder, grid aug is grid with spatial augmentation, patch is patchpool grid encoder, patch aug is patchpool with augmentation, CER is character error rate, and RTF is real time factor. (source: `ev_paper_layout_2026_03_03_table_spatial_all_csv`) path=`results/paper_layout_2026-03-03/table_spatial_all.csv`

### [b_results_k64](blocks/b_results_k64.md) (paragraph)
The electrode reduction table evaluates a reduced channel budget using several selection strategies. The method labels are topk, fps two k, xfer, and rand. The table reports both accuracy and streaming speed so reduction effects can be compared under the same evaluation harness. Across protocols, within participant selection and simple transfer selection yield similar performance. This suggests that a compact subset can preserve a large fraction of the vector baseline performance. Random selection and simple transfer remain slightly worse than within participant selection in the audited results.

### [tbl_k64_all](blocks/tbl_k64_all.md) (table)
Table: Electrode reduction methods across protocols; protocol labels denote word holdout, instance holdout, and cross participant transfer, topk is within participant top ranked selection, fps two k is farthest point sampling, xfer is transfer selection, rand is random selection, CER is character error rate, and RTF is real time factor. (source: `ev_paper_layout_2026_03_03_table_k64_all_csv`) path=`results/paper_layout_2026-03-03/table_k64_all.csv`

### [b_results_k64_2](blocks/b_results_k64_2.md) (paragraph)
The reduction results complement the protocol tables. They show that compact selections preserve much of the vector baseline under within participant tests. Cross participant transfer remains more challenging, so we report paired source and low shot analyses in the subsequent tables.

### [b_results_p3ms](blocks/b_results_p3ms.md) (paragraph)
We evaluate multi source cross participant transfer using paired source participants. The group labels concatenate the two source identifiers and use an arrow to the target identifier. The multi source table reports direction level results for vector and layout aware front ends. This isolates whether combining sources helps under the same target and protocol constraints.

### [tbl_p3ms_compact](blocks/tbl_p3ms_compact.md) (table)
Table: Multi source cross participant results by source pair; group concatenates source participant labels with an arrow to the target, vec is vector baseline, rowcol is row and column pooling, grid is convolutional grid encoder, grid aug is grid with spatial augmentation, CER is character error rate, and RTF is real time factor. (source: `ev_paper_layout_2026_03_03_table_p3ms_compact_csv`) path=`results/paper_layout_2026-03-03/table_p3ms_compact.csv`

### [b_results_p3ms_conditions](blocks/b_results_p3ms_conditions.md) (paragraph)
We further analyze multi source transfer deltas against simple similarity measures. Delta_cer is negative for all audited groups, and corr_src_tgt_mean varies within a narrow range across groups. We report these measures to describe conditions rather than to assert a universal rule.

### [b_results_kshot](blocks/b_results_kshot.md) (paragraph)
We evaluate how models adapt in low shot settings for a new participant by varying the number of training instances per word. For the vector baseline, two shot improves over one shot, and the table reports layout aware variants. This isolates adaptation behavior when only a small amount of labeled target data is available.

### [tbl_kshot_compact](blocks/tbl_kshot_compact.md) (table)
Table: Low shot adaptation results for a new participant; group uses the participant label and k one or k two for the number of training instances per word, vec is vector baseline, rowcol is row and column pooling, grid is convolutional grid encoder, grid aug is grid with spatial augmentation, CER is character error rate, and RTF is real time factor. (source: `ev_paper_layout_2026_03_03_table_kshot_compact_csv`) path=`results/paper_layout_2026-03-03/table_kshot_compact.csv`

## Discussion (discussion)

### [b_discussion](blocks/b_discussion.md) (paragraph)
Our results suggest that an explicit convolutional grid encoder is not automatically beneficial for electropalatography under within participant tests, despite its intuitive spatial structure. A patchpool grid variant reduces the underperformance of the grid encoder under cross participant transfer. This indicates that spatial encoder design choices can materially affect outcomes. The patchpool variant does not yield consistent gains over the vector baseline across protocols. Spatial augmentation can improve robustness to synthetic electrode dropout, but it does not close the accuracy gap for the convolutional grid variants in our multi participant results. We analyze multi source cross participant transfer and how models adapt in low shot settings, and we provide the results as artifact tables. They highlight that cross participant performance remains challenging. We also analyze conditions for multi source transfer deltas against simple dataset similarity measures. The effect is conditional and does not present a single dominant monotonic trend within our evaluated group set. These observations are limited to our audited multi participant dataset collection and protocols.

### [b_discussion_2](blocks/b_discussion_2.md) (paragraph)
Across the audited protocols, within participant performance remains stronger than cross participant transfer. This emphasizes the difficulty of generalization under limited participant coverage. The target participant results reinforce this gap even when source aggregation is enabled. We report these trends as artifact grounded observations rather than broad claims. We expect additional participant data to be necessary for stronger transfer conclusions.

## Artifacts and Auditability (artifacts)

### [b_artifacts](blocks/b_artifacts.md) (paragraph)
This repository uses a strict paper registry that pins every evidence file by checksum and rejects unsupported manuscript blocks. The split manifests, aggregated metrics, compact tables, and analysis summaries referenced in this paper are stored as deterministic artifacts, enabling audit and reproduction within our repository environment. The same artifacts are reused to build the manuscript tables and to support verification in the audit views.

## Ethics and Disclosure (ethics)

### [b_ethics](blocks/b_ethics.md) (paragraph)
We report results only for audited artifacts and do not claim broader demographic coverage. The datasets and splits used in this study are derived from participant recordings, and we focus on methodological clarity and artifact traceability rather than deployment claims.

## Generative AI Use Disclosure (ai_disclosure)

### [b_ai_disclosure](blocks/b_ai_disclosure.md) (paragraph)
We used generative AI tools for language polishing and formatting support, and we verified technical claims against audited artifacts.

## Logic Checks (logic_checks)

### [cl_table_main_has_header](blocks/cl_table_main_has_header.md) (paragraph)
The baseline table includes protocol and aggregate metrics fields.

### [cl_dataset_summary_has_header](blocks/cl_dataset_summary_has_header.md) (paragraph)
The dataset summary table includes id, N, V, Tmed, contact, and zero fields.

### [cl_spatial_table_has_header](blocks/cl_spatial_table_has_header.md) (paragraph)
The spatial modeling table includes protocol, variant, CER, and RTF fields.

### [cl_k64_table_has_header](blocks/cl_k64_table_has_header.md) (paragraph)
The electrode reduction table includes protocol, method, CER, and RTF fields.
