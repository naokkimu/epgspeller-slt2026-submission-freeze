# Supplemental Material Strategy — EPGSpeller SLT 2026

> **Canonical skill:** `~/.codex/skills/llm-audit-supplement-zip` (lessons learned, FAQ tiers, build script, scaffold). This file is project-local notes only.

## Design principle

**The main paper stands alone.** Every claim needed to understand the contribution, protocols, headline numbers, and limitations must remain in the 6-page manuscript. The supplement is not a page-limit workaround; it is a **review accelerator** and **audit surface**.

**The supplement pre-answers FAQs.** Reviewers who wonder “where did this number come from?”, “is this cherry-picked?”, or “why no baseline X?” should find a direct, traceable answer without emailing the authors.

**The supplement is LLM-friendly.** A reviewer (or their coding agent) can load a small, named bundle and verify claim ↔ artifact links in minutes.

Venue constraints ([SLT 2026 authors instructions](https://attend.ieee.org/slt-2026/authors-instructions/)):
- PDF or zip; double-blind; anonymized.
- Reviewers are **encouraged but not obliged** to read it — so the entry file name and first paragraph must sell the value in 10 seconds.
- Rebuttal **must not** refer to supplementary material — design the supplement for **initial review only**.

---

## Two-layer deliverable

| Layer | Audience | Format | Role |
|---|---|---|---|
| **A. Human supplement** | Human reviewers skimming tables | `supplement.pdf` (optional, ≤ few pages) | Extended tables, split definitions, hyperparameter table, SilentSpeller-lite protocol diff |
| **B. Audit bundle** | Reviewers + LLM agents | `put_this_audit_*.md/yaml` inside zip | Traceability, FAQ, deferred-experiment honesty, agent instructions |

Submit **one zip** containing both layers. Name the zip for OpenReview, e.g. `EPGSpeller_supplement.zip` (anonymized, no author paths in file contents).

---

## FAQ preemption map (priority order)

Derived from `paper/source/questions.yaml` (`reviewer_risk`) and `paper/review_loop/iter_009/`.

### Tier 1 — likely review comments (must have evidence in bundle)

| FAQ | Mitigation artifact(s) |
|---|---|
| Greedy CER vs LEX / hidden post-processing | `table_main_compact.csv`, `table_silentspeller_lite.csv`, metric paragraph in FAQ |
| Protocol cherry-picking (P1/P2/P3) | `protocol_split_summary.csv`, `protocol_split_vocab_sets.json`, FAQ protocol table |
| SilentSpeller “exact reproduction”? | `slt_p2_report.md`, `table_silentspeller_lite.csv`, FAQ “compatible-lite” diff |
| k-shot curve incomplete (k=4,8) | `kshot_feasibility.csv`, FAQ with per-word repetition counts |
| Cross-user failure = trivial normalization? | `preproc_ablation_report.md`, `table_preproc_protocol_condition.csv` |
| Missing external baselines | `put_this_audit_deferred_experiments.yaml` — **honest deferral**, not hidden |
| n=4 healthy participants | `dataset_summary.csv`, limitations cross-ref in FAQ |
| No interactive AAC / WPM study | FAQ: offline CER/RTF scope; deferred D-AAC-1 |
| Spatial front-end claimed as novelty? | `table_spatial_k124.csv`, `table_k64_methods.csv` — ablation framing |
| Numbers match paper tables? | `put_this_audit_claim_trace.md` + SHA256 in manifest |

### Tier 2 — methodology clarity (short FAQ entries)

| FAQ | Mitigation |
|---|---|
| What does EPG measure? | `dataset_audit/report.md` excerpt + FAQ |
| Lexicon-free vs closed-vocab commands | related-work coverage matrix + FAQ |
| In-task baselines vs production architecture | FAQ + `table_k64_p1p2.csv` |
| Multi-source P3MS details | `table_p3ms.csv`, `p3ms_all_targets_summary.csv` |

### Tier 3 — do **not** oversell in supplement

- Full `evidence/index.yaml` (12k lines) — ship a **curated manifest** only.
- Internal review-loop raw logs — useful internally; too meta for reviewers unless anonymized summary.
- Format/aesthetic audit PNGs — camera-ready already PASS; skip unless asked.

---

## File naming convention (`put_this_audit_*`)

Names sort to the top of any directory listing and signal intent without breaking anonymity.

```
paper/supplement/
├── put_this_audit_START_HERE.md          # 30-second orientation; point LLM here
├── put_this_audit_agent_instructions.md  # step-by-step verification workflow
├── put_this_audit_reviewer_FAQ.yaml      # structured Q → answer → evidence paths
├── put_this_audit_claim_trace.md         # curated claim ↔ CSV ↔ SHA256 (from generated/)
├── put_this_audit_deferred_experiments.yaml  # D-BASE-1, D-N-1, D-AAC-1 — explicit scope
├── put_this_audit_evidence_manifest.yaml # ~40 artifacts max, not full index
├── tables/                               # copies of results/*/paper_tables/*.csv
├── reports/                              # split audit, slt_p2, preproc reports (anonymized)
└── supplement.pdf                        # optional human-facing tables
```

### `put_this_audit_START_HERE.md` (content contract)

1. One sentence: main paper is self-contained; this bundle helps **verify** claims.
2. Three-step quick start for humans.
3. Copy-paste block for LLM: “Read START_HERE → FAQ → claim_trace; verify table X against paper Table Y.”
4. Explicit **non-goals**: no new experiments, no identity, no page-limit extension.

### `put_this_audit_reviewer_FAQ.yaml` (schema)

```yaml
- id: FAQ-001
  question: "Is greedy CER the primary metric?"
  short_answer: "Yes. LEX and RTF are supplementary diagnostics only."
  paper_pointers: ["Table I", "Sec. IV-A"]
  evidence:
    - path: tables/table_main_compact.csv
      sha256: "..."
  status: answered
```

---

## Main paper — one sentence (proposed)

Add to **Limitations, Ethics, and Reproducibility** (replace or extend current line 23):

> Reproducibility details, extended tabulated results, and an anonymized audit bundle (`put_this_audit_START_HERE.md` in the supplementary zip) map each headline result to underlying split definitions and CSV artifacts for independent verification; the main text remains self-contained if the supplement is not consulted.

Constraints:
- No filesystem paths beyond the **entry filename** (writing loop already removed repo paths from body).
- No “please use ChatGPT” — say “independent verification” / “coding agents” neutrally.

---

## Double-blind checklist before zip

- [ ] Strip absolute paths (`/Users/...`, `/Volumes/...`) from all bundled files
- [ ] No author names, grant IDs, institutional URLs, or identifiable self-citations in supplement text
- [ ] Config tables: hyperparameters only, no usernames or cluster paths
- [ ] If citing prior work in FAQ, use third person (“Kimura et al.”) not “our CHI 2022 work”
- [ ] Zip internal README does not mention qpaper/internal tooling brands unless anonymized

---

## What stays **out** of the supplement (and why)

| Item | Reason |
|---|---|
| New baseline runs | Not done; belongs in deferred_issues + rebuttal-phase work |
| Full training code with secrets | Anonymization burden; defer to acceptance / separate release |
| 12k-line evidence index | Noise for LLM context; curated manifest instead |
| Review-loop iter_009 raw reviews | Meta; extract FAQ entries only |

---

## Build pipeline (implementation order)

1. **Curate** `put_this_audit_evidence_manifest.yaml` (~40 artifacts tied to paper tables).
2. **Generate** `put_this_audit_reviewer_FAQ.yaml` from `questions.yaml` reviewer_risk + iter_009 gaps.
3. **Copy** CSVs/reports into `supplement/tables/` and `supplement/reports/`; re-hash.
4. **Trim** `claim_to_evidence.md` → `put_this_audit_claim_trace.md` (paper claims only).
5. **Write** `put_this_audit_deferred_experiments.yaml` from `deferred_issues.yaml`.
6. **Draft** optional `supplement.pdf` (IEEE-like or plain table PDF, 2–4 pages).
7. **Anonymize pass** + zip + smoke test: load START_HERE in fresh LLM session, ask “verify Table II P1 CER.”

---

## Success criteria

- A skeptical reviewer can answer “where is P1 CER from?” in **< 2 minutes** without repo access.
- An LLM given only the zip can trace **every number in Table II** to a CSV row + SHA256.
- Deferred experiments (external baselines, n>4, interactive AAC) are **visible and bounded**, not discoverable only as weaknesses.
- Main paper reads identically if the supplement is deleted.

---

## Open decisions

1. **supplement.pdf**: include or zip-only markdown/CSV? Recommendation: include 2-page PDF **plus** audit markdown (PDF for humans, yaml for agents).
2. **Anonymous code**: ship decoders/configs in supplement or omit entirely for v1? Recommendation: omit code v1; ship config table + split JSON only.
3. **Related-work survey report**: include 30-page report or 1-page FAQ excerpt? Recommendation: FAQ excerpt + coverage_matrix.csv only.
