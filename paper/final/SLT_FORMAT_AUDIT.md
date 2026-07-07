# SLT Format Audit Report

**Audit-only — no fixes applied during this audit run. Manuscript edited in visual-polish loop before re-audit.**

| Field | Value |
| --- | --- |
| TeX | `paper/final/slt2026.tex` |
| PDF | `paper/final/slt2026.pdf` |
| Track | double-blind |
| Lanes run | A (tex), B (pdf), D (aesthetic), C (visual) |
| Generated | 2026-07-01 (iter_vis2) |

## Verdict

**Overall**: **PASS**

**Submission blockers** (FAIL): **0**

## Page budget

| Metric | Value | Status |
| --- | ---: | --- |
| Content pages | 6 | PASS |
| Reference pages | 1 | PASS |
| Total | 7 | PASS |
| Abstract words | 118 | PASS |

## Compliance Summary

| Guideline | Status | Notes |
| --- | --- | --- |
| LENGTH (6+2) | PASS | Page 7 references-only (visual confirmed) |
| MARGINS | PASS | Float spacing tuned; no `\geometry` |
| FONT SIZE | ADVISORY | 8.97 pt IEEE band |
| AUTHOR/TITLE/ABSTRACT | PASS | |
| REFERENCES | PASS | No body text on ref page |
| PAGE NUMBERS | PASS | |

## Advisories

### [ADVISORY] FONT_SIZE — 8.97 pt template band
- **Provenance**: [Script]
- **Rule**: Minimum 9 pt body; IEEE caption/abstract band exempted by heuristic.

## Visual polish changes (pre-audit edits)

- Removed redundant `tab:decoding_metrics` (inlined metrics prose)
- Merged `tab:spatial_p1` + `tab:electrode_k64` → `tab:spatial_electrode`
- Condensed Discussion D and Conclusion to keep references on page 7 only
- Tuned float spacing in preamble (`\textfloatsep`, etc.)

## Lane Artifacts

- Latest renders: `paper/final/slt_audit_artifacts/lane_d/packet_iter_vis2/`
- Prior: `packet_iter_vis/`, `packet/`

## Commands Run

```bash
latexmk -pdf -interaction=nonstopmode slt2026.tex
uv run ... slt_checks.py slt2026.pdf --tex-file slt2026.tex --track double-blind
uv run ... aesthetic_review_packet.py slt2026.pdf --out_dir .../packet_iter_vis2
```
