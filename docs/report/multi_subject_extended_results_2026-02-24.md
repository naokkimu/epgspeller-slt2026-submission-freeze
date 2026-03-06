# Extended multi-subject results (tag=msx20260224)

- generated_at: 2026-03-06 14:09:19
- metrics_csv: `sweeps/msx20260224/results/msx_all_metrics.csv`
- eda_report: `results/dataset_audit_silentspeller_2026-02-24/report.md`

## Baseline recap (ms20260224)

Per-group mean±std over seeds0–3 (greedy CER / stream RTF / lex CER).

### P1

| group | greedy CER | stream RTF | lex(train) CER | lex(all) CER |
| --- | --- | --- | --- | --- |
| subj1 | 0.1096±0.0158 | 0.000603±0.000223 | 0.4013±0.0213 | 0.0400±0.0042 |
| subj2 | 0.1213±0.0201 | 0.000596±0.000079 | 0.4227±0.0172 | 0.0604±0.0060 |
| subj3 | 0.1945±0.0132 | 0.000375±0.000066 | 0.4634±0.0139 | 0.1149±0.0231 |
| subj4 | 0.2930±0.0163 | 0.000937±0.000072 | 0.4948±0.0133 | 0.1919±0.0215 |

### P2

| group | greedy CER | stream RTF | lex(train) CER | lex(all) CER |
| --- | --- | --- | --- | --- |
| subj1 | 0.1054±0.0071 | 0.000108±0.000004 | 0.0569±0.0040 | 0.0431±0.0059 |
| subj2 | 0.1124±0.0046 | 0.000116±0.000004 | 0.0640±0.0036 | 0.0515±0.0030 |
| subj3 | 0.2174±0.0098 | 0.000097±0.000004 | 0.1428±0.0107 | 0.1295±0.0106 |

### P3

| group | greedy CER | stream RTF | lex(train) CER | lex(all) CER |
| --- | --- | --- | --- | --- |
| subj1to2 | 0.5949±0.0318 | 0.000133±0.000019 | 0.6115±0.0431 | 0.6087±0.0458 |
| subj1to3 | 0.7554±0.0128 | 0.000097±0.000006 | 0.6804±0.0252 | 0.6783±0.0242 |
| subj2to1 | 0.6896±0.0124 | 0.000108±0.000006 | 0.5953±0.0222 | 0.5928±0.0197 |
| subj2to3 | 0.9252±0.0395 | 0.000096±0.000003 | 0.7527±0.0120 | 0.7516±0.0108 |
| subj3to1 | 0.5859±0.0197 | 0.000106±0.000003 | 0.6103±0.0230 | 0.6072±0.0235 |
| subj3to2 | 0.5942±0.0300 | 0.000120±0.000004 | 0.6308±0.0412 | 0.6270±0.0413 |

## Spatial modeling @K=124 (rowcol vs spatial2d aug0/aug1)

Summary over groups: mean±std over per-group mean CER/RTF (seeds0–3).

### P1

| variant | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| rowcol_uni_gru | 0.2016±0.0886 | 0.002401±0.001106 | 4 |
| spatial2d_uni_gru_aug0 | 0.3062±0.1491 | 0.003564±0.001540 | 4 |
| spatial2d_uni_gru_aug1 | 0.3094±0.1440 | 0.003414±0.001054 | 4 |

Figure: `docs/report/figures/msx20260224/spatial_k124_P1_cer_bar.png`

### P2

| variant | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| rowcol_uni_gru | 0.1613±0.0783 | 0.000244±0.000037 | 3 |
| spatial2d_uni_gru_aug0 | 0.2894±0.2126 | 0.000389±0.000047 | 3 |
| spatial2d_uni_gru_aug1 | 0.3139±0.2436 | 0.000392±0.000045 | 3 |

Figure: `docs/report/figures/msx20260224/spatial_k124_P2_cer_bar.png`

### P3

| variant | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| rowcol_uni_gru | 0.6828±0.1510 | 0.000243±0.000033 | 6 |
| spatial2d_uni_gru_aug0 | 0.7507±0.0897 | 0.000393±0.000042 | 6 |
| spatial2d_uni_gru_aug1 | 0.7559±0.0920 | 0.000397±0.000046 | 6 |

Figure: `docs/report/figures/msx20260224/spatial_k124_P3_cer_bar.png`

## Electrode reduction @K=64 (uni_gru)

Summary over groups: mean±std over per-group mean CER/RTF (seeds0–3).

### P1

| method | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| within_topk64 | 0.1952±0.0827 | 0.000657±0.000210 | 4 |
| within_fps2k64 | 0.1912±0.0781 | 0.000619±0.000229 | 4 |
| transfer_subj1_topk64 | 0.2052±0.0951 | 0.000586±0.000218 | 4 |
| random64_seed20260224 | 0.1980±0.0793 | 0.000665±0.000282 | 4 |

Figure: `docs/report/figures/msx20260224/k64_P1_cer_bar.png`

### P2

| method | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| within_topk64 | 0.1544±0.0591 | 0.000110±0.000011 | 3 |
| within_fps2k64 | 0.1539±0.0617 | 0.000110±0.000010 | 3 |
| transfer_subj1_topk64 | 0.1584±0.0709 | 0.000106±0.000009 | 3 |
| random64_seed20260224 | 0.1566±0.0669 | 0.000105±0.000011 | 3 |

Figure: `docs/report/figures/msx20260224/k64_P2_cer_bar.png`

### P3

| method | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| within_topk64 | 0.6473±0.1301 | 0.000108±0.000009 | 6 |
| within_fps2k64 | 0.6564±0.1465 | 0.000107±0.000010 | 6 |
| transfer_subj1_topk64 | 0.6569±0.1441 | 0.000109±0.000009 | 6 |
| random64_seed20260224 | 0.6442±0.1328 | 0.000111±0.000010 | 6 |

Figure: `docs/report/figures/msx20260224/k64_P3_cer_bar.png`

## Spatial modeling @K=64 (within_topk64 subsets)

Compare uni_gru (K64 within_topk64) vs rowcol/spatial2d (aug0/aug1).

### P1

| variant | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| uni_gru (within_topk64) | 0.1952±0.0827 | 0.000657±0.000210 | 4 |
| rowcol_uni_gru (within_topk64) | 0.2006±0.0847 | 0.002487±0.001145 | 4 |
| spatial2d_uni_gru_aug0 | 0.3796±0.2416 | 0.003103±0.001343 | 4 |
| spatial2d_uni_gru_aug1 | 0.3657±0.2070 | 0.003117±0.001337 | 4 |

### P2

| variant | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| uni_gru (within_topk64) | 0.1544±0.0591 | 0.000110±0.000011 | 3 |
| rowcol_uni_gru (within_topk64) | 0.1617±0.0702 | 0.000242±0.000038 | 3 |
| spatial2d_uni_gru_aug0 | 0.3882±0.3314 | 0.000389±0.000051 | 3 |
| spatial2d_uni_gru_aug1 | 0.3810±0.3208 | 0.000391±0.000052 | 3 |

### P3

| variant | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| uni_gru (within_topk64) | 0.6473±0.1301 | 0.000108±0.000009 | 6 |
| rowcol_uni_gru (within_topk64) | 0.6611±0.1486 | 0.000256±0.000027 | 6 |
| spatial2d_uni_gru_aug0 | 0.7470±0.1306 | 0.000405±0.000037 | 6 |
| spatial2d_uni_gru_aug1 | 0.7535±0.1244 | 0.000392±0.000048 | 6 |

## P3MS: multi-source cross-subject (2SRC→1TGT)

Note: vocabulary size may differ from single-source P3 (intersection over 3 subjects vs 2).

### subj23to1

| variant | CER (groups) | RTF (groups) | test n_samples(seed0) |
| --- | --- | --- | --- |
| uni_gru | 0.4735±0.0000 | 0.000121±0.000000 | 1161 |
| rowcol_uni_gru | 0.4759±0.0000 | 0.000237±0.000000 | 1161 |
| spatial2d_uni_gru_aug0 | 0.6020±0.0000 | 0.000389±0.000000 | 1161 |
| spatial2d_uni_gru_aug1 | 0.6911±0.0000 | 0.000386±0.000000 | 1161 |

### subj13to2

| variant | CER (groups) | RTF (groups) | test n_samples(seed0) |
| --- | --- | --- | --- |
| uni_gru | 0.5203±0.0000 | 0.000116±0.000000 | 1161 |
| rowcol_uni_gru | 0.5042±0.0000 | 0.000297±0.000000 | 1161 |
| spatial2d_uni_gru_aug0 | 0.5106±0.0000 | 0.000435±0.000000 | 1161 |
| spatial2d_uni_gru_aug1 | 0.5114±0.0000 | 0.000433±0.000000 | 1161 |

### subj12to3

| variant | CER (groups) | RTF (groups) | test n_samples(seed0) |
| --- | --- | --- | --- |
| uni_gru | 0.8381±0.0000 | 0.000096±0.000000 | 1161 |
| rowcol_uni_gru | 0.7903±0.0000 | 0.000203±0.000000 | 1161 |
| spatial2d_uni_gru_aug0 | 0.7362±0.0000 | 0.000343±0.000000 | 1161 |
| spatial2d_uni_gru_aug1 | 0.7561±0.0000 | 0.000346±0.000000 | 1161 |

## subj3 k-shot (k=1 vs k=2)

### k=1

| variant | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| uni_gru | 0.3503±0.0000 | 0.000164±0.000000 | 1 |
| rowcol_uni_gru | 0.3344±0.0000 | 0.000502±0.000000 | 1 |
| spatial2d_uni_gru_aug0 | 0.5153±0.0000 | 0.000712±0.000000 | 1 |
| spatial2d_uni_gru_aug1 | 0.6105±0.0000 | 0.001067±0.000000 | 1 |

### k=2

| variant | CER (groups) | RTF (groups) | n_groups |
| --- | --- | --- | --- |
| uni_gru | 0.2458±0.0000 | 0.000165±0.000000 | 1 |
| rowcol_uni_gru | 0.2782±0.0000 | 0.000522±0.000000 | 1 |
| spatial2d_uni_gru_aug0 | 0.6156±0.0000 | 0.000769±0.000000 | 1 |
| spatial2d_uni_gru_aug1 | 0.6889±0.0000 | 0.000748±0.000000 | 1 |

## Notes / evidence links

- Split EDA (raw+splits): `results/dataset_audit_silentspeller_2026-02-24/report.md`
- Baseline report: `docs/report/multi_subject_results_2026-02-24.md`
- Figures (this report): `docs/report/figures/msx20260224/`

