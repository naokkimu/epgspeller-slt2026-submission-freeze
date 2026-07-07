# IEEE SLT 2026 Submission Freeze

**Paper:** EPGSpeller: Lexicon-Free Silent Spelling Recognition with Electropalatography

**Status:** submitted (post-submission snapshot)

## Regenerate freeze bundle

```bash
uv run --with pyyaml python scripts/freeze_slt2026_submission.py \
  --root . \
  --export-dir ../epgspeller-slt2026-submission-freeze
```

Outputs:

| Path | Purpose |
|---|---|
| `reports/slt2026/submission/` | OpenReview upload copies + in-repo PDF/zip |
| `reports/slt2026/freeze_manifest_*.json` | Commit hash + artifact SHA256 |
| `reports/slt2026/freeze-slt2026-submission-*.tar.gz` | Portable submission tarball |
| `../epgspeller-slt2026-submission-freeze/` | Standalone GitHub archive export |

## Git freeze branch

- Branch: `freeze/slt2026-submission-20260707`
- Tag: `freeze-slt2026-submission-20260707`
- GitHub archive repo: `naokkimu/epgspeller-slt2026-submission-freeze`

## Verify

```bash
cd reports/slt2026/submission && shasum -a 256 -c ../submission/SHA256SUMS.txt
```

Supplement integrity (pre-freeze build gate):

```bash
uv run --with pyyaml python ~/.codex/skills/llm-audit-supplement-zip/scripts/verify_supplement_integrity.py \
  --staging paper/supplement/staging \
  --zip paper/submission/put_this_zip_to_your_agent_or_llm_chat.zip
```
