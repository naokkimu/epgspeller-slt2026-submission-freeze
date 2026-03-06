# b_models_1

- kind: `paragraph`
- status: `supported`
- section: Models (models) ([models](../sections/models.md))
- generated_utc: 2026-03-04T11:22:19+00:00
- citations: `\\cite{graves2006connectionist,park2019specaugment}`

## Evidence (ids)
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md) kind=`data` path=`scripts/prepare_silentspeller_dataset.py` sha256=`0c13a2f8d7bb7f470851d1928acd1bf51633b42d532c4dc1cbd746f4fb9d69aa`
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md) kind=`data` path=`scripts/train.py` sha256=`9fe71a8eff17ed9d4e8f249a55c2d805e2b011b3068ae75ab47eedb9d3593853`
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md) kind=`data` path=`src/neural_decoder/model.py` sha256=`738e9282960ff03c3d378c3c9f5862ba2d9bde7570822a57e764b42069aed5ed`

## Slices (supports)
- `sl_ev_references_sanitized_ascii_cited_bib_bibtex_entry_bd3d09a82b` kind=`bibtex_entry` evidence=`ev_references_sanitized_ascii_cited_bib` spec={"key": "park2019specaugment"}
- `sl_ev_references_sanitized_ascii_cited_bib_bibtex_entry_fd9095c975` kind=`bibtex_entry` evidence=`ev_references_sanitized_ascii_cited_bib` spec={"key": "graves2006connectionist"}

## Statements

### st_b_models_1_01
Our baseline model encodes each frame as a vector of palate channels and applies a uni-directional recurrent decoder trained with a CTC objective.

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md)
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md)

### st_b_models_1_02
We compare two layout aware front ends.

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md)
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md)

### st_b_models_1_03
One is a row and column pooling front end that aggregates a proxy grid into one dimensional summaries.

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md)
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md)

### st_b_models_1_04
The other is a grid front end that reconstructs a proxy grid and applies a convolutional spatial encoder.

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md)
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md)

### st_b_models_1_05
For the grid model we optionally enable a spatial augmentation that drops and shifts contiguous electrode blocks. ~\\cite{graves2006connectionist,park2019specaugment}

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md)
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md)

slice_supports:
- `sl_ev_references_sanitized_ascii_cited_bib_bibtex_entry_bd3d09a82b` kind=`bibtex_entry` evidence=`ev_references_sanitized_ascii_cited_bib` spec={"key": "park2019specaugment"}
- `sl_ev_references_sanitized_ascii_cited_bib_bibtex_entry_fd9095c975` kind=`bibtex_entry` evidence=`ev_references_sanitized_ascii_cited_bib` spec={"key": "graves2006connectionist"}
