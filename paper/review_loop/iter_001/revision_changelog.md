# Revision Changelog — iter_001

**Date:** 2026-06-30  
**Target file:** `paper/SLT_draft_clean.md`  
**Line count:** 778 → 798 (+20 lines)  
**Basis:** `paper/review_loop/iter_001/composite_writing_review.md`, `slt_review_simulation.md`, `slt_reviewer_*.md`

---

## Changes Applied

### 1. Notation standardization (Priority 1, Item 1)
- **What:** `subj1` → `p1` in Section 5.3 body text and Table `tab:silentspeller_lite` caption/cell.
- **What:** `subj3` → `p3` in Section 5.4 body text (×2) and Table `tab:kshot_curve` caption.
- **Why:** Composite reviewer R4 (Major): inconsistent participant labels `p1/P1/subj1`. Protocol labels P1–P3 refer to evaluation conditions; participant labels p1–p4 refer to individuals. All uses now consistent.

### 2. Contribution paragraph rewritten (Priority 1, Item 3 + Priority 2, Item 8)
- **What:** Rewrote the three-contribution paragraph in Introduction (previously lines 78–82). New structure:
  1. Task/protocol formulation (P1·P2·P3·k-shot taxonomy)
  2. Empirical calibration study with concrete CER numbers (P1: 0.1796, P2: 0.1451, k=1: 0.3503)
  3. Honest negative transfer results (P3: 0.6909)
  - Added explicit statement: "本稿の新規性は CTC 認識器のアーキテクチャではなく、このタスク・プロトコル定式化と較正実証研究にある。"
- **Why:** Composite reviewer R3 (Major): contribution list not sharply prioritized. SLT area-chair: "reframe contribution as recognition-layer + calibration study, not novel recognizer."

### 3. Boilerplate section-opening transitions removed (Priority 1, Item 6)
- **What:** 
  - Section 2 opening: removed two-sentence "前章では...本章では..." block; kept only the substantive third sentence.
  - Section 3 opening: merged three sentences into one concise opener; removed "前章でタスクを...定義したので" back-reference.
  - Section 4 opening: removed "前章では EPGSpeller の認識システムを定義した。" sentence entirely.
- **Why:** Composite reviewer R6–R12: redundant transitions. These sections were re-announcing content already stated in prior section closings.

### 4. AAC spacing fix (Priority 1, Item 7)
- **What:** The rewritten contribution paragraph (Change 2) uses `AAC向け` (no space before 向け) consistently, eliminating the `AAC 向け` variant that appeared on the old line 79.
- **Why:** Composite reviewer: style consistency. The manuscript convention is `AAC向け` (no space); one instance deviated.

### 5. Reproducibility section added — Section 3.7 (new) (Priority 2, Item 10)
- **What:** Inserted new Section 3.7 "再現性のための実装詳細" before the chapter summary (old 3.7 → new 3.9). Values sourced directly from `src/neural_decoder/conf/unified_config.yaml` and `config.yaml`:
  - GRU: nUnits=1024, nLayers=5, bidirectional, input_proj_dim=256
  - Time compression: kernelLen=32, strideLen=4
  - nClasses=40, dropout=0.4
  - Training: batchSize=64, lr=0.02, l2_decay=1e-5, nBatch=10,000
  - SpecAugment: time_mask T=12 p=0.4, electrode_mask F=6 p=0.4, time_warp W=0.05 p=0.2
  - Noise: white σ=0.1 p=0.3, drift σ=0.05 p=0.3, smooth width=2.0 p=0.3
  - PCA variant: 16 components
  - Seeds: 0–3 (4 runs), mean ± std reported
- **Why:** All three SLT reviewers flagged reproducibility gap (score 2/5). No numbers were fabricated; all values drawn from actual config files.

### 6. k-shot protocol clarified (Priority 2, Item 12)
- **What:** Added sentence to Section 4.4: "ここでの $k$-shot 較正は、訓練時に現れた語ラベルと同一の語について対象ユーザーから $k$ 例を取得するものであり、訓練時に存在しなかった未見語への一般化（P1 条件）とは区別する。"
- **Why:** SLT reviewer methodology-skeptic: "k-shot design underspecified." This clarifies the held-out repetitions of same word labels mechanism vs. the unseen-word generalization tested in P1.

### 7. SilentSpeller bridge sharpened (Priority 2, Item 9)
- **What:**
  - Section 4.5: First sentence rewritten to explicitly state the condition is a "controlled unseen-word diagnostic under the same input modality" and "not a replication of SilentSpeller's interactive system."
  - Section 5.3: Added explicit clarification that the evaluation is a "診断的評価" (diagnostic evaluation), not a replication.
- **Why:** Composite reviewer and SLT reviewers: confusion about whether this was claiming to reproduce SilentSpeller results. Now unambiguous.

### 8. AAC scope qualifiers added (Priority 1, Item 4)
- **What:** Section 6.6 ("補助代替コミュニケーションに向けた含意") substantially rewritten. Added explicit opening statement: "本稿の結果はすべて認識層のオフライン評価に基づいており、AACシステムとしての展開評価...は行っていない。" Deployment framing changed from confident to conditional ("潜在的に有用な性質").
- **Why:** Composite reviewer R2 (Major): AAC motivation broader than evidence base. SLT systems-pragmatist: "deployment claim under-evaluated — no end-to-end input study."

### 9. Ethics/privacy subsection added — Section 6.7 (new) (Priority 2, Item 11)
- **What:** Inserted new Section 6.7 "倫理・プライバシーに関する注記" before Limitations (old 6.7 → new 6.8, old 6.8 → new 6.9). Covers:
  - Intraoral EPG as biometric/behavioral data
  - Consent assumption (SilentSpeller provenance)
  - Offline-only scope (no real-time or remote processing)
  - Device hygiene (participant-specific devices; cross-contamination note for multi-user scenarios)
  - Future IRB requirement for longitudinal studies
- **Why:** All three SLT reviewers flagged ethics/privacy gap (scores 2–3). No invented IRB details; stated only verifiable scope facts and appropriate caveats.

### 10. Conclusion strengthened (Priority 1, Item 5)
- **What:** Section 7 conclusion rewritten to:
  - Open with explicit two-point summary of contributions (task formulation + calibration empirical study with numbers)
  - Second paragraph: EPGSpeller as CTC recognizer + "語彙非依存な認識層として成立しうることを具体的な数値で示した点が本稿の実証的な貢献"
  - Third paragraph: negative results retained; added k=1 number; added final AAC offline-only scope reminder
- **Why:** Composite reviewer: strengthen conclusion to foreground recognition-layer contribution AND calibration bottleneck.

---

## What Was NOT Changed
- No tables removed or result values altered
- No baselines added (out of scope for writing revision; empirical gap remains)
- No statistical intervals fabricated
- No new experimental conditions invented
- Core section structure (1–7) retained
- All existing citations retained
- Japanese academic prose style maintained throughout

## Remaining Open Issues (not addressable by writing revision alone)
1. Missing strong baselines — requires new experiments
2. Statistical validation — single CER values without confidence intervals across splits (4-seed std is reported for SilentSpeller condition but not for P1/P2/P3)
3. Dataset scale — 4 participants; cannot be expanded by revision
4. High-k calibration curve — data density insufficient; cannot be fabricated
