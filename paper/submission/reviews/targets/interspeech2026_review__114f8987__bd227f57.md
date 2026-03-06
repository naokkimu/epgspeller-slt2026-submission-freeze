# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 22254,
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
      }
    ],
    "page_count": 5,
    "path": "interspeech2026_review.pdf",
    "sha256": "114f8987690ffa6de54e780859a40cb44fb4250fafc01ef8a94670c54aa931a9",
    "sha8": "114f8987",
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
    "sha256": "bd227f57398ee696ac522075c5395b70a82a8e40b1a318584ca658ac19e01743",
    "sha8": "bd227f57"
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
        "page_count": 5
      },
      "id": "page_limit",
      "message": "page_count=5 <= max_pages=6",
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
      "extracted_chars": 22254,
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
        }
      ],
      "page_count": 5,
      "path": "interspeech2026_review.pdf",
      "sha256": "114f8987690ffa6de54e780859a40cb44fb4250fafc01ef8a94670c54aa931a9",
      "sha8": "114f8987",
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
      "sha256": "bd227f57398ee696ac522075c5395b70a82a8e40b1a318584ca658ac19e01743",
      "sha8": "bd227f57"
    }
  },
  "run_id": "INTSP2026_STATIC_114f8987_bd227f57"
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
tracks the vector baseline more consistently than grid variants,49
while cross-participant transfer remains the dominant bottle-50
neck. [9, 13, 16, 17, 18]51
Within our audited datasets and protocol definitions,52
protocol-level auditability is required for comparable bench-53
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
We evaluate three primary protocols. The word holdout78
protocol uses disjoint vocabularies across train, test, and a com-79
petition partition. The instance holdout protocol tests held out80
instances of seen words. It separates train and competition vo-81
cabularies while keeping the test vocabulary within their union.82
The cross participant protocol trains on a source participant83
and tests on a target participant under a shared vocabulary con-84
straint. We also define a paired source cross participant vari-85
ant and a low shot adaptation variant to isolate source aggrega-86
tion and limited supervision effects under the same audit rules.87
When a target participant has limited within word repetition,88
we configure the cross participant split generators to allow sin-89
gle instance target words. We keep the source side constraints90
unchanged. All split archives used in this study are enumerated91
with sizes and checksums in manifest artifacts.92
All split archives are generated deterministically from au-93
dited exports with fixed seeds. Each train, test, and competition94
partition is stored as an immutable archive with a checksum in95

=== PAGE 2 ===
the manifests to enable reuse and later verification. The man-96
ifests show the word-holdout protocol uses all four participant97
datasets. They show the instance-holdout protocol uses three98
participant datasets. They also show the fourth participant is99
target-only (not used as a source) in the cross-participant splits.100
The audited label histogram for the fourth participant is dom-101
inated by single-instance labels, so we restrict that participant102
to target-only use in cross-participant evaluation. This separa-103
tion explains why the dataset summary includes all participant104
datasets even when a protocol uses only a subset.105
We normalize labels by uppercasing and filtering to alpha-106
bet characters, then represent each label as a space separated107
character sequence for CTC training and greedy decoding. We108
apply this step consistently during split construction and dataset109
preparation to avoid vocabulary drift.110
We keep the label normalization step consistent across all111
splits and dataset preparation steps. This aligns the decoder112
vocabulary with the audited labels and reduces drift between113
training and artifacts used to evaluate.114
We report character error rate from greedy decoding and115
streaming speed using real time factor. We define real time fac-116
tor as total inference time divided by total input duration. For117
character-level decoding we also report lexicon projection error118
rates using a training lexicon and a full lexicon.119
Greedy decoding reports unconstrained character se-120
quences. Lexicon projection maps outputs to finite word sets121
derived from the training vocabulary or the full audited lexicon.122
This allows us to separate decoding quality from lexicon con-123
straints. We compute real time factor by dividing inference time124
by input duration under the same test harness. Tables summa-125
rize results over four split seeds as mean and standard devia-126
tion. We compute two sided t distribution confidence intervals127
for the primary accuracy metric and paired t tests with Holm128
correction; the compact statistical summary table is provided in129
the supplementary archive.130
3. Models131
Our baseline model encodes each frame as a vector of palate132
channels and applies a uni-directional recurrent decoder trained133
with a CTC objective. We compare two layout aware front ends.134
One is a row and column pooling front end that aggregates a135
proxy grid into one dimensional summaries. The other is a grid136
front end that reconstructs a proxy grid and applies a convolu-137
tional spatial encoder. For the grid model we optionally enable a138
spatial augmentation that drops and shifts contiguous electrode139
blocks. [12, 19]140
The proxy grid is constructed from the palate channel lay-141
out. It supports row and column pooling or convolutional fea-142
ture extraction. We use a fixed layout file for the mapping so143
that row and column indices are consistent across splits. We144
augment spatially by perturbing contiguous electrode blocks to145
emulate missing contacts and minor spatial shifts.146
We fix core training hyperparameters across runs and record147
how we configure them in the metrics registry for auditability.148
4. Results149
We report greedy decoding error, lexicon-projected error, and150
streaming cost under a shared evaluation harness for all proto-151
cols. The fourth participant is target-only in cross-participant152
evaluation due to single-instance label dominance. All metrics153
are derived from the same audited registry.154
Table tab:main summarizes baseline performance across155
Table 1:Baseline recap across protocols; P1 means word
holdout, P2 means instance holdout, and P3 means cross-
participant transfer. n is the number of split-seed aggregates.
CER is character error rate and LEX is lexicon-projected error
rate.
protocol n cer lex
P1 4 0.180±0.084 0.102±0.068
P2 3 0.145±0.063 0.075±0.048
P3 6 0.691±0.133 0.644±0.060
Table 2:Spatial modeling at full channels across P1, P2, and
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
the three evaluation protocols.156
Table tab:main shows a clear protocol ordering: CER is157
0.145 to 0.180 for within-participant protocols (P2 and P1) and158
0.691 for cross-participant P3, while LEX rises from 0.075 to159
0.102 up to 0.644. Transfer difficulty, not within-participant de-160
coding, drives the largest residual error.161
Table tab:spatial all compares vector, row/col, and grid-162
based front ends at full channels across protocols.163
From Table tab:spatial all, rowcol tracks vec across proto-164
cols (P1: 0.20 vs 0.18, P2: 0.16 vs 0.15, P3: 0.68 vs 0.69 CER).165
Grid and grid aug are usually higher in CER and RTF, and patch166
variants only partially close this gap. The compact statistical167
summary in supplementary material shows broad interval over-168
lap, so we treat these as directional trends rather than universal169
winners. 170
Table tab:tofour evaluates cross-participant transfer with171
participant p4 as target under single-source and paired-source172
settings. 173
Table tab:tofour shows an aggregate gain for p4 target trans-174
fer: CER drops from 0.686±0.114 in P3 all-¿p4 to 0.582±0.064175
in P3MS all-¿p4, and LEX drops from 0.659±0.073 to176
0.554±0.034. Direction rows remain heterogeneous, so source-177
pair selection stays condition dependent.178
Table tab:kshot evaluates low-shot adaptation by varying179
the number of training instances per word for a new participant.180
From Table tab:kshot, increasing from k1 to k2 improves181

=== PAGE 3 ===
Table 3:Cross-participant transfer targeting participant p4.
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
Table 4:Low-shot adaptation for participant p3 with k1 or k2
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
vec (0.350-¿0.246) and rowcol (0.334-¿0.278), but worsens grid182
(0.515-¿0.616) and grid aug (0.611-¿0.689). Low-shot gain is183
architecture dependent, not automatic.184
Table tab:k64 all evaluates reduced-channel subsets across185
protocols using within-participant, transfer, and random selec-186
tion strategies.187
Table 5:Electrode-reduction methods at K=64 across P1, P2,
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
Table tab:k64 all shows small method deltas at K=64: P1188
CER ranges 0.191-0.205, P2 ranges 0.154-0.158, and P3 ranges189
0.644-0.657. Because these ranges overlap strongly, we avoid a190
universal ranking among topk, fps2k, xfer, and rand.191
Figure fig:kcurve visualizes how accuracy and streaming192
cost vary with electrode budget for the word holdout protocol.193
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
Figure fig:kcurve shows CER improving as K increases to-194
ward full channels, while RTF changes less steeply. Random195
subsets remain below within-participant selections across most196
K, although the absolute gap narrows at larger budgets.197
Table tab:p3ms evaluates paired-source cross-participant198
transfer under the same target and protocol constraints.199
Table 6:Paired-source cross-participant results by source pair;
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
Table tab:p3ms is target dependent: for p23-¿p1, vec 0.473200

=== PAGE 4 ===
and rowcol 0.476 outperform grid 0.602 and grid aug 0.691,201
while for p12-¿p3, grid 0.736 outperforms vec 0.838 and rowcol202
0.790. Multi-source benefit is therefore conditional rather than203
universal.204
5. Discussion205
The dominant and most stable signal is the protocol gap:206
P3 CER is 0.691±0.133, versus 0.180±0.084 for P1 and207
0.145±0.063 for P2. This ordering persists under front-end208
swaps, channel reduction, and low-shot settings, so cross-209
participant mismatch remains the primary error source in this210
audited setup. Layout-aware bias alone is insufficient. Rowcol211
remains close to vec across P1-P3, while grid variants often in-212
crease CER and RTF; patch pooling narrows some gaps but does213
not create a consistent winner. Spatial encoders therefore need214
protocol-specific validation against explicit latency constraints.215
Source aggregation helps at the p4 aggregate level (CER 0.686216
to 0.582), but direction-level outcomes remain heterogeneous.217
Together with k-shot behavior (vec and rowcol improve from218
k1 to k2 while grid variants worsen), this indicates that trans-219
fer benefit depends on source-target compatibility and model220
family. Our practical rule is protocol-specific selection under221
matched audited splits and manifests. We limit all claims to222
these datasets, this normalization pipeline, and these protocol223
definitions, and we do not extrapolate to unaudited populations224
or sensing setups.225
6. Conclusion226
EPGSpeller provides a reproducible benchmark for lexicon-free227
silent spelling under deterministic audited protocols. Within228
this audited setting, cross-participant transfer remains the hard-229
est regime (P3 CER 0.691±0.133), and paired-source aggre-230
gation can reduce aggregate p4 error (0.686 to 0.582) with-231
out removing direction dependence. Deployment claims should232
therefore be validated per protocol, per target, and per latency233
constraint.234
7. Artifacts and Auditability235
This repository uses a strict paper registry that pins every ev-236
idence file by checksum and rejects unsupported manuscript237
blocks. The split manifests, aggregated metrics, compact ta-238
bles, statistical summaries, and analysis reports referenced in239
this paper are stored as deterministic artifacts, enabling audit240
and reproduction within our repository environment. A supple-241
mentary archive includes the compact statistical summary table242
for reviewers.243
8. Ethics and Disclosure244
We report results only for audited artifacts and do not claim245
broader demographic coverage. The datasets and splits used in246
this study are derived from participant recordings, and we focus247
on methodological clarity and artifact traceability rather than248
deployment claims. We used generative AI tools for language249
polishing and verified technical claims against audited artifacts.250

=== PAGE 5 ===
9. References251
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and252
J. Brumberg, “Silent speech interfaces,” 2010.253
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction254
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and255
Computer Engineering. Springer, 2017.256
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,257
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces258
for speech restoration: A review,” 2020.259
[4] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,260
“New developments in electropalatography: A state-of-the-art re-261
port,” 1989.262
[5] W. J. Hardcastle, “Electropalatography in phonetic research and263
in speech training,” 1990.264
[6] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and265
S. Lee, “Biosignal sensors and deep learning-based speech recog-266
nition: A review,” 2021.267
[7] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,268
“Visualisation and analysis of speech production with elec-269
tropalatography,” 2019.270
[8] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and271
evaluation of korean electropalatography (k-epg),” 2021.272
[9] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-273
tion of electropalatographic data using latent variable models,”274
1998.275
[10] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-276
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-277
the-ear silently spelled expressions,” 2024.278
[11] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fagan, R. Moore,279
and P. Green, “Isolated word recognition of silent speech using280
magnetic implants and sensors,” 2010.281
[12] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-282
nectionist temporal classification,” 2006.283
[13] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction284
methods and their implications for studies of lingual coarticula-285
tion,” 1991.286
[14] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and287
M. Stone, “Development of a silent speech interface driven by288
ultrasound and optical images of the tongue and lips,” 2010.289
[15] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,290
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-291
wards mobile, hands-free, silent speech text entry using elec-292
tropalatography,” 2022.293
[16] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-294
surement of face and palate by structured light,” 1993.295
[17] A. Toutios and K. Margaritis, “Learning electropalatograms from296
acoustics,” 2006.297
[18] ——, “On the acoustic-to-electropalatographic mapping,” 2006.298
[19] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,299
and Q. V . Le, “Specaugment: A simple data augmentation method300
for automatic speech recognition,” 2019.301
