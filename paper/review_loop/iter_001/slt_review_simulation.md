# SLT Review Simulation — Consolidated Report — iter_001

## Executive verdict
- **Final simulated decision: Weak Reject**
- Mean overall: 2.67 | Median: 3 | Range: 2–3
- Confidence: all reviewers at 4/5
- Reason: Strong SLT fit and honest framing, but missing baselines, thin statistics, weak reproducibility, and AAC deployment claims exceed offline evidence.

## Reviewer score matrix
| Reviewer | Overall | Conf | Nov | Sound | Exp | SLT | Impact | Clarity | Repro | Ethics | Weighted |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| methodology-skeptic | 2 | 4 | 2 | 3 | 2 | 4 | 3 | 4 | 2 | 2 | 2.9 |
| systems-pragmatist | 3 | 4 | 3 | 3 | 3 | 4 | 3 | 4 | 2 | 2 | 3.2 |
| slt-fit-advocate | 3 | 4 | 3 | 3 | 2 | 5 | 4 | 4 | 2 | 3 | 3.3 |

## Main acceptance blockers (ranked)
1. **Missing strong baselines** — all 3 reviewers (fatal/major)
2. **Reproducibility gap** — architecture, hyperparams, splits underspecified — all 3
3. **Statistical validation** — single CER values, no CI/variance — skeptic
4. **AAC deployment overclaim** — no user-facing eval — pragmatist + advocate
5. **Dataset scale** — 4 participants — all 3
6. **Ethics/privacy** — intraoral sensing not addressed — all 3

## Area-chair meta-review
Problem formulation and protocol taxonomy are SLT-relevant and well-written. Negative transfer results are reported honestly. However, the paper cannot be accepted without stronger baselines, reproducibility detail, and reframed novelty (task/protocol study, not novel recognizer). Writing quality is adequate; empirical package is the blocker.

## Rebuttal strategy (top items)
1. Clarify split construction and rule out leakage
2. Add baseline comparison table (SilentSpeller-era + modern CTC)
3. Report seed variance / CI for headline CERs
4. Reframe contribution as recognition-layer + calibration study
5. Add ethics/privacy subsection for intraoral EPG

## Revision plan (top 10, score impact)
1. Add baseline table — heavy
2. Full reproducibility appendix — medium
3. Statistical uncertainty on main tables — heavy
4. Standardize p1–p4 vs P1–P3 notation — quick
5. Compress repetitive lexicon-free framing — quick
6. Reframe AAC as motivation not deployment claim — quick
7. Quantify k-shot in trials/time — medium
8. Ethics/privacy subsection — medium
9. Sharpen SilentSpeller bridge role — quick
10. Strengthen conclusion takeaway — quick

## Final risk level
**High** — median score 3, no reviewer at Accept (5+)
