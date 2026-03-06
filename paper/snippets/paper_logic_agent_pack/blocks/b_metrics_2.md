# b_metrics_2

- kind: `paragraph`
- status: `supported`
- section: Data and Protocols (data) ([data](../sections/data.md))
- generated_utc: 2026-03-04T11:22:19+00:00

## Evidence (ids)
- [ev_scripts_rebuttal_eval_greedy_clean_py](../evidence/ev_scripts_rebuttal_eval_greedy_clean_py.md) kind=`data` path=`scripts/rebuttal/eval_greedy_clean.py` sha256=`a341ada9fb1e2b0d0a0754edf3e1c122bb9d253c627511256abf39441bfeb0fb`
- [ev_scripts_rebuttal_gc_collect_metrics_py](../evidence/ev_scripts_rebuttal_gc_collect_metrics_py.md) kind=`data` path=`scripts/rebuttal/gc_collect_metrics.py` sha256=`13570f95d81749e176dfb80fdca6f90fa67f7aef83af032e7a57480883e19307`

## Statements

### st_b_metrics_2_01
Greedy decoding reports unconstrained character sequences.

evidence_supports:
- [ev_scripts_rebuttal_eval_greedy_clean_py](../evidence/ev_scripts_rebuttal_eval_greedy_clean_py.md)
- [ev_scripts_rebuttal_gc_collect_metrics_py](../evidence/ev_scripts_rebuttal_gc_collect_metrics_py.md)

### st_b_metrics_2_02
Lexicon projection maps outputs to finite word sets derived from the training vocabulary or the full audited lexicon.

evidence_supports:
- [ev_scripts_rebuttal_eval_greedy_clean_py](../evidence/ev_scripts_rebuttal_eval_greedy_clean_py.md)
- [ev_scripts_rebuttal_gc_collect_metrics_py](../evidence/ev_scripts_rebuttal_gc_collect_metrics_py.md)

### st_b_metrics_2_03
This allows us to separate decoding quality from lexicon constraints.

evidence_supports:
- [ev_scripts_rebuttal_eval_greedy_clean_py](../evidence/ev_scripts_rebuttal_eval_greedy_clean_py.md)
- [ev_scripts_rebuttal_gc_collect_metrics_py](../evidence/ev_scripts_rebuttal_gc_collect_metrics_py.md)

### st_b_metrics_2_04
We compute real time factor by dividing inference time by input duration under the same test harness.

evidence_supports:
- [ev_scripts_rebuttal_eval_greedy_clean_py](../evidence/ev_scripts_rebuttal_eval_greedy_clean_py.md)
- [ev_scripts_rebuttal_gc_collect_metrics_py](../evidence/ev_scripts_rebuttal_gc_collect_metrics_py.md)
