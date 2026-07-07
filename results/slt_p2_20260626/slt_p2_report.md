# P2 SLT Experiment Report (slt_p2_20260626)

Generated: 2026-06-26

## Summary

- **Experiment 9 (low-shot extended):** P2K k=1 for subj1/subj2 with min_repetitions=2.
- **Experiment 10 (k-shot curve):** subj3 k=4 uses a **reduced vocabulary** (feasible_vocab=14, feasible_for_50_word_eval=False); k=8 is **infeasible** per feasibility audit.
- **Experiment 11 (SilentSpeller-compatible-lite):** P1 word-holdout subj1 with 100 test words.

## Table: Low-shot extended

| subject | k | n | CER | RTF | source |
| --- | --- | --- | --- | --- | --- |
| subj1 | 1 | 4 | 0.1082±0.0051 | 0.0001±0.0000 | sltp2:new |
| subj2 | 1 | 4 | 0.1118±0.0067 | 0.0001±0.0000 | sltp2:new |
| subj3 | 1 | 4 | 0.3503±0.0600 | 0.0002±0.0000 | msx:existing |
| subj3 | 2 | 4 | 0.2458±0.0085 | 0.0002±0.0000 | msx:existing |

## Table: k-shot curve (target=subj3)

| k | condition | n | CER | RTF | notes |
| --- | --- | --- | --- | --- | --- |
| 0 | P3_single_source | 8 | 0.8403±0.0948 | 0.0001±0.0000 | msx/uc vector |
| 0 | P3MS_multi_source | 4 | 0.8381±0.0336 | 0.0001±0.0000 | msx:p3ms vector |
| 1 | P2K_within_subject | 4 | 0.3503±0.0600 | 0.0002±0.0000 | msx:existing |
| 2 | P2K_within_subject | 4 | 0.2458±0.0085 | 0.0002±0.0000 | msx:existing |
| 4 | P2K_reduced_vocab | 4 | 0.7816±0.2084 | 0.0025±0.0002 | sltp2:new reduced vocabulary (min_repetitions=5, n_competition_words=1) |
| 8 | N/A | 0 | N/A | N/A | infeasible (feasible_vocab=0, feasible_for_50_word_eval=False) |

## Table: SilentSpeller-compatible-lite

| condition | n_test_words | n | CER | RTF |
| --- | --- | --- | --- | --- |
| subj1_test100 | 100 | 4 | 0.1133±0.0128 | 0.0003±0.0000 |

## Feasibility notes

- Feasibility CSV: `results/slt_p2_20260626/kshot_feasibility.csv`
- subj3 k=4: reduced vocabulary evaluation (not 50-word standard); feasible_vocab=14.
- subj3 k=8: infeasible (feasible_vocab=0, feasible_for_50_word_eval=False).

## Inputs

- New metrics: `/mnt/share_gpu/naokkimu/epg_speller_for_icassp_camera_ready/sweeps/slt_p2_20260626/results/slt_p2_vector_metrics.csv` (found)
- MSX metrics: `/mnt/share_gpu/naokkimu/epg_speller_for_icassp_camera_ready/sweeps/msx20260224/results/msx_all_metrics.csv` (found)
- UC metrics: `/mnt/share_gpu/naokkimu/epg_speller_for_icassp_camera_ready/sweeps/uc20260226/results/uc_to4_metrics.csv` (found)
- Total metric rows loaded: 692
