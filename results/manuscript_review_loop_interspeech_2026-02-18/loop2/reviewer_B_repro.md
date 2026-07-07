Reviewable? **no** — **Reject**

Major issues
- `paper/paper.json` (claim↔evidence registry) is referenced (L108) but is missing from the provided packet, so evidence IDs cannot be resolved to concrete files/full hashes.
- The stated generation protocol is not reproducible: `scripts/paper/generate_facts_tex.py` and `paper/facts_spec.yaml` (L109; also referenced in headers of `paper/generated/*.tex`) are not present in the packet, so `paper/generated/facts.tex`, `paper/generated/provenance.tex`, and the tables cannot be regenerated/verified.
- Result-table evidence is not auditable: provenance lists `\\EvSpatialCompare/\\ShaSpatialCompare`, `\\EvRowcolCompare/\\ShaRowcolCompare`, `\\EvSpatialDropout/\\ShaSpatialDropout` (L112) but no files in the packet match those sha prefixes, so Tables `tab:h11`, `tab:h13`, `tab:h12` are not traceable to pinned CSVs.
- Core protocol is under-defined for replication: “word-holdout protocol” + “random split seeds” (L22, L37–L38, L59) lacks split construction rules and lacks pinned split artifacts.
- Key metrics/heuristics are under-defined: streaming RTF has no definition (L65); TopK/FPS-diverse TopK are not specified beyond names (L62); fixed-dropout masks + “spatial augmentation” are not parameterized (L95–L97).

Unreproducible claims list (line → what should back it)
- L25: “All reported numbers … pinned evidence … deterministic script.” → Needs `paper/paper.json` + generator script + `paper/facts_spec.yaml` + the pinned CSV evidence files used to generate each table.
- L30: “fixed inventory of \\TotalChannels … SmartPalate channel numbering.” → Needs an explicit evidence linkage to `\\EvSmartpalateDistribution`/`\\ShaSmartpalateDistribution` plus a reproducible derivation rule for \\TotalChannels.
- L32: “proxy spatial map … derived from the pinned SmartPalate distribution artifact.” → Needs the exact artifact path (via `paper/paper.json`) and a fully specified index→(row,col) mapping procedure.
- L33: “mapped/unmapped/duplicated channels … aggregated deterministically.” → Needs (a) the aggregation operator definition and (b) evidence/script that deterministically produces \\MappedChannels/\\UnmappedChannels/\\DuplicatedChannels from the pinned artifact.
- L45–L46: shared backbone + unfolding with \\KernelLen/\\StrideLen and backbone params (\\ModelFamilyVector/\\ModelLayers/\\ModelUnits). → Needs a pinned config/run-args snapshot (referenced in `paper/paper.json`) that defines these macros end-to-end.
- L59–L60: “\\NSeedsPone split seeds (\\SeedListPone) … reuse same splits … \\TrainBatches … \\FrameMs … SpecAugment-inspired masking.” → Needs pinned split files + a pinned training config (incl. optimizer/LR/batch size/mask params) linked in `paper/paper.json`.
- L72–L74: “Spatial2D … worse … slower.” → Needs Table `tab:h11` explicitly linked to `\\EvSpatialCompare`/`\\ShaSpatialCompare` (ideally in the caption) and the underlying pinned CSV present.
- L84–L85: “Row/column compression … close … but increases streaming RTF.” → Needs Table `tab:h13` linked to `\\EvRowcolCompare`/`\\ShaRowcolCompare` and the underlying pinned CSV present.
- L95–L98: fixed-dropout robustness + “spatial augmentation reduces … degradation.” → Needs Table `tab:h12` linked to `\\EvSpatialDropout`/`\\ShaSpatialDropout` plus a pinned definition of how dropout masks are constructed/fixed.
- L108–L113: registry + “strict checker” + “key pinned evidence identifiers ….” → Needs the actual `paper/paper.json`, the checker/script/config that enforces “no handwritten numeric facts”, and the referenced evidence files shipped in the packet.

Numeric-handwriting violations (line numbers)
- None: no literal numeric *facts* appear in main.tex; digits occur only in non-fact tokens (format/citation keys/labels/filenames) and in generated table inputs.

Minor issues
- Table captions do not include provenance macros; add per-table “Evidence: `\\Ev… (\\Sha…)`” to make linkage local.
- Proxy-grid construction omits how unmapped channels are combined with grid embeddings; specify concat/sum/projection.
- “Temporal unfolding operator” is underspecified; define the exact operator.
- CER/RTF are named but not formally defined; add exact computation definitions and measurement conditions.
- “SpecAugment-inspired masking” lacks concrete parameters and axis definition.
- TopK/FPS-diverse TopK lack reproducible definitions; specify ranking signal and FPS distance on the proxy grid.
- Evidence hashes are exposed only as prefixes; full sha256 is in `paper/paper.json`.
- Tooling paths claimed in Artifacts are not in the provided review packet; ensure repo includes them and manuscript matches.
