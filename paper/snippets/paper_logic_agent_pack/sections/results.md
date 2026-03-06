# Results (results)

- pack_index: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/snippets/paper_logic_agent_pack/index.md`
- narrative: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/snippets/paper_logic_agent_pack/narrative.md`

## Blocks
- [b_results_1](../blocks/b_results_1.md) kind=`paragraph`
- [b_results_to4](../blocks/b_results_to4.md) kind=`paragraph`
- [tbl_to4_generalization](../blocks/tbl_to4_generalization.md) kind=`table`
- [b_results_to4_2](../blocks/b_results_to4_2.md) kind=`paragraph`
- [b_results_spatial](../blocks/b_results_spatial.md) kind=`paragraph`
- [tbl_spatial_all](../blocks/tbl_spatial_all.md) kind=`table`
- [b_results_k64](../blocks/b_results_k64.md) kind=`paragraph`
- [tbl_k64_all](../blocks/tbl_k64_all.md) kind=`table`
- [b_results_k64_2](../blocks/b_results_k64_2.md) kind=`paragraph`
- [b_results_p3ms](../blocks/b_results_p3ms.md) kind=`paragraph`
- [tbl_p3ms_compact](../blocks/tbl_p3ms_compact.md) kind=`table`
- [b_results_p3ms_conditions](../blocks/b_results_p3ms_conditions.md) kind=`paragraph`
- [b_results_kshot](../blocks/b_results_kshot.md) kind=`paragraph`
- [tbl_kshot_compact](../blocks/tbl_kshot_compact.md) kind=`table`

## Narrative

## Results (results)

### [b_results_1](../blocks/b_results_1.md) (paragraph)
Baseline performance across protocols is derived from the same metrics registry as the remaining tables. We report greedy decoding error and lexicon-projected error to separate open vocabulary decoding quality from lexicon constraints. The vector baseline rows in the spatial modeling and electrode reduction tables serve as the reference for protocol comparisons. We use the same split manifests and deterministic evaluation scripts across all protocols.

### [b_results_to4](../blocks/b_results_to4.md) (paragraph)
We evaluate cross participant transfer with the fourth participant as target under single source and paired source settings. The table uses protocol labels for single source cross participant transfer and multi source transfer. The lvl field marks direction level rows and an across direction aggregate. Group labels join source participant identifiers with an arrow to the target. The split archives that define these targets are pinned by checksum in the manifest. In our audited splits, the multi source aggregate reduces CER relative to the single source aggregate for the same target.

### [tbl_to4_generalization](../blocks/tbl_to4_generalization.md) (table)
Table: Cross participant generalization targeting the fourth participant; proto distinguishes single source cross participant transfer and multi source transfer, lvl marks direction level rows versus an across direction aggregate, group encodes source to target participant labels, CER is character error rate, and lex is lexicon projected error rate. (source: `ev_paper_layout_2026_03_03_table_to4_compact_csv`) path=`results/paper_layout_2026-03-03/table_to4_compact.csv`

### [b_results_to4_2](../blocks/b_results_to4_2.md) (paragraph)
The cross participant results for the fourth participant include both single source and paired source settings. This provides a direct comparison of transfer with and without source aggregation under the same audited protocol constraints. This helps isolate source aggregation effects without changing the target data or evaluation pipeline.

### [b_results_spatial](../blocks/b_results_spatial.md) (paragraph)
The spatial modeling table compares spatial inductive bias variants at full channels across protocols. We include a patchpool grid encoder as a minimal way to implement a rescue for the grid encoder. The patchpool variant keeps a coarser spatial map before recurrent decoding. The variant labels are vec, rowcol, grid, grid_aug, patch, and patch_aug. The row and column front end tracks the vector baseline more closely than the convolutional grid front end under within participant protocols. Patchpool reduces the gap under cross participant transfer. Across protocols, grid variants tend to increase real time factor relative to the vector baseline. We do not observe a consistent accuracy gain over the vector baseline in any protocol.

### [tbl_spatial_all](../blocks/tbl_spatial_all.md) (table)
Table: Spatial modeling at full channels across protocols; protocol labels denote word holdout, instance holdout, and cross participant transfer, vec is vector baseline, rowcol is row and column pooling, grid is convolutional grid encoder, grid aug is grid with spatial augmentation, patch is patchpool grid encoder, patch aug is patchpool with augmentation, CER is character error rate, and RTF is real time factor. (source: `ev_paper_layout_2026_03_03_table_spatial_all_csv`) path=`results/paper_layout_2026-03-03/table_spatial_all.csv`

### [b_results_k64](../blocks/b_results_k64.md) (paragraph)
The electrode reduction table evaluates a reduced channel budget using several selection strategies. The method labels are topk, fps two k, xfer, and rand. The table reports both accuracy and streaming speed so reduction effects can be compared under the same evaluation harness. Across protocols, within participant selection and simple transfer selection yield similar performance. This suggests that a compact subset can preserve a large fraction of the vector baseline performance. Random selection and simple transfer remain slightly worse than within participant selection in the audited results.

### [tbl_k64_all](../blocks/tbl_k64_all.md) (table)
Table: Electrode reduction methods across protocols; protocol labels denote word holdout, instance holdout, and cross participant transfer, topk is within participant top ranked selection, fps two k is farthest point sampling, xfer is transfer selection, rand is random selection, CER is character error rate, and RTF is real time factor. (source: `ev_paper_layout_2026_03_03_table_k64_all_csv`) path=`results/paper_layout_2026-03-03/table_k64_all.csv`

### [b_results_k64_2](../blocks/b_results_k64_2.md) (paragraph)
The reduction results complement the protocol tables. They show that compact selections preserve much of the vector baseline under within participant tests. Cross participant transfer remains more challenging, so we report paired source and low shot analyses in the subsequent tables.

### [b_results_p3ms](../blocks/b_results_p3ms.md) (paragraph)
We evaluate multi source cross participant transfer using paired source participants. The group labels concatenate the two source identifiers and use an arrow to the target identifier. The multi source table reports direction level results for vector and layout aware front ends. This isolates whether combining sources helps under the same target and protocol constraints.

### [tbl_p3ms_compact](../blocks/tbl_p3ms_compact.md) (table)
Table: Multi source cross participant results by source pair; group concatenates source participant labels with an arrow to the target, vec is vector baseline, rowcol is row and column pooling, grid is convolutional grid encoder, grid aug is grid with spatial augmentation, CER is character error rate, and RTF is real time factor. (source: `ev_paper_layout_2026_03_03_table_p3ms_compact_csv`) path=`results/paper_layout_2026-03-03/table_p3ms_compact.csv`

### [b_results_p3ms_conditions](../blocks/b_results_p3ms_conditions.md) (paragraph)
We further analyze multi source transfer deltas against simple similarity measures. Delta_cer is negative for all audited groups, and corr_src_tgt_mean varies within a narrow range across groups. We report these measures to describe conditions rather than to assert a universal rule.

### [b_results_kshot](../blocks/b_results_kshot.md) (paragraph)
We evaluate how models adapt in low shot settings for a new participant by varying the number of training instances per word. For the vector baseline, two shot improves over one shot, and the table reports layout aware variants. This isolates adaptation behavior when only a small amount of labeled target data is available.

### [tbl_kshot_compact](../blocks/tbl_kshot_compact.md) (table)
Table: Low shot adaptation results for a new participant; group uses the participant label and k one or k two for the number of training instances per word, vec is vector baseline, rowcol is row and column pooling, grid is convolutional grid encoder, grid aug is grid with spatial augmentation, CER is character error rate, and RTF is real time factor. (source: `ev_paper_layout_2026_03_03_table_kshot_compact_csv`) path=`results/paper_layout_2026-03-03/table_kshot_compact.csv`
