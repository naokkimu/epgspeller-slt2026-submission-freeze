# Anti-GPT Lint Report

- Generated: 2026-07-01T18:26:09+09:00
- File: `/Volumes/ly_backup/resc_before_erase/naokkimu/lyworks_ssd/epgspeller_local_workspace/epgspeller-lexicon-free-silent-spelling-recognition-with-electropalatography/paper/writing_loop/iter_003/manuscript_plain.txt`
- TOOL_ROOT: `/Users/naokkimu/Desktop/SLT_submission/extras/kimuras_word_distribution`

> Note: This report does **not** classify authorship. It surfaces rule-based *signals* that often read as generic assistant prose.

## Summary

- HIGH hits: 0 (rules fired: 0)
- MEDIUM hits: 10 (rules fired: 1)
- Kimura score/grade: 50/C

## Text Stats (computed)

- Characters: 33147
- Words: 4742
- Sentences: 247
- Avg sentence length: 19.2
- Sentence length variance: 129.39
- Long sentences (>40w): 9

## Kimura Style (computed)

- Score: 50
- Grade: C (普通 - いくつかの改善が必要)

| Metric | Value |
|---|---:|
| `sentence_length` | 20.8 |
| `flesch_kincaid_grade` | 13.2 |
| `flesch_reading_ease` | 29.8 |
| `passive_ratio` | 0.151 |
| `awl_coverage` | 0.0463 |
| `hedge_per_1000` | 10.5 |
| `nominalization_per_1000` | 88.6 |

### Kimura Issues

- [DIFFICULTY_HIGH] 文章が難しすぎます (Grade 13.2 > 目標11.0)
- [NOMINALIZATION_HIGH] 名詞化が多すぎます (88.6/1000語 > 目標31.5)
- [LONG_SENTENCES] 40語以上の長文が 5 個あります

### Kimura Warnings

- [AWL_LOW] 学術語彙が不足しています (4.6% < 目標10.9%)

## HIGH signals (remove for academic prose)

- (none)

## MEDIUM signals (often worth tightening)

### EM_DASH (10)

- Why: Em dash usage (—) can read chatty
- Suggestion: Consider replacing em dashes with periods, commas, or parentheses for a more literal, translation-friendly style.
- Examples:
  - Match: `—`
    - Context: lent Spelling Recognition with Electropalatography Anonymous Submission Abstract—Hands-free character entry motivates decoding be- yond fixed command vocabularie
  - Match: `—`
    - Context: recognition-layer evaluation; interactive AAC input is future work. Index Terms—electropalatography, silent spelling, AAC, lexicon-free recognition, character-l
  - Match: `—`
    - Context: . Accordingly, bringing silent input closer to AAC requires spelling recognition—decoding character strings—rather than recognition confined to a closed vocabula

## Repetition signals (heuristic)

- 5×: `and low shot calibration`
- 5×: `from the target user`
- 4×: `cross user transfer and`
- 4×: `epg contact time series`
- 4×: `greedy character string decoding`
- 3×: `a multichannel time series`
- 3×: `character error rate cer`
- 3×: `connectionist temporal classification ctc`
