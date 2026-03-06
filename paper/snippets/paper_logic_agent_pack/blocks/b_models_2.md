# b_models_2

- kind: `paragraph`
- status: `supported`
- section: Models (models) ([models](../sections/models.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md) kind=`data` path=`scripts/prepare_silentspeller_dataset.py` sha256=`0c13a2f8d7bb7f470851d1928acd1bf51633b42d532c4dc1cbd746f4fb9d69aa`
- [ev_scripts_smartpalate_distribution_csv](../evidence/ev_scripts_smartpalate_distribution_csv.md) kind=`data` path=`scripts/smartpalate_distribution.csv` sha256=`d21d93c9ec3c0ecd6676908c8d8bc58ea2019533260b883c3d0a3b86213c0b84`
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md) kind=`data` path=`scripts/train.py` sha256=`9fe71a8eff17ed9d4e8f249a55c2d805e2b011b3068ae75ab47eedb9d3593853`
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md) kind=`data` path=`src/neural_decoder/model.py` sha256=`738e9282960ff03c3d378c3c9f5862ba2d9bde7570822a57e764b42069aed5ed`

## Statements

### st_b_models_2_01
The proxy grid is constructed from the palate channel layout.

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_smartpalate_distribution_csv](../evidence/ev_scripts_smartpalate_distribution_csv.md)
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md)
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md)

### st_b_models_2_02
It supports row and column pooling or convolutional feature extraction.

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_smartpalate_distribution_csv](../evidence/ev_scripts_smartpalate_distribution_csv.md)
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md)
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md)

### st_b_models_2_03
We use a fixed layout file for the mapping so that row and column indices are consistent across splits.

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_smartpalate_distribution_csv](../evidence/ev_scripts_smartpalate_distribution_csv.md)
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md)
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md)

### st_b_models_2_04
We augment spatially by perturbing contiguous electrode blocks to emulate missing contacts and minor spatial shifts.

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_smartpalate_distribution_csv](../evidence/ev_scripts_smartpalate_distribution_csv.md)
- [ev_scripts_train_py](../evidence/ev_scripts_train_py.md)
- [ev_src_neural_decoder_model_py](../evidence/ev_src_neural_decoder_model_py.md)
