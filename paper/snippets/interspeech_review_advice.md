# Interspeech査読向けリビジョン・アドバイス（paper.jsonベース）

## Inputs
- paper_json: `paper/paper.json`
- root: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- generated_date: 2026-03-05

## Evidence Used
- `paper/paper.json`
- `paper/submission/interspeech2026_review.tex`
- `results/paper_layout_2026-03-03/table_main_compact.csv`
- `results/paper_layout_2026-03-03/table_to4_compact.csv`
- `results/paper_layout_2026-03-03/table_spatial_all.csv`
- `reviews/curated/INTSP2026_STATIC_e558be0f_de16d6d4__static_checks.md`

## Advice Summary (JSON)
```json
{
  "must_fix": [],
  "should_improve": [
    "Results本文の\"Table tab:*\"参照文を、最終版でより自然な英文にする。 (evidence: paper/submission/interspeech2026_review.tex)",
    "supplementary統計表へのアクセス方法を本文または提出メタデータで明示する。 (evidence: paper/submission/interspeech2026_review.tex)"
  ],
  "nice_to_have": [
    "Abstractの先頭文をさらに短縮し、主要差分に到達するまでの文数を減らす。 (evidence: paper/submission/interspeech2026_review.tex)",
    "P3MS条件依存の一文をDiscussion末尾に再掲し、誤読をさらに減らす。 (evidence: results/paper_layout_2026-03-03/table_to4_compact.csv)"
  ],
  "confidence": 4
}
```

## 評価軸別アドバイス
- Novelty: 監査可能プロトコル設計の価値は十分に提示できている。 (evidence: paper/paper.json)
- Technical quality: 主結果の定量アンカーが本文に入り、説得力が改善した。 (evidence: results/paper_layout_2026-03-03/table_main_compact.csv; results/paper_layout_2026-03-03/table_to4_compact.csv)
- Significance: P3難易度とto4改善の同時提示で、実務上の含意が明確化した。 (evidence: paper/submission/interspeech2026_review.tex)
- Clarity: 主要修正は完了したが、表参照文の自然化で最終可読性を上げられる。 (evidence: paper/submission/interspeech2026_review.tex)
- Relevance: SSI/EPG文脈とsilent spelling framingは維持されている。 (evidence: paper/submission/interspeech2026_review.tex)

## paper.json への具体的修正提案（ブロック/セクション）
- 現時点の必須修正はなし。
- 任意調整候補:
  - `b_results_main`, `b_results_spatial`, `b_results_to4`, `b_results_k64`, `b_results_kshot`, `b_results_p3ms`, `b_results_kcurve` の参照文を最終読み上げ向けに微修正。
  - `b_abs` の先頭一文を短縮して、主結果提示までの遅延を削減。

## 新規データが必要な項目
- なし。現時点の改善は文面調整のみで対応可能。
