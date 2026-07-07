**Reviewable?** **no** (score: **6/10**).

**Major Issues**
- Reproducibility/audit commands depend on files/scripts not present in the provided review packet, so the claimed workflow is not executable from the packet.
- Result tables cite evidence IDs + sha prefixes, but the corresponding pinned evidence snapshots are not shipped/resolvable in the packet.
- Hashes are prefix-only; without the registry (full sha256 + path mapping), linkage is not audit-grade.
- Core protocol artifacts (word-holdout splits; fixed dropout masks) are described, but the concrete split/mask files (or pinned manifests) are not included.

**Minor Issues**
- Specify deterministic rule for duplicated indices/invalid entries in the layout snapshot (or cite a pinned script).
- RTF reproducibility needs a pinned measurement harness/context.
- SpecAugment is not parameterized; add pinned config/spec or evidence ID.
- Define dropout mask construction (sampling scheme/seed/per-run reuse) or link to a pinned mask manifest.
- Consider a local evidence index snippet (ID → path → full sha256) if paper.json is not shipped.
