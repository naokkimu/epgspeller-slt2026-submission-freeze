Reviewable? **no** (score: **4/10**)

Major issues
- **Missing registry + spec**: `paper/paper.json` and `paper/facts_spec.yaml` are referenced but not present in the provided review packet, so evidence IDs cannot be resolved to concrete files/full hashes.
- **Missing tooling**: reproducibility/audit commands reference scripts not present in the provided review packet; regeneration and the “strict checker” gate are therefore not executable/verifiable from the packet.
- **Result evidence snapshots not shipped**: tables cite evidence IDs and sha prefixes but the corresponding CSVs are not present in the provided review packet, so tables are not traceable.
- **Hash display is prefix-only**: captions expose only short sha prefixes; without shipping `paper/paper.json`, linkage is not audit-grade.

Unreproducible claims list (line → what should back it)
- Claims about “worse/slower”, “close”, and robustness require the pinned evidence files (full sha256 + paths via `paper/paper.json`) and the raw snapshots matching the sha prefixes.
- Claims about registry/checker require shipping `paper/paper.json`, `paper/facts_spec.yaml`, and the generator/checker/audit scripts.

Numeric-handwriting violations
- None in the provided excerpt: prose avoids literal numeric facts.

Minor issues
- Add an explicit pointer to pinned protocol/config artifacts when claiming “matched training settings”.
- Consider a deterministic local mapping (ID → path + full sha256) in the artifacts section if `paper/paper.json` is not guaranteed to be shipped.
- Clarify dropout mask construction (what “fixed” means) or point to a pinned script/artifact.
