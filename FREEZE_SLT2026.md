# SLT 2026 Submission Freeze

**Submitted:** IEEE SLT 2026 (OpenReview)  
**Freeze tag:** `freeze-slt2026-submission-20260707`  
**Canonical archive repo:** https://github.com/naokkimu/epgspeller-slt2026-submission-freeze

## Local artifacts

| Path | Role |
| --- | --- |
| `reports/slt2026/submission/` | OpenReview upload bundle copies + SHA256SUMS |
| `reports/slt2026/freeze_manifest_*.json` | Freeze manifest with file hashes |
| `reports/slt2026/freeze-slt2026-submission-20260707.tar.gz` | Tarball of submission bundle |
| `../epgspeller-slt2026-submission-freeze/` | Standalone export (mirrors GitHub archive) |

## Regenerate export

```bash
uv run --system-certs --with pyyaml python scripts/freeze_slt2026_submission.py \
  --root . \
  --export-dir ../epgspeller-slt2026-submission-freeze \
  --freeze-tag freeze-slt2026-submission-20260707
```

## Submission hashes (OpenReview pack)

See `reports/slt2026/freeze_manifest_freeze-slt2026-submission-20260707.json`.

Main PDF SHA256: `466a89d2ee6bddcfd14951c4ee5b21fdcf2b7d85a7ff22326405b622232d0d0f`  
Supplement zip SHA256: `088a966a6296bb316dd269d2d3060cb3d6a348b95c74b0ac4de7769ca062f40e`

## Active development

Do not continue feature work on branch `slt2026-submission-freeze`. Use `main` / feature branches in the dev tree.
