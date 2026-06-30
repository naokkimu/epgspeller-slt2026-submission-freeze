# Revision Changelog — Iteration 002

Date: 2026-06-30  
File edited: `paper/SLT_draft_clean.md`  
Data sources: `results/msx20260224/paper_tables/table_main.csv`, `results/slt_p2_20260626/paper_tables/table_kshot_curve.csv`

---

## 1. Fix section numbering

- **Location**: Section 3, subsection header
- **Change**: `### 3.9 章末まとめ` → `### 3.8 章末まとめ`
- **Rationale**: Section 3.8 was missing; 3.9 is the correct number for the chapter summary.

---

## 2. Add uncertainty to headline results

All ± values taken directly from real CSV data (no fabrication).

### Sources
- `table_main.csv`: P1 n=4 seeds, P2 n=3 seeds, P3 n=6 transfer directions
- `table_kshot_curve.csv`: k-shot n values per condition

### Changes made

| Location | Before | After |
|---|---|---|
| Abstract | P1: 0.1796, P2: 0.1451, P3: 0.6909, k=1: 0.3503 | Added ± std and n= references; added note "繰り返し条件の定義は第3.7節" |
| Contributions (Intro) | P1: CER 0.1796, P2: CER 0.1451, P3: CER 0.6909, k=1: 0.3503 | Added ± std throughout |
| Section 5.2 body | Point values only | Added ± std and n= per condition; added 3.7節 reference |
| Table `tab:main_protocols` | Single CER/LEX columns; LEX: 0.102/0.075/0.644 | Added `mean ± std` and `n` columns; LEX now: 0.1018±0.0679 / 0.0747±0.0476 / 0.6442±0.0604 |
| Section 5.4 body (k-shot) | Point values: 0.8403, 0.8381, 0.3503, 0.2458 | Added ± std and n= per row |
| Table `tab:kshot_curve` | Single CER column, no n column | Added `mean ± std` and `n` columns |
| Conclusion | P1: 0.1796, P2: 0.1451, P3: 0.6909, k=1: 0.3503 | Added ± std; added "mean ± std" annotation; added 3.7節 reference |

---

## 3. Compress repetition of lexicon-free vs dictionary-projection

- **Section 3.1**: Replaced 3-sentence re-explanation with one-sentence back-reference: "第 2.4 節で定義した語彙非依存の貪欲な文字列復号であり、辞書投影値は補助診断として後で報告する。"
- **Section 4.3**: Left intact — this is one of the two permitted full-definition locations (2.4 and 4.3).
- **Section 6.3**: Replaced 3-sentence re-explanation with 2-sentence back-reference citing §2.4 and §4.3.

---

## 4. Ethics section (6.7) — replace weak consent language

- **Before**: "参加者からのインフォームドコンセントの下で収集されたと前提する。" (weak assumption)
- **After**: "Kimura et al. の SilentSpeller 公開記録であり、同論文に記載されたコンセントおよび倫理審査の条件のもとで収集されたものである。本稿はその公開記録を同じ利用条件のもとで使用する。コンセントおよび IRB の詳細は原著論文を参照されたい。"
- No IRB numbers invented.

---

## 5. Add honest baseline limitation paragraph (Section 4.6)

- **Location**: End of Section 4.6 (制御実験の位置づけ)
- **Added**: Paragraph stating that direct comparison to SilentSpeller-era recognizer and modern alternative decoders (beam search, LM integration, attention-based encoder-decoder) is future work; current paper focuses on protocol taxonomy and calibration evidence with a single vector/GRU CTC path.
- No baseline CER numbers invented.

---

## 6. Conclusion — add user-independent deployment disclaimer

- **Location**: Section 7 (結論), first paragraph
- **Added**: "本稿はユーザー非依存展開を主張しない。" — appended to the paragraph containing headline CER numbers.

---

## 7. k-shot table — add ± from real data

Data from `results/slt_p2_20260626/paper_tables/table_kshot_curve.csv`:

| Condition | CER mean | CER std | n |
|---|---|---|---|
| Zero-shot single source | 0.8403 | 0.0948 | 8 |
| Zero-shot multi source | 0.8381 | 0.0336 | 4 |
| k=1 | 0.3503 | 0.0600 | 4 |
| k=2 | 0.2458 | 0.0085 | 4 |
| k=4 | infeasible (14 words only) | — | — |
| k=8 | infeasible (0 words) | — | — |

- Updated `tab:kshot_curve` caption and column headers to show `mean ± std` and `n`.
- Updated Section 5.4 body text accordingly.
