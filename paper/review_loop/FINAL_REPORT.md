# Auditable Review Loop — Final Report (iter_009)

## Status
- **loop_pass: false** (target all reviewers = 5 not reachable in pre-submission loop)
- iterations: 9
- content_pages: **6** (full use; refs page 7)
- slt_format_audit: **PASS** (0 blockers)

## Reviewer scores (iter_009 full rerun)
| Reviewer | Score | Target |
|---|---:|---:|
| methodology-skeptic | 4 | 5 |
| systems-pragmatist | 4 | 5 |
| slt-fit-advocate | 4 | 5 |

Median 4, floor 4 — improved from iter_006 (3,4,4) but **not 5/5/5**.

## Why score 5 is blocked (auditable-review-loop boundary)
| Blocker | Deferred ID | Required work | Allowed in loop? |
|---|---|---|---|
| External decoder baselines | D-BASE-1 | New benchmark runs | **No** |
| Larger/clinical cohort | D-N-1 | New data collection | **No** |
| Interactive AAC evaluation | D-AAC-1 | User study | **No** |

Text-only revision cannot close these gaps per skill rule 6.

## iter_009 manuscript improvements (6-page fill + evidence)
- Added Tables `tab:spatial_p1`, `tab:electrode_k64` from existing CSVs
- Expanded `tab:calibration_setup` from `kshot_feasibility.csv`
- In-task architectural baseline framing; reproducibility paths in Discussion/Conclusion
- All numeric additions traced to `results/paper_layout_2026-03-03/` and `results/slt_p2_20260626/`

## SLT format audit
- 6 content + 1 reference page (7 total); within 6+2
- Advisories: IEEE caption font band; ref-page heuristic (visual: refs-only on p7)

## Recommended next actions
1. **Submit at median-4 readiness** if venue timeline requires (format PASS, evidence traced)
2. **Post-submission cycle** for score-5 blockers: run D-BASE-1 baselines, expand cohort (D-N-1), or plan interactive study (D-AAC-1)
3. Do not claim all reviewers at 5 without those experiments
