# ev_positioning_analysis_epgspeller_2026_02_18_report_md

- kind: `document`
- path: `results/positioning_analysis_epgspeller_2026-02-18/report.md`
- sha256: `94f8a086cc48489bf7b1377903b996aca2e7617b25b933cd41c6af8c75ccf356`
- size_bytes: 8557
- root_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- abs_path_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/results/positioning_analysis_epgspeller_2026-02-18/report.md`

## Excerpt

```md
# Positioning Analysis: EPGSpeller in the SSI/EPG spatial landscape (2026-02-18)

This document positions **EPGSpeller** within an **EPG-centered Silent Speech Interface (SSI)** related-work space using a fixed multi-lens taxonomy.
All statements are grounded in repository evidence: the frozen related-work survey exports and the H11–H13 experiment evidence snapshots.

## 1. One-paragraph positioning statement

EPGSpeller is positioned as an **EPG-centered silent spelling/text-entry** study within SSI, focusing on **open-vocabulary character-level decoding** (CTC-style) rather than constrained-vocabulary recognition or speech reconstruction pipelines. Within our frozen survey set, the closest task anchors for open-vocabulary silent spelling are SilentSpeller and ReHEarSSE \cite{kimura2022silentspeller,dong2024rehearsse}, and the decoding formulation is grounded in the CTC objective \cite{graves2006connectionist}.

## 2. Positioning by lens (V1–V6)

### V1: Task / output unit

Within the frozen survey set, silent spelling/text-entry systems are represented by \cite{dong2024rehearsse,kimura2022silentspeller}. Closed-vocabulary SSI recognition is represented by \cite{gilbert2010isolated}. Speech reconstruction/generation pipelines provide a contrasting SSI framing \cite{a8287fa9,hueber2010development}.

### V2: Decoding constraint

Open-vocabulary spelling relies on character-level decoding that can compose unseen words, while several SSI pipelines use stronger lexicon/dictionary constraints. In our frozen survey set, open-vocabulary spelling uses CTC-like decoding \cite{kimura2022silentspeller,dong2024rehearsse,graves2006connectionist}, whereas constrained pipelines appear in ultrasound-based reconstruction systems \cite{hueber2010development}.

### V3: Spatial inductive bias (EPG is spatial; what happens when we exploit layout?)

EPG produces spatial tongue–palate contact patterns whose layout and visualization have been emphasized in foundational and device/visualization work \cite{carreira1998dimensionality,hardcastle1989new,hardcastle1990electropalatography,hardcastle1991epg,shadle1993depth,verhoeven2019visualisation,woo2021design}. Historical EPG representation studies also investigate explicit reduction/compression of contact patterns \cite{hardcastle1991epg,carreira1998dimensionality}.

In our experiments, we directly test whether explicitly reconstructing a 16×16 grid and applying a 2D conv front-end improves over a vector baseline (H11), and whether a geometry-aware row/col compression retains performance (H13). The evidence-grounded results are summarized in Section 3.

### V4: Robustness / augmentation

SSI surveys highlight robustness challenges from sensor variability and noise \cite{denby2010silent,gonzalez2020silent,lee2021biosignal,freitas2017an}. SpecAugment provides a widely used feature-masking augmentation baseline in ASR \cite{park2019specaugment}.

For spatial models, we evaluate a spatial augmentation (block dropout + shift) and quantify its effect on robustness to fixed electrode dropout (H12), summarized in Section 3.

### V5: Sensor design / electrode selection

EPG devices and electrode layouts are device-specific, motivating explicit discussion of layout/design constraints \cite{hardcastle1989new,verhoeven2019visualisation,woo2021design}. Our broader `ed20260217` study (outside this document) focuses on electrode importance and K-budget trade-offs for next-EPG design.

### V6: Protocol / generalization

EPGSpeller is designed with multiple protocols (P1/P2/XSUB) as described in the roadmap, but the H11–H13 spatial analyses in this document are grounded in P1 (seed0–3) evidence only. We do not extrapolate these findings to P2/P3 without additional runs.

## 3. Evidence-grounded spatial findings (H11–H13)

### H11: 16×16 reconstruction + 2D conv front-end vs vector baseline

Evidence snapshot CSV: `results/ed20260217/paperjson/h11_spatial2d_vs_vector_p1_k32_k64_k96_k124_2026-02-17.csv`

| subset_method | K | vec CER | s2d CER | ΔCER(s2d-vec) | vec rtf | s2d rtf |
|---|---:|---:|---:|---:|---:|---:|
| topk | 32 | 0.1399±0.0187 | 0.4885±0.1465 | +0.3485 | 0.0005 | 0.0027 |
| fps2k | 32 | 0.1440±0.0157 | 0.5795±0.3525 | +0.4355 | 0.0005 | 0.0027 |
| topk | 64 | 0.1289±0.0155 | 0.2609±0.0346 | +0.1320 | 0.0005 | 0.0029 |
| fps2k | 64 | 0.1195±0.0118 | 0.3581±0.3556 | +0.2386 | 0.0005 | 0.0028 |
| topk | 96 | 0.1194±0.0200 | 0.2304±0.0405 | +0.1110 | 0.0005 | 0.0028 |
| fps2k | 96 | 0.1137±0.0185 | 0.3438±0.3584 | +0.2301 | 0.0005 | 0.0026 |
| all | 124 | 0.1048±0.0108 | 0.1831±0.0119 | +0.0784 | 0.0005 | 0.0026 |

**Conclusion (H11):** For P1 (seed0–3) across the evaluated settings, the 2D conv front-end (spatial2d) yields **higher** greedy test CER than the vector baseline, and also incurs **higher** streaming RTF. Therefore, under this implementation and dataset protocol, explicit 16×16 reconstruction + 2D conv does **not** improve performance and is slower.

### H12: Spatial augmentation and robustness to fixed electrode dropout

Evidence snapshot CSV: `results/ed20260217/paperjson/h12_spatial_aug_fixed_dropout_summary_p1_topk_k64_2026-02-17.csv`

| drop_rate | ΔCER (aug=0) | ΔCER (aug=1) |
|---:|---:|---:|
| 0.0 | 0.0000±0.0000 | 0.0000±0.0000 |
| 0.1 | 0.0245±0.0027 | 0.0183±0.0065 |
| 0.2 | 0.0783±0.0162 | 0.0660±0.0097 |
| 0.3 | 0.1440±0.0183 | 0.1224±0.0120 |

**Conclusion (H12):** Under fixed electrode dropout rates q∈{0.1,0.2,0.3}, training with spatial augmentation (enable_spatial_aug=1) yields **lower mean CER degradation (ΔCER)** than without spatial augmentation (enable_spatial_aug=0). This supports the claim that 2D-enabled spatial augmentation can improve robustness to electrode failures, at least for the spatial2d front-end.

### H13: Row/col compression (geometry-aware 1D pooling) vs vector baseline

Evidence snapshot CSV: `results/ed20260217/paperjson/h13_rowcol_vs_vector_p1_k32_k64_2026-02-17.csv`

| subset_method | K | vec CER | rowcol CER | ΔCER(rowcol-vec) | vec rtf | rowcol rtf |
|---|---:|---:|---:|---:|---:|---:|
| topk | 32 | 0.1399±0.0187 | 0.1448±0.0236 | +0.0049 | 0.0005 | 0.0021 |
| fps2k | 32 | 0.1440±0.0157 | 0.1466±0.0092 | +0.0026 | 0.0005 | 0.0022 |
| topk | 64 | 0.1289±0.0155 | 0.1269±0.0165 | -0.0020 | 0.0005 | 0.0021 |
| fps2k | 64 | 0.1195±0.0118 | 0.1255±0.0223 | +0.0061 | 0.0005 | 0.0021 |

**Conclusion (H13):** For K=32 and K=64 (topk/fps2k), the row/col compression model’s greedy test CER mean differs from the vector baseline by <0.01 absolute, while its streaming RTF is higher. Thus, this particular row/col compression preserves accuracy but does not improve streaming efficiency in the current implementation.

## 4. Review-weakness closure map (W1–W9) for this evidence bundle

Figure: `w_matrix_evidence_map.png` (binary mapping)

| Weakness | Short description | Notes |
|---|---|---|
| W1 | Novelty/positioning is limited or unclear | Covered by evidence bundles |
| W2 | Insufficient baseline / horizontal comparison | Not covered by this bundle |
| W3 | Small test case / single-subject study; unclear generalization to new users | Not covered by this bundle |
| W4 | Experimental design robustness | Covered by evidence bundles |
| W5 | SpecAugment / PCA setting inconsistency | Not covered by this bundle |
| W6 | Writing/exposition issues | Covered by evidence bundles |
| W7 | Representation choice rationale unclear | Covered by evidence bundles |
| W8 | Model size is large | Covered by evidence bundles |
| W9 | Decoding is “basic CTC” | Not covered by this bundle |

## 5. Figures

- results/positioning_analysis_epgspeller_2026-02-18/figures/positioning_space_systems.png
- results/positioning_analysis_epgspeller_2026-02-18/figures/positioning_space_representation.png
- results/positioning_analysis_epgspeller_2026-02-18/figures/w_matrix_evidence_map.png

## 6. Limits and future work (proposal; not a claim)

- The H11–H13 findings are grounded in P1 only; extending the same comparisons to P2/XSUB is required before making protocol-general statements.
- Explicit 2D reconstruction did not improve accuracy in H11; future work could test alternative spatial encoders (e.g., graph-based or 3D palate-aware models) and re-check implementation choices without changing the evidence reported here.
- Robustness gains from spatial augmentation were demonstrated under synthetic fixed dropout (H12); additional robustness axes (session drift, sensor shift) would require new evidence runs.
```
