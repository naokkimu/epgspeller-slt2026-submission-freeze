# Search Log - related_work_survey_epgspeller_2026-06-27_v2

Date: 2026-06-27
Topic: Related work and positioning update for EPGSpeller: auditable lexicon-free EPG silent spelling benchmarks, protocol-specific generalization, and transfer-aware SSI evaluation

## Baseline

- Reused the frozen 2026-02-17 EPG-centered survey as the seed set: 20 JSON files from `results/related_work_survey_epgspeller_2026-02-17/results/*.json`.
- Enriched the copied v2 JSON files with protocol/audit/transfer fields required by the v2 `fields.yaml`.
- The original 2026-02-17 search log noted a remaining gap around EPG/EPG-adjacent recognition beyond SilentSpeller; v2 adds Stone & Birkholz 2020 electro-optical stomatography as a gap-closure item.

## Web/metadata supplement actually performed

Queries focused on:
- EPG/electropalatography/deep-learning/palatogram/electrode-reduction gaps.
- Silent spelling/text-entry/open-vocabulary SSI.
- Cross-participant, heterogeneous-electrode, low-resource, cross-modal, and benchmark/generalization framing.
- LLM-assisted silent speech recognition and text entry.

Metadata services used:
- Crossref API title search and DOI records.
- OpenAlex DOI records.
- arXiv API for arXiv:2403.05583 and arXiv:2603.11877.
- DOI URLs for ACM, ISCA, IEEE, Nature Sensors, and ICASSP/TASLP entries.

## Added v2 items

- `su2025_wordinitials_conditioned_llm_text_entry`: LLM-conditioned silent-speech text entry; included to separate sensor decoding from LM-assisted text entry.
- `hiraki2025_silentwhisper`: faint-whisper silent interaction; included as a near-silent acoustic modality contrast.
- `chugh2026_morsear`: low-resource/generalizable earable covert messaging; included for wearable low-resource/generalization framing.
- `wang2024_watch_your_mouth_depth_sensing`: depth-sensing silent speech recognition; included as spatial articulatory-sensing context.
- `tang2026_sensing_technologies_ssi`: current SSI sensing review; included to update broad taxonomy beyond 2010/2017/2020 surveys.
- `benster2024_mona_llm_enhanced_ssr`: cross-modal LLM-enhanced silent speech recognition; included for cross-modal and LLM-assisted decoding framing.
- `xu2026_llm_era_ssi_review`: LLM-era SSI systematic review preprint; included as contemporary taxonomy/future-work context.
- `inoue2025_eeg_emg_heterogeneous_electrodes`: heterogeneous EEG/EMG electrode silent speech decoding; included for sensor-layout mismatch framing.
- `guo2026_cross_modal_meta_generalization_uti`: ultrasound cross-modal meta-generalization; included for transfer/generalization framing.
- `stone2020_electro_optical_stomatography_cross_speaker`: EPG-adjacent cross-speaker command-word recognition; included to close the frozen survey's recognition-focused gap.

## Interpretation policy

- Added LLM/LM-assisted items are not numeric baselines for EPGSpeller greedy CER.
- Added non-EPG SSI systems are used for positioning only unless their protocols match EPGSpeller's P1/P2/P3/P3MS definitions.
- Preprint items are explicitly marked in `venue` and `source_quality_notes`.
