# Related Work and Positioning Update for EPGSpeller v2

**Topic:** Related work and positioning update for EPGSpeller: auditable lexicon-free EPG silent spelling benchmarks, protocol-specific generalization, and transfer-aware SSI evaluation

## Summary

- Total items: 30
- Seeded from frozen 2026-02-17 survey: 20
- Added or gap-closure items in 2026-06-27 v2: 10
- This report distinguishes prior frozen EPG-centered coverage from v2 additions and does not treat non-EPG or LM-assisted systems as direct numeric baselines for EPGSpeller.

## Gap / Relevance to Current EPGSpeller Manuscript

The v2 update supports the current manuscript by sharpening three boundaries: protocol-specific generalization, sensor/modality-specific comparison, and decoder-assistance separation. The added LLM-conditioned and LLM-era items motivate keeping greedy CER, lexicon projection, and LM/LLM-assisted text entry as separate evaluation regimes. The added transfer and heterogeneous-sensor items support the manuscript emphasis that cross-participant and hardware/layout mismatch are first-class protocol issues. The electro-optical stomatography item closes a prior gap around EPG-adjacent cross-speaker recognition, while also reinforcing that command-word recognition is not directly comparable with lexicon-free silent spelling.

## Table of Contents

1. [A Cross-Modal Approach to Silent Speech with LLM-Enhanced Recognition](#benster2024-mona-llm-enhanced-ssr) - 2024 | added_in_v2_2026-06-27_web_supplement
2. [Watch Your Mouth: Silent Speech Recognition with Depth Sensing](#wang2024-watch-your-mouth-depth-sensing) - 2024 | added_in_v2_2026-06-27_web_supplement
3. [SilentWhisper: inaudible faint whisper speech input for silent speech interaction](#hiraki2025-silentwhisper) - 2025 | added_in_v2_2026-06-27_web_supplement
4. [A Silent Speech Decoding System from EEG and EMG with Heterogenous Electrode Configurations](#inoue2025-eeg-emg-heterogeneous-electrodes) - 2025 | added_in_v2_2026-06-27_web_supplement
5. [Multimodal Silent Speech-based Text Entry with Word-initials Conditioned LLM](#su2025-wordinitials-conditioned-llm-text-entry) - 2025 | added_in_v2_2026-06-27_web_supplement
6. [MorsEar: Toward Generalizable Low-Resource Covert Messaging via Earable based Inertial Sensing](#chugh2026-morsear) - 2026 | added_in_v2_2026-06-27_web_supplement
7. [Cross-Modal Meta-Generalization for Silent Speech Recognition via Ultrasound Tongue Images](#guo2026-cross-modal-meta-generalization-uti) - 2026 | added_in_v2_2026-06-27_web_supplement
8. [Sensing technologies for silent speech interfaces](#tang2026-sensing-technologies-ssi) - 2026 | added_in_v2_2026-06-27_web_supplement
9. [Silent Speech Interfaces in the Era of Large Language Models: A Comprehensive Taxonomy and Systematic Review](#xu2026-llm-era-ssi-review) - 2026 | added_in_v2_2026-06-27_web_supplement
10. [Cross-Speaker Silent-Speech Command Word Recognition Using Electro-Optical Stomatography](#stone2020-electro-optical-stomatography-cross-speaker) - 2020 | added_in_v2_2026-06-27_web_supplement_gap_closure
11. [New developments in electropalatography: A state-of-the-art report](#hardcastle1989-state-of-art-epg) - 1989 | seeded_from_frozen_related_work_survey_2026-02-17
12. [Electropalatography in phonetic research and in speech training](#hardcastle1990-epg-phonetic-research) - 1990 | seeded_from_frozen_related_work_survey_2026-02-17
13. [EPG data reduction methods and their implications for studies of lingual coarticulation](#hardcastle1991-epg-data-reduction-coarticulation) - 1991 | seeded_from_frozen_related_work_survey_2026-02-17
14. [Depth measurement of face and palate by structured light](#shadle1993-epg-structured-light) - 1993 | seeded_from_frozen_related_work_survey_2026-02-17
15. [Dimensionality reduction of electropalatographic data using latent variable models](#carreira-perpinan1998-dimred-epg) - 1998 | seeded_from_frozen_related_work_survey_2026-02-17
16. [Connectionist Temporal Classification: Labelling Unsegmented Sequence Data with Recurrent Neural Networks](#graves2006-ctc) - 2006 | seeded_from_frozen_related_work_survey_2026-02-17
17. [On the Acoustic-to-Electropalatographic Mapping](#toutios2006-acoustic-to-epg-mapping) - 2006 | seeded_from_frozen_related_work_survey_2026-02-17
18. [Learning Electropalatograms from Acoustics](#toutios2006-learning-epg-from-acoustics) - 2006 | seeded_from_frozen_related_work_survey_2026-02-17
19. [Silent speech interfaces](#denby2010-silent-speech-interfaces) - 2010 | seeded_from_frozen_related_work_survey_2026-02-17
20. [Isolated word recognition of silent speech using magnetic implants and sensors](#gilbert2010-magnetic-implants-silent-speech) - 2010 | seeded_from_frozen_related_work_survey_2026-02-17
21. [Development of a silent speech interface driven by ultrasound and optical images of the tongue and lips](#hueber2010-ultrasound-optical-ssi) - 2010 | seeded_from_frozen_related_work_survey_2026-02-17
22. [An Introduction to Silent Speech Interfaces](#ssi-book-springer2017) - 2016 | seeded_from_frozen_related_work_survey_2026-02-17
23. [SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition](#park2019-specaugment) - 2019 | seeded_from_frozen_related_work_survey_2026-02-17
24. [Visualisation and Analysis of Speech Production with Electropalatography](#verhoeven2019-visualisation-analysis-epg) - 2019 | seeded_from_frozen_related_work_survey_2026-02-17
25. [Silent Speech Interfaces for Speech Restoration: A Review](#gonzalezlopez2020-ssi-restoration-review) - 2020 | seeded_from_frozen_related_work_survey_2026-02-17
26. [Biosignal Sensors and Deep Learning-Based Speech Recognition: A Review](#lee2021-biosignal-speechrec-review) - 2021 | seeded_from_frozen_related_work_survey_2026-02-17
27. [Design and Evaluation of Korean Electropalatography (K-EPG)](#woo2021-kepg-design) - 2021 | seeded_from_frozen_related_work_survey_2026-02-17
28. [EPG2S: Speech Generation and Speech Enhancement based on Electropalatography and Audio Signals using Multimodal Learning](#chen2022-epg2s) - 2022 | seeded_from_frozen_related_work_survey_2026-02-17
29. [SilentSpeller: Towards mobile, hands-free, silent speech text entry using electropalatography](#silentspeller-chi2022) - 2022 | seeded_from_frozen_related_work_survey_2026-02-17
30. [ReHEarSSE: Recognizing Hidden-in-the-Ear Silently Spelled Expressions](#rehearsse-chi2024) - 2024 | seeded_from_frozen_related_work_survey_2026-02-17

## Added v2 Items

- **A Cross-Modal Approach to Silent Speech with LLM-Enhanced Recognition** (2024): Supports adding language about future LM-assisted decoding while keeping current claims limited to audited lexicon-free/lexicon-projected protocols.
- **Watch Your Mouth: Silent Speech Recognition with Depth Sensing** (2024): Helps position row/column/grid EPG front ends against other spatial SSI modalities while keeping claims EPG-specific.
- **SilentWhisper: inaudible faint whisper speech input for silent speech interaction** (2025): Helps limit deployment/privacy claims to the audited EPG setup and avoid overgeneralizing from other silent-interaction modalities.
- **A Silent Speech Decoding System from EEG and EMG with Heterogenous Electrode Configurations** (2025): Useful for motivating EPGSpeller’s electrode reduction and layout-aware analyses without claiming cross-modality performance equivalence.
- **Multimodal Silent Speech-based Text Entry with Word-initials Conditioned LLM** (2025): Directly supports the current manuscript’s constraint separation: open-character decoding, lexicon projection, and LM/LLM assistance should not be collapsed into one leaderboard.
- **MorsEar: Toward Generalizable Low-Resource Covert Messaging via Earable based Inertial Sensing** (2026): Useful background for low-shot and cross-participant framing, without serving as a direct CER comparison.
- **Cross-Modal Meta-Generalization for Silent Speech Recognition via Ultrasound Tongue Images** (2026): Helps position P3/P3MS results as part of a broader transfer-generalization problem while keeping the evidence EPG-specific.
- **Sensing technologies for silent speech interfaces** (2026): Strengthens the Introduction/Related Work with current survey context while preserving EPGSpeller’s narrow evidence claims.
- **Silent Speech Interfaces in the Era of Large Language Models: A Comprehensive Taxonomy and Systematic Review** (2026): Supports a short future-work/positioning note: EPGSpeller could later add LM-assisted decoding, but current claims remain lexicon-free and audit-bound.
- **Cross-Speaker Silent-Speech Command Word Recognition Using Electro-Optical Stomatography** (2020): Addresses the 2026-02-17 search-log gap for EPG/EPG-adjacent recognition and helps sharpen the distinction between command-word cross-speaker recognition and lexicon-free spelling.

## Detailed Items

<a id="benster2024-mona-llm-enhanced-ssr"></a>
### A Cross-Modal Approach to Silent Speech with LLM-Enhanced Recognition

#### Basic Info

- **paper_id**: benster2024_mona_llm_enhanced_ssr
- **title**: A Cross-Modal Approach to Silent Speech with LLM-Enhanced Recognition
- **authors**: - Tyler Benster<br>- Guy Wilson<br>- Reshef Elisha<br>- Francis R. Willett<br>- Shaul Druckmann
- **year**: 2024
- **venue**: arXiv preprint arXiv:2403.05583
- **doi**: arXiv:2403.05583
- **primary_url**: https://arxiv.org/abs/2403.05583
- **pdf_url**: https://arxiv.org/pdf/2403.05583
- **code_or_data_release**: N/A
- **citation_key_suggestion**: benster2024mona
- **coverage_origin**: added_in_v2_2026-06-27_web_supplement

#### Task & Data

- **modality**: Multimodal Orofacial Neural Audio (MONA); cross-modal silent speech recognition using noninvasive orofacial signals and audio-only data alignment.
- **device**: MONA setup described in the arXiv paper.
- **task**: Silent speech recognition with cross-modal training and LLM-enhanced recognition.
- **output_unit**: Text/speech recognition output as defined by the paper.
- **vocabulary_setting**: LLM-enhanced recognition; not pure lexicon-free character decoding.
- **datasets**: Paper uses silent-speech data and audio-only resources such as LibriSpeech according to the arXiv abstract.

#### Protocol & Evaluation

- **evaluation_protocol**: Paper-specific cross-modal silent speech evaluation.
- **protocol_generalization**: Important for cross-modal transfer framing: audio-only data can support silent recognition, but protocol constraints differ from EPGSpeller.
- **participant_generalization**: Participant generalization should be read from the paper; v2 uses this for cross-modal and LLM-assisted framing.
- **metrics_reported**: Recognition metrics reported by the arXiv paper.
- **benchmark_or_audit_status**: Preprint; no v2-confirmed deterministic public split stack comparable to EPGSpeller.
- **leakage_or_constraint_notes**: LLM scoring adjustment changes the decoding regime; compare separately from sensor-only greedy decoding.

#### Methods

- **decoder**: Cross-modal model with LLM Integrated Scoring Adjustment according to the arXiv abstract.
- **model_architecture**: Shared latent multimodal model with cross-modal training losses described by the authors.
- **spatial_frontend**: Orofacial signal representation, not EPG palatogram layout.
- **augmentation**: Cross-modal use of audio-only resources rather than simple sensor augmentation.
- **language_model_or_postprocessing**: Central: LLM Integrated Scoring Adjustment is part of the reported approach.
- **transfer_or_adaptation_method**: Cross-modal alignment from audio-only resources to silent speech recognition.

#### Auditability

- **source_quality_notes**: arXiv primary record plus arXiv API/PDF sources; preprint status should be stated.
- **reproducibility_artifacts**: No v2-confirmed code/data release.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Introduces MONA, a cross-modal silent speech approach using audio-only data to help silent recognition.; Adds LLM-enhanced scoring to silent speech recognition.; Useful for contemporary transfer and language-model framing.
- **limitations**: Preprint status in v2 evidence.; LLM-assisted results should not be merged with lexicon-free sensor-only metrics.; Non-EPG modality.
- **reported_results_summary**: See arXiv:2403.05583; v2 uses the item for cross-modal/LLM framing.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Shows why EPGSpeller should explicitly separate sensor-only benchmark claims from LM/LLM-assisted decoding variants.
- **takeaways_for_related_work_section**: LLM-enhanced SSI is emerging, but language-model assistance creates a different evaluation layer from EPGSpeller greedy CER.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Supports adding language about future LM-assisted decoding while keeping current claims limited to audited lexicon-free/lexicon-projected protocols.

#### Sources

- arXiv: A Cross-Modal Approach to Silent Speech with LLM-Enhanced Recognition (academic, retrieved 2026-06-27). https://arxiv.org/abs/2403.05583
- PDF: A Cross-Modal Approach to Silent Speech with LLM-Enhanced Recognition (academic, retrieved 2026-06-27). https://arxiv.org/pdf/2403.05583
- arXiv API: 2403.05583 (web, retrieved 2026-06-27). http://export.arxiv.org/api/query?id_list=2403.05583

<a id="wang2024-watch-your-mouth-depth-sensing"></a>
### Watch Your Mouth: Silent Speech Recognition with Depth Sensing

#### Basic Info

- **paper_id**: wang2024_watch_your_mouth_depth_sensing
- **title**: Watch Your Mouth: Silent Speech Recognition with Depth Sensing
- **authors**: Xue Wang; Zixiong Su; Jun Rekimoto; Yang Zhang
- **year**: 2024
- **venue**: Proceedings of the CHI Conference on Human Factors in Computing Systems
- **doi**: 10.1145/3613904.3642092
- **primary_url**: https://doi.org/10.1145/3613904.3642092
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: wang2024watchyourmouth
- **coverage_origin**: added_in_v2_2026-06-27_web_supplement

#### Task & Data

- **modality**: Depth sensing of mouth/orofacial movement for silent speech recognition.
- **device**: Depth sensing setup described in the CHI 2024 paper.
- **task**: Silent speech recognition using mouth depth signals.
- **output_unit**: Speech/text units defined by the paper-specific recognition task.
- **vocabulary_setting**: Paper-specific recognition setting; likely constrained relative to open-character EPG spelling.
- **datasets**: Paper-specific depth-sensing silent speech dataset.

#### Protocol & Evaluation

- **evaluation_protocol**: Paper-specific participant/task evaluation.
- **protocol_generalization**: Contemporary non-EPG articulatory-sensing benchmark context; not directly comparable without matched vocabulary and splits.
- **participant_generalization**: Cross-user status should be read from the source; v2 keeps it as modality/protocol context.
- **metrics_reported**: Recognition metrics reported by the CHI 2024 paper.
- **benchmark_or_audit_status**: Publisher-indexed paper; no v2-confirmed shared deterministic split/audit registry comparable to EPGSpeller.
- **leakage_or_constraint_notes**: Depth-sensing recognition constraints and vocabulary support differ from lexicon-free EPG character decoding.

#### Methods

- **decoder**: Paper-specific depth-signal recognition pipeline.
- **model_architecture**: Paper-specific depth-sensing model.
- **spatial_frontend**: Depth image/spatial mouth representation, not EPG palatogram layout.
- **augmentation**: See paper.
- **language_model_or_postprocessing**: Paper-specific; not the main v2 relevance.
- **transfer_or_adaptation_method**: Not the main v2 relevance unless source reports cross-user adaptation.

#### Auditability

- **source_quality_notes**: Confirmed through DOI/Crossref/OpenAlex metadata.
- **reproducibility_artifacts**: No v2-confirmed code/data release.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Shows depth sensing as a contemporary articulatory SSI modality.; Provides a non-EPG spatial sensing contrast for silent speech recognition.; Useful for protocol-aware positioning of EPG spatial front ends.
- **limitations**: Different sensor physics and privacy profile from intra-oral EPG.; Numeric comparison to EPGSpeller would require matched tasks and splits.
- **reported_results_summary**: See CHI 2024 paper; v2 uses it for modality and spatial-sensing positioning.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Supports discussion that spatial representations are modality-specific; depth images and EPG palatograms should not be conflated.
- **takeaways_for_related_work_section**: Recent SSI systems use spatial or image-like articulatory cues, but protocol comparability remains the central issue.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Helps position row/column/grid EPG front ends against other spatial SSI modalities while keeping claims EPG-specific.

#### Sources

- DOI: Watch Your Mouth (academic, retrieved 2026-06-27). https://doi.org/10.1145/3613904.3642092 DOI: 10.1145/3613904.3642092
- Crossref API: 10.1145/3613904.3642092 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1145/3613904.3642092 DOI: 10.1145/3613904.3642092
- OpenAlex: Watch Your Mouth (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.1145/3613904.3642092 DOI: 10.1145/3613904.3642092

<a id="hiraki2025-silentwhisper"></a>
### SilentWhisper: inaudible faint whisper speech input for silent speech interaction

#### Basic Info

- **paper_id**: hiraki2025_silentwhisper
- **title**: SilentWhisper: inaudible faint whisper speech input for silent speech interaction
- **authors**: Hirotaka Hiraki; Jun Rekimoto
- **year**: 2025
- **venue**: Proceedings of the Extended Abstracts of the CHI Conference on Human Factors in Computing Systems
- **doi**: 10.1145/3706599.3721185
- **primary_url**: https://doi.org/10.1145/3706599.3721185
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: hiraki2025silentwhisper
- **coverage_origin**: added_in_v2_2026-06-27_web_supplement

#### Task & Data

- **modality**: Inaudible or ultra-low-volume whispered acoustic input for silent speech interaction.
- **device**: Wearable or near-mouth acoustic capture setup described by the CHI Extended Abstracts paper.
- **task**: Silent speech interaction using faint whisper input.
- **output_unit**: Speech/text units as defined by the paper-specific recognition task.
- **vocabulary_setting**: Whisper-based recognition setting; not EPG lexicon-free silent spelling.
- **datasets**: Paper-specific faint-whisper interaction dataset.

#### Protocol & Evaluation

- **evaluation_protocol**: Paper-specific prototype/evaluation protocol.
- **protocol_generalization**: Contextual SSI modality comparison; protocol differs from EPG word/instance/cross-participant split families.
- **participant_generalization**: User-independent or cross-user status must be read from the paper; v2 does not infer it.
- **metrics_reported**: Recognition/interaction metrics reported by the CHI Extended Abstracts paper.
- **benchmark_or_audit_status**: Publisher-indexed paper; no v2-confirmed deterministic split benchmark comparable to EPGSpeller.
- **leakage_or_constraint_notes**: Do not compare faint-whisper acoustic recognition directly with contact-sensor lexicon-free EPG decoding.

#### Methods

- **decoder**: Paper-specific recognition pipeline for faint whispered speech.
- **model_architecture**: Paper-specific acoustic/interaction model.
- **spatial_frontend**: Not applicable to EPG palate layout.
- **augmentation**: Not emphasized in v2 extraction; see paper.
- **language_model_or_postprocessing**: Paper-specific; not the main v2 relevance.
- **transfer_or_adaptation_method**: Not the main v2 relevance; included as a modality contrast.

#### Auditability

- **source_quality_notes**: Confirmed through DOI/Crossref/OpenAlex metadata.
- **reproducibility_artifacts**: No v2-confirmed code/data release.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Adds a contemporary faint-whisper SSI modality for silent interaction.; Shows that acoustic-near-silent methods occupy a different point in the SSI design space than EPG.; Useful for privacy and interaction framing.
- **limitations**: Faint whisper input may still rely on residual acoustic production unlike fully non-acoustic SSI.; Not directly comparable to EPGSpeller protocol families.
- **reported_results_summary**: See CHI EA 2025 paper; v2 uses this for modality positioning.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Supports careful wording around silent speech: EPGSpeller is non-acoustic palate-contact decoding rather than faint-whisper recognition.
- **takeaways_for_related_work_section**: Recent SSI interaction work spans non-acoustic sensing and near-silent acoustics; comparisons must separate modality, privacy, and protocol assumptions.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Helps limit deployment/privacy claims to the audited EPG setup and avoid overgeneralizing from other silent-interaction modalities.

#### Sources

- DOI: SilentWhisper: inaudible faint whisper speech input for silent speech interaction (academic, retrieved 2026-06-27). https://doi.org/10.1145/3706599.3721185 DOI: 10.1145/3706599.3721185
- Crossref API: 10.1145/3706599.3721185 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1145/3706599.3721185 DOI: 10.1145/3706599.3721185
- OpenAlex: SilentWhisper (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.1145/3706599.3721185 DOI: 10.1145/3706599.3721185

<a id="inoue2025-eeg-emg-heterogeneous-electrodes"></a>
### A Silent Speech Decoding System from EEG and EMG with Heterogenous Electrode Configurations

#### Basic Info

- **paper_id**: inoue2025_eeg_emg_heterogeneous_electrodes
- **title**: A Silent Speech Decoding System from EEG and EMG with Heterogenous Electrode Configurations
- **authors**: - Masakazu Inoue<br>- Motoshige Sato<br>- Kenichi Tomeoka<br>- Nathania Nah<br>- Eri Hatakeyama<br>- Kai Arulkumaran<br>- Ilya Horiguchi<br>- Shuntaro Sasai
- **year**: 2025
- **venue**: Interspeech 2025
- **doi**: 10.21437/interspeech.2025-1183
- **primary_url**: https://doi.org/10.21437/interspeech.2025-1183
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: inoue2025heterogeneouseegemg
- **coverage_origin**: added_in_v2_2026-06-27_web_supplement

#### Task & Data

- **modality**: EEG and EMG biosignals for silent speech decoding.
- **device**: Heterogeneous EEG/EMG electrode configurations described in the Interspeech paper.
- **task**: Silent speech decoding from EEG and EMG.
- **output_unit**: Speech/text units as defined by the paper.
- **vocabulary_setting**: Paper-specific; not EPG open-character spelling.
- **datasets**: Paper-specific EEG/EMG silent speech data.

#### Protocol & Evaluation

- **evaluation_protocol**: Paper-specific heterogeneous-electrode evaluation.
- **protocol_generalization**: Relevant to sensor-layout mismatch and heterogeneous hardware, a close conceptual analogue to EPG electrode-layout transfer issues.
- **participant_generalization**: Generalization status should be read from the paper; v2 uses it for heterogeneous sensor configuration framing.
- **metrics_reported**: Silent speech decoding metrics reported by Interspeech 2025 paper.
- **benchmark_or_audit_status**: Peer-reviewed conference paper; no v2-confirmed shared split/audit stack comparable to EPGSpeller.
- **leakage_or_constraint_notes**: Decoder constraints and vocabulary support differ from EPGSpeller; use for sensor heterogeneity framing.

#### Methods

- **decoder**: Paper-specific EEG/EMG silent speech decoder.
- **model_architecture**: Paper-specific biosignal model.
- **spatial_frontend**: Electrode-configuration-aware biosignal input, not EPG palate layout.
- **augmentation**: See paper.
- **language_model_or_postprocessing**: Paper-specific; not main v2 relevance.
- **transfer_or_adaptation_method**: Heterogeneous electrode configurations are central to the framing.

#### Auditability

- **source_quality_notes**: Confirmed through DOI/Crossref/OpenAlex metadata.
- **reproducibility_artifacts**: No v2-confirmed code/data release.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Addresses silent speech decoding under heterogeneous electrode configurations.; Offers contemporary biosignal evidence for hardware-layout mismatch challenges.; Useful analogy for EPG electrode selection and transfer constraints.
- **limitations**: Non-EPG modality.; Metric and protocol differences prevent direct comparison to EPGSpeller.
- **reported_results_summary**: See Interspeech 2025 paper; v2 uses it for heterogeneous-electrode positioning.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Supports the claim that sensor/electrode configuration is a meaningful evaluation variable, not just an implementation detail.
- **takeaways_for_related_work_section**: Recent SSI decoding work treats electrode configuration as a first-class issue; EPGSpeller’s electrode-budget and protocol audits fit this broader trend.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Useful for motivating EPGSpeller’s electrode reduction and layout-aware analyses without claiming cross-modality performance equivalence.

#### Sources

- DOI: A Silent Speech Decoding System from EEG and EMG with Heterogenous Electrode Configurations (academic, retrieved 2026-06-27). https://doi.org/10.21437/interspeech.2025-1183 DOI: 10.21437/interspeech.2025-1183
- Crossref API: 10.21437/interspeech.2025-1183 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.21437/interspeech.2025-1183 DOI: 10.21437/interspeech.2025-1183
- OpenAlex: A Silent Speech Decoding System from EEG and EMG (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.21437/interspeech.2025-1183 DOI: 10.21437/interspeech.2025-1183

<a id="su2025-wordinitials-conditioned-llm-text-entry"></a>
### Multimodal Silent Speech-based Text Entry with Word-initials Conditioned LLM

#### Basic Info

- **paper_id**: su2025_wordinitials_conditioned_llm_text_entry
- **title**: Multimodal Silent Speech-based Text Entry with Word-initials Conditioned LLM
- **authors**: Zixiong Su; Shitao Fang; Jun Rekimoto
- **year**: 2025
- **venue**: Proceedings of the 7th ACM Conference on Conversational User Interfaces
- **doi**: 10.1145/3719160.3736612
- **primary_url**: https://doi.org/10.1145/3719160.3736612
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: su2025wordinitialsllm
- **coverage_origin**: added_in_v2_2026-06-27_web_supplement

#### Task & Data

- **modality**: Multimodal silent-speech text entry; exact sensing channels are paper-specific and non-EPG unless otherwise stated by the source.
- **device**: Multimodal SSI input setup described in the ACM CUI 2025 paper.
- **task**: Silent speech-based text entry with word-initial cues and LLM-conditioned prediction.
- **output_unit**: Text/words produced from silent input cues with word-initial conditioning.
- **vocabulary_setting**: LLM-assisted text-entry setting; output support is shaped by word prediction and language-model conditioning rather than pure unconstrained greedy character decoding.
- **datasets**: Paper-specific text-entry/SSI dataset; use source paper for participant and session details.

#### Protocol & Evaluation

- **evaluation_protocol**: Paper-specific multimodal text-entry evaluation; not directly CER-leaderboard comparable to EPGSpeller without matched splits and metrics.
- **protocol_generalization**: Important contrast case because language-model conditioning changes the protocol from pure sensor decoding toward assisted text entry.
- **participant_generalization**: Participant/user generalization must be read from the source; v2 treats it as contextual unless cross-user evidence is explicit.
- **metrics_reported**: Text-entry and recognition metrics reported by the CUI paper.
- **benchmark_or_audit_status**: Publisher-indexed paper; no v2-confirmed shared benchmark stack comparable to EPGSpeller split manifests.
- **leakage_or_constraint_notes**: LLM conditioning and word-initial cues should be separated from lexicon-free sensor decoding claims; do not compare directly against EPGSpeller greedy CER.

#### Methods

- **decoder**: LLM-conditioned text prediction/postprocessing around silent-speech cues.
- **model_architecture**: Paper-specific multimodal text-entry system with an LLM-conditioned component.
- **spatial_frontend**: Not EPG-specific; no palate-contact spatial frontend in the v2 evidence summary.
- **augmentation**: Not emphasized in v2 extraction; see paper.
- **language_model_or_postprocessing**: Central: word-initials conditioned LLM is part of the text-entry mechanism.
- **transfer_or_adaptation_method**: Not the primary v2 relevance; item is included for LM-assisted SSI positioning.

#### Auditability

- **source_quality_notes**: Confirmed through DOI/Crossref/OpenAlex publisher metadata.
- **reproducibility_artifacts**: No v2-confirmed code/data release.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Introduces or evaluates LLM-conditioned word-initial assisted silent-speech text entry.; Provides a contemporary example where silent input is combined with language-model priors.; Useful for separating sensor decoding from text-entry assistance in related work.
- **limitations**: LLM assistance can obscure sensor-decoding quality if compared directly with lexicon-free CER.; Protocol and vocabulary constraints are paper-specific.
- **reported_results_summary**: See the ACM CUI 2025 paper; v2 uses the item for framing, not numeric normalization.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Helps EPGSpeller justify reporting greedy CER and lexicon projection separately from LM/LLM-assisted text entry.
- **takeaways_for_related_work_section**: Recent SSI text-entry work increasingly uses language-model assistance, so EPGSpeller should explicitly frame lexicon-free and lexicon/LM-assisted results as different evaluation regimes.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Directly supports the current manuscript’s constraint separation: open-character decoding, lexicon projection, and LM/LLM assistance should not be collapsed into one leaderboard.

#### Sources

- DOI: Multimodal Silent Speech-based Text Entry with Word-initials Conditioned LLM (academic, retrieved 2026-06-27). https://doi.org/10.1145/3719160.3736612 DOI: 10.1145/3719160.3736612
- Crossref API: 10.1145/3719160.3736612 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1145/3719160.3736612 DOI: 10.1145/3719160.3736612
- OpenAlex: Multimodal Silent Speech-based Text Entry with Word-initials Conditioned LLM (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.1145/3719160.3736612 DOI: 10.1145/3719160.3736612

<a id="chugh2026-morsear"></a>
### MorsEar: Toward Generalizable Low-Resource Covert Messaging via Earable based Inertial Sensing

#### Basic Info

- **paper_id**: chugh2026_morsear
- **title**: MorsEar: Toward Generalizable Low-Resource Covert Messaging via Earable based Inertial Sensing
- **authors**: - Garvit Chugh<br>- Indrajeet Ghosh<br>- Nirmalya Roy<br>- Sandip Chakraborty<br>- Suchetana Chakraborty
- **year**: 2026
- **venue**: Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems
- **doi**: 10.1145/3772318.3791436
- **primary_url**: https://doi.org/10.1145/3772318.3791436
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: chugh2026morsear
- **coverage_origin**: added_in_v2_2026-06-27_web_supplement

#### Task & Data

- **modality**: Earable inertial sensing for covert/silent messaging.
- **device**: Earable inertial sensor platform described in the CHI 2026 paper.
- **task**: Low-resource covert messaging / silent communication.
- **output_unit**: Messaging units defined by the MorsEar task.
- **vocabulary_setting**: Low-resource covert messaging; not direct EPG open-character spelling.
- **datasets**: Paper-specific earable dataset.

#### Protocol & Evaluation

- **evaluation_protocol**: Paper-specific generalization and low-resource evaluation.
- **protocol_generalization**: Relevant because the title and metadata emphasize generalizable low-resource behavior; protocol is still modality-specific.
- **participant_generalization**: Included for generalization framing; exact participant split definitions should be read from the paper.
- **metrics_reported**: Messaging/recognition metrics reported by the CHI 2026 paper.
- **benchmark_or_audit_status**: Publisher-indexed paper; no v2-confirmed shared benchmark stack comparable to EPGSpeller.
- **leakage_or_constraint_notes**: Task constraints differ from lexicon-free character spelling; compare only at the level of low-resource/generalization framing.

#### Methods

- **decoder**: Paper-specific classifier/decoder for earable inertial covert messaging.
- **model_architecture**: Paper-specific low-resource earable model.
- **spatial_frontend**: Not applicable to EPG palate layout.
- **augmentation**: See paper.
- **language_model_or_postprocessing**: Not the main v2 relevance.
- **transfer_or_adaptation_method**: Low-resource and generalizable modeling are central to the paper framing.

#### Auditability

- **source_quality_notes**: Confirmed through DOI/Crossref/OpenAlex metadata.
- **reproducibility_artifacts**: No v2-confirmed code/data release.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Adds a contemporary earable covert messaging SSI-like system.; Emphasizes low-resource/generalizable behavior in wearable sensing.; Provides a contrast point for EPGSpeller low-shot/cross-participant discussion.
- **limitations**: Different task and sensor modality from EPGSpeller.; Protocol-level details must be kept separate from EPG split families.
- **reported_results_summary**: See CHI 2026 paper; v2 uses this for generalization/low-resource framing.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Supports the current manuscript emphasis that generalization claims should be protocol-specific and target-specific.
- **takeaways_for_related_work_section**: Wearable SSI work increasingly foregrounds low-resource and generalizable settings; EPGSpeller can align rhetorically while keeping EPG-specific evidence separate.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Useful background for low-shot and cross-participant framing, without serving as a direct CER comparison.

#### Sources

- DOI: MorsEar (academic, retrieved 2026-06-27). https://doi.org/10.1145/3772318.3791436 DOI: 10.1145/3772318.3791436
- Crossref API: 10.1145/3772318.3791436 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1145/3772318.3791436 DOI: 10.1145/3772318.3791436
- OpenAlex: MorsEar (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.1145/3772318.3791436 DOI: 10.1145/3772318.3791436

<a id="guo2026-cross-modal-meta-generalization-uti"></a>
### Cross-Modal Meta-Generalization for Silent Speech Recognition via Ultrasound Tongue Images

#### Basic Info

- **paper_id**: guo2026_cross_modal_meta_generalization_uti
- **title**: Cross-Modal Meta-Generalization for Silent Speech Recognition via Ultrasound Tongue Images
- **authors**: - Minghao Guo<br>- Qiang Fang<br>- Hongcheng Zhang<br>- Wenhuan Lu<br>- Jianguo Wei
- **year**: 2026
- **venue**: IEEE Transactions on Audio, Speech and Language Processing
- **doi**: 10.1109/taslpro.2025.3646808
- **primary_url**: https://doi.org/10.1109/taslpro.2025.3646808
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: guo2026crossmodalmetageneralization
- **coverage_origin**: added_in_v2_2026-06-27_web_supplement

#### Task & Data

- **modality**: Ultrasound tongue images for silent speech recognition.
- **device**: Ultrasound tongue imaging system described in the IEEE paper.
- **task**: Silent speech recognition via ultrasound tongue images with cross-modal meta-generalization.
- **output_unit**: Speech/text units defined by the paper-specific recognition task.
- **vocabulary_setting**: Paper-specific SSR setting; not EPG open-character silent spelling.
- **datasets**: Paper-specific ultrasound tongue image SSR datasets.

#### Protocol & Evaluation

- **evaluation_protocol**: Cross-modal meta-generalization protocol described by the IEEE paper.
- **protocol_generalization**: Highly relevant for transfer/generalization framing, though modality and task differ from EPGSpeller.
- **participant_generalization**: Generalization is central at the cross-modal level; participant split details must be read from the paper.
- **metrics_reported**: Recognition metrics reported by IEEE TASLP paper.
- **benchmark_or_audit_status**: Peer-reviewed journal paper; no v2-confirmed shared benchmark artifacts comparable to EPGSpeller.
- **leakage_or_constraint_notes**: Cross-modal training resources and vocabulary constraints should be separated from EPGSpeller sensor-only protocols.

#### Methods

- **decoder**: Paper-specific ultrasound SSR decoder.
- **model_architecture**: Cross-modal meta-generalization model described by the authors.
- **spatial_frontend**: Ultrasound image representation, not EPG palatogram layout.
- **augmentation**: Cross-modal/meta-learning strategy rather than simple augmentation.
- **language_model_or_postprocessing**: Paper-specific; not the main v2 relevance.
- **transfer_or_adaptation_method**: Central: cross-modal meta-generalization.

#### Auditability

- **source_quality_notes**: Confirmed through DOI/Crossref/OpenAlex metadata.
- **reproducibility_artifacts**: No v2-confirmed code/data release.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Targets cross-modal generalization in ultrasound-based silent speech recognition.; Provides a contemporary transfer-learning contrast for articulatory SSI.; Useful for EPGSpeller cross-participant transfer framing.
- **limitations**: Non-EPG modality.; Cross-modal gains should not be assumed for EPG palate contact without evidence.
- **reported_results_summary**: See IEEE TASLP paper; v2 uses this for transfer/generalization framing.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Supports the manuscript’s view that transfer mismatch is a primary SSI bottleneck and needs explicit protocol separation.
- **takeaways_for_related_work_section**: Cross-modal and meta-generalization are active SSR directions; EPGSpeller contributes an auditable EPG-specific benchmark rather than a universal transfer method.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Helps position P3/P3MS results as part of a broader transfer-generalization problem while keeping the evidence EPG-specific.

#### Sources

- DOI: Cross-Modal Meta-Generalization for Silent Speech Recognition via Ultrasound Tongue Images (academic, retrieved 2026-06-27). https://doi.org/10.1109/taslpro.2025.3646808 DOI: 10.1109/taslpro.2025.3646808
- Crossref API: 10.1109/taslpro.2025.3646808 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1109/taslpro.2025.3646808 DOI: 10.1109/taslpro.2025.3646808
- OpenAlex: Cross-Modal Meta-Generalization for Silent Speech Recognition via Ultrasound Tongue Images (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.1109/taslpro.2025.3646808 DOI: 10.1109/taslpro.2025.3646808

<a id="tang2026-sensing-technologies-ssi"></a>
### Sensing technologies for silent speech interfaces

#### Basic Info

- **paper_id**: tang2026_sensing_technologies_ssi
- **title**: Sensing technologies for silent speech interfaces
- **authors**: - Chenyu Tang<br>- Liang Qi<br>- Shuo Gao<br>- Zibo Zhang<br>- Wentian Yi<br>- Muzi Xu<br>- Edoardo Occhipinti<br>- Yu Pan<br>- Luigi G. Occhipinti
- **year**: 2026
- **venue**: Nature Sensors
- **doi**: 10.1038/s44460-025-00010-2
- **primary_url**: https://doi.org/10.1038/s44460-025-00010-2
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: tang2026sensingtechnologiesssi
- **coverage_origin**: added_in_v2_2026-06-27_web_supplement

#### Task & Data

- **modality**: Review of sensing technologies for SSI across modalities.
- **device**: Multiple SSI sensing technologies surveyed.
- **task**: Review and taxonomy of silent speech interface sensing technologies.
- **output_unit**: Not a decoder benchmark; taxonomy/review output.
- **vocabulary_setting**: Not applicable; review article.
- **datasets**: Multiple datasets/systems discussed by the review.

#### Protocol & Evaluation

- **evaluation_protocol**: Review-level synthesis rather than one benchmark protocol.
- **protocol_generalization**: Current review source for sensor taxonomy; useful for avoiding overbroad claims about EPG as one SSI modality among many.
- **participant_generalization**: Review item; participant generalization varies across surveyed systems.
- **metrics_reported**: Review-level comparison dimensions rather than a single metric table.
- **benchmark_or_audit_status**: High-level review; not a reproducibility artifact for EPGSpeller.
- **leakage_or_constraint_notes**: Use as modality taxonomy, not as evidence for EPGSpeller numeric performance.

#### Methods

- **decoder**: Not a decoder paper.
- **model_architecture**: Not applicable; review.
- **spatial_frontend**: Surveyed across modalities; EPG-specific spatial assumptions should still cite EPG papers.
- **augmentation**: Varies across reviewed systems.
- **language_model_or_postprocessing**: Varies across reviewed systems.
- **transfer_or_adaptation_method**: Varies across reviewed systems.

#### Auditability

- **source_quality_notes**: Current peer-reviewed review confirmed through DOI/Crossref/OpenAlex metadata.
- **reproducibility_artifacts**: Review article; no single dataset artifact.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Provides a 2026 synthesis of sensing technologies for SSI.; Updates the broader modality taxonomy beyond earlier 2010/2017/2020 reviews.; Useful for contemporary positioning of EPG as one SSI sensor family.
- **limitations**: Review-level claims do not replace protocol-matched benchmark evidence.; Specific EPG conclusions still require EPG-centered sources.
- **reported_results_summary**: Review article; use for taxonomy rather than normalized metrics.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Updates the SSI review backbone and helps frame EPGSpeller as an auditable benchmark within a broad sensing landscape.
- **takeaways_for_related_work_section**: A current SSI sensing review should be cited alongside older SSI surveys when describing modality scope and sensor variability.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Strengthens the Introduction/Related Work with current survey context while preserving EPGSpeller’s narrow evidence claims.

#### Sources

- DOI: Sensing technologies for silent speech interfaces (academic, retrieved 2026-06-27). https://doi.org/10.1038/s44460-025-00010-2 DOI: 10.1038/s44460-025-00010-2
- Crossref API: 10.1038/s44460-025-00010-2 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1038/s44460-025-00010-2 DOI: 10.1038/s44460-025-00010-2
- OpenAlex: Sensing technologies for silent speech interfaces (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.1038/s44460-025-00010-2 DOI: 10.1038/s44460-025-00010-2

<a id="xu2026-llm-era-ssi-review"></a>
### Silent Speech Interfaces in the Era of Large Language Models: A Comprehensive Taxonomy and Systematic Review

#### Basic Info

- **paper_id**: xu2026_llm_era_ssi_review
- **title**: Silent Speech Interfaces in the Era of Large Language Models: A Comprehensive Taxonomy and Systematic Review
- **authors**: - Kele Xu<br>- Yifan Wang<br>- Ming Feng<br>- Qisheng Xu<br>- Wuyang Chen<br>- Yutao Dou<br>- Cheng Yang<br>- Huaimin Wang
- **year**: 2026
- **venue**: arXiv preprint arXiv:2603.11877
- **doi**: arXiv:2603.11877
- **primary_url**: https://arxiv.org/abs/2603.11877
- **pdf_url**: https://arxiv.org/pdf/2603.11877
- **code_or_data_release**: N/A
- **citation_key_suggestion**: xu2026llmerassi
- **coverage_origin**: added_in_v2_2026-06-27_web_supplement

#### Task & Data

- **modality**: Systematic review across silent speech interface modalities with an LLM-era taxonomy.
- **device**: Multiple SSI devices/sensing technologies reviewed.
- **task**: Comprehensive taxonomy and systematic review of SSI in the LLM era.
- **output_unit**: Review/taxonomy, not a decoder benchmark.
- **vocabulary_setting**: Not applicable; review article.
- **datasets**: Multiple SSI datasets/systems surveyed.

#### Protocol & Evaluation

- **evaluation_protocol**: Review-level synthesis.
- **protocol_generalization**: Useful for current LLM-era framing and taxonomy; not numeric benchmark evidence.
- **participant_generalization**: Varies across reviewed systems.
- **metrics_reported**: Review dimensions rather than one shared metric.
- **benchmark_or_audit_status**: Preprint review; use as contemporary taxonomy with caution.
- **leakage_or_constraint_notes**: Review helps identify LLM/decoder layers but does not define leakage-safe EPG evaluation by itself.

#### Methods

- **decoder**: Review item; discusses multiple decoders.
- **model_architecture**: Review item; discusses multiple architectures.
- **spatial_frontend**: Varies by reviewed modality.
- **augmentation**: Varies by reviewed system.
- **language_model_or_postprocessing**: Central theme: LLM-era SSI taxonomy.
- **transfer_or_adaptation_method**: Varies by reviewed system.

#### Auditability

- **source_quality_notes**: arXiv primary record plus arXiv API/PDF sources; preprint status should be stated.
- **reproducibility_artifacts**: Review article; no single dataset artifact.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Provides a current taxonomy for SSI in the LLM era.; Highlights shift from transducer-centric views toward intent-to-execution systems.; Useful for framing LM/LLM assistance separately from sensing.
- **limitations**: Preprint status in v2 evidence.; Not an EPG-specific benchmark source.
- **reported_results_summary**: Review item; no normalized numeric results used in v2.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Helps update the survey backbone beyond older SSI reviews and motivates explicit treatment of LLM-assisted decoding as out-of-scope for current audited EPG results.
- **takeaways_for_related_work_section**: Related work should acknowledge LLM-era SSI while preserving EPGSpeller’s stricter sensor-decoding evidence boundaries.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Supports a short future-work/positioning note: EPGSpeller could later add LM-assisted decoding, but current claims remain lexicon-free and audit-bound.

#### Sources

- arXiv: Silent Speech Interfaces in the Era of Large Language Models (academic, retrieved 2026-06-27). https://arxiv.org/abs/2603.11877
- PDF: Silent Speech Interfaces in the Era of Large Language Models (academic, retrieved 2026-06-27). https://arxiv.org/pdf/2603.11877
- arXiv API: 2603.11877 (web, retrieved 2026-06-27). http://export.arxiv.org/api/query?id_list=2603.11877

<a id="stone2020-electro-optical-stomatography-cross-speaker"></a>
### Cross-Speaker Silent-Speech Command Word Recognition Using Electro-Optical Stomatography

#### Basic Info

- **paper_id**: stone2020_electro_optical_stomatography_cross_speaker
- **title**: Cross-Speaker Silent-Speech Command Word Recognition Using Electro-Optical Stomatography
- **authors**: Simon Stone; Peter Birkholz
- **year**: 2020
- **venue**: ICASSP 2020 - IEEE International Conference on Acoustics, Speech and Signal Processing
- **doi**: 10.1109/ICASSP40776.2020.9053447
- **primary_url**: https://doi.org/10.1109/ICASSP40776.2020.9053447
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: stone2020stomatography
- **coverage_origin**: added_in_v2_2026-06-27_web_supplement_gap_closure

#### Task & Data

- **modality**: Electro-optical stomatography; intraoral/articulatory sensing related to palate/tongue-contact style SSI.
- **device**: Electro-optical stomatography setup described in the ICASSP paper.
- **task**: Cross-speaker silent-speech command word recognition.
- **output_unit**: Command words.
- **vocabulary_setting**: Closed or constrained command-word recognition.
- **datasets**: Paper-specific electro-optical stomatography command-word dataset.

#### Protocol & Evaluation

- **evaluation_protocol**: Cross-speaker command-word recognition protocol.
- **protocol_generalization**: Important gap-closure item: directly addresses cross-speaker silent-speech recognition in a mouth/palate-related sensor setting, but under constrained command words.
- **participant_generalization**: Cross-speaker evaluation is central according to the title/metadata.
- **metrics_reported**: Command-word recognition metrics reported by ICASSP 2020 paper.
- **benchmark_or_audit_status**: Peer-reviewed conference paper; no v2-confirmed shared deterministic EPGSpeller-style artifact registry.
- **leakage_or_constraint_notes**: Closed command-word recognition is not comparable to lexicon-free spelling CER; cite as cross-speaker sensor context only.

#### Methods

- **decoder**: Paper-specific command-word recognizer.
- **model_architecture**: Paper-specific electro-optical stomatography recognition model.
- **spatial_frontend**: Mouth/stomatography sensor representation; related to but not identical with EPG electrode palatograms.
- **augmentation**: See paper.
- **language_model_or_postprocessing**: Likely constrained by command vocabulary; not LM/LLM-assisted open text entry.
- **transfer_or_adaptation_method**: Cross-speaker recognition is central.

#### Auditability

- **source_quality_notes**: Confirmed through DOI/Crossref/OpenAlex metadata.
- **reproducibility_artifacts**: No v2-confirmed code/data release.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Adds a cross-speaker silent-speech command-word recognition reference in a stomatography sensor setting.; Closes the prior search-log gap around EPG-adjacent recognition work beyond SilentSpeller.; Useful contrast between cross-speaker closed-vocabulary recognition and EPGSpeller cross-participant spelling.
- **limitations**: Closed command-word task differs from open-character silent spelling.; Sensor modality is EPG-adjacent but not the same as the EPGSpeller data source.
- **reported_results_summary**: See ICASSP 2020 paper; v2 uses it as gap-closure context rather than normalized metrics.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Provides a closer articulatory/intraoral cross-speaker recognition reference than broad SSI surveys, while reinforcing the need to separate vocabulary constraints.
- **takeaways_for_related_work_section**: Cross-speaker mouth-sensor recognition existed before EPGSpeller, but often in constrained command-word settings; EPGSpeller’s contribution is audited open-character/protocol-separated benchmarking.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Addresses the 2026-02-17 search-log gap for EPG/EPG-adjacent recognition and helps sharpen the distinction between command-word cross-speaker recognition and lexicon-free spelling.

#### Sources

- DOI: Cross-Speaker Silent-Speech Command Word Recognition Using Electro-Optical Stomatography (academic, retrieved 2026-06-27). https://doi.org/10.1109/ICASSP40776.2020.9053447 DOI: 10.1109/ICASSP40776.2020.9053447
- Crossref API: 10.1109/ICASSP40776.2020.9053447 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1109/ICASSP40776.2020.9053447 DOI: 10.1109/ICASSP40776.2020.9053447
- OpenAlex: Cross-Speaker Silent-Speech Command Word Recognition Using Electro-Optical Stomatography (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.1109/ICASSP40776.2020.9053447 DOI: 10.1109/ICASSP40776.2020.9053447

<a id="hardcastle1989-state-of-art-epg"></a>
### New developments in electropalatography: A state-of-the-art report

#### Basic Info

- **paper_id**: hardcastle1989_state_of_art_epg
- **title**: New developments in electropalatography: A state-of-the-art report
- **authors**: - W. Hardcastle<br>- W. Jones<br>- C. Knight<br>- A. Trudgeon<br>- G. Calder
- **year**: 1989
- **venue**: Clinical Linguistics & Phonetics
- **doi**: 10.3109/02699208908985268
- **primary_url**: https://doi.org/10.3109/02699208908985268
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: hardcastle1989epg
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Electropalatography (EPG)
- **device**: EPG pseudopalate (palate-contact electrode arrays; instrumentation report)
- **task**: State-of-the-art overview of EPG developments (instrumentation, visualization, and analysis)
- **output_unit**: N/A (instrumentation / overview paper)
- **vocabulary_setting**: N/A
- **datasets**: N/A (overview/report)

#### Protocol & Evaluation

- **evaluation_protocol**: N/A (overview/report)
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: N/A (overview/report)
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: N/A
- **model_architecture**: N/A
- **spatial_frontend**: EPG electrode arrays yield spatial tongue–palate contact patterns
- **augmentation**: N/A
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Provides an early state-of-the-art report summarizing developments in EPG instrumentation and usage.; Serves as a foundational reference for what EPG measures (contact patterns) and how EPG data are represented/visualized.; Useful background for motivating spatially structured representations when modeling EPG time series.
- **limitations**: Not a machine-learning decoding paper; focuses on EPG technology and practice rather than text/speech decoding benchmarks.; As an early report, it predates later deep-learning approaches and modern wearable form factors.
- **reported_results_summary**: Overview/report; it synthesizes developments and usage rather than presenting a single benchmark.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Provides foundational EPG background and motivates why the electrode layout and spatial structure matter, supporting Related Work sections on EPG sensing and sensor design assumptions.
- **takeaways_for_related_work_section**: A foundational EPG state-of-the-art report that can be cited to explain EPG sensing/representation basics and to motivate spatial inductive biases and electrode-layout considerations.
- **gap_or_relevance_to_current_epgspeller_manuscript**: EPG representation/device context. In v2 it supports the manuscript discussion of spatial layout, electrode budget, and device-specific assumptions.

#### Sources

- DOI: 10.3109/02699208908985268 (academic, retrieved 2026-06-27). https://doi.org/10.3109/02699208908985268 DOI: 10.3109/02699208908985268
- Crossref API: 10.3109/02699208908985268 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.3109/02699208908985268 DOI: 10.3109/02699208908985268
- OpenAlex: New developments in electropalatography: A state-of-the-art report (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.3109/02699208908985268 DOI: 10.3109/02699208908985268

<a id="hardcastle1990-epg-phonetic-research"></a>
### Electropalatography in phonetic research and in speech training

#### Basic Info

- **paper_id**: hardcastle1990_epg_phonetic_research
- **title**: Electropalatography in phonetic research and in speech training
- **authors**: William J. Hardcastle
- **year**: 1990
- **venue**: ICSLP 1990 (ISCA Archive)
- **doi**: 10.21437/icslp.1990-305
- **primary_url**: https://www.isca-archive.org/icslp_1990/hardcastle90b_icslp.html
- **pdf_url**: https://www.isca-archive.org/icslp_1990/hardcastle90b_icslp.pdf
- **code_or_data_release**: N/A
- **citation_key_suggestion**: hardcastle1990epg
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Electropalatography (EPG)
- **device**: EPG pseudopalate (electrode palate contact sensing)
- **task**: Phonetic research and speech training using EPG (visual feedback)
- **output_unit**: N/A (methodology paper)
- **vocabulary_setting**: N/A
- **datasets**: Pilot experiment described in the paper (pronunciation teaching example)

#### Protocol & Evaluation

- **evaluation_protocol**: Pilot pronunciation teaching experiment and discussion of EPG applications
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: Qualitative discussion; focuses on EPG utility rather than a single standardized metric
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: N/A
- **model_architecture**: N/A
- **spatial_frontend**: EPG provides spatio-temporal tongue-palate contact patterns (palate electrode grid)
- **augmentation**: N/A
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Explains EPG as an instrumental technique to record spatio-temporal tongue-palate contact patterns.; Discusses EPG applications in phonetic research, speech pathology, and pronunciation teaching via visual feedback.; Provides foundational context for EPG as a sensing modality and its constraints (contact-only, palate-limited).
- **limitations**: Not a machine learning decoding paper; focuses on EPG instrumentation and applications.; Primarily qualitative; does not establish decoding benchmarks or cross-speaker generalization results.
- **reported_results_summary**: Descriptive/pilot paper on EPG usage for phonetic research and training; consult ISCA page for details.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Provides foundational EPG background for the Related Work (Section on EPG sensing), helping clarify what EPG measures and why spatial structure matters when designing decoders/front-ends.
- **takeaways_for_related_work_section**: Use as a foundational EPG reference describing the sensing principle and clinical/training applications; motivates treating EPG as spatio-temporal contact patterns and sets context for learning-based decoding.
- **gap_or_relevance_to_current_epgspeller_manuscript**: EPG representation/device context. In v2 it supports the manuscript discussion of spatial layout, electrode budget, and device-specific assumptions.

#### Sources

- ISCA Archive: Electropalatography in phonetic research and in speech training (Hardcastle, 1990) (academic, retrieved 2026-06-27). https://www.isca-archive.org/icslp_1990/hardcastle90b_icslp.html DOI: 10.21437/icslp.1990-305
- DOI: 10.21437/icslp.1990-305 (academic, retrieved 2026-06-27). https://doi.org/10.21437/icslp.1990-305 DOI: 10.21437/icslp.1990-305
- Crossref API: 10.21437/icslp.1990-305 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.21437/icslp.1990-305 DOI: 10.21437/icslp.1990-305

<a id="hardcastle1991-epg-data-reduction-coarticulation"></a>
### EPG data reduction methods and their implications for studies of lingual coarticulation

#### Basic Info

- **paper_id**: hardcastle1991_epg_data_reduction_coarticulation
- **title**: EPG data reduction methods and their implications for studies of lingual coarticulation
- **authors**: W.J. Hardcastle; F. Gibbon; K. Nicolaidis
- **year**: 1991
- **venue**: Journal of Phonetics
- **doi**: 10.1016/S0095-4470(19)30343-2
- **primary_url**: https://doi.org/10.1016/S0095-4470(19)30343-2
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: hardcastle1991epgreduction
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Electropalatography (EPG)
- **device**: EPG pseudopalate (electrode contact array)
- **task**: EPG data reduction / representation methods for analyzing lingual coarticulation
- **output_unit**: reduced EPG representations (contact-pattern summaries)
- **vocabulary_setting**: N/A (phonetic analysis focus)
- **datasets**: EPG data for coarticulation studies as reported in the paper

#### Protocol & Evaluation

- **evaluation_protocol**: Methodological comparison/discussion of reduction approaches in coarticulation analysis (see paper)
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: Analysis outcomes depend on reduction method; see paper for the specific measures used
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: N/A (analysis/representation paper, not a decoding benchmark)
- **model_architecture**: N/A
- **spatial_frontend**: EPG contact patterns summarized via data reduction methods (paper discusses representation choices)
- **augmentation**: N/A
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Discusses and evaluates EPG data reduction methods and how representation choices affect conclusions in coarticulation studies.; Provides historical precedent for treating EPG as structured spatial data that can be summarized/compressed in multiple ways.; Relevant background for modern electrode-selection and low-K designs: reduction choices trade off spatial detail and interpretability.
- **limitations**: Focuses on phonetic analysis rather than end-to-end text decoding; does not provide CER/WER-style benchmarks.; Reduction methods are evaluated in the context of coarticulation analysis and may not directly translate to modern neural decoders.
- **reported_results_summary**: Methodological/analysis paper; it discusses implications of EPG representation choices for coarticulation analysis rather than reporting a decoding benchmark.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Directly relevant to electrode reduction / representation discussions (EPG compression and information loss), supporting Related Work on sensor design and on spatial representation baselines for EPG.
- **takeaways_for_related_work_section**: An early EPG data-reduction paper showing that representation choices materially affect what information is preserved; useful for motivating K-curves, selection strategies, and explicit spatial modeling in modern EPG decoders.
- **gap_or_relevance_to_current_epgspeller_manuscript**: EPG representation/device context. In v2 it supports the manuscript discussion of spatial layout, electrode budget, and device-specific assumptions.

#### Sources

- DOI: 10.1016/S0095-4470(19)30343-2 (academic, retrieved 2026-06-27). https://doi.org/10.1016/S0095-4470(19)30343-2 DOI: 10.1016/S0095-4470(19)30343-2
- Crossref API: 10.1016/S0095-4470(19)30343-2 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1016/S0095-4470(19)30343-2 DOI: 10.1016/S0095-4470(19)30343-2
- OpenAlex: EPG data reduction methods and their implications for studies of lingual coarticulation (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.1016/S0095-4470(19)30343-2 DOI: 10.1016/S0095-4470(19)30343-2

<a id="shadle1993-epg-structured-light"></a>
### Depth measurement of face and palate by structured light

#### Basic Info

- **paper_id**: shadle1993_epg_structured_light
- **title**: Depth measurement of face and palate by structured light
- **authors**: Christine H. Shadle; J. N. Carter; T. P. Monks; J. Field
- **year**: 1993
- **venue**: Eurospeech 1993 (ISCA Archive)
- **doi**: 10.21437/eurospeech.1993-403
- **primary_url**: https://www.isca-archive.org/eurospeech_1993/shadle93_eurospeech.html
- **pdf_url**: https://www.isca-archive.org/eurospeech_1993/shadle93_eurospeech.pdf
- **code_or_data_release**: N/A
- **citation_key_suggestion**: shadle1993structured
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Electropalatography-related instrumentation (palate geometry measurement)
- **device**: Structured-light depth measurement system for face/palate and EPG palate
- **task**: Measuring palate/face geometry to enhance EPG visualization and derive parameters
- **output_unit**: 3D/2D depth maps and derived geometric parameters
- **vocabulary_setting**: N/A
- **datasets**: Instrument measurement examples described in the paper

#### Protocol & Evaluation

- **evaluation_protocol**: Instrumentation calibration and preliminary measurement results
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: System resolution and measurement considerations (paper-specific)
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: N/A
- **model_architecture**: N/A
- **spatial_frontend**: Provides geometric context for EPG patterns (enhanced visualization / distance measures)
- **augmentation**: N/A
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Describes structured-light depth measurement applied to EPG palates and lower face.; Motivates enhancing EPG images with geometric information and enabling automatic distance measurements.; Connects EPG sensing to geometry-aware visualization/parameterization, relevant to spatial modeling discussions.
- **limitations**: Not a decoding/recognition paper; focuses on measurement and visualization infrastructure.; Preliminary results; not a standardized evaluation of decoding accuracy.
- **reported_results_summary**: Instrumentation paper describing structured-light depth measurement for palate/face and its use for EPG visualization; see ISCA Archive for details.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Relevant to spatial modeling motivation: EPG is inherently spatial, and geometry-aware representations can potentially improve model inductive bias (ties to H11 2D reconstruction concept).
- **takeaways_for_related_work_section**: Use as an early reference connecting EPG to geometry-aware visualization/parameterization; supports the argument that spatial structure is meaningful and motivates explicit spatial front-ends.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- ISCA Archive: Depth measurement of face and palate by structured light (Shadle et al., 1993) (academic, retrieved 2026-06-27). https://www.isca-archive.org/eurospeech_1993/shadle93_eurospeech.html DOI: 10.21437/eurospeech.1993-403
- DOI: 10.21437/eurospeech.1993-403 (academic, retrieved 2026-06-27). https://doi.org/10.21437/eurospeech.1993-403 DOI: 10.21437/eurospeech.1993-403
- Crossref API: 10.21437/eurospeech.1993-403 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.21437/eurospeech.1993-403 DOI: 10.21437/eurospeech.1993-403

<a id="carreira-perpinan1998-dimred-epg"></a>
### Dimensionality reduction of electropalatographic data using latent variable models

#### Basic Info

- **paper_id**: carreira_perpinan1998_dimred_epg
- **title**: Dimensionality reduction of electropalatographic data using latent variable models
- **authors**: Miguel A. Carreira-Perpiñán; Steve Renals
- **year**: 1998
- **venue**: Speech Communication 26(4):259-282
- **doi**: 10.1016/S0167-6393(98)00059-4
- **primary_url**: https://www.sciencedirect.com/science/article/pii/S0167639398000594
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: carreiraperpinan1998epg
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Electropalatography (EPG)
- **device**: Reading EPG system (EPG frames as binary electrode-contact vectors; EUR-ACCOR database)
- **task**: Unsupervised dimensionality reduction / representation learning for EPG frames
- **output_unit**: continuous latent variables / low-dimensional embeddings
- **vocabulary_setting**: N/A
- **datasets**: Subset of the EUR-ACCOR database (as reported in the paper)

#### Protocol & Evaluation

- **evaluation_protocol**: Train/test splits on EPG frame datasets; evaluation via log-likelihood and reconstruction error across speakers/styles (as reported)
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Multi-participant or cross-participant behavior is discussed in the source-specific protocol; exact comparability depends on the paper definition.
- **metrics_reported**: Log-likelihood and reconstruction error for latent variable models (paper reports comparisons)
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: Latent variable modeling (factor analysis, PCA, GTM, mixture models) for EPG frame modeling
- **model_architecture**: Probabilistic latent variable models (linear and nonlinear)
- **spatial_frontend**: EPG frames treated as high-dimensional binary vectors; dimensionality reduction learns low-D representations
- **augmentation**: N/A
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Applies probabilistic latent variable models to learn low-dimensional representations of EPG frames.; Compares linear (FA/PCA) vs nonlinear (GTM, mixture models) methods and reports nonlinear advantages.; Connects EPG dimensionality reduction to applications in analysis, visualization, and speech-related modeling.
- **limitations**: Focuses on spatial dimensionality reduction of EPG frames; temporal dynamics are treated separately.; Data and conclusions are specific to the EUR-ACCOR subset and EPG configuration used.
- **reported_results_summary**: The paper reports that nonlinear latent variable models outperform linear ones in log-likelihood and reconstruction error on EUR-ACCOR EPG data; see the official paper for exact figures.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Directly relevant to representation choice and why PCA-like compression is a standard baseline in EPG analysis; provides historical context for Axis C (representation) and motivates exploring richer nonlinear/spatial models.
- **takeaways_for_related_work_section**: A foundational EPG representation paper comparing PCA/FA to nonlinear latent-variable models on EUR-ACCOR; supports discussing PCA as a principled compression baseline and motivates more expressive spatial front-ends.
- **gap_or_relevance_to_current_epgspeller_manuscript**: EPG representation/device context. In v2 it supports the manuscript discussion of spatial layout, electrode budget, and device-specific assumptions.

#### Sources

- ScienceDirect: Dimensionality reduction of electropalatographic data using latent variable models (academic, retrieved 2026-06-27). https://www.sciencedirect.com/science/article/pii/S0167639398000594 DOI: 10.1016/S0167-6393(98)00059-4
- DOI: 10.1016/S0167-6393(98)00059-4 (academic, retrieved 2026-06-27). https://doi.org/10.1016/S0167-6393(98)00059-4 DOI: 10.1016/S0167-6393(98)00059-4
- Carreira-Perpiñán research page: Dimensionality reduction of EPG data (lists 1998 papers) (web, retrieved 2026-06-27). https://faculty.ucmerced.edu/mcarreira-perpinan/research/epg.html

<a id="graves2006-ctc"></a>
### Connectionist Temporal Classification: Labelling Unsegmented Sequence Data with Recurrent Neural Networks

#### Basic Info

- **paper_id**: graves2006_ctc
- **title**: Connectionist Temporal Classification: Labelling Unsegmented Sequence Data with Recurrent Neural Networks
- **authors**: Alex Graves; Santiago Fernández; Faustino Gomez; Jürgen Schmidhuber
- **year**: 2006
- **venue**: ICML 2006
- **doi**: 10.1145/1143844.1143891
- **primary_url**: https://dl.acm.org/doi/10.1145/1143844.1143891
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: graves2006ctc
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Method paper (sequence learning / speech recognition)
- **device**: N/A
- **task**: Sequence labeling without pre-segmented alignments
- **output_unit**: generic label sequences (e.g., phonemes/characters)
- **vocabulary_setting**: N/A
- **datasets**: Demonstrated on TIMIT (as stated in the paper)

#### Protocol & Evaluation

- **evaluation_protocol**: Speech recognition evaluation on TIMIT as reported
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: Speech recognition error rates as reported in the paper
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: CTC objective + dynamic programming alignment; decoding can be greedy or beam search (not fixed by the objective)
- **model_architecture**: Recurrent neural networks trained with CTC
- **spatial_frontend**: N/A
- **augmentation**: N/A
- **language_model_or_postprocessing**: Foundational CTC objective; not an SSI system and has no lexicon/LLM constraint itself.
- **transfer_or_adaptation_method**: Relevant as non-EPG SSI or method context; transfer/adaptation evidence should not be extrapolated to EPG without matched data.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Introduces CTC for training sequence models without frame-level alignments.; Enables end-to-end mapping from input sequences to label sequences with monotonic alignment.; Became a foundational objective for speech recognition and other sequence transduction tasks.
- **limitations**: Assumes monotonic alignment; not suitable for general non-monotonic seq2seq tasks.; Decoding quality depends on inference strategy (greedy vs beam search with language model).
- **reported_results_summary**: The paper demonstrates CTC on speech recognition (TIMIT) and compares against baselines; see ACM DL/DOI sources for details.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Core method used in EPGSpeller-style models (RNN/CTC). Needed for Related Work section on decoding formulations and to justify open-vocabulary greedy decoding vs constrained decoding variants.
- **takeaways_for_related_work_section**: CTC is the standard alignment-free objective enabling RNN-based character/phoneme decoding from unsegmented inputs; cite this to ground the modeling choice and to discuss decoding (greedy vs constrained/LM).
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- ACM Digital Library: Connectionist Temporal Classification (ICML 2006) (academic, retrieved 2026-06-27). https://dl.acm.org/doi/10.1145/1143844.1143891 DOI: 10.1145/1143844.1143891
- DOI: 10.1145/1143844.1143891 (academic, retrieved 2026-06-27). https://doi.org/10.1145/1143844.1143891 DOI: 10.1145/1143844.1143891
- Crossref API: 10.1145/1143844.1143891 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1145/1143844.1143891 DOI: 10.1145/1143844.1143891

<a id="toutios2006-acoustic-to-epg-mapping"></a>
### On the Acoustic-to-Electropalatographic Mapping

#### Basic Info

- **paper_id**: toutios2006_acoustic_to_epg_mapping
- **title**: On the Acoustic-to-Electropalatographic Mapping
- **authors**: Asterios Toutios; Konstantinos Margaritis
- **year**: 2006
- **venue**: Lecture Notes in Computer Science (book chapter)
- **doi**: 10.1007/11613107_16
- **primary_url**: https://link.springer.com/chapter/10.1007/11613107_16
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: toutios2006acoustic2epg
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Speech acoustics + Electropalatography (EPG)
- **device**: Audio recording + EPG palate-contact sensing (as reported)
- **task**: Acoustic-to-EPG mapping (predicting electropalatograms from acoustic signals)
- **output_unit**: EPG contact patterns (electropalatograms)
- **vocabulary_setting**: N/A (mapping task; not a lexicon-decoding benchmark)
- **datasets**: Paired acoustic+EPG data as reported in the chapter

#### Protocol & Evaluation

- **evaluation_protocol**: Mapping evaluation protocol as reported (see chapter for details)
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: Mapping/reconstruction performance metrics as reported in the chapter
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: Supervised acoustic-to-EPG mapping model
- **model_architecture**: Machine learning approach for acoustic-to-EPG mapping (chapter-specific)
- **spatial_frontend**: EPG contact patterns treated as structured high-dimensional targets; representation choices are central to mapping
- **augmentation**: N/A / not central
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Discusses the acoustic-to-electropalatographic mapping problem and proposes/analyses approaches for predicting EPG patterns from acoustics.; Provides historical context for modeling EPG as a structured spatial signal, supporting modern spatial front-end motivations.; Relevant to discussions of representation/compression baselines for EPG contact patterns.
- **limitations**: Not an EPG-to-text decoding paper; relevance is via representation/modeling context.; Chapter-level details (dataset, evaluation setup) must be consulted for precise reproduction.
- **reported_results_summary**: Book chapter; reports mapping performance under its protocol and discusses the mapping formulation (see Springer/DOI sources).

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Provides relevant background on representing and modeling EPG contact patterns as structured spatial objects, supporting Related Work sections on spatial modeling and representation choices.
- **takeaways_for_related_work_section**: A 2006 LNCS chapter on acoustic-to-EPG mapping; useful for articulatory modeling context and for motivating explicit spatial representations of EPG contact patterns.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- SpringerLink: On the Acoustic-to-Electropalatographic Mapping (academic, retrieved 2026-06-27). https://link.springer.com/chapter/10.1007/11613107_16 DOI: 10.1007/11613107_16
- DOI: 10.1007/11613107_16 (academic, retrieved 2026-06-27). https://doi.org/10.1007/11613107_16 DOI: 10.1007/11613107_16
- Crossref API: 10.1007/11613107_16 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1007/11613107_16 DOI: 10.1007/11613107_16

<a id="toutios2006-learning-epg-from-acoustics"></a>
### Learning Electropalatograms from Acoustics

#### Basic Info

- **paper_id**: toutios2006_learning_epg_from_acoustics
- **title**: Learning Electropalatograms from Acoustics
- **authors**: A. Toutios; K. Margaritis
- **year**: 2006
- **venue**: ICASSP 2006 (IEEE International Conference on Acoustics, Speech and Signal Processing)
- **doi**: 10.1109/ICASSP.2006.1660032
- **primary_url**: https://doi.org/10.1109/ICASSP.2006.1660032
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: toutios2006learnedepg
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Speech acoustics + Electropalatography (EPG)
- **device**: Audio recording + EPG palate-contact sensing (as reported)
- **task**: Acoustic-to-EPG mapping (predicting electropalatograms from acoustics)
- **output_unit**: EPG contact patterns (electropalatograms)
- **vocabulary_setting**: N/A (mapping task; not a lexicon-decoding benchmark)
- **datasets**: Acoustic + EPG paired data as reported in the paper

#### Protocol & Evaluation

- **evaluation_protocol**: Mapping evaluation on held-out data as reported (see paper for details)
- **protocol_generalization**: Includes or motivates compositional/open-vocabulary or held-out-word evaluation; still not directly leaderboard-comparable without matched splits and metrics.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: Mapping/reconstruction performance metrics as reported in the paper
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: Supervised mapping model from acoustics to EPG patterns
- **model_architecture**: Machine learning model for acoustic-to-EPG prediction (paper-specific)
- **spatial_frontend**: EPG represented as multi-electrode contact patterns (palatograms) predicted from acoustic features
- **augmentation**: N/A / not central
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Proposes learning to predict EPG contact patterns from acoustic observations (acoustic-to-EPG mapping).; Illustrates that EPG contact patterns can be modeled/predicted as structured high-dimensional outputs, motivating representation discussions.; Useful related work for articulatory modeling context and for motivating spatially structured EPG representations.
- **limitations**: Task is acoustic-to-EPG prediction rather than EPG-to-text decoding; relevance is indirect (representation/modeling context).; Specific dataset and evaluation details are paper-specific and must be consulted for precise reproduction.
- **reported_results_summary**: The paper reports performance for predicting EPG patterns from acoustics under its protocol; consult DOI/Crossref sources and the paper for details.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Provides articulatory modeling context for EPG as a learnable structured signal; supports the Related Work discussion on spatial representations and why richer front-ends (2D/geometry-aware) may be appropriate.
- **takeaways_for_related_work_section**: An ICASSP 2006 paper on acoustic-to-EPG mapping; useful to cite for articulatory modeling context and for motivating structured representations of EPG contact patterns.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- DOI: 10.1109/ICASSP.2006.1660032 (academic, retrieved 2026-06-27). https://doi.org/10.1109/ICASSP.2006.1660032 DOI: 10.1109/ICASSP.2006.1660032
- Crossref API: 10.1109/ICASSP.2006.1660032 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1109/ICASSP.2006.1660032 DOI: 10.1109/ICASSP.2006.1660032
- OpenAlex: Learning Electropalatograms from Acoustics (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.1109/ICASSP.2006.1660032 DOI: 10.1109/ICASSP.2006.1660032

<a id="denby2010-silent-speech-interfaces"></a>
### Silent speech interfaces

#### Basic Info

- **paper_id**: denby2010_silent_speech_interfaces
- **title**: Silent speech interfaces
- **authors**: - Bruce Denby<br>- Tanja Schultz<br>- Kiyoshi Honda<br>- Thomas Hueber<br>- Jim M. Gilbert<br>- Jonathan S. Brumberg
- **year**: 2010
- **venue**: Speech Communication 52(4):270-287
- **doi**: 10.1016/j.specom.2009.08.002
- **primary_url**: https://www.sciencedirect.com/science/article/pii/S0167639309001307
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: denby2010ssi
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Survey / overview (multiple SSI modalities)
- **device**: N/A
- **task**: Silent Speech Interface (SSI) overview: technologies, applications, and challenges
- **output_unit**: N/A (survey)
- **vocabulary_setting**: N/A (survey)
- **datasets**: N/A (survey)

#### Protocol & Evaluation

- **evaluation_protocol**: N/A (survey)
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Primarily source-specific; use only as a task anchor unless the paper explicitly reports cross-user/user-independent evaluation.
- **metrics_reported**: N/A (survey)
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: N/A (survey)
- **model_architecture**: N/A (survey)
- **spatial_frontend**: N/A (survey)
- **augmentation**: N/A (survey)
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant as non-EPG SSI or method context; transfer/adaptation evidence should not be extrapolated to EPG without matched data.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Defines the SSI concept and surveys SSI technologies spanning multiple sensing modalities.; Summarizes common challenges in SSI (data, sensing variability, decoding, usability) and outlines future directions.; Serves as a canonical SSI reference for positioning EPG-based silent spelling within broader SSI research.
- **limitations**: As a 2010 survey, it predates many recent deep-learning-based SSI advances.; Survey scope emphasizes representative systems rather than exhaustive coverage of every subcommunity.
- **reported_results_summary**: Survey paper; it reviews representative SSI systems and challenges rather than reporting a single benchmark.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Provides a standard SSI definition and taxonomy to support clearer positioning/related work (W1/W6). Also motivates why comparing open-vocabulary vs constrained decoding must be protocol-aware (W2).
- **takeaways_for_related_work_section**: A canonical SSI survey defining problem scope and modality taxonomy; can be cited to contextualize EPGSpeller as an articulatory-sensing SSI focused on open-vocabulary silent spelling.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- ScienceDirect: Silent speech interfaces (Speech Communication, 2010) (academic, retrieved 2026-06-27). https://www.sciencedirect.com/science/article/pii/S0167639309001307 DOI: 10.1016/j.specom.2009.08.002
- DOI: 10.1016/j.specom.2009.08.002 (academic, retrieved 2026-06-27). https://doi.org/10.1016/j.specom.2009.08.002 DOI: 10.1016/j.specom.2009.08.002
- KITopen: Silent Speech Interfaces (Denby et al., Speech Communication 2010) (web, retrieved 2026-06-27). https://publikationen.bibliothek.kit.edu/1000026320 DOI: 10.1016/j.specom.2009.08.002

<a id="gilbert2010-magnetic-implants-silent-speech"></a>
### Isolated word recognition of silent speech using magnetic implants and sensors

#### Basic Info

- **paper_id**: gilbert2010_magnetic_implants_silent_speech
- **title**: Isolated word recognition of silent speech using magnetic implants and sensors
- **authors**: - J. M. Gilbert<br>- S. I. Rybchenko<br>- R. Hofe<br>- S. R. Ell<br>- M. J. Fagan<br>- R. K. Moore<br>- P. Green
- **year**: 2010
- **venue**: Medical Engineering & Physics 32(10):1189-1197
- **doi**: 10.1016/j.medengphy.2010.08.011
- **primary_url**: https://www.sciencedirect.com/science/article/pii/S1350453310001803
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: gilbert2010magnetic
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Magnetic implants + external magnetic sensors (articulator motion sensing)
- **device**: Permanent magnets on tongue/lips + magnetic sensors around face/head
- **task**: Silent speech recognition (isolated-word recognition for small vocabulary)
- **output_unit**: words
- **vocabulary_setting**: closed vocabulary (isolated words)
- **datasets**: Speaker-dependent recordings described in the paper

#### Protocol & Evaluation

- **evaluation_protocol**: Isolated-word recognition with template sets and evaluation trials as reported in the paper
- **protocol_generalization**: Closed-vocabulary or constrained protocol; useful as contrast but not directly comparable to EPGSpeller open-character decoding.
- **participant_generalization**: Primarily source-specific; use only as a task anchor unless the paper explicitly reports cross-user/user-independent evaluation.
- **metrics_reported**: Recognition rates for closed-vocabulary isolated-word tasks
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: Template matching using Dynamic Time Warping (DTW)
- **model_architecture**: Non-neural template-based classifier (DTW)
- **spatial_frontend**: Magnetic sensor array around the face; not an image-like 2D palate grid
- **augmentation**: Not central; focus is on sensor concept and DTW recognition
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant as non-EPG SSI or method context; transfer/adaptation evidence should not be extrapolated to EPG without matched data.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Demonstrates silent speech recognition using magnetic implants/sensors without acoustic input.; Uses DTW-based template matching to achieve high recognition rates on small-vocabulary isolated-word tasks.; Discusses feasibility for laryngectomy-related silent communication scenarios.
- **limitations**: Invasive (requires magnets/implants), raising practical and safety concerns.; Closed-vocabulary isolated-word setting; does not directly address open-vocabulary silent spelling.; Speaker-dependent training; generalization across speakers and sessions is challenging.
- **reported_results_summary**: The paper reports >90% recognition rates for a closed vocabulary (e.g., 57 isolated words) under its protocol; see the official paper for details.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Included as minimal SSI comparison and as an example of articulator-motion sensing for silent speech; helps contextualize why sensor modality and protocol choice matter when comparing to EPG-based silent spelling.
- **takeaways_for_related_work_section**: A representative non-EPG articulator-sensing SSI (magnetic implants) showing high closed-vocabulary isolated-word recognition with DTW; useful for framing modality trade-offs and why open-vocabulary silent spelling requires different evaluation protocols.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- PubMed: Isolated word recognition of silent speech using magnetic implants and sensors (academic, retrieved 2026-06-27). https://pubmed.ncbi.nlm.nih.gov/20863739/ DOI: 10.1016/j.medengphy.2010.08.011
- ScienceDirect: Isolated word recognition of silent speech using magnetic implants and sensors (academic, retrieved 2026-06-27). https://www.sciencedirect.com/science/article/pii/S1350453310001803 DOI: 10.1016/j.medengphy.2010.08.011
- DOI: 10.1016/j.medengphy.2010.08.011 (academic, retrieved 2026-06-27). https://doi.org/10.1016/j.medengphy.2010.08.011 DOI: 10.1016/j.medengphy.2010.08.011

<a id="hueber2010-ultrasound-optical-ssi"></a>
### Development of a silent speech interface driven by ultrasound and optical images of the tongue and lips

#### Basic Info

- **paper_id**: hueber2010_ultrasound_optical_ssi
- **title**: Development of a silent speech interface driven by ultrasound and optical images of the tongue and lips
- **authors**: Thomas Hueber; Elie-Laurent Benaroya; Bruce Denby; Gérard Chollet
- **year**: 2010
- **venue**: Speech Communication 52(4):288-300
- **doi**: 10.1016/j.specom.2009.11.004
- **primary_url**: https://www.sciencedirect.com/science/article/pii/S0167639309001733
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: hueber2010ultrasound
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Ultrasound tongue imaging + optical lip video (silent speech interface)
- **device**: Ultrasound imaging of tongue + CCD camera for lips
- **task**: Silent speech interface: articulatory-to-speech reconstruction
- **output_unit**: speech waveform (via segmental vocoder / concatenative synthesis)
- **vocabulary_setting**: phonetic target sequence prediction; vocabulary setting depends on decoder constraints (paper evaluates constraints)
- **datasets**: Audiovisual database with ultrasound + lip video + audio (1 hour per speaker; 2 speakers) as reported in the paper

#### Protocol & Evaluation

- **evaluation_protocol**: Experiments reported on recorded uttered speech; intended for silent-speech use (paper notes need for silent evaluation)
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Primarily source-specific; use only as a task anchor unless the paper explicitly reports cross-user/user-independent evaluation.
- **metrics_reported**: Phone recognition performance and speech reconstruction quality metrics reported in the paper.
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: HMM-based visual phone recognition + dictionary-driven unit selection + waveform generation (HNM-based prosody adaptation)
- **model_architecture**: Statistical models (continuous HMMs) for visual observations; segmental synthesis pipeline
- **spatial_frontend**: PCA-based image coding for ultrasound tongue and lip video features
- **augmentation**: Not central; paper focuses on feature extraction and decoding/synthesis pipeline
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant as non-EPG SSI or method context; transfer/adaptation evidence should not be extrapolated to EPG without matched data.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Early SSI system combining ultrasound tongue imaging and lip video to reconstruct speech.; Uses PCA-based visual feature coding and HMM-based phone recognition to constrain unit selection for synthesis.; Provides a concrete articulatory-to-speech pipeline and discusses constraints needed for intelligible reconstruction.
- **limitations**: Experiments are performed on uttered speech recordings; silent-speech evaluation may differ (explicitly noted by authors).; Imaging-based sensing can be bulky compared to wearable intra-oral devices.; System complexity (multi-stage recognizer + unit selection + synthesis) may limit real-time deployment.
- **reported_results_summary**: The paper reports phone recognition and reconstruction results under different constraints; consult the official paper for exact metrics.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Provides SSI context and a contrasting articulatory sensing modality (ultrasound/video) with a PCA-based spatial feature approach, relevant to discussing representation alternatives (W7) and decoding constraints (W2).
- **takeaways_for_related_work_section**: A representative SSI using ultrasound+video with PCA-coded spatial features and HMM-based decoding; useful to contrast imaging-based articulatory sensing with EPG and to motivate why simple compressions (e.g., PCA) are common in low-data articulatory interfaces.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- ScienceDirect: Development of a silent speech interface driven by ultrasound and optical images of the tongue and lips (academic, retrieved 2026-06-27). https://www.sciencedirect.com/science/article/pii/S0167639309001733 DOI: 10.1016/j.specom.2009.11.004
- DOI: 10.1016/j.specom.2009.11.004 (academic, retrieved 2026-06-27). https://doi.org/10.1016/j.specom.2009.11.004 DOI: 10.1016/j.specom.2009.11.004
- ScienceDirect: Speech Communication special issue Silent Speech Interfaces (Volume 52, Issue 4) (web, retrieved 2026-06-27). https://www.sciencedirect.com/journal/speech-communication/vol/52/issue/4

<a id="ssi-book-springer2017"></a>
### An Introduction to Silent Speech Interfaces

#### Basic Info

- **paper_id**: ssi_book_springer2017
- **title**: An Introduction to Silent Speech Interfaces
- **authors**: João Freitas; António Teixeira; Miguel Sales Dias; Samuel Silva
- **year**: 2016
- **venue**: SpringerBriefs in Speech Technology (Springer)
- **doi**: 10.1007/978-3-319-40174-4
- **primary_url**: https://link.springer.com/book/10.1007/978-3-319-40174-4
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: freitas2016ssi
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Survey / book
- **device**: N/A
- **task**: Silent Speech Interfaces (SSI) overview and taxonomy
- **output_unit**: N/A
- **vocabulary_setting**: N/A
- **datasets**: N/A

#### Protocol & Evaluation

- **evaluation_protocol**: N/A
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Primarily source-specific; use only as a task anchor unless the paper explicitly reports cross-user/user-independent evaluation.
- **metrics_reported**: N/A
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: N/A
- **model_architecture**: N/A
- **spatial_frontend**: N/A
- **augmentation**: N/A
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant as non-EPG SSI or method context; transfer/adaptation evidence should not be extrapolated to EPG without matched data.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Provides a taxonomy and overview of SSI modalities and system components.; Summarizes challenges and design trade-offs across SSI approaches.; Useful positioning reference for articulatory sensing (including EPG) in SSI.
- **limitations**: Publication-time snapshot (2016/2017 era); may not cover later deep-learning SSI advances.; Depth varies across modalities depending on literature maturity at publication time.
- **reported_results_summary**: Book-style survey; it synthesizes prior results rather than presenting a single benchmark.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Used for Related Work positioning and SSI taxonomy; supports clearer related-work structure and motivation for choosing EPG as an articulatory sensing modality.
- **takeaways_for_related_work_section**: A compact SSI overview that can be cited to define SSI modalities and motivate where EPG-based silent spelling sits within SSI, clarifying scope and terminology.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- SpringerLink: An Introduction to Silent Speech Interfaces (academic, retrieved 2026-06-27). https://link.springer.com/book/10.1007/978-3-319-40174-4 DOI: 10.1007/978-3-319-40174-4
- DOI: 10.1007/978-3-319-40174-4 (academic, retrieved 2026-06-27). https://doi.org/10.1007/978-3-319-40174-4 DOI: 10.1007/978-3-319-40174-4
- Crossref API: 10.1007/978-3-319-40174-4 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1007/978-3-319-40174-4 DOI: 10.1007/978-3-319-40174-4

<a id="park2019-specaugment"></a>
### SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition

#### Basic Info

- **paper_id**: park2019_specaugment
- **title**: SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition
- **authors**: - Daniel S. Park<br>- William Chan<br>- Yu Zhang<br>- Chung-Cheng Chiu<br>- Barret Zoph<br>- Ekin D. Cubuk<br>- Quoc V. Le
- **year**: 2019
- **venue**: Interspeech 2019 (ISCA Archive); also available on arXiv (1904.08779)
- **doi**: 10.21437/interspeech.2019-2680
- **primary_url**: https://www.isca-archive.org/interspeech_2019/park19_interspeech.html
- **pdf_url**: https://www.isca-archive.org/interspeech_2019/park19_interspeech.pdf
- **code_or_data_release**: N/A
- **citation_key_suggestion**: park2019specaugment
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Method paper (data augmentation for speech recognition features)
- **device**: N/A
- **task**: Data augmentation for end-to-end ASR
- **output_unit**: speech recognition labels (e.g., characters/words)
- **vocabulary_setting**: ASR settings in the paper (task-dependent)
- **datasets**: LibriSpeech and Switchboard (as reported)

#### Protocol & Evaluation

- **evaluation_protocol**: ASR evaluation on standard benchmarks (as reported)
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: WER on LibriSpeech/Switchboard under reported settings
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: Not the focus; augmentation is applied at feature level and can be used with various decoders
- **model_architecture**: Applied to end-to-end ASR architectures (e.g., Listen, Attend and Spell) as reported
- **spatial_frontend**: N/A
- **augmentation**: SpecAugment (time/frequency masking, optional warping) applied to input features
- **language_model_or_postprocessing**: Augmentation method context; no lexical decoding constraint.
- **transfer_or_adaptation_method**: Relevant as non-EPG SSI or method context; transfer/adaptation evidence should not be extrapolated to EPG without matched data.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Introduces SpecAugment as a simple, effective augmentation method applied directly on input features for ASR.; Demonstrates improved ASR performance on standard benchmarks without requiring additional labeled data.; Provides a general augmentation idea that can be adapted to other time-series modalities (e.g., EPG frames).
- **limitations**: Designed for spectrogram-like acoustic features; adaptation to other modalities requires careful interpretation.; Augmentation policy interacts with model architecture and data regime; not universally optimal.
- **reported_results_summary**: The arXiv paper reports WER improvements on LibriSpeech and Switchboard using SpecAugment; see the paper for exact settings and numbers.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Relevant as the conceptual basis for frame-level masking augmentations (Axis F / robustness). Helps justify using SpecAugment-like masking on EPG time-series and motivates evaluating robustness under sensor dropout.
- **takeaways_for_related_work_section**: SpecAugment is a widely used feature-level masking augmentation for ASR; it motivates analogous time/channel masking augmentations for EPG decoding to improve robustness and generalization.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- ISCA Archive: SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition (Interspeech 2019) (academic, retrieved 2026-06-27). https://www.isca-archive.org/interspeech_2019/park19_interspeech.html DOI: 10.21437/interspeech.2019-2680
- DOI: 10.21437/interspeech.2019-2680 (academic, retrieved 2026-06-27). https://doi.org/10.21437/interspeech.2019-2680 DOI: 10.21437/interspeech.2019-2680
- Crossref API: 10.21437/interspeech.2019-2680 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.21437/interspeech.2019-2680 DOI: 10.21437/interspeech.2019-2680
- arXiv: SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition (academic, retrieved 2026-06-27). https://arxiv.org/abs/1904.08779

<a id="verhoeven2019-visualisation-analysis-epg"></a>
### Visualisation and Analysis of Speech Production with Electropalatography

#### Basic Info

- **paper_id**: verhoeven2019_visualisation_analysis_epg
- **title**: Visualisation and Analysis of Speech Production with Electropalatography
- **authors**: Jo Verhoeven; Naomi Rachel Miller; Luc Daems; Constantino Carlos Reyes-Aldasoro
- **year**: 2019
- **venue**: Journal of Imaging
- **doi**: 10.3390/jimaging5030040
- **primary_url**: https://doi.org/10.3390/jimaging5030040
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: verhoeven2019epgimaging
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Electropalatography (EPG)
- **device**: EPG pseudopalate / electrode contact array (as used in EPG studies)
- **task**: Visualization and analysis methods for EPG-based speech production research
- **output_unit**: visualizations / analysis outputs (paper-specific)
- **vocabulary_setting**: N/A (analysis/visualization focus)
- **datasets**: EPG data used for visualization/analysis examples (see paper for specifics)

#### Protocol & Evaluation

- **evaluation_protocol**: Methodological discussion and illustrative analyses (see paper)
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: Varies by analysis; paper focuses on visualization and analysis techniques
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: N/A
- **model_architecture**: N/A (methodological/analysis paper)
- **spatial_frontend**: EPG inherently provides a spatial contact pattern that can be visualized on palate layouts
- **augmentation**: N/A
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Discusses methods for visualizing and analyzing EPG contact patterns in speech production studies.; Provides context for representing EPG as spatial patterns (palatograms) and motivates explicit spatial modeling assumptions.; Useful background for connecting electrode-layout geometry to analysis and to model front-end design.
- **limitations**: Not an end-to-end decoding benchmark; focuses on visualization/analysis rather than CER/WER-style evaluation.; Specific visualization conventions depend on the EPG hardware/layout used.
- **reported_results_summary**: Methodological/analysis paper; it presents visualization and analysis approaches rather than a single decoding benchmark.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Supports Related Work sections that argue EPG should be treated as spatial data and that geometry/layout assumptions matter, complementing experiments on 2D reconstruction and electrode selection.
- **takeaways_for_related_work_section**: A modern EPG visualization/analysis reference (Journal of Imaging 2019) that can be cited to motivate spatially structured representations (palatograms) and to justify investigating geometry-aware front-ends.
- **gap_or_relevance_to_current_epgspeller_manuscript**: EPG representation/device context. In v2 it supports the manuscript discussion of spatial layout, electrode budget, and device-specific assumptions.

#### Sources

- DOI: 10.3390/jimaging5030040 (academic, retrieved 2026-06-27). https://doi.org/10.3390/jimaging5030040 DOI: 10.3390/jimaging5030040
- Crossref API: 10.3390/jimaging5030040 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.3390/jimaging5030040 DOI: 10.3390/jimaging5030040
- OpenAlex: Visualisation and Analysis of Speech Production with Electropalatography (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.3390/jimaging5030040 DOI: 10.3390/jimaging5030040

<a id="gonzalezlopez2020-ssi-restoration-review"></a>
### Silent Speech Interfaces for Speech Restoration: A Review

#### Basic Info

- **paper_id**: gonzalezlopez2020_ssi_restoration_review
- **title**: Silent Speech Interfaces for Speech Restoration: A Review
- **authors**: - Jose A. Gonzalez-Lopez<br>- Alejandro Gomez-Alanis<br>- Juan M. Martin Donas<br>- Jose L. Perez-Cordoba<br>- Angel M. Gomez
- **year**: 2020
- **venue**: IEEE Access
- **doi**: 10.1109/access.2020.3026579
- **primary_url**: https://ieeexplore.ieee.org/document/9205294/
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: gonzalezlopez2020ssi
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Survey / review (Silent Speech Interfaces, SSI)
- **device**: N/A (review of multiple devices and sensing modalities)
- **task**: Silent Speech Interfaces for speech restoration (speech reconstruction / communication without audible speech)
- **output_unit**: N/A (review; varies by system, e.g., speech or text)
- **vocabulary_setting**: N/A (review; varies by system/protocol)
- **datasets**: N/A (review; summarizes multiple datasets across modalities)

#### Protocol & Evaluation

- **evaluation_protocol**: N/A (review; summarizes multiple evaluation protocols)
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Multi-participant or cross-participant behavior is discussed in the source-specific protocol; exact comparability depends on the paper definition.
- **metrics_reported**: N/A (review; discusses metrics used in SSI literature)
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: Varies by modality (review; e.g., HMM/DNN/CTC/seq2seq depending on system)
- **model_architecture**: Varies (review; includes classical and deep-learning approaches depending on sensing modality)
- **spatial_frontend**: Varies (review; modality-specific front-ends, including spatial encoders for imaging/arrays)
- **augmentation**: Varies / not consistently standardized across SSI literature
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant as non-EPG SSI or method context; transfer/adaptation evidence should not be extrapolated to EPG without matched data.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Surveys Silent Speech Interfaces with a focus on speech restoration, covering sensing modalities, system pipelines, and challenges.; Provides a modality-centric organization useful for positioning EPG-based silent spelling within the broader SSI landscape.; Highlights practical issues (sensing variability, usability, robustness) that directly motivate systematic protocol reporting.
- **limitations**: As a review, it does not define a single standardized benchmark; comparisons across modalities remain protocol-dependent.; Focus is on speech restoration; open-vocabulary silent spelling/text-entry is not the sole emphasis.
- **reported_results_summary**: Review paper; it synthesizes prior results and challenges rather than reporting a single unified benchmark.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Provides a recent SSI survey for positioning and for motivating why EPG-based silent spelling must be evaluated with protocol-aware comparisons (lexicon constraints, open-vocabulary settings, robustness).
- **takeaways_for_related_work_section**: A modern SSI review (IEEE Access 2020) that can be cited to define SSI scope and challenges, and to position EPG-based open-vocabulary silent spelling among other speech-restoration modalities.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- IEEE Xplore: Silent Speech Interfaces for Speech Restoration: A Review (academic, retrieved 2026-06-27). https://ieeexplore.ieee.org/document/9205294/ DOI: 10.1109/access.2020.3026579
- DOI: 10.1109/ACCESS.2020.3026579 (academic, retrieved 2026-06-27). https://doi.org/10.1109/ACCESS.2020.3026579 DOI: 10.1109/access.2020.3026579
- Crossref API: 10.1109/access.2020.3026579 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.1109/access.2020.3026579 DOI: 10.1109/access.2020.3026579

<a id="lee2021-biosignal-speechrec-review"></a>
### Biosignal Sensors and Deep Learning-Based Speech Recognition: A Review

#### Basic Info

- **paper_id**: lee2021_biosignal_speechrec_review
- **title**: Biosignal Sensors and Deep Learning-Based Speech Recognition: A Review
- **authors**: - Wookey Lee<br>- Jessica Jiwon Seong<br>- Busra Ozlu<br>- Bong Sup Shim<br>- Azizbek Marakhimov<br>- Suan Lee
- **year**: 2021
- **venue**: Sensors
- **doi**: 10.3390/s21041399
- **primary_url**: https://doi.org/10.3390/s21041399
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: lee2021biosignalreview
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Survey / review (biosignal-based speech recognition)
- **device**: N/A (review of multiple biosignal sensors and setups)
- **task**: Speech recognition from biosignals using deep learning (review)
- **output_unit**: N/A (review; varies by system, e.g., phonemes/words/characters)
- **vocabulary_setting**: N/A (review; varies by dataset and system)
- **datasets**: N/A (review; summarizes multiple datasets and sensing modalities)

#### Protocol & Evaluation

- **evaluation_protocol**: N/A (review; summarizes multiple evaluation protocols)
- **protocol_generalization**: Survey or review item; protocol content is taxonomy-level rather than a benchmark result.
- **participant_generalization**: Multi-participant or cross-participant behavior is discussed in the source-specific protocol; exact comparability depends on the paper definition.
- **metrics_reported**: N/A (review; discusses metrics used across studies)
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: Varies (review; depending on modality and task formulation)
- **model_architecture**: Varies (review; emphasizes deep learning approaches for biosignal-based speech recognition)
- **spatial_frontend**: Varies (review; includes modality-specific spatial/array handling when applicable)
- **augmentation**: Varies (review; augmentation policies are not standardized across modalities)
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant as non-EPG SSI or method context; transfer/adaptation evidence should not be extrapolated to EPG without matched data.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Reviews biosignal sensors and deep-learning approaches for speech recognition, providing a modality-level overview beyond acoustics.; Useful high-level reference to contextualize EPG as one biosignal modality among many, and to motivate why spatial modeling and robustness are recurring themes.; Summarizes challenges common to biosignal speech recognition (variability, limited data, sensor reliability) that map to EPGSpeller experimental axes (robustness, augmentation, sensor design).
- **limitations**: Broad scope; individual modality-specific details may be covered at different depths.; Does not provide a unified benchmark; cross-paper comparisons remain protocol-dependent.
- **reported_results_summary**: Review paper; it synthesizes prior results rather than reporting a single unified benchmark.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Provides additional context and vocabulary for positioning EPG-based decoding within the broader biosignal+DL speech recognition literature, supporting the motivation for spatial front-ends and robustness evaluations.
- **takeaways_for_related_work_section**: A broad biosignal+DL review (Sensors 2021) that can be cited for general challenges and trends in biosignal-based speech recognition, complementing SSI-focused surveys when motivating robustness and representation choices for EPG.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- DOI: 10.3390/s21041399 (academic, retrieved 2026-06-27). https://doi.org/10.3390/s21041399 DOI: 10.3390/s21041399
- Crossref API: 10.3390/s21041399 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.3390/s21041399 DOI: 10.3390/s21041399
- OpenAlex: Biosignal Sensors and Deep Learning-Based Speech Recognition: A Review (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.3390/s21041399 DOI: 10.3390/s21041399

<a id="woo2021-kepg-design"></a>
### Design and Evaluation of Korean Electropalatography (K-EPG)

#### Basic Info

- **paper_id**: woo2021_kepg_design
- **title**: Design and Evaluation of Korean Electropalatography (K-EPG)
- **authors**: - Seong-Tak Woo<br>- Ji-Wan Ha<br>- Sungdae Na<br>- Hyunjoo Choi<br>- Sung-Bom Pyun
- **year**: 2021
- **venue**: Sensors
- **doi**: 10.3390/s21113802
- **primary_url**: https://doi.org/10.3390/s21113802
- **pdf_url**: N/A
- **code_or_data_release**: N/A
- **citation_key_suggestion**: woo2021kepg
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Electropalatography (EPG) device / instrumentation
- **device**: K-EPG (Korean Electropalatography) system as described in the paper
- **task**: Design and evaluation of an EPG system (hardware + measurement validation)
- **output_unit**: EPG contact measurements (electrode contact patterns)
- **vocabulary_setting**: N/A (device/instrumentation focus)
- **datasets**: Device evaluation measurements as reported (see paper for specifics)

#### Protocol & Evaluation

- **evaluation_protocol**: Device design and evaluation protocol as reported (see paper)
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: Device/system evaluation metrics as reported (paper-specific)
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: N/A
- **model_architecture**: N/A
- **spatial_frontend**: EPG electrode layout and contact-pattern representation (device-defined)
- **augmentation**: N/A
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Describes the design and evaluation of a Korean EPG system (K-EPG), contributing to the diversity of EPG device designs and layouts.; Provides relevant context for sensor design constraints (electrode layouts, manufacturing, evaluation) that influence modeling assumptions.; Useful for discussing that EPG layouts are device-specific and that electrode selection/design questions are meaningful.
- **limitations**: Not an end-to-end decoding benchmark; focuses on device design and evaluation rather than CER/WER-style metrics.; Conclusions may be tied to the specific K-EPG hardware and evaluation setup.
- **reported_results_summary**: Device/instrumentation paper; reports design and evaluation results specific to K-EPG (see DOI/Crossref sources).

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Supports Related Work on EPG device diversity and electrode-layout considerations, providing context for electrode selection and spatial front-end assumptions.
- **takeaways_for_related_work_section**: A modern EPG device paper (Sensors 2021) that can be cited to emphasize that electrode layouts/devices vary and that sensor design (layout, coverage) is an explicit dimension in EPG-based decoding systems.
- **gap_or_relevance_to_current_epgspeller_manuscript**: EPG representation/device context. In v2 it supports the manuscript discussion of spatial layout, electrode budget, and device-specific assumptions.

#### Sources

- DOI: 10.3390/s21113802 (academic, retrieved 2026-06-27). https://doi.org/10.3390/s21113802 DOI: 10.3390/s21113802
- Crossref API: 10.3390/s21113802 (web, retrieved 2026-06-27). https://api.crossref.org/works/10.3390/s21113802 DOI: 10.3390/s21113802
- OpenAlex: Design and Evaluation of Korean Electropalatography (K-EPG) (web, retrieved 2026-06-27). https://api.openalex.org/works/https://doi.org/10.3390/s21113802 DOI: 10.3390/s21113802

<a id="chen2022-epg2s"></a>
### EPG2S: Speech Generation and Speech Enhancement based on Electropalatography and Audio Signals using Multimodal Learning

#### Basic Info

- **paper_id**: chen2022_epg2s
- **title**: EPG2S: Speech Generation and Speech Enhancement based on Electropalatography and Audio Signals using Multimodal Learning
- **authors**: Li-Chin Chen; Po-Hsun Chen; Richard Tzong-Han Tsai; Yu Tsao
- **year**: 2022
- **venue**: arXiv (2206.07860) / ICASSP 2023 presentation material
- **doi**: N/A
- **primary_url**: https://arxiv.org/abs/2206.07860
- **pdf_url**: https://arxiv.org/pdf/2206.07860.pdf
- **code_or_data_release**: N/A
- **citation_key_suggestion**: chen2022epg2s
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Electropalatography (EPG) + audio (multimodal learning)
- **device**: EPG sensing + audio recording (as reported in the paper)
- **task**: Articulatory-to-speech generation and speech enhancement using EPG (multimodal)
- **output_unit**: speech waveform / enhanced speech (via learned mapping)
- **vocabulary_setting**: N/A (speech generation/enhancement task)
- **datasets**: EPG+audio dataset described in the paper

#### Protocol & Evaluation

- **evaluation_protocol**: Objective/subjective speech quality/intelligibility evaluation as reported in the paper
- **protocol_generalization**: Protocol is paper-specific; v2 report treats it as contextual unless split/metric definitions align with EPGSpeller.
- **participant_generalization**: Not a participant-generalization benchmark; use for modality, method, or representation context.
- **metrics_reported**: Speech generation/enhancement metrics reported in the paper (see sources)
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: Neural multimodal fusion strategies (early/late fusion variants as evaluated)
- **model_architecture**: Multimodal deep learning model for EPG-to-speech generation/enhancement
- **spatial_frontend**: EPG is used as an articulatory modality; internal representation details are paper-specific
- **augmentation**: Not central; paper focuses on fusion strategies and multimodal learning
- **language_model_or_postprocessing**: No v2-specific language-model or postprocessing mechanism was added beyond the original survey extraction.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Proposes an EPG-to-speech generation/enhancement system using multimodal learning.; Evaluates fusion strategies combining EPG with noisy speech signals and shows EPG contributes to quality/intelligibility.; Highlights that EPG has been underexplored compared to other articulatory modalities for speech generation tasks.
- **limitations**: Task differs from text decoding (silent spelling); results do not directly translate to CER/WER.; Reproducibility depends on access to EPG+audio datasets and hardware.; Model details and performance are tied to the dataset and fusion setup used.
- **reported_results_summary**: The paper reports that EPG-only can generate speech with desirable outcomes and that adding EPG to noisy audio improves enhancement; see arXiv/IEEE presentation sources for details.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Demonstrates EPG as a useful articulatory signal for learned speech mapping, supporting the motivation to explore richer spatial front-ends (H11–H13) and robustness/augmentation ideas for EPG-based decoding.
- **takeaways_for_related_work_section**: EPG2S shows that EPG provides informative articulatory cues for neural speech generation/enhancement; it supports the broader claim that EPG can be a strong input modality beyond clinical visualization and motivates learning-based front-ends.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Seeded from the frozen 2026-02-17 survey; v2 uses this item to preserve the original EPG-centered baseline while adding protocol/audit/transfer lenses for the current manuscript.

#### Sources

- arXiv: EPG2S: Speech Generation and Speech Enhancement based on Electropalatography and Audio Signals using Multimodal Learning (academic, retrieved 2026-06-27). https://arxiv.org/abs/2206.07860
- arXiv PDF: EPG2S (2206.07860) (academic, retrieved 2026-06-27). https://arxiv.org/pdf/2206.07860.pdf
- IEEE Resource Center (ICASSP 2023): EPG2S presentation material (web, retrieved 2026-06-27). https://resourcecenter.ieee.org/conferences/icassp-2023/spsicassp23vid2694

<a id="silentspeller-chi2022"></a>
### SilentSpeller: Towards mobile, hands-free, silent speech text entry using electropalatography

#### Basic Info

- **paper_id**: silentspeller_chi2022
- **title**: SilentSpeller: Towards mobile, hands-free, silent speech text entry using electropalatography
- **authors**: - Naoki Kimura<br>- Tan Gemicioglu<br>- Jonathan Womack<br>- Richard Li<br>- Yuhui Zhao<br>- Abdelkareem Bedri<br>- Zixiong Su<br>- Alex Olwal<br>- Jun Rekimoto<br>- Thad Starner
- **year**: 2022
- **venue**: CHI 2022 (ACM CHI Conference on Human Factors in Computing Systems)
- **doi**: 10.1145/3491102.3502015
- **primary_url**: https://dl.acm.org/doi/10.1145/3491102.3502015
- **pdf_url**: https://dl.acm.org/doi/pdf/10.1145/3491102.3502015
- **code_or_data_release**: N/A
- **citation_key_suggestion**: kimura2022silentspeller
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: EPG (electropalatography; intra-oral palate contact sensing)
- **device**: Intra-oral dental retainer with palate-contact sensing (SmartPalate-like EPG form factor)
- **task**: Silent spelling / silent speech text entry
- **output_unit**: characters (letters), aggregated to words
- **vocabulary_setting**: open-vocabulary silent spelling with held-out (unseen) words evaluation
- **datasets**: EPG text-entry dataset described in the paper

#### Protocol & Evaluation

- **evaluation_protocol**: The paper reports offline evaluations and includes an unseen-word generalization setting; see the official paper for exact split definitions.
- **protocol_generalization**: Includes or motivates compositional/open-vocabulary or held-out-word evaluation; still not directly leaderboard-comparable without matched splits and metrics.
- **participant_generalization**: Primarily source-specific; use only as a task anchor unless the paper explicitly reports cross-user/user-independent evaluation.
- **metrics_reported**: Character/word-level accuracy/error rates and text-entry metrics (see paper).
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: CTC-based sequence decoding (details in the paper)
- **model_architecture**: Deep sequence model trained with CTC (details in the paper)
- **spatial_frontend**: Multi-channel EPG time series (no explicit 2D reconstruction in the baseline description)
- **augmentation**: See paper (augmentation/robustness details are paper-specific)
- **language_model_or_postprocessing**: Character-level silent spelling anchor; compare decoding constraints carefully and avoid mixing lexicon/word-prediction effects with sensor decoding.
- **transfer_or_adaptation_method**: Relevant to EPG spatial/device representation; transfer/adaptation is not necessarily evaluated unless stated in the original item.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: EPG-based wearable silent spelling text-entry system for mobile, hands-free scenarios.; Unseen-word generalization via letter-level composition (silent spelling).; Evaluation beyond isolated words (e.g., phrase entry and walking robustness).
- **limitations**: Requires a custom intra-oral device and user-specific fit.; Performance depends on sensor fit and intra-oral conditions.; Cross-study comparisons require careful protocol alignment (lexicon size, unseen-word setting, etc.).
- **reported_results_summary**: The paper reports protocol-specific character/word-level results including an unseen-word evaluation; see the ACM DL paper for exact numbers and definitions.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Directly relevant EPG silent spelling/text entry system; a key horizontal comparison point for positioning open-vocabulary silent spelling with palate-contact sensing.
- **takeaways_for_related_work_section**: SilentSpeller (CHI 2022) is a primary EPG-based silent spelling system demonstrating wearable text entry and unseen-word generalization via letter-by-letter composition; it anchors the EPG silent spelling related-work discussion.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Direct EPG silent spelling anchor. In v2 it supports positioning EPGSpeller as a protocol-audited benchmark rather than a claim of a single cross-paper CER leaderboard.

#### Sources

- ACM Digital Library: SilentSpeller: Towards mobile, hands-free, silent speech text entry using electropalatography (academic, retrieved 2026-06-27). https://dl.acm.org/doi/10.1145/3491102.3502015 DOI: 10.1145/3491102.3502015
- DOI: 10.1145/3491102.3502015 (academic, retrieved 2026-06-27). https://doi.org/10.1145/3491102.3502015 DOI: 10.1145/3491102.3502015
- DBLP: SilentSpeller: Towards mobile, hands-free, silent speech text entry using electropalatography (web, retrieved 2026-06-27). https://dblp.org/rec/conf/chi/KimuraGWLZBSORS22 DOI: 10.1145/3491102.3502015

<a id="rehearsse-chi2024"></a>
### ReHEarSSE: Recognizing Hidden-in-the-Ear Silently Spelled Expressions

#### Basic Info

- **paper_id**: rehearsse_chi2024
- **title**: ReHEarSSE: Recognizing Hidden-in-the-Ear Silently Spelled Expressions
- **authors**: - Xuefu Dong<br>- Yifei Chen<br>- Yuuki Nishiyama<br>- Kaoru Sezaki<br>- Yuntao Wang<br>- Ken Christofferson<br>- Alex Mariakakis
- **year**: 2024
- **venue**: CHI 2024 (ACM CHI Conference on Human Factors in Computing Systems)
- **doi**: 10.1145/3613904.3642095
- **primary_url**: https://dl.acm.org/doi/10.1145/3613904.3642095
- **pdf_url**: https://dl.acm.org/doi/pdf/10.1145/3613904.3642095
- **code_or_data_release**: N/A
- **citation_key_suggestion**: dong2024rehearsse
- **coverage_origin**: seeded_from_frozen_related_work_survey_2026-02-17

#### Task & Data

- **modality**: Ultrasonic ear-canal sensing (earbud-based SSI)
- **device**: Earbud form factor with ultrasonic sensing
- **task**: Silent spelling / silently spelled word recognition
- **output_unit**: characters/letters aggregated to words
- **vocabulary_setting**: includes unseen-word generalization (see paper)
- **datasets**: Ear-canal ultrasonic silent spelling dataset described in the paper

#### Protocol & Evaluation

- **evaluation_protocol**: Participant/session splits; includes unseen-word evaluation (see paper)
- **protocol_generalization**: Includes or motivates compositional/open-vocabulary or held-out-word evaluation; still not directly leaderboard-comparable without matched splits and metrics.
- **participant_generalization**: Primarily source-specific; use only as a task anchor unless the paper explicitly reports cross-user/user-independent evaluation.
- **metrics_reported**: Character/word-level accuracy/error rates and system-level comparisons (see paper)
- **benchmark_or_audit_status**: Prior-work item from the frozen survey; not an EPGSpeller artifact. Sources are preserved and reprocessed in v2 for bibliography/audit consistency.
- **leakage_or_constraint_notes**: Use this item only under its own vocabulary/decoder constraints; EPGSpeller should keep greedy CER, lexicon projection, and LM/LLM assistance separated.

#### Methods

- **decoder**: CTC-based modeling (paper describes intermediate embeddings and CTC-based recognition)
- **model_architecture**: Deep learning sequence model trained with CTC (details in the paper)
- **spatial_frontend**: Not applicable to EPG; ultrasonic sensing features are modeled as sequences
- **augmentation**: Paper describes synthetic/regularization augmentations for training (see paper)
- **language_model_or_postprocessing**: Character-level silent spelling anchor; compare decoding constraints carefully and avoid mixing lexicon/word-prediction effects with sensor decoding.
- **transfer_or_adaptation_method**: Relevant as non-EPG SSI or method context; transfer/adaptation evidence should not be extrapolated to EPG without matched data.

#### Auditability

- **source_quality_notes**: Seed item retained from the 2026-02-17 survey; sources include DOI/publisher/index records where available.
- **reproducibility_artifacts**: No v2-confirmed code/data artifact beyond cited publisher/index pages.
- **evidence_retrieved_at**: 2026-06-27

#### Claims

- **key_contributions**: Earbud-based ultrasonic SSI for silent spelling with large-vocabulary and unseen-word generalization.; CTC-based modeling tailored to silently spelled letter transitions.; Provides a modern non-EPG silent spelling baseline for positioning open-vocabulary silent spelling systems.
- **limitations**: Modality differs from EPG; comparisons to EPG require careful protocol alignment.; Wearability and robustness depend on earbud fit and acoustic environment.; Letter-by-letter spelling may limit entry speed (inherent trade-off).
- **reported_results_summary**: The paper reports unseen-word recognition performance and includes comparative tables against prior SSI systems; consult ACM DL for exact definitions and results.

#### Relevance to EPGSpeller

- **relevance_to_epgspeller**: Minimal SSI comparison for open-vocabulary silent spelling beyond EPG; resolves the ICASSP review mention of ReHEarSSE and helps contextualize EPGSpeller in silent spelling literature.
- **takeaways_for_related_work_section**: ReHEarSSE (CHI 2024) demonstrates silent spelling via earbud ultrasonic sensing and CTC-based modeling with unseen-word generalization; it is a key non-EPG reference for positioning open-vocabulary silent spelling in wearable SSI.
- **gap_or_relevance_to_current_epgspeller_manuscript**: Open-vocabulary non-EPG silent spelling anchor. In v2 it sharpens the distinction between task similarity and protocol comparability.

#### Sources

- ACM Digital Library: ReHEarSSE: Recognizing Hidden-in-the-Ear Silently Spelled Expressions (academic, retrieved 2026-06-27). https://dl.acm.org/doi/10.1145/3613904.3642095 DOI: 10.1145/3613904.3642095
- DOI: 10.1145/3613904.3642095 (academic, retrieved 2026-06-27). https://doi.org/10.1145/3613904.3642095 DOI: 10.1145/3613904.3642095
- DBLP: ReHEarSSE: Recognizing Hidden-in-the-Ear Silently Spelled Expressions (web, retrieved 2026-06-27). https://dblp.org/rec/conf/chi/DongCNS0CM24 DOI: 10.1145/3613904.3642095
