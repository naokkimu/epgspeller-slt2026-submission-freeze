# Models (models)

- pack_index: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/snippets/paper_logic_agent_pack/index.md`
- narrative: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/snippets/paper_logic_agent_pack/narrative.md`

## Blocks
- [b_models_1](../blocks/b_models_1.md) kind=`paragraph`
- [b_models_2](../blocks/b_models_2.md) kind=`paragraph`
- [b_training_1](../blocks/b_training_1.md) kind=`paragraph`

## Narrative

## Models (models)

### [b_models_1](../blocks/b_models_1.md) (paragraph)
Our baseline model encodes each frame as a vector of palate channels and applies a uni-directional recurrent decoder trained with a CTC objective. We compare two layout aware front ends. One is a row and column pooling front end that aggregates a proxy grid into one dimensional summaries. The other is a grid front end that reconstructs a proxy grid and applies a convolutional spatial encoder. For the grid model we optionally enable a spatial augmentation that drops and shifts contiguous electrode blocks. ~\\cite{graves2006connectionist,park2019specaugment}

### [b_models_2](../blocks/b_models_2.md) (paragraph)
The proxy grid is constructed from the palate channel layout. It supports row and column pooling or convolutional feature extraction. We use a fixed layout file for the mapping so that row and column indices are consistent across splits. We augment spatially by perturbing contiguous electrode blocks to emulate missing contacts and minor spatial shifts.

### [b_training_1](../blocks/b_training_1.md) (paragraph)
We fix core training hyperparameters across runs and record how we configure them in the metrics registry for auditability.
