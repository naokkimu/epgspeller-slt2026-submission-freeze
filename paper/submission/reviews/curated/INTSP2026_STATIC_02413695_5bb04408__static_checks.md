# Interspeech 2026 Manuscript Review (static, deterministic)

This report is API-key-free and does not use LLMs. It checks venue rules and basic manuscript hygiene from PDF/TeX inputs.

## Summary

- errors: 0
- warnings: 0

## Inputs

- stage: review
- paper_type: regular
- ai_tools_used: unknown
- pdf: interspeech2026_review.pdf (sha8=02413695, pages=5, extracted_chars=20623, truncated=False)
- tex: interspeech2026_review.tex (sha8=5bb04408)

## Checks

| id | severity | ok | message |
|---|---:|:---:|---|
| `abstract_ascii` | info | yes | abstract is ASCII-only |
| `abstract_length` | info | yes | abstract_chars=913 <= max_characters=1000 |
| `abstract_no_citations` | info | yes | no \cite* in abstract |
| `ai_disclosure_present` | info | no | Generative AI Use Disclosure section not found |
| `anonymity_cameraready_flag` | info | yes | no cameraready option in review stage |
| `anonymity_email_heuristic` | info | yes | no email-like strings detected in extracted PDF text |
| `banned_tokens` | info | yes | no banned tokens |
| `page_limit` | info | yes | page_count=5 <= max_pages=6 |

## Notes

- This checker cannot assess novelty/correctness of the science beyond what can be inferred from the manuscript text.
- If PDF text extraction is empty, rerun with `--prefer tex` or provide `--tex`.
