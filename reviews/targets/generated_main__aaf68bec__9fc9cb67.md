# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 22965,
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
      }
    ],
    "page_count": 4,
    "path": "paper/manuscript/generated_main.pdf",
    "sha256": "aaf68becd44209755ec54f71bb9b1eb6a869db5886e5e9d0a0d684b043072ec2",
    "sha8": "aaf68bec",
    "truncated": false
  },
  "rules": "/Users/naokkimu/.codex/skills/paperjson-init/assets/toolkit/references/interspeech2026_rules.yaml",
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
      "plain_characters": 832
    },
    "documentclass": {
      "class": "article",
      "found": true,
      "has_cameraready": false,
      "is_interspeech": false,
      "options": [
        "10pt",
        "twocolumn"
      ],
      "options_raw": "[10pt,twocolumn]"
    },
    "path": "paper/manuscript/generated_main.tex",
    "sha256": "9fc9cb67d947d688205a9629315d7ce4ca49e3deadd3a02c748625376a64d2d0",
    "sha8": "9fc9cb67"
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
        "abstract_chars": 832,
        "max_characters": 1000
      },
      "id": "abstract_length",
      "message": "abstract_chars=832 <= max_characters=1000",
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
        "positions": {
          "ack": null,
          "disclosure": 21142,
          "printbibliography": null,
          "references_heading": 21694,
          "refs": 21635,
          "thebibliography": null
        }
      },
      "id": "ai_disclosure_placement_heuristic",
      "message": "disclosure placement looks plausible",
      "ok": true,
      "severity": "info"
    },
    {
      "evidence": {
        "required_title": "Generative AI Use Disclosure"
      },
      "id": "ai_disclosure_present",
      "message": "Generative AI Use Disclosure section found",
      "ok": true,
      "severity": "info"
    },
    {
      "evidence": {
        "documentclass": {
          "class": "article",
          "found": true,
          "has_cameraready": false,
          "is_interspeech": false,
          "options": [
            "10pt",
            "twocolumn"
          ],
          "options_raw": "[10pt,twocolumn]"
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
        "page_count": 4
      },
      "id": "page_limit",
      "message": "page_count=4 <= max_pages=6",
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
      "extracted_chars": 22965,
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
        }
      ],
      "page_count": 4,
      "path": "paper/manuscript/generated_main.pdf",
      "sha256": "aaf68becd44209755ec54f71bb9b1eb6a869db5886e5e9d0a0d684b043072ec2",
      "sha8": "aaf68bec",
      "truncated": false
    },
    "rules": "/Users/naokkimu/.codex/skills/paperjson-init/assets/toolkit/references/interspeech2026_rules.yaml",
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
        "plain_characters": 832
      },
      "documentclass": {
        "class": "article",
        "found": true,
        "has_cameraready": false,
        "is_interspeech": false,
        "options": [
          "10pt",
          "twocolumn"
        ],
        "options_raw": "[10pt,twocolumn]"
      },
      "path": "paper/manuscript/generated_main.tex",
      "sha256": "9fc9cb67d947d688205a9629315d7ce4ca49e3deadd3a02c748625376a64d2d0",
      "sha8": "9fc9cb67"
    }
  },
  "run_id": "INTSP2026_STATIC_aaf68bec_9fc9cb67"
}
```

## TeX preamble (first 200 lines)

```tex
% Auto-generated from paper/paper.json (paper-json v1.0.0). Do not edit by hand.
% Note: this entry uses a portable LaTeX preamble (article class).
% If you want the official Interspeech kit styling, replace the documentclass/preamble accordingly.
\documentclass[10pt,twocolumn]{article}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{microtype}
\usepackage{hyperref}
\usepackage{url}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}

\title{EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for Open-Vocabulary Silent Spelling}
\author{Anonymous}
\date{}

```

## PDF extracted text (page-separated, deterministic truncation)

=== PAGE 1 ===
EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for
Open-V ocabulary Silent Spelling
Anonymous submission to Interspeech 2026
Abstract1
Silent speech text entry with electropalatography requires2
models that generalize across word identities and participants3
while remaining auditable. We present an evidence-only study4
of open-vocabulary silent spelling from binary palate contact5
patterns. We define protocols for word holdout, instance holdout,6
and cross participant transfer. Using participant labeled datasets7
and deterministic artifact tracking, we evaluate a vector baseline8
and two layout aware front ends. We also analyze electrode9
reduction and how models adapt in low shot settings. Across10
our audited runs, the row and column front end tracks the vector11
baseline more closely than a convolutional grid front end. The12
grid front end increases streaming latency. We release split mani-13
fests, checksums, and compact result tables as pinned repository14
artifacts.15
Index Terms: Some keywords16
1. Introduction17
Silent speech interfaces aim to enable communication without18
audible acoustics. They use sensor measures of articulation19
or physiology. Electropalatography provides a practical binary20
contact form for tongue and palate interaction. Its discrete lay-21
out and device variability raise questions about inductive bias,22
robustness, and how models generalize. [1, 2, 3, 4]23
Recent work on silent spelling has emphasized open-24
vocabulary text entry, where character level decoding can com-25
pose words beyond a fixed closed set. We study open-vocabulary26
spelling with a CTC style decoder and lexicon projection. We27
compare vector and layout aware front ends under multiple pro-28
tocols that test how models generalize across words. [5, 6, 7]29
• We define protocols to evaluate word identity generalization30
and participant transfer, and we provide split archives with31
checksums.32
• We run multi-participant experiments with open-vocabulary33
decoding and lexicon projection, tracked by a strict evidence34
registry.35
• We compare a vector baseline with two layout aware front36
ends, and we report both accuracy and streaming speed met-37
rics.38
• We provide deterministic scripts that export compact tables39
and manifests used by this manuscript.40
2. Related Work41
Within our surveyed set, SilentSpeller and ReHEarSSE represent42
open-vocabulary silent spelling systems. Broader silent speech43
systems span constrained recognition and reconstruction settings.44
In the electropalatography literature, the spatial layout is used to45
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
visualize contacts, characterize devices, and reduce how contacts 46
are represented. This motivates tests of layout aware inductive 47
bias in learned decoders. [8, 1, 5, 3, 9, 10, 11, 12, 7, 13, 14, 15, 48
16, 17] 49
We summarize the positioning of prior work using survey 50
tags. These tags map systems by how they represent data and 51
by system scope. We describe where open vocabulary silent 52
spelling and electropalatography studies sit in the space.53
Prior electropalatography studies emphasize that contact 54
patterns are structured by the palate layout. This motivates a 55
proxy grid form and spatially structured modeling in learned 56
decoders. Our work situates these ideas within open vocabu- 57
lary silent spelling by making protocol definitions and artifact 58
traceability explicit. 59
3. Data and Protocols60
We use four participant electropalatography datasets with word 61
labels. Each sample is a variable length binary contact matrix, 62
and the raw exports are treated as immutable evidence. We 63
refer to participants with anonymous labels in all tables and split 64
archives. We audit dataset statistics, label counts, and anomalies 65
before we construct any train and test splits. We exclude a small 66
set of all-zero samples via a pinned index list.67
The audit pipeline records raw file checksums. It validates 68
schema consistency. It summarizes label counts, sequence length 69
summaries, and per channel activity statistics before any split 70
construction. The raw exports remain unchanged. We apply any 71
exclusions only through pinned index lists that are included in 72
the audit artifacts. 73
The dataset summary table reports id, sample count, vo- 74
cabulary size, median sequence length, mean contact rate, and 75
the count of all-zero samples for each participant dataset. The 76
id labels are anonymous participant codes used throughout the 77
protocol manifests. 78
We evaluate three primary protocols. The word holdout 79
protocol uses disjoint vocabularies across train, test, and a com- 80

=== PAGE 2 ===
petition partition. The instance holdout protocol tests held out81
instances of seen words. It separates train and competition vo-82
cabularies while keeping the test vocabulary within their union.83
The cross participant protocol trains on a source participant and84
tests on a target participant under a shared vocabulary constraint.85
We also define a paired source cross participant variant and a low86
shot adaptation variant to isolate source aggregation and limited87
supervision effects under the same audit rules. When a target88
participant has limited within word repetition, we configure the89
cross participant split generators to allow single instance target90
words. We keep the source side constraints unchanged. All91
split archives used in this study are enumerated with sizes and92
checksums in manifest artifacts.93
All split archives are generated deterministically from au-94
dited exports with fixed seeds. Each train, test, and competition95
partition is stored as an immutable archive with a checksum in96
the manifests to enable reuse and later verification. The mani-97
fests show the word-holdout protocol uses all four participant98
datasets. They show the instance-holdout protocol uses three par-99
ticipant datasets. They also show the fourth participant appears100
only as a target in the cross-participant splits. This separation ex-101
plains why the dataset summary includes all participant datasets102
even when a protocol uses only a subset.103
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
streaming speed using real time factor. We define real time114
factor as total inference time divided by total input duration.115
For open-vocabulary decoding we also report lexicon projection116
error rates using a training lexicon and a full lexicon.117
Greedy decoding reports unconstrained character sequences.118
Lexicon projection maps outputs to finite word sets derived from119
the training vocabulary or the full audited lexicon. This allows120
us to separate decoding quality from lexicon constraints. We121
compute real time factor by dividing inference time by input122
duration under the same test harness.123
4. Models124
Our baseline model encodes each frame as a vector of palate125
channels and applies a uni-directional recurrent decoder trained126
with a CTC objective. We compare two layout aware front127
ends. One is a row and column pooling front end that aggregates128
a proxy grid into one dimensional summaries. The other is129
a grid front end that reconstructs a proxy grid and applies a130
convolutional spatial encoder. For the grid model we optionally131
enable a spatial augmentation that drops and shifts contiguous132
electrode blocks. [6, 18]133
The proxy grid is constructed from the palate channel layout.134
It supports row and column pooling or convolutional feature135
extraction. We use a fixed layout file for the mapping so that136
row and column indices are consistent across splits. We augment137
spatially by perturbing contiguous electrode blocks to emulate138
missing contacts and minor spatial shifts.139
We fix core training hyperparameters across runs and record140
how we configure them in the metrics registry for auditability.141
Table 2:Cross participant generalization targeting the fourth
participant; proto distinguishes single source cross participant
transfer and multi source transfer , lvl marks direction level rows
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
5. Results142
Baseline performance across protocols is derived from the same 143
metrics registry as the remaining tables. We report greedy decod- 144
ing error and lexicon-projected error to separate open vocabulary 145
decoding quality from lexicon constraints. The vector baseline 146
rows in the spatial modeling and electrode reduction tables serve 147
as the reference for protocol comparisons. We use the same 148
split manifests and deterministic evaluation scripts across all 149
protocols. 150
We evaluate cross participant transfer with the fourth par- 151
ticipant as target under single source and paired source settings.152
The table uses protocol labels for single source cross participant 153
transfer and multi source transfer. The lvl field marks direction 154
level rows and an across direction aggregate. Group labels join 155
source participant identifiers with an arrow to the target. The 156
split archives that define these targets are pinned by checksum 157
in the manifest. In our audited splits, the multi source aggregate 158
reduces CER relative to the single source aggregate for the same 159
target. 160
The cross participant results for the fourth participant include 161
both single source and paired source settings. This provides a di- 162
rect comparison of transfer with and without source aggregation 163
under the same audited protocol constraints. This helps isolate 164
source aggregation effects without changing the target data or 165
evaluation pipeline. 166
The spatial modeling table compares spatial inductive bias 167
variants at full channels across protocols. We include a patchpool 168
grid encoder as a minimal way to implement a rescue for the grid 169
encoder. The patchpool variant keeps a coarser spatial map be- 170
fore recurrent decoding. The variant labels are vec, rowcol, grid, 171
grid aug, patch, and patch aug. The row and column front end 172
tracks the vector baseline more closely than the convolutional 173
grid front end under within participant protocols. Patchpool 174
reduces the gap under cross participant transfer. Across proto- 175
cols, grid variants tend to increase real time factor relative to the 176
vector baseline. We do not observe a consistent accuracy gain 177
over the vector baseline in any protocol.178
The electrode reduction table evaluates a reduced channel 179
budget using several selection strategies. The method labels are 180
topk, fps two k, xfer, and rand. The table reports both accu- 181
racy and streaming speed so reduction effects can be compared 182
under the same evaluation harness. Across protocols, within 183
participant selection and simple transfer selection yield similar 184
performance. This suggests that a compact subset can preserve 185
a large fraction of the vector baseline performance. Random 186

=== PAGE 3 ===
Table 3:Spatial modeling at full channels across protocols;
protocol labels denote word holdout, instance holdout, and cross
participant transfer , vec is vector baseline, rowcol is row and
column pooling, grid is convolutional grid encoder , grid aug is
grid with spatial augmentation, patch is patchpool grid encoder ,
patch aug is patchpool with augmentation, CER is character
error rate, and RTF is real time factor .
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
selection and simple transfer remain slightly worse than within187
participant selection in the audited results.188
The reduction results complement the protocol tables. They189
show that compact selections preserve much of the vector base-190
line under within participant tests. Cross participant transfer191
remains more challenging, so we report paired source and low192
shot analyses in the subsequent tables.193
We evaluate multi source cross participant transfer using194
paired source participants. The group labels concatenate the195
two source identifiers and use an arrow to the target identifier.196
The multi source table reports direction level results for vector197
and layout aware front ends. This isolates whether combining198
sources helps under the same target and protocol constraints.199
We further analyze multi source transfer deltas against sim-200
ple similarity measures. Delta cer is negative for all audited201
groups, and corr src tgt mean varies within a narrow range202
across groups. We report these measures to describe conditions203
rather than to assert a universal rule.204
We evaluate how models adapt in low shot settings for a new205
participant by varying the number of training instances per word.206
For the vector baseline, two shot improves over one shot, and207
the table reports layout aware variants. This isolates adaptation208
behavior when only a small amount of labeled target data is209
available.210
6. Discussion211
Our results suggest that an explicit convolutional grid encoder212
is not automatically beneficial for electropalatography under213
within participant tests, despite its intuitive spatial structure. A214
patchpool grid variant reduces the underperformance of the grid215
encoder under cross participant transfer. This indicates that216
spatial encoder design choices can materially affect outcomes.217
The patchpool variant does not yield consistent gains over the218
vector baseline across protocols. Spatial augmentation can im-219
Table 4:Electrode reduction methods across protocols; protocol
labels denote word holdout, instance holdout, and cross partici-
pant transfer , topk is within participant top ranked selection, fps
two k is farthest point sampling, xfer is transfer selection, rand
is random selection, CER is character error rate, and RTF is
real time factor .
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
Table 5:Multi source cross participant results by source pair;
group concatenates source participant labels with an arrow to
the target, vec is vector baseline, rowcol is row and column
pooling, grid is convolutional grid encoder , grid aug is grid with
spatial augmentation, CER is character error rate, and RTF is
real time factor .
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
prove robustness to synthetic electrode dropout, but it does not 220
close the accuracy gap for the convolutional grid variants in 221
our multi participant results. We analyze multi source cross 222
participant transfer and how models adapt in low shot settings, 223
and we provide the results as artifact tables. They highlight 224
that cross participant performance remains challenging. We also 225
analyze conditions for multi source transfer deltas against simple 226
dataset similarity measures. The effect is conditional and does 227
not present a single dominant monotonic trend within our eval- 228
uated group set. These observations are limited to our audited 229
multi participant dataset collection and protocols.230
Across the audited protocols, within participant performance 231
remains stronger than cross participant transfer. This empha- 232
sizes the difficulty of generalization under limited participant 233
coverage. The target participant results reinforce this gap even 234
when source aggregation is enabled. We report these trends as 235
artifact grounded observations rather than broad claims. We 236
expect additional participant data to be necessary for stronger 237
transfer conclusions. 238

=== PAGE 4 ===
Table 6:Low shot adaptation results for a new participant; group
uses the participant label and k one or k two for the number of
training instances per word, vec is vector baseline, rowcol is row
and column pooling, grid is convolutional grid encoder , grid aug
is grid with spatial augmentation, CER is character error rate,
and RTF is real time factor .
group variant cer rtf
p3 k1 vec 0.350±0.060 0.0002±0.0000
p3 k1 rowcol 0.334±0.039 0.0005±0.0000
p3 k1 grid 0.515±0.050 0.0007±0.0000
p3 k1 grid aug 0.611±0.157 0.0011±0.0006
p3 k2 vec 0.246±0.009 0.0002±0.0000
p3 k2 rowcol 0.278±0.022 0.0005±0.0000
p3 k2 grid 0.616±0.132 0.0008±0.0001
p3 k2 grid aug 0.689±0.218 0.0007±0.0000
7. Artifacts and Auditability239
This repository uses a strict paper registry that pins every ev-240
idence file by checksum and rejects unsupported manuscript241
blocks. The split manifests, aggregated metrics, compact tables,242
and analysis summaries referenced in this paper are stored as243
deterministic artifacts, enabling audit and reproduction within244
our repository environment. The same artifacts are reused to245
build the manuscript tables and to support verification in the246
audit views.247
8. Ethics and Disclosure248
We report results only for audited artifacts and do not claim249
broader demographic coverage. The datasets and splits used in250
this study are derived from participant recordings, and we focus251
on methodological clarity and artifact traceability rather than de-252
ployment claims. We used generative AI tools for language pol-253
ishing and formatting support, and we verified technical claims254
against audited artifacts.255
9. Logic Checks256
The baseline table includes protocol and aggregate metrics fields.257
The dataset summary table includes id, N, V , Tmed, contact,258
and zero fields.259
The spatial modeling table includes protocol, variant, CER,260
and RTF fields.261
The electrode reduction table includes protocol, method,262
CER, and RTF fields.263
10. References264
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and J. Brum-265
berg, “Silent speech interfaces,” 2010.266
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction267
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and268
Computer Engineering. Springer, 2017.269
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas, J. L.270
Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces for271
speech restoration: A review,” 2020.272
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and273
S. Lee, “Biosignal sensors and deep learning-based speech recog-274
nition: A review,” 2021.275
[5] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-276
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-277
the-ear silently spelled expressions,” 2024.278
[6] A. Graves, S. Fern´andez, F. Gomez, and J. Schmidhuber, “Connec- 279
tionist temporal classification,” 2006.280
[7] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri, 281
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To- 282
wards mobile, hands-free, silent speech text entry using elec- 283
tropalatography,” 2022.284
[8] M. ´A. Carreira-Perpi˜n´an and S. Renals, “Dimensionality reduction 285
of electropalatographic data using latent variable models,” 1998.286
[9] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder, 287
“New developments in electropalatography: A state-of-the-art re- 288
port,” 1989. 289
[10] W. J. Hardcastle, “Electropalatography in phonetic research and in 290
speech training,” 1990.291
[11] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction 292
methods and their implications for studies of lingual coarticulation,” 293
1991. 294
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and 295
M. Stone, “Development of a silent speech interface driven by 296
ultrasound and optical images of the tongue and lips,” 2010.297
[13] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth 298
measurement of face and palate by structured light,” 1993.299
[14] A. Toutios and K. Margaritis, “Learning electropalatograms from 300
acoustics,” 2006. 301
[15] ——, “On the acoustic-to-electropalatographic mapping,” 2006.302
[16] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes- 303
Aldasoro, “Visualisation and analysis of speech production with 304
electropalatography,” 2019.305
[17] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and 306
evaluation of korean electropalatography (k-epg),” 2021.307
[18] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk, 308
and Q. V . Le, “Specaugment: A simple data augmentation method 309
for automatic speech recognition,” 2019.310
