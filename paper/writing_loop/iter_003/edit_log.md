# edit_log — iter_003

## Cluster: Required Corrections + gate blockers

| Issue ID | File | Change |
|----------|------|--------|
| RC1 / AG-C01 / PE-001 | `03_system.tex` | Removed `src/neural_decoder/conf/unified_config.yaml`; → supplementary configuration table |
| RC2 / AG-C02 | `07_conclusion.tex` | Removed "public results tree"; → supplementary materials |
| RC3 / AG-C03 | `06_discussion.tex` | Reproducibility: train/validation/test splits; supplementary materials (no competition/CSV/repo jargon) |
| RC4 / STR-003 | `06_discussion.tex` | Merged 4 thin subsections → 2 (`Findings and Calibration Bottleneck`; `Limitations, Ethics, and Reproducibility`) |
| RC5 / AG-M06 | `01_introduction.tex` | Merged micro-paragraphs into 9 multi-sentence paragraphs; added P2 upper-bound clause |
| AG-M01 | `05_results.tex` | Expanded `tab:main_protocols` caption with LEX/RTF |
| AA-01 | `slt2026.tex` | Abstract: CER expanded; P1/P2/P3 protocol tags |
| AA-03 | `05_results.tex` | Removed interpretive deployment sentence from Results |
| PE-012 | `03_system.tex`, `05_results.tex`, `07_conclusion.tex` | Varied "lexicon-free string decoding" → greedy string decoding |
| Layout | `slt2026.tex` | `\linespread{1.06}`, float spacing, `\clearpage` before bibliography → 6 content + refs-only p7 |

## Verify
- Compile: OK (`slt2026.pdf`, 7 pages)
- Page map: p1–6 content; p7 REFERENCES only
- Anti-GPT: Kimura 50/C, HIGH 0, MEDIUM 10 (PDF em-dash artifacts)
