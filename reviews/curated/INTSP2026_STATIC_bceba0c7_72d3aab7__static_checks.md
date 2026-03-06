# Interspeech 2026 Manuscript Review (static, deterministic)

This report is API-key-free and does not use LLMs. It checks venue rules and basic manuscript hygiene from PDF/TeX inputs.

## Summary

- errors: 0
- warnings: 0

## Inputs

- stage: review
- paper_type: regular
- ai_tools_used: unknown
- pdf: paper/manuscript/generated_main.pdf (sha8=bceba0c7, pages=6, extracted_chars=19706, truncated=False)
- tex: paper/manuscript/generated_main.tex (sha8=72d3aab7)

## Checks

| id | severity | ok | message |
|---|---:|:---:|---|
| `abstract_ascii` | info | yes | abstract is ASCII-only |
| `abstract_length` | info | yes | abstract_chars=803 <= max_characters=1000 |
| `abstract_no_citations` | info | yes | no \cite* in abstract |
| `ai_disclosure_present` | info | no | Generative AI Use Disclosure section not found |
| `anonymity_cameraready_flag` | info | yes | no cameraready option in review stage |
| `anonymity_email_heuristic` | info | yes | no email-like strings detected in extracted PDF text |
| `banned_tokens` | info | yes | no banned tokens |
| `page_limit` | info | yes | page_count=6 <= max_pages=6 |

## Notes

- This checker cannot assess novelty/correctness of the science beyond what can be inferred from the manuscript text.
- If PDF text extraction is empty, rerun with `--prefer tex` or provide `--tex`.
