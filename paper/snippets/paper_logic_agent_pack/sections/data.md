# Data and Protocols (data)

- pack_index: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/snippets/paper_logic_agent_pack/index.md`
- narrative: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/snippets/paper_logic_agent_pack/narrative.md`

## Blocks
- [b_data_1](../blocks/b_data_1.md) kind=`paragraph`
- [b_data_audit_2](../blocks/b_data_audit_2.md) kind=`paragraph`
- [b_data_summary](../blocks/b_data_summary.md) kind=`paragraph`
- [tbl_dataset_summary](../blocks/tbl_dataset_summary.md) kind=`table`
- [b_protocols_1](../blocks/b_protocols_1.md) kind=`paragraph`
- [b_protocols_2](../blocks/b_protocols_2.md) kind=`paragraph`
- [b_labels_1](../blocks/b_labels_1.md) kind=`paragraph`
- [b_labels_2](../blocks/b_labels_2.md) kind=`paragraph`
- [b_metrics_1](../blocks/b_metrics_1.md) kind=`paragraph`
- [b_metrics_2](../blocks/b_metrics_2.md) kind=`paragraph`

## Narrative

## Data and Protocols (data)

### [b_data_1](../blocks/b_data_1.md) (paragraph)
We use four participant electropalatography datasets with word labels. Each sample is a variable length binary contact matrix, and the raw exports are treated as immutable evidence. We refer to participants with anonymous labels in all tables and split archives. We audit dataset statistics, label counts, and anomalies before we construct any train and test splits. We exclude a small set of all-zero samples via a pinned index list.

### [b_data_audit_2](../blocks/b_data_audit_2.md) (paragraph)
The audit pipeline records raw file checksums. It validates schema consistency. It summarizes label counts, sequence length summaries, and per channel activity statistics before any split construction. The raw exports remain unchanged. We apply any exclusions only through pinned index lists that are included in the audit artifacts.

### [b_data_summary](../blocks/b_data_summary.md) (paragraph)
The dataset summary table reports id, sample count, vocabulary size, median sequence length, mean contact rate, and the count of all-zero samples for each participant dataset. The id labels are anonymous participant codes used throughout the protocol manifests.

### [tbl_dataset_summary](../blocks/tbl_dataset_summary.md) (table)
Table: Raw dataset summary for each participant dataset; id is an anonymous participant label, N is sample count, V is vocabulary size, Tmed is median sequence length in frames, contact is mean contact rate, and zero is the count of all-zero samples. (source: `ev_paper_layout_2026_03_03_table_dataset_summary_csv`) path=`results/paper_layout_2026-03-03/table_dataset_summary.csv`

### [b_protocols_1](../blocks/b_protocols_1.md) (paragraph)
We evaluate three primary protocols. The word holdout protocol uses disjoint vocabularies across train, test, and a competition partition. The instance holdout protocol tests held out instances of seen words. It separates train and competition vocabularies while keeping the test vocabulary within their union. The cross participant protocol trains on a source participant and tests on a target participant under a shared vocabulary constraint. We also define a paired source cross participant variant and a low shot adaptation variant to isolate source aggregation and limited supervision effects under the same audit rules. When a target participant has limited within word repetition, we configure the cross participant split generators to allow single instance target words. We keep the source side constraints unchanged. All split archives used in this study are enumerated with sizes and checksums in manifest artifacts.

### [b_protocols_2](../blocks/b_protocols_2.md) (paragraph)
All split archives are generated deterministically from audited exports with fixed seeds. Each train, test, and competition partition is stored as an immutable archive with a checksum in the manifests to enable reuse and later verification. The manifests show the word-holdout protocol uses all four participant datasets. They show the instance-holdout protocol uses three participant datasets. They also show the fourth participant appears only as a target in the cross-participant splits. This separation explains why the dataset summary includes all participant datasets even when a protocol uses only a subset.

### [b_labels_1](../blocks/b_labels_1.md) (paragraph)
We normalize labels by uppercasing and filtering to alphabet characters, then represent each label as a space separated character sequence for CTC training and greedy decoding. We apply this step consistently during split construction and dataset preparation to avoid vocabulary drift.

### [b_labels_2](../blocks/b_labels_2.md) (paragraph)
We keep the label normalization step consistent across all splits and dataset preparation steps. This aligns the decoder vocabulary with the audited labels and reduces drift between training and artifacts used to evaluate.

### [b_metrics_1](../blocks/b_metrics_1.md) (paragraph)
We report character error rate from greedy decoding and streaming speed using real time factor. We define real time factor as total inference time divided by total input duration. For open-vocabulary decoding we also report lexicon projection error rates using a training lexicon and a full lexicon.

### [b_metrics_2](../blocks/b_metrics_2.md) (paragraph)
Greedy decoding reports unconstrained character sequences. Lexicon projection maps outputs to finite word sets derived from the training vocabulary or the full audited lexicon. This allows us to separate decoding quality from lexicon constraints. We compute real time factor by dividing inference time by input duration under the same test harness.
