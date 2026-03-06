# Taxonomy rubric: EPGSpeller positioning analysis (2026-02-18)

This rubric defines a **multi-lens taxonomy** for positioning EPGSpeller within an **EPG-centered SSI** related-work space. The analyzed prior-work set is **frozen** to the 20 items under:

- `results/related_work_survey_epgspeller_2026-02-17/results/*.json`

Category assignments are **explicit** (no heuristic inference) and stored in:

- `results/positioning_analysis_epgspeller_2026-02-18/taxonomy_rules.json`

If a label cannot be assigned without guessing beyond the extracted survey JSON fields, the rule entry must include an `uncertain` note.

---

## Lens V1: Task / output unit

### `task_class`
One of:
- `silent_spelling_text_entry`: silent spelling / text entry systems (character-level or spelling-to-word).
- `silent_speech_recognition_closed_vocab`: silent speech recognition in a closed-vocabulary / isolated-word setting.
- `speech_reconstruction_generation`: articulatory-to-speech reconstruction, generation, enhancement.
- `mapping_prediction`: mapping/prediction tasks (e.g., acoustic→EPG) that are not text decoding.
- `instrumentation_visualization`: instrumentation, visualization, analysis, and representation studies not framed as decoding systems.
- `survey_method`: surveys/books and general methods (e.g., CTC, SpecAugment) used for context.

### `output_unit_class`
One of:
- `characters`, `words`, `phonemes_or_labels`, `acoustics_waveform`, `epg_patterns`, `n_a`.

`n_a` is used when the item is not a decoding benchmark (survey/method/instrumentation/analysis) or the output unit does not match the above classes.

---

## Lens V2: Decoding constraint

### `vocab_constraint`
One of:
- `open_vocab`: explicitly open-vocabulary / unseen-word generalization via compositional character decoding.
- `lexicon_or_dictionary_constrained`: lexicon/dictionary constraints are central to decoding.
- `closed_vocab`: explicitly closed vocabulary / isolated words.
- `n_a`: not applicable (survey/method/instrumentation/mapping) or unclear from extracted fields.

### `decoding_form`
One of:
- `ctc_like`: CTC-based sequence decoding / alignment-free labeling.
- `dtw_template`: DTW/template matching.
- `hmm_pipeline`: HMM/segmental pipelines with explicit lexicons/dictionaries.
- `not_a_decoder`: not a sequence decoder paper (survey/method/instrumentation/mapping).

---

## Lens V3: Spatial inductive bias (core)

### `spatial_representation`
One of:
- `vector_no_layout`: multi-channel vector/time-series without explicitly using electrode/layout geometry.
- `linear_compression`: explicit linear/statistical compression of high-D vectors (e.g., PCA / latent-variable reduction).
- `explicit_2d_image`: explicit 2D reconstruction/image-like representation processed with image encoders.
- `geometry_aware_nonimage`: geometry/layout is used, but not as a full 2D conv image (e.g., visualization/geometry measures, structured pooling).
- `not_applicable`: not meaningfully a spatial representation (surveys, general method papers).

### `layout_assumption`
One of:
- `explicit_layout_used`: the work depends on explicit spatial layout/geometry.
- `implicit_or_none`: layout not explicitly used/assumed (treated as unordered channels).
- `not_applicable`: surveys/general methods.

---

## Lens V4: Robustness / augmentation

### `augmentation_class`
One of:
- `none`
- `specaug_like`
- `spatial_aug_like`
- `other`
- `varies` (surveys/reviews)

### `robustness_eval`
One of:
- `none_reported`
- `qualitative_only`
- `quantitative_sensor_failure_or_noise`

---

## Lens V5: Sensor design / electrode selection

### `sensor_design_focus`
One of:
- `layout_device_design`: electrode/layout/device design is a primary focus.
- `electrode_selection_importance`: electrode selection/importance or K-budget curves are a primary focus.
- `representation_reduction`: reduction/compression of EPG representations is a primary focus.
- `none`

---

## Lens V6: Protocol / generalization

### `protocol_class`
One of:
- `within_subject`
- `multi_subject`
- `cross_subject`
- `mixed_or_review`
- `n_a` (not applicable or unclear from extracted fields)
