# ev_uc20260226_p3ms_conditions_md

- kind: `document`
- path: `docs/report/p3ms_conditions_2026-02-26.md`
- sha256: `59fac410e5e864470cd6950109ef23be3b9e5fa0d76e3d3f846444b44dfeeeca`
- size_bytes: 1341
- root_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- abs_path_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/docs/report/p3ms_conditions_2026-02-26.md`

## Excerpt

```md
# P3MS condition analysis (uc20260226)
## Inputs
- msx_metrics_csv: `/mnt/share_gpu/naokkimu/epg_speller_for_icassp_camera_ready/sweeps/msx20260224/results/msx_all_metrics.csv`
- uc_to4_metrics_csv: `/mnt/share_gpu/naokkimu/epg_speller_for_icassp_camera_ready/sweeps/uc20260226/results/uc_to4_metrics.csv`
- raw_npz:
  - subj1: `/mnt/share_gpu/naokkimu/epg_speller_for_icassp_camera_ready/raw/silentspeller_dataset/p1_2328_old_dataset.npz`
  - subj2: `/mnt/share_gpu/naokkimu/epg_speller_for_icassp_camera_ready/raw/silentspeller_dataset/thad_2328_old_dataset.npz`
  - subj3: `/mnt/share_gpu/naokkimu/epg_speller_for_icassp_camera_ready/raw/silentspeller_dataset/john_2328_dataset.npz`
  - subj4: `/mnt/share_gpu/naokkimu/epg_speller_for_icassp_camera_ready/raw/silentspeller_dataset/su_1167_old_dataset.npz`
- subj3_exclusions: `/mnt/share_gpu/naokkimu/epg_speller_for_icassp_camera_ready/results/dataset_audit_silentspeller_2026-02-24/exclusions/john_2328_exclude_indices.json`

## Outputs
- `results/uc20260226/p3ms_conditions.csv`
- `docs/report/figures/uc20260226/p3ms_delta_vs_similarity.png`

## Summary (observations only)
- delta_cer range (P3MS - mean(P3 singles)): [-0.164265, -0.002240]
- mean(src-target corr) range: [0.914025, 0.958087]
- See the CSV for per-group values and the scatter plot for the delta-vs-similarity view.
```
