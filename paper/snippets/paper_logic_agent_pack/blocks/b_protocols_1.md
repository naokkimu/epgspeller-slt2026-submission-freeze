# b_protocols_1

- kind: `paragraph`
- status: `supported`
- section: Data and Protocols (data) ([data](../sections/data.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md) kind=`data` path=`results/msx20260224/split_npz_manifest.csv` sha256=`8eef0bb574044a4d527c4a3d16a1fa17c31c3b61f83fc7c25a9f8462c5c33363`
- [ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py.md) kind=`data` path=`scripts/rebuttal/make_cross_subject_instance_holdout_split.py` sha256=`7c41255d135ad856637c39c7ac3162041a18d71a53b043a2c97c226157e0b87c`
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md) kind=`data` path=`scripts/rebuttal/make_instance_holdout_split.py` sha256=`07041c24ac0120a854ca55921017f9e628510b7e0b783e8bf74b55f3b6c783e2`
- [ev_scripts_rebuttal_make_kshot_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_kshot_instance_holdout_split_py.md) kind=`data` path=`scripts/rebuttal/make_kshot_instance_holdout_split.py` sha256=`246e41e934eb225d74fc6a738d880c2f16336112b7f8ccb4450bc4c09ff1c763`
- [ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py.md) kind=`data` path=`scripts/rebuttal/make_multi_source_cross_subject_instance_holdout_split.py` sha256=`4b831294d8fab58c02d485c6197ce3fdce4ab8104f7d771417b876dbc7254b34`
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md) kind=`data` path=`scripts/rebuttal/make_word_holdout_split.py` sha256=`29765a348234ddafcd7c0bb3aeedc3dad1813fa863da921039dcf2b5e4be5065`
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md) kind=`data` path=`results/uc20260226/split_npz_manifest_to4.csv` sha256=`8a00315026803e752c9fad58a43a002418ce52dbb338f14e8d46de630b65a766`

## Statements

### st_b_protocols_1_01
We evaluate three primary protocols.

evidence_supports:
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_kshot_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_kshot_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)

### st_b_protocols_1_02
The word holdout protocol uses disjoint vocabularies across train, test, and a competition partition.

evidence_supports:
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_kshot_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_kshot_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)

### st_b_protocols_1_03
The instance holdout protocol tests held out instances of seen words.

evidence_supports:
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_kshot_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_kshot_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)

### st_b_protocols_1_04
It separates train and competition vocabularies while keeping the test vocabulary within their union.

evidence_supports:
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_kshot_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_kshot_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)

### st_b_protocols_1_05
The cross participant protocol trains on a source participant and tests on a target participant under a shared vocabulary constraint.

evidence_supports:
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_kshot_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_kshot_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)

### st_b_protocols_1_06
We also define a paired source cross participant variant and a low shot adaptation variant to isolate source aggregation and limited supervision effects under the same audit rules.

evidence_supports:
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_kshot_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_kshot_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)

### st_b_protocols_1_07
When a target participant has limited within word repetition, we configure the cross participant split generators to allow single instance target words.

evidence_supports:
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_kshot_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_kshot_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)

### st_b_protocols_1_08
We keep the source side constraints unchanged.

evidence_supports:
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_kshot_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_kshot_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)

### st_b_protocols_1_09
All split archives used in this study are enumerated with sizes and checksums in manifest artifacts.

evidence_supports:
- [ev_msx20260224_split_npz_manifest_csv](../evidence/ev_msx20260224_split_npz_manifest_csv.md)
- [ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_kshot_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_kshot_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py](../evidence/ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py.md)
- [ev_scripts_rebuttal_make_word_holdout_split_py](../evidence/ev_scripts_rebuttal_make_word_holdout_split_py.md)
- [ev_uc20260226_split_npz_manifest_to4_csv](../evidence/ev_uc20260226_split_npz_manifest_to4_csv.md)
