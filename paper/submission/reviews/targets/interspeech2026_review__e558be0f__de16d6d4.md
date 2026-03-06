# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 22122,
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
    "sha256": "e558be0f41a0b75aa4bb678980265ed7a8cdcb5f462bd192a85448c3333304cc",
    "sha8": "e558be0f",
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
      "plain_characters": 892
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
    "sha256": "de16d6d4571d6b265de7e050d225fac5c5eff74e2ab8984d29d96b9fbbb78195",
    "sha8": "de16d6d4"
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
        "abstract_chars": 892,
        "max_characters": 1000
      },
      "id": "abstract_length",
      "message": "abstract_chars=892 <= max_characters=1000",
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
      "extracted_chars": 22122,
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
      "sha256": "e558be0f41a0b75aa4bb678980265ed7a8cdcb5f462bd192a85448c3333304cc",
      "sha8": "e558be0f",
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
        "plain_characters": 892
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
      "sha256": "de16d6d4571d6b265de7e050d225fac5c5eff74e2ab8984d29d96b9fbbb78195",
      "sha8": "de16d6d4"
    }
  },
  "run_id": "INTSP2026_STATIC_e558be0f_de16d6d4"
}
```

## TeX preamble (first 200 lines)

```tex
% Auto-generated from paper/paper.json (paper-json v1.0.0). Do not edit by hand.
% Target: INTERSPEECH 2026 Paper Kit (Interspeech.cls).
\documentclass{Interspeech}
\usepackage{placeins}
\usepackage{float}

\title{EPGSpeller: Lexicon-Free Silent Spelling Recognition}
\keywords{silent speech interface, electropalatography, character-level decoding, text entry, auditability}

```

## PDF extracted text (page-separated, deterministic truncation)

=== PAGE 1 ===
EPGSpeller: Lexicon-Free Silent Spelling Recognition
Anonymous submission to Interspeech 2026
Abstract1
Protocol mixing still obscures progress in EPG silent2
spelling when word holdout, seen-word instance holdout, and3
cross-participant transfer are reported together. We present4
EPGSpeller, an evidence-tracked benchmark for lexicon-5
free character decoding with deterministic split generation,6
checksum-pinned manifests, and a shared metric harness.7
Across audited runs, CER is 0.180+/-0.084 in P1 and 0.145+/-8
0.063 in P2, but rises to 0.691+/-0.133 in P3, identifying cross-9
participant transfer as the dominant bottleneck. At full chan-10
nels, rowcol tracks vec more closely than grid variants in most11
settings. For the p4 target aggregate, paired-source transfer low-12
ers CER from 0.686+/-0.114 to 0.582+/-0.064 and LEX from13
0.659+/-0.073 to 0.554+/-0.034, while direction-level gains re-14
main mixed. These findings provide a reproducible baseline15
within our audited datasets and protocol definitions.16
Index Terms: silent speech interface, electropalatography,17
character-level decoding, text entry, auditability18
1. Introduction19
Silent speech interfaces (SSI) infer linguistic intent from20
non-acoustic signals, including articulatory sensing and other21
biosignals. For silent spelling with electropalatography (EPG),22
a practical failure remains: many evaluations mix word-identity23
holdout, repeated-instance holdout, and cross-participant trans-24
fer, so reported gains can reflect protocol differences rather than25
decoder differences. [1, 2, 3, 4, 5, 6, 7, 8]26
Recent systems such as SilentSpeller and ReHEarSSE show27
lexicon-scale character-level spelling beyond small command28
sets. However, these lines of work do not provide a unified, au-29
ditable protocol stack that isolates each generalization regime30
under a shared artifact trace. In parallel, prior EPG studies mo-31
tivate structured representations and spatial inductive bias, but32
their evaluation settings are heterogeneous across datasets and33
tasks. [9, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18]34
To address this gap, we introduce EPGSpeller, an35
evidence-tracked evaluation framework for EPG silent spelling.36
EPGSpeller fixes deterministic split generation, pinned split37
manifests, and a common metric harness for greedy decod-38
ing, lexicon projection, and streaming cost. It explicitly sep-39
arates word holdout, instance holdout, and cross-participant40
transfer so model comparisons remain protocol-specific and41
reproducible. We validate EPGSpeller with four participant42
datasets and compare a vector baseline with row-column and43
grid-based front ends under matched settings. We also evalu-44
ate electrode reduction and low-shot adaptation under the same45
audit rules. Across our audited runs, row-column pooling46
tracks the vector baseline more consistently than grid variants,47
while cross-participant transfer remains the dominant bottle-48
neck. [9, 13, 16, 17, 18]49
Within our audited datasets and protocol definitions,50
protocol-level auditability is required for comparable bench-51
marking. 52
• We define deterministic protocol families that isolate word-53
identity, instance-level, and cross-participant generalization.54
• We provide checksum-pinned split archives and manifests so55
each reported result is reproducible from audited artifacts.56
• We benchmark vector, row-column, and grid front ends un-57
der a shared evaluation harness with accuracy and streaming58
metrics. 59
• We report electrode-reduction and low-shot analyses under60
the same protocol constraints.61
2. Data and Protocols62
We use four participant electropalatography datasets with word63
labels. Each sample is a variable length binary contact matrix,64
and the raw exports are treated as immutable evidence. We re-65
fer to participants with anonymous labels in all tables and split66
archives. We audit dataset statistics, label counts, and anoma-67
lies before we construct any train and test splits. We exclude a68
small set of all-zero samples via a pinned index list.69
The audit pipeline records raw file checksums. It vali-70
dates schema consistency. It summarizes label counts, sequence71
length summaries, and per channel activity statistics before any72
split construction. The raw exports remain unchanged. We ap-73
ply any exclusions only through pinned index lists that are in-74
cluded in the audit artifacts.75
We evaluate three primary protocols. The word holdout76
protocol uses disjoint vocabularies across train, test, and a com-77
petition partition. The instance holdout protocol tests held out78
instances of seen words. It separates train and competition vo-79
cabularies while keeping the test vocabulary within their union.80
The cross participant protocol trains on a source participant81
and tests on a target participant under a shared vocabulary con-82
straint. We also define a paired source cross participant vari-83
ant and a low shot adaptation variant to isolate source aggrega-84
tion and limited supervision effects under the same audit rules.85
When a target participant has limited within word repetition,86
we configure the cross participant split generators to allow sin-87
gle instance target words. We keep the source side constraints88
unchanged. All split archives used in this study are enumerated89
with sizes and checksums in manifest artifacts.90
All split archives are generated deterministically from au-91
dited exports with fixed seeds. Each train, test, and competition92
partition is stored as an immutable archive with a checksum in93
the manifests to enable reuse and later verification. The man-94

=== PAGE 2 ===
ifests show the word-holdout protocol uses all four participant95
datasets. They show the instance-holdout protocol uses three96
participant datasets. They also show the fourth participant is97
target-only (not used as a source) in the cross-participant splits.98
The audited label histogram for the fourth participant is dom-99
inated by single-instance labels, so we restrict that participant100
to target-only use in cross-participant evaluation. This separa-101
tion explains why the dataset summary includes all participant102
datasets even when a protocol uses only a subset.103
We normalize labels by uppercasing and filtering to alpha-104
bet characters, then represent each label as a space separated105
character sequence for CTC training and greedy decoding. We106
apply this step consistently during split construction and dataset107
preparation to avoid vocabulary drift.108
We keep the label normalization step consistent across all109
splits and dataset preparation steps. This aligns the decoder110
vocabulary with the audited labels and reduces drift between111
training and artifacts used to evaluate.112
We report character error rate from greedy decoding and113
streaming speed using real time factor. We define real time fac-114
tor as total inference time divided by total input duration. For115
character-level decoding we also report lexicon projection error116
rates using a training lexicon and a full lexicon.117
Greedy decoding reports unconstrained character se-118
quences. Lexicon projection maps outputs to finite word sets119
derived from the training vocabulary or the full audited lexicon.120
This allows us to separate decoding quality from lexicon con-121
straints. We compute real time factor by dividing inference time122
by input duration under the same test harness. Tables summa-123
rize results over four split seeds as mean and standard devia-124
tion. We compute two sided t distribution confidence intervals125
for the primary accuracy metric and paired t tests with Holm126
correction; the compact statistical summary table is provided in127
the supplementary archive.128
3. Models129
Our baseline model encodes each frame as a vector of palate130
channels and applies a uni-directional recurrent decoder trained131
with a CTC objective. We compare two layout aware front ends.132
One is a row and column pooling front end that aggregates a133
proxy grid into one dimensional summaries. The other is a grid134
front end that reconstructs a proxy grid and applies a convolu-135
tional spatial encoder. For the grid model we optionally enable a136
spatial augmentation that drops and shifts contiguous electrode137
blocks. [12, 19]138
The proxy grid is constructed from the palate channel lay-139
out. It supports row and column pooling or convolutional fea-140
ture extraction. We use a fixed layout file for the mapping so141
that row and column indices are consistent across splits. We142
augment spatially by perturbing contiguous electrode blocks to143
emulate missing contacts and minor spatial shifts.144
We fix core training hyperparameters across runs and record145
how we configure them in the metrics registry for auditability.146
4. Results147
We report greedy decoding error, lexicon-projected error, and148
streaming cost under a shared evaluation harness for all proto-149
cols. The fourth participant is target-only in cross-participant150
evaluation due to single-instance label dominance. All metrics151
are derived from the same audited registry.152
Table tab:main summarizes baseline performance across153
the three evaluation protocols.154
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
Table tab:main shows a clear protocol ordering: CER is155
0.145 to 0.180 for within-participant protocols (P2 and P1) and156
0.691 for cross-participant P3, while LEX rises from 0.075 to157
0.102 up to 0.644. Transfer difficulty, not within-participant de-158
coding, drives the largest residual error.159
Table tab:spatial all compares vector, row/col, and grid-160
based front ends at full channels across protocols.161
From Table tab:spatial all, rowcol tracks vec across proto-162
cols (P1: 0.20 vs 0.18, P2: 0.16 vs 0.15, P3: 0.68 vs 0.69 CER).163
Grid and grid aug are usually higher in CER and RTF, and patch164
variants only partially close this gap. The compact statistical165
summary in supplementary material shows broad interval over-166
lap, so we treat these as directional trends rather than universal167
winners. 168
Table tab:tofour evaluates cross-participant transfer with169
participant p4 as target under single-source and paired-source170
settings. 171
Table tab:tofour shows an aggregate gain for p4 target trans-172
fer: CER drops from 0.686±0.114 in P3 all-¿p4 to 0.582±0.064173
in P3MS all-¿p4, and LEX drops from 0.659±0.073 to174
0.554±0.034. Direction rows remain heterogeneous, so source-175
pair selection stays condition dependent.176
Table tab:kshot evaluates low-shot adaptation by varying177
the number of training instances per word for a new participant.178
From Table tab:kshot, increasing from k1 to k2 improves179
vec (0.350-¿0.246) and rowcol (0.334-¿0.278), but worsens grid180

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
(0.515-¿0.616) and grid aug (0.611-¿0.689). Low-shot gain is181
architecture dependent, not automatic.182
Table tab:k64 all evaluates reduced-channel subsets across183
protocols using within-participant, transfer, and random selec-184
tion strategies.185
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
Table tab:k64 all shows small method deltas at K=64: P1186
CER ranges 0.191-0.205, P2 ranges 0.154-0.158, and P3 ranges187
0.644-0.657. Because these ranges overlap strongly, we avoid a188
universal ranking among topk, fps2k, xfer, and rand.189
Figure fig:kcurve visualizes how accuracy and streaming190
cost vary with electrode budget for the word holdout protocol.191
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
Figure fig:kcurve shows CER improving as K increases to-192
ward full channels, while RTF changes less steeply. Random193
subsets remain below within-participant selections across most194
K, although the absolute gap narrows at larger budgets.195
Table tab:p3ms evaluates paired-source cross-participant196
transfer under the same target and protocol constraints.197
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
Table tab:p3ms is target dependent: for p23-¿p1, vec 0.473198
and rowcol 0.476 outperform grid 0.602 and grid aug 0.691,199

=== PAGE 4 ===
while for p12-¿p3, grid 0.736 outperforms vec 0.838 and rowcol200
0.790. Multi-source benefit is therefore conditional rather than201
universal.202
5. Discussion203
The dominant and most stable signal is the protocol gap:204
P3 CER is 0.691±0.133, versus 0.180±0.084 for P1 and205
0.145±0.063 for P2. This ordering persists under front-end206
swaps, channel reduction, and low-shot settings, so cross-207
participant mismatch remains the primary error source in this208
audited setup. Layout-aware bias alone is insufficient. Rowcol209
remains close to vec across P1-P3, while grid variants often in-210
crease CER and RTF; patch pooling narrows some gaps but does211
not create a consistent winner. Spatial encoders therefore need212
protocol-specific validation against explicit latency constraints.213
Source aggregation helps at the p4 aggregate level (CER 0.686214
to 0.582), but direction-level outcomes remain heterogeneous.215
Together with k-shot behavior (vec and rowcol improve from216
k1 to k2 while grid variants worsen), this indicates that trans-217
fer benefit depends on source-target compatibility and model218
family. Our practical rule is protocol-specific selection under219
matched audited splits and manifests. We limit all claims to220
these datasets, this normalization pipeline, and these protocol221
definitions, and we do not extrapolate to unaudited populations222
or sensing setups.223
6. Conclusion224
EPGSpeller provides a reproducible benchmark for lexicon-free225
silent spelling under deterministic audited protocols. Within226
this audited setting, cross-participant transfer remains the hard-227
est regime (P3 CER 0.691±0.133), and paired-source aggre-228
gation can reduce aggregate p4 error (0.686 to 0.582) with-229
out removing direction dependence. Deployment claims should230
therefore be validated per protocol, per target, and per latency231
constraint.232
7. Artifacts and Auditability233
This repository uses a strict paper registry that pins every ev-234
idence file by checksum and rejects unsupported manuscript235
blocks. The split manifests, aggregated metrics, compact ta-236
bles, statistical summaries, and analysis reports referenced in237
this paper are stored as deterministic artifacts, enabling audit238
and reproduction within our repository environment. A supple-239
mentary archive includes the compact statistical summary table240
for reviewers.241
8. Ethics and Disclosure242
We report results only for audited artifacts and do not claim243
broader demographic coverage. The datasets and splits used in244
this study are derived from participant recordings, and we focus245
on methodological clarity and artifact traceability rather than246
deployment claims. We used generative AI tools for language247
polishing and verified technical claims against audited artifacts.248

=== PAGE 5 ===
9. References249
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and250
J. Brumberg, “Silent speech interfaces,” 2010.251
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction252
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and253
Computer Engineering. Springer, 2017.254
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,255
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces256
for speech restoration: A review,” 2020.257
[4] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,258
“New developments in electropalatography: A state-of-the-art re-259
port,” 1989.260
[5] W. J. Hardcastle, “Electropalatography in phonetic research and261
in speech training,” 1990.262
[6] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and263
S. Lee, “Biosignal sensors and deep learning-based speech recog-264
nition: A review,” 2021.265
[7] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,266
“Visualisation and analysis of speech production with elec-267
tropalatography,” 2019.268
[8] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and269
evaluation of korean electropalatography (k-epg),” 2021.270
[9] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-271
tion of electropalatographic data using latent variable models,”272
1998.273
[10] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-274
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-275
the-ear silently spelled expressions,” 2024.276
[11] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fagan, R. Moore,277
and P. Green, “Isolated word recognition of silent speech using278
magnetic implants and sensors,” 2010.279
[12] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-280
nectionist temporal classification,” 2006.281
[13] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction282
methods and their implications for studies of lingual coarticula-283
tion,” 1991.284
[14] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and285
M. Stone, “Development of a silent speech interface driven by286
ultrasound and optical images of the tongue and lips,” 2010.287
[15] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,288
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-289
wards mobile, hands-free, silent speech text entry using elec-290
tropalatography,” 2022.291
[16] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-292
surement of face and palate by structured light,” 1993.293
[17] A. Toutios and K. Margaritis, “Learning electropalatograms from294
acoustics,” 2006.295
[18] ——, “On the acoustic-to-electropalatographic mapping,” 2006.296
[19] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,297
and Q. V . Le, “Specaugment: A simple data augmentation method298
for automatic speech recognition,” 2019.299
