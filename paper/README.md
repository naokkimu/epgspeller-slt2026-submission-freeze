# paper.json registry

This repository uses `paper/paper.json` as a lightweight registry that links:

- **claims** (what we assert)
- **evidence** (files that support/refute claims; pinned by sha256)
- **runs / experiments** (the commands and outputs that produced the evidence)

The goal is to make every scientific statement traceable to concrete artifacts.

## Quick commands

- Lint the registry:
  - `python3 tools/paper_json_lint.py --paper-json paper/paper.json --root .`

- Render a deterministic claim audit (Markdown):
  - `python3 scripts/render_paper_json_claim_audit.py --paper-json paper/paper.json --root . --out-md paper/snippets/claim_audit.md --strict`

- Render an evidence-only review simulation (Markdown):
  - `python3 scripts/render_paper_json_interspeech_review.py --paper-json paper/paper.json --root . --out-md paper/snippets/interspeech_review.md`

## Evidence conventions

- Prefer **stable relative paths** under `results/` or `artifacts/`.
- Pin `sha256` for every evidence file.
- Avoid absolute paths.

