% Related work survey search log (EPGSpeller)
% Date: 2026-02-17

# Search Log — related_work_survey_epgspeller_2026-02-17

This file records the literature search actions actually performed for this survey. The goal is to reduce omissions via systematic queries + citation chaining. This log is not a proof of completeness.

## Inclusion / Exclusion criteria (operational)

**Include (EPG-centered)**
- Electropalatography (EPG / SmartPalate / palate contact) used for silent spelling/text entry, or for learned decoding/mapping tasks where EPG is a central input/output modality.
- Work directly informing EPG representation (dimensionality reduction, explicit spatial modeling, geometry-aware visualization) and sensor/layout design questions (data reduction, layout/device design).

**Include (minimal non-EPG SSI comparisons)**
- Silent spelling/text-entry systems in other modalities (e.g., ultrasonic ear-canal SSI) that are commonly compared in open-vocabulary silent spelling discussions.
- Canonical SSI surveys that provide shared terminology and a modality taxonomy.

**Exclude (unless seminal for EPG instrumentation context)**
- Clinical-only EPG therapy papers without an automatic decoding/mapping component (kept out of the main list unless needed as foundational background).

## Note on databases

- Semantic Scholar API search returned HTTP 429 (rate limit) during this session, so discovery was performed primarily with **Crossref** and **OpenAlex**, then verified via **DOI/ISCA/ACM/Springer** primary pages.
- Google Scholar was not used programmatically (terms-of-service constraints). The survey relies on DOI-based and publisher-indexed records for auditability.

## Queries and outcomes (high-level)

### Crossref API — discovery & DOI confirmation

1) Query: `electropalatography speech recognition`
- Top hits (examples): various EPG clinical/tool papers; **Hardcastle 1990** appeared with DOI `10.21437/icslp.1990-305`.
- Action: Added DOI to `hardcastle1990_epg_phonetic_research.json` and replaced non-primary sources with ISCA/DOI/Crossref sources.

2) Query: `Depth measurement of face and palate by structured light Shadle`
- Top hit: Shadle et al. 1993 with DOI `10.21437/eurospeech.1993-403`.
- Action: Added DOI + ISCA PDF URL; removed Wikipedia source.

3) Query: `SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition`
- Top hit: Interspeech 2019 DOI `10.21437/interspeech.2019-2680`.
- Action: Switched primary source to ISCA Archive and added DOI/Crossref sources.

4) Query: `EPG data reduction methods and their implications for studies of lingual coarticulation`
- Top hit: Journal of Phonetics DOI `10.1016/S0095-4470(19)30343-2`.
- Action: Added as a sensor/layout-relevant representation baseline (`hardcastle1991_epg_data_reduction_coarticulation.json`).

5) Query: `Learning Electropalatograms from Acoustics`
- Top hit: ICASSP DOI `10.1109/ICASSP.2006.1660032`.
- Action: Added as articulatory modeling context (`toutios2006_learning_epg_from_acoustics.json`).

### OpenAlex — discovery (broad) and cross-checking

1) Search: `electropalatography electrode number` / `electropalatography electrode reduction`
- Notable hits: K-EPG device paper (Sensors 2021 DOI `10.3390/s21113802`), EPG data reduction (1991 DOI above).
- Action: Added `woo2021_kepg_design.json` and `hardcastle1991_epg_data_reduction_coarticulation.json`.

2) Search: `EPG electropalatography machine learning`
- Notable hit: Journal of Imaging 2019 DOI `10.3390/jimaging5030040`.
- Action: Added `verhoeven2019_visualisation_analysis_epg.json`.

3) Search: `electropalatography silent speech recognition`
- Notable hit: IEEE Access 2020 SSI review DOI `10.1109/access.2020.3026579`.
- Action: Added `gonzalezlopez2020_ssi_restoration_review.json`.

4) Search: `electropalatography speech recognition`
- Notable hit: Sensors 2021 biosignal+DL speech recognition review DOI `10.3390/s21041399`.
- Action: Added `lee2021_biosignal_speechrec_review.json`.

### DBLP — targeted verification (non-EPG SSI comparison)

1) Query: `ReHEarSSE`
- Result: DBLP record `https://dblp.org/rec/conf/chi/DongCNS0CM24` with DOI `10.1145/3613904.3642095`.
- Action: Replaced a non-primary index page source with DBLP in `rehearsse_chi2024.json`.

## Remaining gaps / next search iteration (not executed in this session)

- Systematic backward/forward citation chaining for **SilentSpeller (CHI 2022)** and **EPG representation papers** (depth=2) was not exhaustively executed here.
- If the paper requires stronger coverage of **EPG-to-phoneme/text decoding** beyond SilentSpeller-style text entry, run a dedicated search iteration focusing on "EPG recognition / phone classification / CNN palatogram" and add any decoding-focused EPG papers that meet inclusion criteria.
