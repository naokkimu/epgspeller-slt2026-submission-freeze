# paper.json 面白さ重視レビュー（3査読＋メタレビュー）

## Inputs
- paper_json: /Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/paper.json
- root: /Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo
- generated_date: 2026-03-04

## Evidence Used
- results/related_work_survey_epgspeller_2026-02-17/fields.yaml
- results/related_work_survey_epgspeller_2026-02-17/outline.yaml
- results/paper_layout_2026-03-03/table_dataset_summary.csv
- results/paper_layout_2026-03-03/table_k64_p3.csv
- results/paper_layout_2026-03-03/table_spatial_p1.csv
- results/paper_layout_2026-03-03/table_spatial_p2.csv
- results/paper_layout_2026-03-03/table_spatial_p3.csv
- results/paper_layout_2026-03-03/table_k64_p1p2.csv
- results/paper_layout_2026-03-03/table_k64_all.csv
- results/paper_layout_2026-03-03/table_p3ms_compact.csv

## Summary (JSON)
```json
{
  "paper_type_guess": "experiment",
  "one_sentence_pitch": "監査可能なEPGサイレントスペリング評価を、複数プロトコルと多被験者で整理し、空間front-endと電極削減の効果を比較する。",
  "main_contributions": [
    "EPG silent spellingのprotocol整理と、監査可能なartifact固定による評価枠組み（results/related_work_survey_epgspeller_2026-02-17/outline.yaml）。",
    "空間front-end比較とK=64削減のprotocol別集計（results/paper_layout_2026-03-03/table_spatial_p1.csv, results/paper_layout_2026-03-03/table_spatial_p2.csv, results/paper_layout_2026-03-03/table_spatial_p3.csv, results/paper_layout_2026-03-03/table_k64_all.csv）。"
  ],
  "key_results": [
    {
      "result": "P1ではvecがCER 0.18±0.08で、gridはCER 0.31±0.15と高い。",
      "evidence_path": "results/paper_layout_2026-03-03/table_spatial_p1.csv"
    },
    {
      "result": "P3ではrowcolがCER 0.68±0.15、gridが0.75±0.09で、cross-participantでは誤り率が高い。",
      "evidence_path": "results/paper_layout_2026-03-03/table_spatial_p3.csv"
    },
    {
      "result": "P3のK=64ではtopkがCER 0.647±0.130で、削減でも性能低下は限定的。",
      "evidence_path": "results/paper_layout_2026-03-03/table_k64_p3.csv"
    }
  ],
  "overall_interest": 3,
  "overall_recommendation": "Weak Accept",
  "confidence": 3,
  "major_uncertainties": [
    "外部ベースラインとの位置づけが表からは判断できず、相対的な改善幅が不明（results/paper_layout_2026-03-03/table_spatial_p1.csv）。"
  ]
}
```

## Reviewer A (Novelty / Vision)
### Summary
監査可能なprotocol整理は価値があるが、新規性は「評価設計とartifact固定」に寄る（results/related_work_survey_epgspeller_2026-02-17/outline.yaml）。

### Strengths (面白さに直結する点)
- 空間front-endと電極削減をprotocol別にまとめた比較は、研究の方向性を整理できる（results/paper_layout_2026-03-03/table_spatial_p1.csv, results/paper_layout_2026-03-03/table_k64_all.csv）。

### Weaknesses / Risks (面白さを損なう点のみ)
- 外部比較が無く、得られた差分の「位置づけ」が弱くなる（results/paper_layout_2026-03-03/table_spatial_p1.csv）。

### Questions to the authors
- 外部ベースラインを入れられない理由はprotocolの不一致か、データの制約か（results/related_work_survey_epgspeller_2026-02-17/outline.yaml）。

### Requested analyses / experiments (あれば)
- なし。

### Scores (JSON)
```json
{"novelty": 2, "significance": 3, "surprise": 2, "interest": 3, "confidence": 3, "overall_recommendation": "Weak Accept"}
```

## Reviewer B (Skeptical / Prior-work positioning)
### Summary
protocol依存性を強調する立場からは、比較の範囲が限定的に見える（results/related_work_survey_epgspeller_2026-02-17/outline.yaml）。

### Strengths (面白さに直結する点)
- cross-participantとmulti-sourceを表で明示し、方向依存の比較ができる（results/paper_layout_2026-03-03/table_p3ms_compact.csv）。

### Weaknesses / Risks (面白さを損なう点のみ)
- grid系の不利が一貫しており、空間仮定の有効性が読み取りにくい（results/paper_layout_2026-03-03/table_spatial_p2.csv, results/paper_layout_2026-03-03/table_spatial_p3.csv）。

### Questions to the authors
- patchpoolやaugmentationの狙いと、どの条件で効くのかをもう少し明示できるか（results/paper_layout_2026-03-03/table_spatial_p3.csv）。

### Requested analyses / experiments (あれば)
- なし。

### Scores (JSON)
```json
{"novelty": 2, "significance": 3, "surprise": 2, "interest": 3, "confidence": 2, "overall_recommendation": "Weak Accept"}
```

## Reviewer C (Empirical / Practical impact)
### Summary
実用面ではcross-participantの誤り率が高く、限界も明確に示されている（results/paper_layout_2026-03-03/table_spatial_p3.csv）。

### Strengths (面白さに直結する点)
- K=64削減でも性能が大きく崩れないという観測は実用上の示唆がある（results/paper_layout_2026-03-03/table_k64_all.csv）。

### Weaknesses / Risks (面白さを損なう点のみ)
- cross-participantのCERが高く、汎化性能の強い主張は難しい（results/paper_layout_2026-03-03/table_spatial_p3.csv）。

### Questions to the authors
- participant間の差が大きい場合に、どの条件で転移が安定するか示せるか（results/paper_layout_2026-03-03/table_spatial_p3.csv）。

### Requested analyses / experiments (あれば)
- なし。

### Scores (JSON)
```json
{"novelty": 2, "significance": 3, "surprise": 2, "interest": 3, "confidence": 3, "overall_recommendation": "Weak Accept"}
```

## Meta-review
### Consensus
監査可能性とprotocol整理は価値があるが、外部比較が無い点が面白さ評価の上限になる（results/related_work_survey_epgspeller_2026-02-17/outline.yaml）。

### Main reasons
- protocol別比較が明確（results/paper_layout_2026-03-03/table_spatial_p1.csv）。
- cross-participantの難しさが残る（results/paper_layout_2026-03-03/table_spatial_p3.csv）。

### Required revisions for acceptance
- 外部比較を入れない理由と範囲限定の説明を強化する（results/related_work_survey_epgspeller_2026-02-17/outline.yaml）。

### Optional improvements
- participant追加の方向性を短く示す（results/related_work_survey_epgspeller_2026-02-17/outline.yaml）。
