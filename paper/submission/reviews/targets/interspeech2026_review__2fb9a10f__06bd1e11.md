# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 24527,
    "max_chars": 120000,
    "media_boxes": [
      {
        "height_pt": 841.89,
        "page": 1,
        "width_pt": 595.276
      },
      {
        "height_pt": 841.89,
        "page": 2,
        "width_pt": 595.276
      },
      {
        "height_pt": 841.89,
        "page": 3,
        "width_pt": 595.276
      },
      {
        "height_pt": 841.89,
        "page": 4,
        "width_pt": 595.276
      },
      {
        "height_pt": 841.89,
        "page": 5,
        "width_pt": 595.276
      },
      {
        "height_pt": 841.89,
        "page": 6,
        "width_pt": 595.276
      }
    ],
    "page_count": 6,
    "path": "interspeech2026_review.pdf",
    "sha256": "2fb9a10f29e3d75d4693df87e90438a76960adf50b7e5e47789c4aa9ef64005f",
    "sha8": "2fb9a10f",
    "truncated": false
  },
  "rules": "/Users/naokkimu/.codex/skills/interspeech-manuscript-review/references/interspeech2026_rules.yaml",
  "rules_meta": {
    "source": {
      "kind": "overleaf_template",
      "notes": "Rules extracted from the template instructions embedded in the Overleaf source and abstract comments.",
      "retrieved_local_date": "2026-02-24",
      "title": "Interspeech Paper Kit",
      "url": "https://www.overleaf.com/latex/templates/interspeech-paper-kit/svqkgcpdbxfg"
    },
    "venue": "Interspeech",
    "year": 2026
  },
  "stage": "review",
  "tex": {
    "abstract": {
      "found": true,
      "plain_characters": 990
    },
    "documentclass": {
      "class": "Interspeech",
      "found": true,
      "has_cameraready": false,
      "is_interspeech": true,
      "options": [],
      "options_raw": ""
    },
    "path": "interspeech2026_review.tex",
    "sha256": "06bd1e1193b79ab78da89e5b68ddefc0b317e44ca323f39baaa85848d70b25fc",
    "sha8": "06bd1e11"
  }
}
```

## Static checks (JSON)

```json
{
  "checks": [
    {
      "evidence": {},
      "id": "abstract_ascii",
      "message": "abstract is ASCII-only",
      "ok": true,
      "severity": "info"
    },
    {
      "evidence": {
        "abstract_chars": 990,
        "max_characters": 1000
      },
      "id": "abstract_length",
      "message": "abstract_chars=990 <= max_characters=1000",
      "ok": true,
      "severity": "info"
    },
    {
      "evidence": {},
      "id": "abstract_no_citations",
      "message": "no \\cite* in abstract",
      "ok": true,
      "severity": "info"
    },
    {
      "evidence": {
        "required_title": "Generative AI Use Disclosure"
      },
      "id": "ai_disclosure_present",
      "message": "Generative AI Use Disclosure section not found",
      "ok": false,
      "severity": "info"
    },
    {
      "evidence": {
        "documentclass": {
          "class": "Interspeech",
          "found": true,
          "has_cameraready": false,
          "is_interspeech": true,
          "options": [],
          "options_raw": ""
        }
      },
      "id": "anonymity_cameraready_flag",
      "message": "no cameraready option in review stage",
      "ok": true,
      "severity": "info"
    },
    {
      "evidence": {
        "email_hits": []
      },
      "id": "anonymity_email_heuristic",
      "message": "no email-like strings detected in extracted PDF text",
      "ok": true,
      "severity": "info"
    },
    {
      "evidence": {
        "banned_token_re": "\\\\b(TBD|TODO|placeholder|mock)\\\\b",
        "hits": []
      },
      "id": "banned_tokens",
      "message": "no banned tokens",
      "ok": true,
      "severity": "info"
    },
    {
      "evidence": {
        "max_pages": 6,
        "page_count": 6
      },
      "id": "page_limit",
      "message": "page_count=6 <= max_pages=6",
      "ok": true,
      "severity": "info"
    }
  ],
  "format": {
    "name": "interspeech-static-review",
    "version": "0.1.0"
  },
  "inputs": {
    "ai_tools_used": "unknown",
    "paper_type": "regular",
    "pdf": {
      "extracted_chars": 24527,
      "max_chars": 120000,
      "media_boxes": [
        {
          "height_pt": 841.89,
          "page": 1,
          "width_pt": 595.276
        },
        {
          "height_pt": 841.89,
          "page": 2,
          "width_pt": 595.276
        },
        {
          "height_pt": 841.89,
          "page": 3,
          "width_pt": 595.276
        },
        {
          "height_pt": 841.89,
          "page": 4,
          "width_pt": 595.276
        },
        {
          "height_pt": 841.89,
          "page": 5,
          "width_pt": 595.276
        },
        {
          "height_pt": 841.89,
          "page": 6,
          "width_pt": 595.276
        }
      ],
      "page_count": 6,
      "path": "interspeech2026_review.pdf",
      "sha256": "2fb9a10f29e3d75d4693df87e90438a76960adf50b7e5e47789c4aa9ef64005f",
      "sha8": "2fb9a10f",
      "truncated": false
    },
    "rules": "/Users/naokkimu/.codex/skills/interspeech-manuscript-review/references/interspeech2026_rules.yaml",
    "rules_meta": {
      "source": {
        "kind": "overleaf_template",
        "notes": "Rules extracted from the template instructions embedded in the Overleaf source and abstract comments.",
        "retrieved_local_date": "2026-02-24",
        "title": "Interspeech Paper Kit",
        "url": "https://www.overleaf.com/latex/templates/interspeech-paper-kit/svqkgcpdbxfg"
      },
      "venue": "Interspeech",
      "year": 2026
    },
    "stage": "review",
    "tex": {
      "abstract": {
        "found": true,
        "plain_characters": 990
      },
      "documentclass": {
        "class": "Interspeech",
        "found": true,
        "has_cameraready": false,
        "is_interspeech": true,
        "options": [],
        "options_raw": ""
      },
      "path": "interspeech2026_review.tex",
      "sha256": "06bd1e1193b79ab78da89e5b68ddefc0b317e44ca323f39baaa85848d70b25fc",
      "sha8": "06bd1e11"
    }
  },
  "run_id": "INTSP2026_STATIC_2fb9a10f_06bd1e11"
}
```

## TeX preamble (first 200 lines)

```tex
% Auto-generated from paper/paper.json (paper-json v1.0.0). Do not edit by hand.
% Target: INTERSPEECH 2026 Paper Kit (Interspeech.cls).
\documentclass{Interspeech}
\usepackage{placeins}
\usepackage{float}

\title{EPGSpeller: Lexicon-Free Silent Spelling Recognition with Electropalatography}
\keywords{silent speech interface, electropalatography, character-level decoding, text entry, auditability}

```

## PDF extracted text (page-separated, deterministic truncation)

=== PAGE 1 ===
EPGSpeller: Lexicon-Free Silent Spelling Recognition with
Electropalatography
Anonymous submission to Interspeech 2026
Abstract1
We show that lexicon-free electropalatography (EPG) silent2
spelling can reach low error in audited within-participant set-3
tings (CER 0.180+/-0.084 in P1 and 0.145+/-0.063 in P2). Pro-4
tocol mixing still obscures progress when word holdout, in-5
stance holdout, and cross-participant transfer are reported to-6
gether. We present EPGSpeller, an auditable benchmark with7
deterministic splits, checksum-pinned artifacts, and a shared8
CER/LEX/RTF harness for protocol-matched comparison. In9
652 audited runs, P3 remains much harder (CER 0.691+/-10
0.133), marking transfer mismatch as the main bottleneck.11
Rowcol stays closest to vec, while grid variants are usually12
higher in CER and RTF. For p4 target transfer, paired-source13
aggregation improves the all-direction aggregate (CER 0.686+/-14
0.114 to 0.582+/-0.064; LEX 0.659+/-0.073 to 0.554+/-0.034),15
but effects remain mixed by direction. We therefore treat de-16
ployment claims as protocol-specific and limit conclusions to17
audited datasets and definitions.18
Index Terms: silent speech interface, electropalatography,19
character-level decoding, text entry, auditability20
1. Introduction21
Silent speech interfaces (SSI) infer linguistic intent from22
non-acoustic signals, including articulatory sensing and other23
biosignals. For silent spelling with electropalatography (EPG),24
a practical failure remains: many evaluations mix word-identity25
holdout, repeated-instance holdout, and cross-participant trans-26
fer, so reported gains can reflect protocol differences rather than27
decoder differences. [1, 2, 3, 4, 5, 6, 7, 8]28
Recent systems such as SilentSpeller and ReHEarSSE show29
lexicon-scale character-level spelling beyond small command30
sets. However, these lines of work do not provide a unified, au-31
ditable protocol stack that isolates each generalization regime32
under a shared artifact trace. In parallel, prior EPG studies mo-33
tivate structured representations and spatial inductive bias, but34
their evaluation settings are heterogeneous across datasets and35
tasks. [9, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18]36
To address this gap, we introduce EPGSpeller, an37
evidence-tracked evaluation framework for EPG silent spelling.38
EPGSpeller fixes deterministic split generation, pinned split39
manifests, and a common metric harness for greedy decod-40
ing, lexicon projection, and streaming cost. It explicitly sep-41
arates word holdout, instance holdout, and cross-participant42
transfer so model comparisons remain protocol-specific and43
reproducible. We validate EPGSpeller with four participant44
datasets and compare a vector baseline with row-column and45
grid-based front ends under matched settings. We also evalu-46
ate electrode reduction and low-shot adaptation under the same47
audit rules. Across our audited runs, row-column pooling48
Table 1:Raw dataset summary for each participant dataset;
id is an anonymous participant label, N is sample count, V is
vocabulary size, Tmed is median sequence length in frames,
contact is mean contact rate, and zero is the count of all-zero
samples.
id N V Tmed contact zero
p1 2328 1164 234 0.19 0
p2 2328 1164 196 0.20 0
p3 2797 1164 283 0.12 4
p4 1167 1162 229 0.19 0
tracks the vector baseline more consistently than grid variants,49
while cross-participant transfer remains the dominant bottle-50
neck. [9, 13, 16, 17, 18]51
Within these audited datasets and protocol definitions,52
protocol-level auditability is necessary for interpretable bench-53
marking. 54
• We define deterministic protocol families that isolate word-55
identity, instance-level, and cross-participant generalization.56
• We provide checksum-pinned split archives and manifests so57
each reported result is reproducible from audited artifacts.58
• We benchmark vector, row-column, and grid front ends un-59
der a shared evaluation harness with accuracy and streaming60
metrics. 61
• We report electrode-reduction and low-shot analyses under62
the same protocol constraints.63
2. Data and Protocols64
We use four participant electropalatography datasets with word65
labels. Each sample is a variable length binary contact matrix,66
and the raw exports are treated as immutable evidence. We re-67
fer to participants with anonymous labels in all tables and split68
archives. We audit dataset statistics, label counts, and anoma-69
lies before we construct any train and test splits. We exclude a70
small set of all-zero samples via a pinned index list.71
The audit pipeline records raw file checksums. It vali-72
dates schema consistency. It summarizes label counts, sequence73
length summaries, and per channel activity statistics before any74
split construction. The raw exports remain unchanged. We ap-75
ply any exclusions only through pinned index lists that are in-76
cluded in the audit artifacts.77
Table 1 reports sample count, vocabulary size, median se-78
quence length, mean contact rate, and all-zero count for each79
participant dataset. The id labels are anonymous participant80
codes used throughout the protocol manifests.81
We evaluate three primary protocols. The word holdout82

=== PAGE 2 ===
protocol uses disjoint vocabularies across train, test, and a com-83
petition partition. The instance holdout protocol tests held out84
instances of seen words. It separates train and competition vo-85
cabularies while keeping the test vocabulary within their union.86
The cross participant protocol trains on a source participant87
and tests on a target participant under a shared vocabulary con-88
straint. We also define a paired source cross participant vari-89
ant and a low shot adaptation variant to isolate source aggrega-90
tion and limited supervision effects under the same audit rules.91
When a target participant has limited within word repetition,92
we configure the cross participant split generators to allow sin-93
gle instance target words. We keep the source side constraints94
unchanged. All split archives used in this study are enumerated95
with sizes and checksums in manifest artifacts.96
All split archives are generated deterministically from au-97
dited exports with fixed seeds. Each train, test, and competition98
partition is stored as an immutable archive with a checksum in99
the manifests to enable reuse and later verification. The man-100
ifests show the word-holdout protocol uses all four participant101
datasets. They show the instance-holdout protocol uses three102
participant datasets. They also show the fourth participant is103
target-only (not used as a source) in the cross-participant splits.104
The audited label histogram for the fourth participant is dom-105
inated by single-instance labels, so we restrict that participant106
to target-only use in cross-participant evaluation. This separa-107
tion explains why the dataset summary includes all participant108
datasets even when a protocol uses only a subset.109
We normalize labels by uppercasing and filtering to alpha-110
bet characters, then represent each label as a space separated111
character sequence for CTC training and greedy decoding. We112
apply this step consistently during split construction and dataset113
preparation to avoid vocabulary drift.114
We keep the label normalization step consistent across all115
splits and dataset preparation steps. This aligns the decoder116
vocabulary with the audited labels and reduces drift between117
training and artifacts used to evaluate.118
We report character error rate from greedy decoding and119
streaming speed using real time factor. We define real time fac-120
tor as total inference time divided by total input duration. For121
character-level decoding we also report lexicon projection error122
rates using a training lexicon and a full lexicon.123
Greedy decoding reports unconstrained character se-124
quences. Lexicon projection maps outputs to finite word sets125
derived from the training vocabulary or the full audited lexicon.126
This allows us to separate decoding quality from lexicon con-127
straints. We compute real time factor by dividing inference time128
by input duration under the same test harness. Tables summa-129
rize results over four split seeds as mean and standard devia-130
tion. We compute two sided t distribution confidence intervals131
for the primary accuracy metric and paired t tests with Holm132
correction; the compact statistical summary table is provided in133
the supplementary archive.134
3. Models135
Our baseline model encodes each frame as a vector of palate136
channels and applies a uni-directional recurrent decoder trained137
with a CTC objective. We compare two layout aware front ends.138
One is a row and column pooling front end that aggregates a139
proxy grid into one dimensional summaries. The other is a grid140
front end that reconstructs a proxy grid and applies a convolu-141
tional spatial encoder. For the grid model we optionally enable a142
spatial augmentation that drops and shifts contiguous electrode143
blocks. [12, 19]144
Table 2:Baseline recap across protocols; P1 means word
holdout, P2 means instance holdout, and P3 means cross-
participant transfer. n is the number of split-seed aggregates.
CER is character error rate and LEX is lexicon-projected error
rate.
protocol n cer lex
P1 4 0.180±0.084 0.102±0.068
P2 3 0.145±0.063 0.075±0.048
P3 6 0.691±0.133 0.644±0.060
The proxy grid is constructed from the palate channel lay-145
out. It supports row and column pooling or convolutional fea-146
ture extraction. We use a fixed layout file for the mapping so147
that row and column indices are consistent across splits. We148
augment spatially by perturbing contiguous electrode blocks to149
emulate missing contacts and minor spatial shifts.150
We fix core training hyperparameters across runs and record151
how we configure them in the metrics registry for auditability.152
4. Results153
We report greedy decoding error, lexicon-projected error, and154
streaming cost under a shared evaluation harness for all proto-155
cols. The fourth participant is target-only in cross-participant156
evaluation due to single-instance label dominance. All metrics157
are derived from the same audited registry of 652 runs (P1=176,158
P2=132, P3=264, P3MS=48, P2K=32).159
Table 2 summarizes baseline performance across the three160
evaluation protocols. 161
Table 2 shows a clear protocol ordering: CER is 0.145 to162
0.180 for within-participant protocols (P2 and P1) and 0.691163
for cross-participant P3, while LEX rises from 0.075 to 0.102164
up to 0.644. Transfer difficulty, not within-participant decoding,165
drives the largest residual error.166
Table 2 also shows that lexicon projection helps more167
in within-participant settings than in transfer: CER to LEX168
changes are 0.180 to 0.102 for P1 and 0.145 to 0.075 for P2,169
versus 0.691 to 0.644 for P3. Lexicon constraints reduce lo-170
cal decoding variance, but they do not remove cross-participant171
mismatch. 172
Table 3 compares vector, row/col, and grid-based front ends173
at full channels across protocols.174
From Table 3, rowcol tracks vec across protocols (P1: 0.20175
vs 0.18, P2: 0.16 vs 0.15, P3: 0.68 vs 0.69 CER). Grid and176
grid aug are usually higher in CER and RTF, and patch variants177
only partially close this gap. The compact statistical summary178
in supplementary material shows broad interval overlap, so we179
treat these as directional trends rather than universal winners.180
Latency shows a similarly stable tradeoff. In P1, vec runs181
at RTF 0.0006 while rowcol is 0.0024 and grid-family variants182
are 0.0034 to 0.0039; in P3, all variants remain below 0.001 but183
grid-family models are still slower than vec and rowcol. Under184
this audit setting, the expensive spatial front ends do not pro-185
duce a consistent accuracy return.186
Table 4 evaluates cross-participant transfer with participant187
p4 as target under single-source and paired-source settings.188
Table 4 shows an aggregate gain: CER drops from189
0.686±0.114 in P3 all-¿p4 to 0.582±0.064 in P3MS all-¿p4, and190
LEX drops from 0.659±0.073 to 0.554±0.034. Direction rows191
remain heterogeneous, so source-pair selection stays condition192
dependent. 193
Direction rows in Table 4 show where the aggregate194

=== PAGE 3 ===
Table 3:Spatial modeling at full channels across P1, P2, and
P3; P1 means word holdout, P2 means instance holdout, and
P3 means cross-participant transfer. CER is character error
rate and RTF is real time factor.
protocol variant cer rtf
P1 vec 0.18±0.08 0.0006±0.0002
P1 rowcol 0.20±0.09 0.0024±0.0011
P1 grid 0.31±0.15 0.0036±0.0015
P1 grid aug 0.31±0.14 0.0034±0.0011
P1 patch 0.30±0.07 0.0038±0.0017
P1 patch aug 0.30±0.09 0.0039±0.0017
P2 vec 0.15±0.06 0.0001±0.0000
P2 rowcol 0.16±0.08 0.0002±0.0000
P2 grid 0.29±0.21 0.0004±0.0000
P2 grid aug 0.31±0.24 0.0004±0.0000
P2 patch 0.34±0.23 0.0007±0.0001
P2 patch aug 0.30±0.16 0.0006±0.0000
P3 vec 0.69±0.13 0.0001±0.0000
P3 rowcol 0.68±0.15 0.0002±0.0000
P3 grid 0.75±0.09 0.0004±0.0000
P3 grid aug 0.76±0.09 0.0004±0.0000
P3 patch 0.69±0.11 0.0006±0.0001
P3 patch aug 0.70±0.13 0.0005±0.0001
Table 4:Cross-participant transfer targeting participant p4.
Proto marks P3 single-source transfer or P3MS paired-source
transfer. Lvl marks direction rows or all-direction aggregates.
Group encodes source-to-target participant IDs p1 to p4. CER
is character error rate and LEX is lexicon-projected error rate.
proto lvl group cer lex
P3 dir p1-¿p4 0.666±0.024 0.651±0.026
P3 dir p2-¿p4 0.809±0.021 0.736±0.022
P3 dir p3-¿p4 0.584±0.018 0.591±0.029
P3 all all-¿p4 0.686±0.114 0.659±0.073
P3MS dir p12-¿p4 0.655±0.016 0.593±0.016
P3MS dir p13-¿p4 0.536±0.009 0.533±0.008
P3MS dir p23-¿p4 0.555±0.005 0.537±0.011
P3MS all all-¿p4 0.582±0.064 0.554±0.034
gain comes from: p13-¿p4 reaches 0.536±0.009 CER versus195
0.809±0.021 for p2-¿p4, and p23-¿p4 reaches 0.555±0.005 ver-196
sus 0.666±0.024 for p1-¿p4. The remaining direction goes the197
other way (p12-¿p4 0.655±0.016 versus p3-¿p4 0.584±0.018),198
so source aggregation helps on average but not for every source-199
target match.200
Table 5 evaluates low-shot adaptation by varying the num-201
ber of training instances per word for a new participant.202
From Table 5, increasing from k1 to k2 improves vec203
(0.350-¿0.246) and rowcol (0.334-¿0.278), but worsens grid204
(0.515-¿0.616) and grid aug (0.611-¿0.689). Low-shot gain is205
architecture dependent, not automatic.206
Table 6 evaluates reduced-channel subsets across protocols207
using within-participant, transfer, and random selection strate-208
gies.209
Table 6 shows small method deltas at K=64: P1 CER ranges210
0.191-0.205, P2 ranges 0.154-0.158, and P3 ranges 0.644-211
0.657. Because these ranges overlap strongly, we avoid a uni-212
versal ranking among topk, fps2k, xfer, and rand.213
Fig. 1 visualizes how accuracy and streaming cost vary with214
electrode budget for the word holdout protocol.215
Table 5:Low-shot adaptation for participant p3 with k1 or k2
training instances per word. vec is vector baseline, rowcol is
row-column pooling, grid is a convolutional grid encoder, and
grid aug adds spatial augmentation. CER is character error
rate and RTF is real time factor.
group variant cer rtf
p3 k1 vec 0.350±0.060 0.0002±0.0000
p3 k1 rowcol 0.334±0.039 0.0005±0.0000
p3 k1 grid 0.515±0.050 0.0007±0.0000
p3 k1 grid aug 0.611±0.157 0.0011±0.0006
p3 k2 vec 0.246±0.009 0.0002±0.0000
p3 k2 rowcol 0.278±0.022 0.0005±0.0000
p3 k2 grid 0.616±0.132 0.0008±0.0001
p3 k2 grid aug 0.689±0.218 0.0007±0.0000
Table 6:Electrode-reduction methods at K=64 across P1, P2,
and P3; P1 means word holdout, P2 means instance holdout,
and P3 means cross-participant transfer. topk and fps2k are
within-participant selections, xfer transfers a source ranking,
and rand is a fixed random subset. CER is character error rate
and RTF is real time factor.
protocol method cer rtf
P1 topk 0.195±0.083 0.0007±0.0002
P1 fps2k 0.191±0.078 0.0006±0.0002
P1 xfer 0.205±0.095 0.0006±0.0002
P1 rand 0.198±0.079 0.0007±0.0003
P2 topk 0.154±0.059 0.0001±0.0000
P2 fps2k 0.154±0.062 0.0001±0.0000
P2 xfer 0.158±0.071 0.0001±0.0000
P2 rand 0.157±0.067 0.0001±0.0000
P3 topk 0.647±0.130 0.0001±0.0000
P3 fps2k 0.656±0.146 0.0001±0.0000
P3 xfer 0.657±0.144 0.0001±0.0000
P3 rand 0.644±0.133 0.0001±0.0000
Fig. 1 shows CER improving as K increases toward full216
channels, while RTF changes less steeply. Random subsets are217
generally above within-participant selections in CER, although218
the gap narrows at larger budgets.219
Fig. 1 also shows where electrode-budget sensitivity is con-220
centrated. At K=16, CER is 0.210 for random versus 0.192221
for topk and 0.166 for fps2k; by K=64, these values narrow to222
0.130, 0.129, and 0.119. Around K=80, all three are near 0.121,223
indicating a practical regime where selection strategy matters224
less than at sparse budgets.225
Table 7 evaluates paired-source cross-participant transfer226
under the same target and protocol constraints.227
Table 7 is target dependent: for p23-¿p1, vec 0.473 and228
rowcol 0.476 outperform grid 0.602 and grid aug 0.691, while229
for p12-¿p3, grid 0.736 outperforms vec 0.838 and rowcol230
0.790. Multi-source benefit is therefore conditional rather than231
universal. 232
Table 7 also contains an intermediate regime where meth-233
ods are close: for p13-¿p2, CER is 0.520 for vec, 0.504 for234
rowcol, and 0.511 for both grid variants. This narrow band con-235
trasts with p23-¿p1 and p12-¿p3, reinforcing that source-target236
compatibility, not model family alone, governs paired-source237
behavior. 238

=== PAGE 4 ===
0.10
0.15
0.20
CER
topk
fps2k
random
full budget
16 32 48 64 80 96 112
Electrode budget (K)
0.0004
0.0005
0.0006
0.0007
streaming RTF
Figure 1:Electrode-budget trends for P1 word holdout; topk
uses within-participant importance ranking, diversity corre-
sponds to fps2k, and random is a fixed random subset. CER
is character error rate and RTF is real time factor.
Table 7:Paired-source cross-participant results by source pair;
group denotes source participants to target participant with
participant IDs p1 to p4. vec is vector baseline, rowcol is
row-column pooling, grid is a convolutional grid encoder, and
grid aug adds spatial augmentation. CER is character error
rate and RTF is real time factor.
group variant cer rtf
p23-¿p1 vec 0.473±0.014 0.0001±0.0000
p23-¿p1 rowcol 0.476±0.014 0.0002±0.0000
p23-¿p1 grid 0.602±0.076 0.0004±0.0000
p23-¿p1 grid aug 0.691±0.165 0.0004±0.0000
p13-¿p2 vec 0.520±0.003 0.0001±0.0000
p13-¿p2 rowcol 0.504±0.012 0.0003±0.0000
p13-¿p2 grid 0.511±0.047 0.0004±0.0000
p13-¿p2 grid aug 0.511±0.016 0.0004±0.0000
p12-¿p3 vec 0.838±0.034 0.0001±0.0000
p12-¿p3 rowcol 0.790±0.033 0.0002±0.0000
p12-¿p3 grid 0.736±0.018 0.0003±0.0000
p12-¿p3 grid aug 0.756±0.020 0.0003±0.0000

=== PAGE 5 ===
5. Discussion239
The dominant and most stable signal is the protocol gap:240
P3 CER is 0.691±0.133, versus 0.180±0.084 for P1 and241
0.145±0.063 for P2. This ordering persists under front-end242
swaps, channel reduction, and low-shot settings, so cross-243
participant mismatch remains the primary error source in this244
audited setup. Layout-aware bias alone is insufficient. Rowcol245
remains close to vec across P1-P3, while grid variants often in-246
crease CER and RTF; patch pooling narrows some gaps but does247
not create a consistent winner. Spatial encoders therefore need248
protocol-specific validation against explicit latency constraints.249
Source aggregation helps at the p4 aggregate level (CER 0.686250
to 0.582), but direction-level outcomes remain heterogeneous.251
Together with k-shot behavior (vec and rowcol improve from252
k1 to k2 while grid variants worsen), this indicates that trans-253
fer benefit depends on source-target compatibility and model254
family. Our practical rule is protocol-specific selection under255
matched audited splits and manifests. We limit all claims to256
these datasets, this normalization pipeline, and these protocol257
definitions, and we do not extrapolate to unaudited populations258
or sensing setups.259
6. Conclusion260
EPGSpeller provides a reproducible benchmark for lexicon-free261
silent spelling under deterministic audited protocols. Within262
this audited setting, cross-participant transfer remains the hard-263
est regime (P3 CER 0.691±0.133), and paired-source aggre-264
gation can reduce aggregate p4 error (0.686 to 0.582) with-265
out removing direction dependence. Deployment claims should266
therefore be validated per protocol, per target, and per latency267
constraint.268
7. Artifacts and Auditability269
This repository uses a strict paper registry that pins every ev-270
idence file by checksum and rejects unsupported manuscript271
blocks. The split manifests, aggregated metrics, compact ta-272
bles, statistical summaries, and analysis reports referenced in273
this paper are stored as deterministic artifacts, enabling audit274
and reproduction within our repository environment. A supple-275
mentary archive includes the compact statistical summary table276
for reviewers.277
8. Ethics and Disclosure278
We report results only for audited artifacts and do not claim279
broader demographic coverage. The datasets and splits used in280
this study are derived from participant recordings, and we focus281
on methodological clarity and artifact traceability rather than282
deployment claims. We used generative AI tools for language283
polishing and verified technical claims against audited artifacts.284

=== PAGE 6 ===
9. References285
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and286
J. Brumberg, “Silent speech interfaces,” 2010.287
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction288
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and289
Computer Engineering. Springer, 2017.290
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,291
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces292
for speech restoration: A review,” 2020.293
[4] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,294
“New developments in electropalatography: A state-of-the-art re-295
port,” 1989.296
[5] W. J. Hardcastle, “Electropalatography in phonetic research and297
in speech training,” 1990.298
[6] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and299
S. Lee, “Biosignal sensors and deep learning-based speech recog-300
nition: A review,” 2021.301
[7] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,302
“Visualisation and analysis of speech production with elec-303
tropalatography,” 2019.304
[8] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and305
evaluation of korean electropalatography (k-epg),” 2021.306
[9] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-307
tion of electropalatographic data using latent variable models,”308
1998.309
[10] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-310
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-311
the-ear silently spelled expressions,” 2024.312
[11] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fagan, R. Moore,313
and P. Green, “Isolated word recognition of silent speech using314
magnetic implants and sensors,” 2010.315
[12] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-316
nectionist temporal classification,” 2006.317
[13] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction318
methods and their implications for studies of lingual coarticula-319
tion,” 1991.320
[14] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and321
M. Stone, “Development of a silent speech interface driven by322
ultrasound and optical images of the tongue and lips,” 2010.323
[15] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,324
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-325
wards mobile, hands-free, silent speech text entry using elec-326
tropalatography,” 2022.327
[16] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-328
surement of face and palate by structured light,” 1993.329
[17] A. Toutios and K. Margaritis, “Learning electropalatograms from330
acoustics,” 2006.331
[18] ——, “On the acoustic-to-electropalatographic mapping,” 2006.332
[19] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,333
and Q. V . Le, “Specaugment: A simple data augmentation method334
for automatic speech recognition,” 2019.335
