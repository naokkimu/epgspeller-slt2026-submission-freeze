# Related Work (EPG-centered survey up to 2026-02-17)

This document is a paper-ready Related Work draft for **EPGSpeller: open-vocabulary silent spelling with electropalatography (EPG)**. It is intentionally **EPG-centered**, with **minimal non-EPG SSI comparisons** used only for positioning and protocol context. References are provided via `references.bib`.

## 1. Silent Speech Interfaces (SSI): positioning and modalities (brief)

Silent Speech Interfaces (SSI) aim to restore communication when audible speech is unavailable or undesirable by decoding speech-related information from non-acoustic signals. Canonical SSI surveys define the scope, modality taxonomy, and recurring challenges such as sensing variability, limited data, and evaluation protocol mismatches across systems. \\cite{denby2010silent,freitas2017an,gonzalez2020silent,lee2021biosignal}

SSI modalities include articulatory sensing (e.g., ultrasound tongue imaging, magnetic sensing of articulator motion) and other biosignals. Representative systems and reviews illustrate that **system-level comparisons are highly protocol-dependent** (vocabulary constraints, subject dependence, and session variability), which motivates careful positioning of EPG-based silent spelling within SSI. \\cite{denby2010silent,hueber2010development,gilbert2010isolated,gonzalez2020silent}

For **open-vocabulary silent spelling**, recent wearable SSI work outside EPG (e.g., ultrasonic ear-canal sensing) provides a useful minimal comparison point for the task framing and decoding formulation. \\cite{dong2024rehearsse}

## 2. Electropalatography (EPG) for silent speech / text entry

EPG measures **tongue–palate contact patterns** via an intra-oral pseudopalate instrumented with electrodes. Foundational EPG work and instrumentation reports describe what EPG captures (contact-only, palate-limited) and how palatograms are represented/visualized. \\cite{hardcastle1989new,hardcastle1990electropalatography,verhoeven2019visualisation}

Modern EPG systems and layouts are device-specific, motivating explicit discussion of electrode layouts and design constraints when comparing models or proposing reduced-electrode designs. \\cite{woo2021design,verhoeven2019visualisation}

Within SSI tasks, **EPG-based silent spelling / text entry** is exemplified by SilentSpeller (CHI 2022), which demonstrates wearable EPG-based text entry and an unseen-word generalization setting via letter-level decoding. \\cite{kimura2022silentspeller}

Beyond direct text entry, EPG has also been used as an articulatory modality in multimodal learning for speech generation/enhancement, underscoring that EPG can provide informative cues for learned mappings (even when the task is not text decoding). \\cite{a8287fa9}

## 3. Decoding formulations: open-vocabulary vs constrained decoding (CTC/LM/lexicon)

Many modern sensor-to-sequence decoders use alignment-free objectives such as Connectionist Temporal Classification (CTC), enabling label-sequence decoding from unsegmented time series. \\cite{graves2006connectionist}

Open-vocabulary silent spelling is naturally framed as **character-level sequence decoding** (often CTC-style), enabling composition into unseen words when evaluation includes held-out lexicon items. SilentSpeller and ReHEarSSE are representative open-vocabulary silent spelling systems that motivate this formulation. \\cite{kimura2022silentspeller,dong2024rehearsse,graves2006connectionist}

In contrast, many SSI pipelines (especially earlier work) employ **strong constraints** (isolated-word recognition, dictionary constraints, or multi-stage pipelines) to manage ambiguity and limited data. These constrained settings are important to cite and distinguish from open-vocabulary silent spelling when discussing fairness of comparisons and the need for protocol clarity. \\cite{hueber2010development,gilbert2010isolated,denby2010silent}

## 4. Spatial modeling of EPG (2D reconstruction, CNN/other front-ends)

EPG is intrinsically spatial: each frame is a contact pattern over an electrode layout, and palatogram-style visualizations emphasize the underlying geometry. Geometry-aware instrumentation and visualization work further motivate treating EPG as structured spatial data rather than an unordered feature vector. \\cite{shadle1993depth,hardcastle1989new,verhoeven2019visualisation}

A long-standing approach is to **compress or reduce** EPG dimensionality via learned or statistical latent-variable models, including comparisons of linear vs nonlinear reductions. Such work motivates explicit evaluation of representation choices and their information trade-offs. \\cite{carreira1998dimensionality,hardcastle1991epg}

Related articulatory modeling work also treats EPG as a structured output for supervised mapping (e.g., acoustic-to-EPG prediction), which supports the view that palatograms can be modeled with structured inductive biases and that representation choices matter. \\cite{toutios2006learning,toutios2006on}

## 5. Robustness and augmentation for sensor-based decoding (incl. missing electrodes)

SSI surveys repeatedly emphasize robustness challenges arising from sensor placement variability, session drift, and device-specific noise characteristics. These challenges motivate both augmentation strategies and explicit robustness evaluations. \\cite{denby2010silent,gonzalez2020silent,lee2021biosignal}

Feature-level masking augmentation (SpecAugment) is a widely used method in end-to-end ASR and is often adapted as a conceptual baseline for time-series modalities where structured corruption (masking, dropout) can improve generalization. \\cite{park2019specaugment}

For wearable silent spelling systems, robustness considerations (e.g., movement, fit variability) further motivate protocol design and evaluation beyond clean, static settings. \\cite{kimura2022silentspeller,dong2024rehearsse}

## 6. Sensor design & electrode selection (importance/coverage; closest prior work)

EPG device/layout diversity implies that electrode geometry and coverage are not incidental implementation details; they shape what spatial information is available and how models should be compared. Device-focused work (e.g., K-EPG) and EPG visualization/analysis references support this framing. \\cite{woo2021design,verhoeven2019visualisation,hardcastle1989new}

Prior EPG research also explicitly addresses **data reduction** and representation choices, which provides historical context for modern electrode-selection studies and K-budget curves (how much spatial detail can be removed while preserving performance for a target task). \\cite{hardcastle1991epg,carreira1998dimensionality}

## 7. Gap summary and how EPGSpeller addresses them

Across SSI and EPG literature, several gaps motivate EPGSpeller-style investigations:

1) **Protocol clarity for open-vocabulary silent spelling**: comparisons across constrained vs open-vocabulary settings are not directly interchangeable. \\cite{denby2010silent,gilbert2010isolated,kimura2022silentspeller,dong2024rehearsse}

2) **Spatial inductive bias**: EPG is spatially structured, yet many pipelines reduce it to vectors; prior work on visualization, geometry, and dimensionality reduction suggests representation choices can matter. \\cite{verhoeven2019visualisation,shadle1993depth,carreira1998dimensionality,hardcastle1991epg}

3) **Robustness and augmentation**: SSI surveys highlight sensor variability and noise; principled augmentation and robustness evaluation are needed for wearable deployment. \\cite{gonzalez2020silent,lee2021biosignal,park2019specaugment}

4) **Sensor design questions**: electrode layouts and reductions are meaningful design axes, supported by prior EPG device and data-reduction literature. \\cite{woo2021design,hardcastle1989new,hardcastle1991epg}

EPGSpeller is positioned to address these gaps by reporting protocol-aware open-vocabulary decoding, explicitly evaluating spatial front-ends and reductions, and quantifying robustness/design trade-offs using reproducible evidence files in this repository.

---

## Appendix A. Surveyed papers (summary table)

This is a compact index; for structured per-paper extraction, see `results/*.json`. Citekeys correspond to `references.bib`.

| Paper | Year | Modality | Task (short) | Spatial / representation angle |
|---|---:|---|---|---|
| \\cite{kimura2022silentspeller} | 2022 | EPG | silent spelling text entry | multi-channel EPG time series |
| \\cite{dong2024rehearsse} | 2024 | ultrasonic ear-canal | silent spelling | non-EPG baseline for positioning |
| \\cite{denby2010silent} | 2010 | multi-modality | SSI survey | positioning + challenges |
| \\cite{freitas2017an} | 2017 | multi-modality | SSI book | taxonomy/definitions |
| \\cite{gonzalez2020silent} | 2020 | multi-modality | SSI review | speech restoration focus |
| \\cite{lee2021biosignal} | 2021 | biosignals | review | DL trends + robustness themes |
| \\cite{hardcastle1990electropalatography} | 1990 | EPG | instrumentation / training | what EPG measures |
| \\cite{hardcastle1989new} | 1989 | EPG | state-of-the-art report | instrumentation + representation context |
| \\cite{verhoeven2019visualisation} | 2019 | EPG | visualization/analysis | palatograms, spatial framing |
| \\cite{woo2021design} | 2021 | EPG | device design | layout/device diversity |
| \\cite{hardcastle1991epg} | 1991 | EPG | data reduction | compression + implications |
| \\cite{carreira1998dimensionality} | 1998 | EPG | dim. reduction | latent variable representations |
| \\cite{shadle1993depth} | 1993 | EPG-related | geometry measurement | geometry-aware motivation |
| \\cite{toutios2006learning} | 2006 | audio→EPG | mapping | structured EPG output modeling |
| \\cite{toutios2006on} | 2006 | audio→EPG | mapping | representation/mapping context |
| \\cite{graves2006connectionist} | 2006 | method | CTC | open-vocabulary decoding basis |
| \\cite{park2019specaugment} | 2019 | method | augmentation | masking baseline concept |
| \\cite{gilbert2010isolated} | 2010 | magnetic | silent speech (closed vocab) | constrained decoding (DTW) |
| \\cite{hueber2010development} | 2010 | ultrasound+video | SSI speech reconstruction | spatial coding (PCA) + constraints |
| \\cite{a8287fa9} | 2022 | EPG+audio | EPG-to-speech generation/enhancement | EPG as informative articulatory modality |

## Appendix B. Coverage matrix

See `coverage_matrix.csv` for a machine-readable mapping from paper_id to Related Work sections.
