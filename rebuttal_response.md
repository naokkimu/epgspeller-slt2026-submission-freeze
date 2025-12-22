Author Response

We thank the reviewers for the constructive feedback. We will revise the manuscript for clearer positioning and exposition: (i) define all abbreviations at first use; (ii) unify PCA notation as “PCA (k=…)”; and (iii) restructure Sec. 2 to focus on prior SSR/CTC-based decoding work, moving general EPG motivation to background.

Baseline / horizontal comparison (R3, R6). To address the concern about limited baselines, we evaluated constrained decoding baselines under the identical EPG recordings, identical splits, identical preprocessing (PCA k=32), and the same metric (CER). Under the held-out-word protocol (unseen words at test time), open-vocabulary greedy decoding achieves test CER=0.1156. Constraining predictions by projecting to the training lexicon only yields test CER=0.3859 (word-level accuracy is necessarily 0 under this protocol because test words are unseen in the training lexicon). For reference, projecting to the full (oracle) vocabulary provides an upper bound of test CER=0.0719 when the vocabulary is known.

We further evaluated a complementary seen-word protocol (instance holdout: one rendition per word for training and the other for testing) on two subjects (2328 samples, 1164 words each; 2 renditions/word). Under this protocol, open-vocabulary greedy decoding yields mean±std test CER 0.1306±0.0104 (n=4 runs: 2 subjects × 2 seeded splits), while constraining predictions by projecting to the training lexicon improves to 0.0781±0.0089. Together, these results quantify the trade-off: constrained decoding is beneficial when the vocabulary is known/seen, whereas open-vocabulary decoding is required for genuinely unseen words.

SpecAugment / PCA consistency (R3 Q1). We added the missing condition using the final setting (PCA k=32) with online SpecAugment. With PCA(k=32), SpecAugment improves test CER from 0.1156 to 0.1109; we will clarify which configuration is used in each experiment and keep it consistent across tables.

Split robustness (R3 Q2, R6). Across three seeded held-out-word splits (SpecAugment OFF, greedy decoding), mean±std test CER is 0.1302±0.0122.

Single-subject scope, representation choice, and model size (R7559). We will explicitly scope the current study as a case study and add a concrete generalization plan (additional speakers, normalization, and few-shot calibration). We chose PCA as a data-efficient, low-compute spatial compression and will expand this rationale; we will also discuss model size as a limitation and add a lightweight-architecture ablation and/or efficiency discussion in the camera-ready.


