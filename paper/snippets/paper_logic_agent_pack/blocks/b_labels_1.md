# b_labels_1

- kind: `paragraph`
- status: `supported`
- section: Data and Protocols (data) ([data](../sections/data.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md) kind=`data` path=`scripts/prepare_silentspeller_dataset.py` sha256=`0c13a2f8d7bb7f470851d1928acd1bf51633b42d532c4dc1cbd746f4fb9d69aa`
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md) kind=`data` path=`scripts/rebuttal/make_instance_holdout_split.py` sha256=`07041c24ac0120a854ca55921017f9e628510b7e0b783e8bf74b55f3b6c783e2`
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md) kind=`data` path=`scripts/rebuttal/make_word_holdout_split.py` sha256=`29765a348234ddafcd7c0bb3aeedc3dad1813fa863da921039dcf2b5e4be5065`

## Statements

### st_b_labels_1_01
We normalize labels by uppercasing and filtering to alphabet characters, then represent each label as a space separated character sequence for CTC training and greedy decoding.

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)

### st_b_labels_1_02
We apply this step consistently during split construction and dataset preparation to avoid vocabulary drift.

evidence_supports:
- [ev_scripts_prepare_silentspeller_dataset_py](../evidence/ev_scripts_prepare_silentspeller_dataset_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)
