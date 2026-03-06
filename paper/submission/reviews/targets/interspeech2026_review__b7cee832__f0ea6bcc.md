# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 20833,
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
    "sha256": "b7cee832438a1414a7845294bc0c1bd268b620e78fc37e0b1584bf60fed98404",
    "sha8": "b7cee832",
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
      "plain_characters": 772
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
    "sha256": "f0ea6bccb6f36086d2e18f016645d9d32215b9dcc9922c2306b7d4692a6ba9c4",
    "sha8": "f0ea6bcc"
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
        "abstract_chars": 772,
        "max_characters": 1000
      },
      "id": "abstract_length",
      "message": "abstract_chars=772 <= max_characters=1000",
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
      "extracted_chars": 20833,
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
      "sha256": "b7cee832438a1414a7845294bc0c1bd268b620e78fc37e0b1584bf60fed98404",
      "sha8": "b7cee832",
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
        "plain_characters": 772
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
      "sha256": "f0ea6bccb6f36086d2e18f016645d9d32215b9dcc9922c2306b7d4692a6ba9c4",
      "sha8": "f0ea6bcc"
    }
  },
  "run_id": "INTSP2026_STATIC_b7cee832_f0ea6bcc"
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
Audited protocol design enables comparable evaluation of2
EPG silent spelling under matched conditions. We present an3
evidence-only study from binary palate contact patterns using4
lexicon-free character decoding with complementary lexicon-5
projected evaluation. We define deterministic protocols for6
word holdout, instance holdout, and cross-participant trans-7
fer, and we evaluate a vector baseline with row and column8
and grid-based front ends under shared settings. Across au-9
dited runs, cross-participant transfer is the dominant bottleneck,10
paired-source transfer reduces aggregate error for the fourth-11
participant target while direction-level outcomes remain hetero-12
geneous, and row and column pooling tracks the vector baseline13
more consistently than grid-based variants.14
Index Terms: silent speech interface, electropalatography,15
character-level decoding, text entry, auditability16
1. Introduction17
Silent speech interfaces (SSI) infer linguistic intent from18
non-acoustic signals, including articulatory sensing and other19
biosignals. For silent spelling with electropalatography (EPG),20
a practical failure remains: many evaluations mix word-identity21
holdout, repeated-instance holdout, and cross-participant trans-22
fer, so reported gains can reflect protocol differences rather than23
decoder differences. [1, 2, 3, 4, 5, 6, 7, 8]24
Recent systems such as SilentSpeller and ReHEarSSE show25
lexicon-scale character-level spelling beyond small command26
sets. However, these lines of work do not provide a unified, au-27
ditable protocol stack that isolates each generalization regime28
under a shared artifact trace. In parallel, prior EPG studies mo-29
tivate structured representations and spatial inductive bias, but30
their evaluation settings are heterogeneous across datasets and31
tasks. [9, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18]32
To address this gap, we introduce EPGSpeller, an33
evidence-tracked evaluation framework for EPG silent spelling.34
EPGSpeller fixes deterministic split generation, pinned split35
manifests, and a common metric harness for greedy decod-36
ing, lexicon projection, and streaming cost. It explicitly sep-37
arates word holdout, instance holdout, and cross-participant38
transfer so model comparisons remain protocol-specific and39
reproducible. We validate EPGSpeller with four participant40
datasets and compare a vector baseline with row-column and41
grid-based front ends under matched settings. We also evalu-42
ate electrode reduction and low-shot adaptation under the same43
audit rules. Across our audited runs, row-column pooling44
tracks the vector baseline more consistently than grid variants,45
while cross-participant transfer remains the dominant bottle-46
neck. [9, 13, 16, 17, 18]47
Our evidence indicates that protocol-level auditability is48
necessary for comparable benchmarking within the audited49
EPG setting. We do not claim generality beyond these datasets50
and protocol definitions.51
• We define deterministic protocol families that isolate word-52
identity, instance-level, and cross-participant generalization.53
• We provide checksum-pinned split archives and manifests so54
each reported result is reproducible from audited artifacts.55
• We benchmark vector, row-column, and grid front ends un-56
der a shared evaluation harness with accuracy and streaming57
metrics. 58
• We report electrode-reduction and low-shot analyses under59
the same protocol constraints.60
2. Data and Protocols61
We use four participant electropalatography datasets with word62
labels. Each sample is a variable length binary contact matrix,63
and the raw exports are treated as immutable evidence. We re-64
fer to participants with anonymous labels in all tables and split65
archives. We audit dataset statistics, label counts, and anoma-66
lies before we construct any train and test splits. We exclude a67
small set of all-zero samples via a pinned index list.68
The audit pipeline records raw file checksums. It vali-69
dates schema consistency. It summarizes label counts, sequence70
length summaries, and per channel activity statistics before any71
split construction. The raw exports remain unchanged. We ap-72
ply any exclusions only through pinned index lists that are in-73
cluded in the audit artifacts.74
We evaluate three primary protocols. The word holdout75
protocol uses disjoint vocabularies across train, test, and a com-76
petition partition. The instance holdout protocol tests held out77
instances of seen words. It separates train and competition vo-78
cabularies while keeping the test vocabulary within their union.79
The cross participant protocol trains on a source participant80
and tests on a target participant under a shared vocabulary con-81
straint. We also define a paired source cross participant vari-82
ant and a low shot adaptation variant to isolate source aggrega-83
tion and limited supervision effects under the same audit rules.84
When a target participant has limited within word repetition,85
we configure the cross participant split generators to allow sin-86
gle instance target words. We keep the source side constraints87
unchanged. All split archives used in this study are enumerated88
with sizes and checksums in manifest artifacts.89
All split archives are generated deterministically from au-90
dited exports with fixed seeds. Each train, test, and competition91
partition is stored as an immutable archive with a checksum in92
the manifests to enable reuse and later verification. The man-93
ifests show the word-holdout protocol uses all four participant94

=== PAGE 2 ===
datasets. They show the instance-holdout protocol uses three95
participant datasets. They also show the fourth participant is96
target-only (not used as a source) in the cross-participant splits.97
The audited label histogram for the fourth participant is dom-98
inated by single-instance labels, so we restrict that participant99
to target-only use in cross-participant evaluation. This separa-100
tion explains why the dataset summary includes all participant101
datasets even when a protocol uses only a subset.102
We normalize labels by uppercasing and filtering to alpha-103
bet characters, then represent each label as a space separated104
character sequence for CTC training and greedy decoding. We105
apply this step consistently during split construction and dataset106
preparation to avoid vocabulary drift.107
We keep the label normalization step consistent across all108
splits and dataset preparation steps. This aligns the decoder109
vocabulary with the audited labels and reduces drift between110
training and artifacts used to evaluate.111
We report character error rate from greedy decoding and112
streaming speed using real time factor. We define real time fac-113
tor as total inference time divided by total input duration. For114
character-level decoding we also report lexicon projection error115
rates using a training lexicon and a full lexicon.116
Greedy decoding reports unconstrained character se-117
quences. Lexicon projection maps outputs to finite word sets118
derived from the training vocabulary or the full audited lexicon.119
This allows us to separate decoding quality from lexicon con-120
straints. We compute real time factor by dividing inference time121
by input duration under the same test harness. Tables summa-122
rize results over four split seeds as mean and standard devia-123
tion. We compute two sided t distribution confidence intervals124
for the primary accuracy metric and paired t tests with Holm125
correction; the compact statistical summary table is provided in126
the supplementary archive.127
3. Models128
Our baseline model encodes each frame as a vector of palate129
channels and applies a uni-directional recurrent decoder trained130
with a CTC objective. We compare two layout aware front ends.131
One is a row and column pooling front end that aggregates a132
proxy grid into one dimensional summaries. The other is a grid133
front end that reconstructs a proxy grid and applies a convolu-134
tional spatial encoder. For the grid model we optionally enable a135
spatial augmentation that drops and shifts contiguous electrode136
blocks. [12, 19]137
The proxy grid is constructed from the palate channel lay-138
out. It supports row and column pooling or convolutional fea-139
ture extraction. We use a fixed layout file for the mapping so140
that row and column indices are consistent across splits. We141
augment spatially by perturbing contiguous electrode blocks to142
emulate missing contacts and minor spatial shifts.143
We fix core training hyperparameters across runs and record144
how we configure them in the metrics registry for auditability.145
4. Results146
We report greedy decoding error, lexicon-projected error, and147
streaming cost under a shared evaluation harness for all proto-148
cols. The fourth participant is target-only in cross-participant149
evaluation due to single-instance label dominance. All metrics150
are derived from the same audited registry.151
We summarize baseline performance across the three eval-152
uation protocols.153
Baseline error is lowest for word and instance holdout and154
Table 1:Baseline recap across evaluation protocols; the proto-
col column denotes word holdout, instance holdout, and cross
participant transfer, n counts split aggregates, CER is character
error rate, and lex is lexicon projected error rate.
protocol n cer lex
P1 4 0.180±0.084 0.102±0.068
P2 3 0.145±0.063 0.075±0.048
P3 6 0.691±0.133 0.644±0.060
Table 2:Spatial modeling at full channels across protocols
(protocol one word holdout, protocol two instance holdout, pro-
tocol three cross participant).
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
highest for cross participant transfer, consistent with the proto-155
col difficulty ordering.156
We compare vector, row/col, and grid-based front ends at157
full channels across protocols.158
Row and column pooling stays close to the vector base-159
line, whereas grid-based variants are usually higher in error and160
streaming cost. The compact statistical summary supports treat-161
ing these differences as directional trends rather than universal162
improvements. 163
We evaluate cross-participant transfer with the fourth par-164
ticipant as target under single-source and paired-source settings.165
For the fourth-participant aggregate, paired-source transfer166
yields lower error than single-source transfer. Direction-level167
outcomes remain mixed across source combinations.168
We evaluate low-shot adaptation by varying the number of169
training instances per word for a new participant.170
Moving from one-shot to two-shot improves vector and row171
and column variants, while grid variants worsen. Low-shot172
gains are therefore architecture dependent.173
We evaluate reduced-channel subsets across protocols using174
within-participant, transfer, and random selection strategies.175
At reduced channels, method differences are small and pro-176
tocol dependent, so we avoid a universal ranking of subset se-177
lection strategies. 178
We visualize how accuracy and streaming cost vary with179
electrode budget for the word holdout protocol.180
Accuracy improves as electrode budget increases, random181
selection remains weaker than within participant selection, and182

=== PAGE 3 ===
Table 3:Cross participant generalization targeting the fourth
participant; proto distinguishes single source cross participant
transfer and multi source transfer, lvl marks direction level rows
versus an across direction aggregate, group encodes source to
target participant labels, CER is character error rate, and lex is
lexicon projected error rate.
proto lvl group cer lex
P3 dir p1-¿p4 0.666±0.024 0.651±0.026
P3 dir p2-¿p4 0.809±0.021 0.736±0.022
P3 dir p3-¿p4 0.584±0.018 0.591±0.029
P3 all all-¿p4 0.686±0.114 0.659±0.073
P3MS dir p12-¿p4 0.655±0.016 0.593±0.016
P3MS dir p13-¿p4 0.536±0.009 0.533±0.008
P3MS dir p23-¿p4 0.555±0.005 0.537±0.011
P3MS all all-¿p4 0.582±0.064 0.554±0.034
Table 4:Low shot adaptation results for a new participant;
group uses the participant label and k one or k two for the num-
ber of training instances per word, vec is vector baseline, row-
col is row and column pooling, grid is convolutional grid en-
coder, grid aug is grid with spatial augmentation, CER is char-
acter error rate, and RTF is real time factor.
group variant cer rtf
p3 k1 vec 0.350±0.060 0.0002±0.0000
p3 k1 rowcol 0.334±0.039 0.0005±0.0000
p3 k1 grid 0.515±0.050 0.0007±0.0000
p3 k1 grid aug 0.611±0.157 0.0011±0.0006
p3 k2 vec 0.246±0.009 0.0002±0.0000
p3 k2 rowcol 0.278±0.022 0.0005±0.0000
p3 k2 grid 0.616±0.132 0.0008±0.0001
p3 k2 grid aug 0.689±0.218 0.0007±0.0000
streaming cost varies less than error.183
We evaluate paired-source cross-participant transfer under184
the same target and protocol constraints.185
Paired-source transfer helps for some targets but not for all186
targets, so multi-source benefit is conditional rather than univer-187
sal.188
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
Figure 1:Electrode budget trends for word holdout comparing
topk, diversity, and random selection, showing accuracy and
streaming cost.
Table 5:Electrode reduction methods across protocols (proto-
col one word holdout, protocol two instance holdout, protocol
three cross participant).
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

=== PAGE 4 ===
Table 6:Multi source cross participant results by source pair;
group concatenates source participant labels with an arrow to
the target, vec is vector baseline, rowcol is row and column
pooling, grid is convolutional grid encoder, grid aug is grid with
spatial augmentation, CER is character error rate, and RTF is
real time factor.
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
5. Discussion189
Our results show a stable pattern: the main bottleneck is cross-190
participant transfer, while within-participant protocols are eas-191
ier under the same audited pipeline. This gap persists when192
we vary front ends, electrode subsets, and low-shot settings.193
Layout-aware inductive bias alone does not guarantee gains.194
Row and column pooling is the most stable compromise in195
our audited runs, whereas grid-based variants can trade accu-196
racy for latency unless tuning is validated for the specific pro-197
tocol. Source aggregation can improve transfer for the fourth-198
participant target at the aggregate level, but direction-level out-199
comes remain heterogeneous. This target dependence means200
source composition should be selected and validated per de-201
ployment scenario rather than fixed by architecture preference.202
Therefore, we treat protocol-specific benchmarking as the safe203
decision rule: compare candidate models under matched au-204
dited splits, then select by the operating constraint that matters205
most. These conclusions are limited to the audited datasets, la-206
bel normalization, and protocol definitions used here.207
6. Conclusion208
EPGSpeller provides a reproducible benchmark for lexicon-free209
silent spelling under deterministic audited protocols. Within210
this audited setting, cross-participant transfer remains the hard-211
est regime, and paired-source transfer can reduce aggregate212
error without removing target dependence. We recommend213
protocol-specific validation before deployment claims.214
7. Artifacts and Auditability215
This repository uses a strict paper registry that pins every ev-216
idence file by checksum and rejects unsupported manuscript217
blocks. The split manifests, aggregated metrics, compact ta-218
bles, statistical summaries, and analysis reports referenced in219
this paper are stored as deterministic artifacts, enabling audit220
and reproduction within our repository environment. A supple-221
mentary archive includes the compact statistical summary table222
for reviewers.223
8. Ethics and Disclosure224
We report results only for audited artifacts and do not claim225
broader demographic coverage. The datasets and splits used in226
this study are derived from participant recordings, and we focus227
on methodological clarity and artifact traceability rather than228
deployment claims. We used generative AI tools for language229
polishing and verified technical claims against audited artifacts.230

=== PAGE 5 ===
9. References231
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and232
J. Brumberg, “Silent speech interfaces,” 2010.233
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction234
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and235
Computer Engineering. Springer, 2017.236
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,237
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces238
for speech restoration: A review,” 2020.239
[4] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,240
“New developments in electropalatography: A state-of-the-art re-241
port,” 1989.242
[5] W. J. Hardcastle, “Electropalatography in phonetic research and243
in speech training,” 1990.244
[6] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and245
S. Lee, “Biosignal sensors and deep learning-based speech recog-246
nition: A review,” 2021.247
[7] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,248
“Visualisation and analysis of speech production with elec-249
tropalatography,” 2019.250
[8] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and251
evaluation of korean electropalatography (k-epg),” 2021.252
[9] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-253
tion of electropalatographic data using latent variable models,”254
1998.255
[10] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-256
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-257
the-ear silently spelled expressions,” 2024.258
[11] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fagan, R. Moore,259
and P. Green, “Isolated word recognition of silent speech using260
magnetic implants and sensors,” 2010.261
[12] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-262
nectionist temporal classification,” 2006.263
[13] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction264
methods and their implications for studies of lingual coarticula-265
tion,” 1991.266
[14] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and267
M. Stone, “Development of a silent speech interface driven by268
ultrasound and optical images of the tongue and lips,” 2010.269
[15] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,270
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-271
wards mobile, hands-free, silent speech text entry using elec-272
tropalatography,” 2022.273
[16] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-274
surement of face and palate by structured light,” 1993.275
[17] A. Toutios and K. Margaritis, “Learning electropalatograms from276
acoustics,” 2006.277
[18] ——, “On the acoustic-to-electropalatographic mapping,” 2006.278
[19] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,279
and Q. V . Le, “Specaugment: A simple data augmentation method280
for automatic speech recognition,” 2019.281
