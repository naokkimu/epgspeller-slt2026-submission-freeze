# Discussion (discussion)

- pack_index: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/snippets/paper_logic_agent_pack/index.md`
- narrative: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/snippets/paper_logic_agent_pack/narrative.md`

## Blocks
- [b_discussion](../blocks/b_discussion.md) kind=`paragraph`
- [b_discussion_2](../blocks/b_discussion_2.md) kind=`paragraph`

## Narrative

## Discussion (discussion)

### [b_discussion](../blocks/b_discussion.md) (paragraph)
Our results suggest that an explicit convolutional grid encoder is not automatically beneficial for electropalatography under within participant tests, despite its intuitive spatial structure. A patchpool grid variant reduces the underperformance of the grid encoder under cross participant transfer. This indicates that spatial encoder design choices can materially affect outcomes. The patchpool variant does not yield consistent gains over the vector baseline across protocols. Spatial augmentation can improve robustness to synthetic electrode dropout, but it does not close the accuracy gap for the convolutional grid variants in our multi participant results. We analyze multi source cross participant transfer and how models adapt in low shot settings, and we provide the results as artifact tables. They highlight that cross participant performance remains challenging. We also analyze conditions for multi source transfer deltas against simple dataset similarity measures. The effect is conditional and does not present a single dominant monotonic trend within our evaluated group set. These observations are limited to our audited multi participant dataset collection and protocols.

### [b_discussion_2](../blocks/b_discussion_2.md) (paragraph)
Across the audited protocols, within participant performance remains stronger than cross participant transfer. This emphasizes the difficulty of generalization under limited participant coverage. The target participant results reinforce this gap even when source aggregation is enabled. We report these trends as artifact grounded observations rather than broad claims. We expect additional participant data to be necessary for stronger transfer conclusions.
