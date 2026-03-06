# Interspeech査読シミュレーション（複数レビュワー＋メタレビュー）

## Inputs
- narrative: `paper/submission/interspeech2026_review.pdf`
- root: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- generated_date: 2026-03-05

## Evidence Used
- `paper/submission/interspeech2026_review.pdf`
- `paper/submission/interspeech2026_review.tex`
- `paper/paper.json`
- `results/paper_layout_2026-03-03/table_main_compact.csv`
- `results/paper_layout_2026-03-03/table_to4_compact.csv`
- `results/paper_layout_2026-03-03/table_spatial_all.csv`
- `results/paper_layout_2026-03-03/table_k64_all.csv`
- `results/paper_layout_2026-03-03/table_kshot_compact.csv`
- `reviews/curated/INTSP2026_STATIC_e558be0f_de16d6d4__static_checks.md`
- `/Users/naokkimu/.codex/skills/texpdf-interspeech-review/references/llm_review_strategy.md`
- `/Users/naokkimu/.codex/skills/texpdf-interspeech-review/references/rekimoto_kenkyuuhou.yaml`

## Summary (JSON)
```json
{
  "paper_type_guess": "experiment",
  "one_sentence_pitch": "監査済みプロトコルでEPG silent spellingを分離評価し、cross-participant転移の難しさとpaired-sourceの条件付き改善を定量化した研究。 (evidence: paper/submission/interspeech2026_review.tex; results/paper_layout_2026-03-03/table_main_compact.csv; results/paper_layout_2026-03-03/table_to4_compact.csv)",
  "main_contributions": [
    "P1/P2/P3を分離する監査可能プロトコルとchecksum-pinned artifact導線を提示。 (evidence: paper/submission/interspeech2026_review.tex; paper/paper.json)",
    "vector/rowcol/grid系を同一評価ハーネスで比較し、空間前段の効果を条件付きで提示。 (evidence: results/paper_layout_2026-03-03/table_spatial_all.csv)",
    "p4 target transferでsingle-sourceとpaired-sourceを同条件比較し、aggregate改善と方向依存を併記。 (evidence: results/paper_layout_2026-03-03/table_to4_compact.csv)"
  ],
  "key_results": [
    {"result": "P3はCER 0.691±0.133で、P1 0.180±0.084およびP2 0.145±0.063より明確に高い。", "evidence_path": "results/paper_layout_2026-03-03/table_main_compact.csv"},
    {"result": "p4 aggregateではCERが0.686±0.114から0.582±0.064へ、LEXが0.659±0.073から0.554±0.034へ低下。", "evidence_path": "results/paper_layout_2026-03-03/table_to4_compact.csv"},
    {"result": "k-shotではvec/rowcolはk1→k2で改善する一方、grid系は悪化し、改善はモデル依存。", "evidence_path": "results/paper_layout_2026-03-03/table_kshot_compact.csv"}
  ],
  "overall_recommendation": "Weak Accept",
  "confidence": 3,
  "major_uncertainties": [],
  "llm_review_countermeasures_summary": {
    "summary": "査読で重視される形式整合性・主張校正・適用範囲限定が本文中で明示されているため、過大主張リスクは低減している。",
    "evidence_path": "/Users/naokkimu/.codex/skills/texpdf-interspeech-review/references/llm_review_strategy.md"
  },
  "rekimoto_comment_summary": {
    "summary": "1行クレームと主要差分の数値アンカーが前面化され、導入の芯は改善している。",
    "evidence_path": "/Users/naokkimu/.codex/skills/texpdf-interspeech-review/references/rekimoto_kenkyuuhou.yaml"
  }
}
```

## LLMレビュー対策（独立セクション）
### Summary
- 静的チェックは error 0, warning 0 で、abstract要件とページ要件を満たしている。 (evidence: reviews/curated/INTSP2026_STATIC_e558be0f_de16d6d4__static_checks.md)

### Priority Fixes
- なし（形式ゲートは通過）。 (evidence: reviews/curated/INTSP2026_STATIC_e558be0f_de16d6d4__static_checks.md)

### Questions to the authors
- supplementary統計表へのアクセス導線を提出時に明示できるか。 (evidence: paper/submission/interspeech2026_review.tex)

## 暦本コメント（独立セクション）
### Summary
- Abstract/Resultsで最重要差分が定量化され、メッセージの焦点は改善した。 (evidence: paper/submission/interspeech2026_review.tex)

### Key Critiques
- 本文中の「Table tab:*」表記は機械可読性には有効だが、自然文としては簡潔化余地が残る。 (evidence: paper/submission/interspeech2026_review.tex)

### Questions to the authors
- 最終版で読者向け可読性を上げるため、表参照文をもう一段自然化するか。 (evidence: paper/submission/interspeech2026_review.tex)

## Reviewer A
### Summary
- 再現性と評価設計は強く、主結果の訴求も改善した。

### Strengths
- protocol分離とartifact pinningが明示されている。 (evidence: paper/submission/interspeech2026_review.tex; paper/paper.json)
- p4 aggregate改善が本文で定量的に示される。 (evidence: results/paper_layout_2026-03-03/table_to4_compact.csv)

### Weaknesses / Risks
- p4 target-only制約によりcross-participant一般化の範囲は依然限定的。 (evidence: paper/submission/interspeech2026_review.tex)

### Questions to the authors
- target-only制約下での実運用想定をどこまで主張範囲に含めるか。 (evidence: paper/submission/interspeech2026_review.tex)

### Requested analyses / experiments (あれば)
- なし（現時点は主張校正で十分）。

### Scores (JSON)
```json
{"novelty": 3, "technical_quality": 4, "significance": 3, "clarity": 4, "relevance": 4, "confidence": 3, "overall_recommendation": "Weak Accept"}
```

## Reviewer B
### Summary
- 条件依存の結果を隠さず記述しており、技術的誠実性は高い。

### Strengths
- P3難易度とto4改善を同時に提示し、主張が校正されている。 (evidence: results/paper_layout_2026-03-03/table_main_compact.csv; results/paper_layout_2026-03-03/table_to4_compact.csv)

### Weaknesses / Risks
- spatial front-endの優位は一貫せず、理論的な一般則は限定的。 (evidence: results/paper_layout_2026-03-03/table_spatial_all.csv)

### Questions to the authors
- spatial biasを採用する判断基準を、遅延制約ごとにさらに明文化できるか。 (evidence: paper/submission/interspeech2026_review.tex)

### Requested analyses / experiments (あれば)
- なし。

### Scores (JSON)
```json
{"novelty": 3, "technical_quality": 4, "significance": 3, "clarity": 4, "relevance": 4, "confidence": 3, "overall_recommendation": "Weak Accept"}
```

## Reviewer C
### Summary
- 以前より主メッセージが読み取りやすく、採択判断に必要な情報が揃っている。

### Strengths
- Abstractで最重要定量差分が先出しされている。 (evidence: paper/submission/interspeech2026_review.tex)
- 形式ルール違反が見当たらない。 (evidence: reviews/curated/INTSP2026_STATIC_e558be0f_de16d6d4__static_checks.md)

### Weaknesses / Risks
- 表数はまだ多く、読者の負荷は中程度に残る。 (evidence: paper/submission/interspeech2026_review.tex)

### Questions to the authors
- 口頭発表向けに最小セットの図表をどう提示するか。 (evidence: paper/submission/interspeech2026_review.tex)

### Requested analyses / experiments (あれば)
- なし。

### Scores (JSON)
```json
{"novelty": 3, "technical_quality": 4, "significance": 3, "clarity": 4, "relevance": 4, "confidence": 2, "overall_recommendation": "Weak Accept"}
```

## Meta-review
### Consensus
- 監査可能性と主張校正が強みで、結果の条件依存も適切に限定されている。

### Main reasons
- P3難易度とto4 aggregate改善が同時に定量提示され、過大主張が抑制されている。 (evidence: results/paper_layout_2026-03-03/table_main_compact.csv; results/paper_layout_2026-03-03/table_to4_compact.csv)

### Required revisions for acceptance
- 必須修正なし（現状の校正水準で投稿可能）。

### Optional improvements
- 表参照文の自然化と、補助資料導線の明示を最終調整として検討。 (evidence: paper/submission/interspeech2026_review.tex)
