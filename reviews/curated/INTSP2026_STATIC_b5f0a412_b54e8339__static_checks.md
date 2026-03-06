# Interspeech 2026 Manuscript Review (static, deterministic)

This report is API-key-free and does not use LLMs. It checks venue rules and basic manuscript hygiene from PDF/TeX inputs.

## Summary

- errors: 1
- warnings: 1

## Inputs

- stage: review
- paper_type: regular
- ai_tools_used: unknown
- pdf: paper/manuscript/generated_main.pdf (sha8=b5f0a412, pages=7, extracted_chars=21206, truncated=False)
- tex: paper/manuscript/generated_main.tex (sha8=b54e8339)

## Checks

| id | severity | ok | message |
|---|---:|:---:|---|
| `abstract_ascii` | warn | no | abstract contains non-ASCII characters |
| `abstract_length` | info | yes | abstract_chars=878 <= max_characters=1000 |
| `abstract_no_citations` | info | yes | no \cite* in abstract |
| `ai_disclosure_present` | info | no | Generative AI Use Disclosure section not found |
| `anonymity_cameraready_flag` | info | yes | no cameraready option in review stage |
| `anonymity_email_heuristic` | info | yes | no email-like strings detected in extracted PDF text |
| `banned_tokens` | info | yes | no banned tokens |
| `page_limit` | error | no | page_count=7 <= max_pages=6 |

## Actionable fixes

- (error) `page_limit`: page_count=7 <= max_pages=6
- (warn) `abstract_ascii`: abstract contains non-ASCII characters

## Notes

- This checker cannot assess novelty/correctness of the science beyond what can be inferred from the manuscript text.
- If PDF text extraction is empty, rerun with `--prefer tex` or provide `--tex`.
