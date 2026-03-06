# ev_config_outline_yaml

- kind: `config_snapshot`
- path: `results/related_work_survey_epgspeller_2026-02-17/outline.yaml`
- sha256: `90e6a179b29cca1331e7613fce62e3c1529fca96c12bc7dbd81112fc1f642fa8`
- size_bytes: 3575
- root_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- abs_path_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/results/related_work_survey_epgspeller_2026-02-17/outline.yaml`

## Excerpt

```yaml
topic: "Related work survey for EPGSpeller (EPG-based open-vocabulary silent spelling)"
items:
  - paper_id: "silentspeller_chi2022"
    seed: true
    notes: "Seed: EPG text entry using electropalatography (SilentSpeller)."
  - paper_id: "ssi_book_springer2017"
    seed: true
    notes: "Seed: SSI overview book; used for positioning and modality taxonomy."
  - paper_id: "rehearsse_chi2024"
    seed: true
    notes: "Seed: Review-mentioned ReHEarSSE identified as CHI 2024 earbud ultrasonic SSI silent spelling paper."
  - paper_id: "denby2010_silent_speech_interfaces"
    seed: false
    notes: "Canonical SSI survey paper (Speech Communication 2010) for positioning and terminology."
  - paper_id: "gonzalezlopez2020_ssi_restoration_review"
    seed: false
    notes: "Recent SSI review (IEEE Access 2020) focused on speech restoration."
  - paper_id: "lee2021_biosignal_speechrec_review"
    seed: false
    notes: "Broad biosignal+DL speech recognition review (Sensors 2021) for general challenges/positioning."
  - paper_id: "hueber2010_ultrasound_optical_ssi"
    seed: false
    notes: "Representative ultrasound+video SSI system (Speech Communication 2010 special issue)."
  - paper_id: "gilbert2010_magnetic_implants_silent_speech"
    seed: false
    notes: "Representative articulator-sensing SSI (magnetic implants) for minimal non-EPG comparison."
  - paper_id: "graves2006_ctc"
    seed: false
    notes: "Foundational CTC method paper for alignment-free sequence decoding."
  - paper_id: "park2019_specaugment"
    seed: false
    notes: "Widely used feature-level augmentation method used to motivate robustness/augmentation choices."
  - paper_id: "hardcastle1989_state_of_art_epg"
    seed: false
    notes: "Foundational EPG state-of-the-art report (instrumentation/representation context)."
  - paper_id: "hardcastle1990_epg_phonetic_research"
    seed: false
    notes: "Foundational EPG usage paper (phonetic research / training)."
  - paper_id: "shadle1993_epg_structured_light"
    seed: false
    notes: "EPG-related geometry measurement/visualization infrastructure (structured light)."
  - paper_id: "carreira_perpinan1998_dimred_epg"
    seed: false
    notes: "EPG representation/dimensionality reduction using latent variable models."
  - paper_id: "hardcastle1991_epg_data_reduction_coarticulation"
    seed: false
    notes: "EPG data reduction methods and implications for information preservation (sensor/representation)."
  - paper_id: "verhoeven2019_visualisation_analysis_epg"
    seed: false
    notes: "Modern EPG visualization and analysis reference (spatial representation motivation)."
  - paper_id: "toutios2006_learning_epg_from_acoustics"
    seed: false
    notes: "Acoustic-to-EPG mapping (ICASSP 2006) for articulatory modeling context."
  - paper_id: "toutios2006_acoustic_to_epg_mapping"
    seed: false
    notes: "Acoustic-to-EPG mapping (LNCS 2006 book chapter) for representation/mapping context."
  - paper_id: "woo2021_kepg_design"
    seed: false
    notes: "EPG device design and evaluation (K-EPG; Sensors 2021) for sensor-layout context."
  - paper_id: "chen2022_epg2s"
    seed: false
    notes: "EPG+audio multimodal learning for speech generation/enhancement (EPG as modality context)."
execution:
  batch_size: 4
  items_per_agent: 1
  output_dir: "./results"
  validation:
    require_all_fields: true
    require_sources: true
    min_sources: 3
  bibliography:
    format: bibtex
    scope: papers
    out_bib: "./references.bib"
    out_json: "./references.json"
    out_audit: "./references_audit.md"
```
