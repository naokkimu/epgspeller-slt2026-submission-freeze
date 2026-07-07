# Edit Plan — iter_007 (format compression)

## Goal
Compress `paper/final/slt2026.tex` from 9 content pages to 6 without removing numeric evidence or claim calibration required by iter_006 gates.

## Edit classes

### safe
- Remove redundant definitional tables duplicated across Sections 2–4
- Inline single-row result tables into prose
- Merge overlapping discussion subsections
- Drop section-summary paragraphs that repeat prior text

### medium
- Tighten intro/AAC framing without removing contribution bullets or CER numbers
- Consolidate system subsections (CTC + vector/GRU + spatial + electrode → two subsections)
- Consolidate evaluation setup (merge protocol narrative; keep protocol_map)

### risky (preserve evidence)
- Keep tab:main_protocols, tab:kshot_curve, tab:dataset_summary, tab:protocol_map, tab:transfer_boundary
- Preserve all CER/LEX/RTF values and n semantics in retained tables

## Forbidden
- Layout hacks: `\scriptsize`, negative `\vspace`, geometry overrides
- Removing limitations, ethics, or calibration bottleneck narrative
- Inventing numbers or dropping deferred-issue acknowledgments
