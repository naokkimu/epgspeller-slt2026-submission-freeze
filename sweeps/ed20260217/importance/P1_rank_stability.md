# Rank stability (P1)

- baseline_csv: `sweeps/gc20260216/matrices/gc_baseline.csv`
- logs_dir: `logs`
- runs: 4 (seeds=seed0, seed1, seed2, seed3)

## Spearman correlation (delta_cer rankings)

| seed_a | seed_b | spearman_rho |
| --- | --- | --- |
| seed0 | seed1 | 0.0072 |
| seed0 | seed2 | 0.2833 |
| seed0 | seed3 | 0.1111 |
| seed1 | seed2 | -0.0821 |
| seed1 | seed3 | -0.0150 |
| seed2 | seed3 | -0.1682 |

## TopK Jaccard overlap (channel sets)

| K | seed_a | seed_b | jaccard |
| --- | --- | --- | --- |
| 32 | seed0 | seed1 | 0.1429 |
| 32 | seed0 | seed2 | 0.3617 |
| 32 | seed0 | seed3 | 0.1429 |
| 32 | seed1 | seed2 | 0.1636 |
| 32 | seed1 | seed3 | 0.1636 |
| 32 | seed2 | seed3 | 0.2075 |
| 32 | mean |  | 0.1970 |
| 32 | min |  | 0.1429 |
| 64 | seed0 | seed1 | 0.4066 |
| 64 | seed0 | seed2 | 0.3913 |
| 64 | seed0 | seed3 | 0.3763 |
| 64 | seed1 | seed2 | 0.3196 |
| 64 | seed1 | seed3 | 0.3913 |
| 64 | seed2 | seed3 | 0.2549 |
| 64 | mean |  | 0.3567 |
| 64 | min |  | 0.2549 |
| 96 | seed0 | seed1 | 0.6696 |
| 96 | seed0 | seed2 | 0.6696 |
| 96 | seed0 | seed3 | 0.6696 |
| 96 | seed1 | seed2 | 0.6134 |
| 96 | seed1 | seed3 | 0.6991 |
| 96 | seed2 | seed3 | 0.6134 |
| 96 | mean |  | 0.6558 |
| 96 | min |  | 0.6134 |

