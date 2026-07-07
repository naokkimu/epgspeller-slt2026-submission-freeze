# P2 SLT Experiment Completion Status

## Scope

- Priority 9: extend low-shot beyond subj3.
- Priority 10: k-shot curve for k=0,1,2,4,8.
- Priority 11: SilentSpeller-compatible-lite split.

## Completion

- Status: complete
- Matrix rows: 16
- Collected metric rows: 16
- Missing required eval artifacts: 0
- Missing metric fields: 0

## Artifacts

- Matrix: `sweeps/slt_p2_20260626/matrices/slt_p2_vector.csv`
- Metrics: `sweeps/slt_p2_20260626/results/slt_p2_vector_metrics.csv`
- Report: `results/slt_p2_20260626/slt_p2_report.md`
- Feasibility audit: `results/slt_p2_20260626/kshot_feasibility.csv`
- Split audit: `results/slt_p2_20260626/split_audit/`
- Paper tables:
  - `results/slt_p2_20260626/paper_tables/table_lowshot_extended.csv`
  - `results/slt_p2_20260626/paper_tables/table_kshot_curve.csv`
  - `results/slt_p2_20260626/paper_tables/table_silentspeller_lite.csv`

## Headline Results

- Low-shot extension:
  - subj1 k=1: CER 0.108222 +- 0.005059
  - subj2 k=1: CER 0.111769 +- 0.006698
  - subj3 k=1 existing: CER 0.350280 +- 0.059950
  - subj3 k=2 existing: CER 0.245802 +- 0.008507
- k-shot curve for subj3:
  - k=0 P3 single-source: CER 0.840301 +- 0.094775
  - k=0 P3MS multi-source: CER 0.838062 +- 0.033612
  - k=1 P2K existing: CER 0.350280 +- 0.059950
  - k=2 P2K existing: CER 0.245802 +- 0.008507
  - k=4 reduced-vocabulary P2K: CER 0.781609 +- 0.208381
  - k=8: infeasible; feasible_vocab=0
- SilentSpeller-compatible-lite:
  - subj1 100 test word-types: CER 0.113343 +- 0.012833

## Notes

- subj3 k=4 is not a standard 50-word evaluation; feasibility audit gives feasible_vocab=14.
- subj3 k=8 is data-infeasible.
- subj4 k=1 is also not feasible for a 50-word evaluation; feasibility audit gives feasible_vocab=5.
