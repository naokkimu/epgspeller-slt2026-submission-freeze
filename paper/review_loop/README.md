# SLT Draft Review Loop

Automated review–revise loop for `SLT_draft_clean.md`.

## Workflow (per iteration)

1. **Review** (gpt-5.5-medium)
   - Composite writing review → `iter_NNN/composite_writing_review.md`
   - SLT review simulation → `iter_NNN/slt_review_simulation.md`
2. **Gate** → `iter_NNN/gate.json`
3. **Revise** (claude-4.6-sonnet) if gate fails → edit `SLT_draft_clean.md`
4. **Commit** → `paper: review loop iter NNN — <summary>`

## Satisfaction criteria

| Review | Pass condition |
|--------|----------------|
| Composite writing | Readiness = Pass, no Critical issues |
| SLT simulation | Median overall ≥ 4 (Weak Accept+), no fatal blockers, final verdict ≥ Weak Accept |

Loop stops when both pass in the same iteration.

## History

See `state.json` and git log for `paper/review_loop/` and `paper/SLT_draft_clean.md`.
