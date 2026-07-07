# Anti-GPT Lint Report

- Generated: 2026-07-01T15:21:24+09:00
- File: `/Volumes/ly_backup/resc_before_erase/naokkimu/lyworks_ssd/epgspeller_local_workspace/epgspeller-lexicon-free-silent-spelling-recognition-with-electropalatography/paper/writing_loop/iter_001/manuscript_plain.txt`
- TOOL_ROOT: `/Users/naokkimu/Desktop/SLT_submission/extras/kimuras_word_distribution`

> Note: This report does **not** classify authorship. It surfaces rule-based *signals* that often read as generic assistant prose.

## Summary

- HIGH hits: 0 (rules fired: 0)
- MEDIUM hits: 2 (rules fired: 2)
- Kimura score/grade: 45/D

## Text Stats (computed)

- Characters: 32974
- Words: 4570
- Sentences: 224
- Avg sentence length: 20.4
- Sentence length variance: 108.49
- Long sentences (>40w): 9

## Kimura Style (computed)

- Score: 45
- Grade: D (要改善 - 大幅な修正が必要)

| Metric | Value |
|---|---:|
| `sentence_length` | 20.0 |
| `flesch_kincaid_grade` | 13.6 |
| `flesch_reading_ease` | 26.5 |
| `passive_ratio` | 0.191 |
| `awl_coverage` | 0.0435 |
| `hedge_per_1000` | 13.1 |
| `nominalization_per_1000` | 93.2 |

### Kimura Issues

- [DIFFICULTY_HIGH] 文章が難しすぎます (Grade 13.6 > 目標11.0)
- [NOMINALIZATION_HIGH] 名詞化が多すぎます (93.2/1000語 > 目標31.5)
- [LONG_SENTENCES] 40語以上の長文が 5 個あります

### Kimura Warnings

- [PASSIVE_HIGH] 受動態が多すぎます (19.1% > 目標10%)
- [AWL_LOW] 学術語彙が不足しています (4.3% < 目標10.9%)

## HIGH signals (remove for academic prose)

- (none)

## MEDIUM signals (often worth tightening)

### OVERCLAIMING_ADVERBS (1)

- Why: Overconfident adverbs (require evidence)
- Suggestion: Either justify with evidence/definition or remove the adverb.
- Examples:
  - Match: `clearly`
    - Context: plicit. Participants articulate continuously, and tongue--palate contact is not clearly segmented at the character level. EPGSpeller uses connectionist temporal classi

### VAGUE_INTENSIFIERS (1)

- Why: Vague intensifiers/adjectives
- Suggestion: Prefer quantitative or specific descriptors; avoid intensifiers when not supported by evidence.
- Examples:
  - Match: `highly`
    - Context: atial structure more explicitly, but electropalatographic contact is sparse and highly participant-dependent, so a strong two-dimensional spatial assumption is not al

## Repetition signals (heuristic)

- 8×: `lexicon free string decoding`
- 5×: `epg silent spelling can`
- 5×: `smartpalate style epg silent`
- 5×: `style epg silent spelling`
- 4×: `epg contact time series`
- 4×: `from the target user`
- 4×: `is treated as a`
- 3×: `a modern string decoder`
