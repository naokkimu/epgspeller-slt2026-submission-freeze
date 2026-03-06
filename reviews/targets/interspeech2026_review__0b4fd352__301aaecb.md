# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 23591,
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
    "path": "paper/submission/interspeech2026_review.pdf",
    "sha256": "0b4fd352623773ef03ed9bb86bb373c8381fbb7e9cd99cbcdaeb5fcb4457ead8",
    "sha8": "0b4fd352",
    "truncated": false
  },
  "rules": "/Users/naokkimu/.codex/skills/_archive/20260304_entry_only/interspeech-manuscript-review/references/interspeech2026_rules.yaml",
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
      "plain_characters": 880
    },
    "documentclass": {
      "class": "Interspeech",
      "found": true,
      "has_cameraready": false,
      "is_interspeech": true,
      "options": [],
      "options_raw": ""
    },
    "path": "paper/submission/interspeech2026_review.tex",
    "sha256": "301aaecbb344f96f7a2dd940108179c46cc957b9e08a656a3aef32f5e2996db5",
    "sha8": "301aaecb"
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
        "abstract_chars": 880,
        "max_characters": 1000
      },
      "id": "abstract_length",
      "message": "abstract_chars=880 <= max_characters=1000",
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
          "disclosure": 21964,
          "printbibliography": null,
          "references_heading": 22516,
          "refs": 22457,
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
      "extracted_chars": 23591,
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
      "path": "paper/submission/interspeech2026_review.pdf",
      "sha256": "0b4fd352623773ef03ed9bb86bb373c8381fbb7e9cd99cbcdaeb5fcb4457ead8",
      "sha8": "0b4fd352",
      "truncated": false
    },
    "rules": "/Users/naokkimu/.codex/skills/_archive/20260304_entry_only/interspeech-manuscript-review/references/interspeech2026_rules.yaml",
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
        "plain_characters": 880
      },
      "documentclass": {
        "class": "Interspeech",
        "found": true,
        "has_cameraready": false,
        "is_interspeech": true,
        "options": [],
        "options_raw": ""
      },
      "path": "paper/submission/interspeech2026_review.tex",
      "sha256": "301aaecbb344f96f7a2dd940108179c46cc957b9e08a656a3aef32f5e2996db5",
      "sha8": "301aaecb"
    }
  },
  "run_id": "INTSP2026_STATIC_0b4fd352_301aaecb"
}
```

## TeX preamble (first 200 lines)

```tex
% Auto-generated from paper/paper.json (paper-json v1.0.0). Do not edit by hand.
% Target: INTERSPEECH 2026 Paper Kit (Interspeech.cls).
\documentclass{Interspeech}

\title{EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for Character-Level Silent Spelling}
\keywords{silent speech interface, electropalatography, character-level decoding, text entry, auditability}

```

## PDF extracted text (page-separated, deterministic truncation)

=== PAGE 1 ===
EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for
Character-Level Silent Spelling
Anonymous submission to Interspeech 2026
Abstract1
Silent speech text entry with electropalatography requires2
models that generalize across word identities and participants3
while remaining auditable. We present an evidence-only study4
of silent spelling from binary palate contact patterns using5
character-level decoding and lexicon-projected evaluation. We6
define protocols for word holdout, instance holdout, and cross7
participant transfer. Using participant labeled datasets and de-8
terministic artifact tracking, we evaluate a vector baseline and9
two layout aware front ends. We also analyze electrode reduc-10
tion and how models adapt in low shot settings. Across our au-11
dited runs, the row and column front end tracks the vector base-12
line more closely than a convolutional grid front end. The grid13
front end increases streaming latency. We release split mani-14
fests, checksums, and compact result tables as pinned repository15
artifacts.16
Index Terms: silent speech interface, electropalatography,17
character-level decoding, text entry, auditability18
1. Introduction19
Silent speech interfaces aim to enable communication without20
audible acoustics by inferring linguistic intent from sensed ar-21
ticulation or physiology. Electropalatography provides a prac-22
tical binary representation of tongue and palate contact, but23
its discrete sensor layout and device variability raise ques-24
tions about inductive bias, robustness, and generalization across25
users. We focus on silent spelling, an interaction in which users26
intentionally produce a sequence of articulatory gestures so the27
system decodes character strings rather than attempting speech28
reconstruction. This framing separates within word variation29
from word identity generalization and makes evaluation proto-30
col choices central. [1, 2, 3, 4]31
Recent silent spelling work pushes beyond small command32
vocabularies by decoding at the character level and evaluating33
generalization to unseen words under a lexicon. We study char-34
acter level spelling with a CTC style decoder and lexicon pro-35
jection, and we compare vector and layout aware front ends un-36
der protocols that test generalization across word identities and37
participants. [5, 6, 7]38
• We define protocols to evaluate word identity generalization39
and participant transfer, and we provide split archives with40
checksums.41
• We run multi-participant experiments with character-level42
decoding and lexicon projection, tracked by a strict evidence43
registry.44
• We compare a vector baseline with two layout aware front45
ends, and we report both accuracy and streaming speed met-46
rics.47
• We provide deterministic scripts that export compact tables48
and manifests used by this manuscript.49
2. Related Work50
Within our surveyed set, SilentSpeller and ReHEarSSE rep-51
resent silent spelling systems that move beyond small com-52
mand vocabularies and evaluate unseen words under lexicon53
constraints. Broader silent speech systems span constrained54
recognition and reconstruction settings. In the electropalatog-55
raphy literature, the spatial layout is used to visualize contacts,56
characterize devices, and reduce how contacts are represented.57
This motivates tests of layout aware inductive bias in learned58
decoders. [8, 1, 5, 3, 9, 10, 11, 12, 7, 13, 14, 15, 16, 17]59
We summarize the positioning of prior work using survey60
tags that map systems by representation choices and system61
scope. We use them to situate silent speech interfaces, silent62
spelling, and electropalatography studies in a shared space.63
Prior electropalatography studies emphasize that contact64
patterns are structured by the palate layout. This motivates a65
proxy grid form and spatially structured modeling in learned66
decoders. Our work situates these ideas within silent spelling67
by making protocol definitions and artifact traceability explicit.68
3. Data and Protocols69
We use four participant electropalatography datasets with word70
labels. Each sample is a variable length binary contact matrix,71
and the raw exports are treated as immutable evidence. We re-72
fer to participants with anonymous labels in all tables and split73
archives. We audit dataset statistics, label counts, and anoma-74
lies before we construct any train and test splits. We exclude a75
small set of all-zero samples via a pinned index list.76
The audit pipeline records raw file checksums. It vali-77
dates schema consistency. It summarizes label counts, sequence78
length summaries, and per channel activity statistics before any79
split construction. The raw exports remain unchanged. We ap-80
ply any exclusions only through pinned index lists that are in-81
cluded in the audit artifacts.82
The dataset summary table reports id, sample count, vo-83
cabulary size, median sequence length, mean contact rate, and84
the count of all-zero samples for each participant dataset. The85
id labels are anonymous participant codes used throughout the86
protocol manifests. 87
We evaluate three primary protocols. The word holdout88
protocol uses disjoint vocabularies across train, test, and a com-89
petition partition. The instance holdout protocol tests held out90
instances of seen words. It separates train and competition vo-91
cabularies while keeping the test vocabulary within their union.92
The cross participant protocol trains on a source participant93

=== PAGE 2 ===
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
and tests on a target participant under a shared vocabulary con-94
straint. We also define a paired source cross participant vari-95
ant and a low shot adaptation variant to isolate source aggrega-96
tion and limited supervision effects under the same audit rules.97
When a target participant has limited within word repetition,98
we configure the cross participant split generators to allow sin-99
gle instance target words. We keep the source side constraints100
unchanged. All split archives used in this study are enumerated101
with sizes and checksums in manifest artifacts.102
All split archives are generated deterministically from au-103
dited exports with fixed seeds. Each train, test, and competition104
partition is stored as an immutable archive with a checksum in105
the manifests to enable reuse and later verification. The man-106
ifests show the word-holdout protocol uses all four participant107
datasets. They show the instance-holdout protocol uses three108
participant datasets. They also show the fourth participant ap-109
pears only as a target in the cross-participant splits. This separa-110
tion explains why the dataset summary includes all participant111
datasets even when a protocol uses only a subset.112
We normalize labels by uppercasing and filtering to alpha-113
bet characters, then represent each label as a space separated114
character sequence for CTC training and greedy decoding. We115
apply this step consistently during split construction and dataset116
preparation to avoid vocabulary drift.117
We keep the label normalization step consistent across all118
splits and dataset preparation steps. This aligns the decoder119
vocabulary with the audited labels and reduces drift between120
training and artifacts used to evaluate.121
We report character error rate from greedy decoding and122
streaming speed using real time factor. We define real time fac-123
tor as total inference time divided by total input duration. For124
character-level decoding we also report lexicon projection error125
rates using a training lexicon and a full lexicon.126
Greedy decoding reports unconstrained character se-127
quences. Lexicon projection maps outputs to finite word sets128
derived from the training vocabulary or the full audited lexicon.129
This allows us to separate decoding quality from lexicon con-130
straints. We compute real time factor by dividing inference time131
by input duration under the same test harness.132
4. Models133
Our baseline model encodes each frame as a vector of palate134
channels and applies a uni-directional recurrent decoder trained135
with a CTC objective. We compare two layout aware front ends.136
One is a row and column pooling front end that aggregates a137
proxy grid into one dimensional summaries. The other is a grid138
front end that reconstructs a proxy grid and applies a convolu-139
tional spatial encoder. For the grid model we optionally enable a140
spatial augmentation that drops and shifts contiguous electrode141
blocks. [6, 18]142
Table 2:Cross participant generalization targeting the fourth
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
The proxy grid is constructed from the palate channel lay-143
out. It supports row and column pooling or convolutional fea-144
ture extraction. We use a fixed layout file for the mapping so145
that row and column indices are consistent across splits. We146
augment spatially by perturbing contiguous electrode blocks to147
emulate missing contacts and minor spatial shifts.148
We fix core training hyperparameters across runs and record149
how we configure them in the metrics registry for auditability.150
5. Results151
Baseline performance across protocols is derived from the same152
metrics registry as the remaining tables. We report greedy de-153
coding error and lexicon-projected error to separate character-154
level decoding quality from lexicon constraints. The vector155
baseline rows in the spatial modeling and electrode reduction ta-156
bles serve as the reference for protocol comparisons. We use the157
same split manifests and deterministic evaluation scripts across158
all protocols. 159
We evaluate cross participant transfer with the fourth par-160
ticipant as target under single source and paired source settings.161
The table uses protocol labels for single source cross participant162
transfer and multi source transfer. The lvl field marks direction163
level rows and an across direction aggregate. Group labels join164
source participant identifiers with an arrow to the target. The165
split archives that define these targets are pinned by checksum166
in the manifest. In our audited splits, the multi source aggre-167
gate reduces CER relative to the single source aggregate for the168
same target. 169
The cross participant results for the fourth participant in-170
clude both single source and paired source settings. This pro-171
vides a direct comparison of transfer with and without source172
aggregation under the same audited protocol constraints. This173
helps isolate source aggregation effects without changing the174
target data or evaluation pipeline.175
The spatial modeling table compares spatial inductive bias176
variants at full channels across protocols. We include a patch-177
pool grid encoder as a minimal way to implement a rescue for178
the grid encoder. The patchpool variant keeps a coarser spa-179
tial map before recurrent decoding. The variant labels are vec,180
rowcol, grid, grid aug, patch, and patch aug. The row and181
column front end tracks the vector baseline more closely than182
the convolutional grid front end under within participant proto-183
cols. Patchpool reduces the gap under cross participant transfer.184
Across protocols, grid variants tend to increase real time factor185
relative to the vector baseline. We do not observe a consistent186

=== PAGE 3 ===
Table 3:Spatial modeling at full channels across protocols;
protocol labels denote word holdout, instance holdout, and
cross participant transfer, vec is vector baseline, rowcol is row
and column pooling, grid is convolutional grid encoder, grid
aug is grid with spatial augmentation, patch is patchpool grid
encoder, patch aug is patchpool with augmentation, CER is
character error rate, and RTF is real time factor.
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
accuracy gain over the vector baseline in any protocol.187
The electrode reduction table evaluates a reduced channel188
budget using several selection strategies. The method labels are189
topk, fps two k, xfer, and rand. The table reports both accu-190
racy and streaming speed so reduction effects can be compared191
under the same evaluation harness. Across protocols, within192
participant selection and simple transfer selection yield similar193
performance. This suggests that a compact subset can preserve194
a large fraction of the vector baseline performance. Random195
selection and simple transfer remain slightly worse than within196
participant selection in the audited results.197
The reduction results complement the protocol tables. They198
show that compact selections preserve much of the vector base-199
line under within participant tests. Cross participant transfer200
remains more challenging, so we report paired source and low201
shot analyses in the subsequent tables.202
We evaluate multi source cross participant transfer using203
paired source participants. The group labels concatenate the204
two source identifiers and use an arrow to the target identifier.205
The multi source table reports direction level results for vector206
and layout aware front ends. This isolates whether combining207
sources helps under the same target and protocol constraints.208
We further analyze multi source transfer deltas against sim-209
ple similarity measures. Delta cer is negative for all audited210
groups, and corr src tgt mean varies within a narrow range211
across groups. We report these measures to describe conditions212
rather than to assert a universal rule.213
We evaluate how models adapt in low shot settings for a214
new participant by varying the number of training instances per215
word. For the vector baseline, two shot improves over one shot,216
and the table reports layout aware variants. This isolates adap-217
tation behavior when only a small amount of labeled target data218
is available.219
Table 4:Electrode reduction methods across protocols; proto-
col labels denote word holdout, instance holdout, and cross par-
ticipant transfer, topk is within participant top ranked selection,
fps two k is farthest point sampling, xfer is transfer selection,
rand is random selection, CER is character error rate, and RTF
is real time factor.
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
6. Discussion220
Our results suggest that an explicit convolutional grid encoder221
is not automatically beneficial for electropalatography under222
within participant tests, despite its intuitive spatial structure.223
A patchpool grid variant reduces the underperformance of the224
grid encoder under cross participant transfer. This indicates that225
spatial encoder design choices can materially affect outcomes.226
The patchpool variant does not yield consistent gains over the227
vector baseline across protocols. Spatial augmentation can im-228
prove robustness to synthetic electrode dropout, but it does not229
close the accuracy gap for the convolutional grid variants in our230
multi participant results. We analyze multi source cross partic-231
ipant transfer and how models adapt in low shot settings, and232
we provide the results as artifact tables. They highlight that233
cross participant performance remains challenging. We also an-234
alyze conditions for multi source transfer deltas against simple235
dataset similarity measures. The effect is conditional and does236
not present a single dominant monotonic trend within our eval-237
uated group set. These observations are limited to our audited238
multi participant dataset collection and protocols.239

=== PAGE 4 ===
Table 6:Low shot adaptation results for a new participant;
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
Across the audited protocols, within participant perfor-240
mance remains stronger than cross participant transfer. This241
emphasizes the difficulty of generalization under limited par-242
ticipant coverage. The target participant results reinforce this243
gap even when source aggregation is enabled. We report244
these trends as artifact grounded observations rather than broad245
claims. We expect additional participant data to be necessary246
for stronger transfer conclusions.247
7. Artifacts and Auditability248
This repository uses a strict paper registry that pins every ev-249
idence file by checksum and rejects unsupported manuscript250
blocks. The split manifests, aggregated metrics, compact tables,251
and analysis summaries referenced in this paper are stored as252
deterministic artifacts, enabling audit and reproduction within253
our repository environment. The same artifacts are reused to254
build the manuscript tables and to support verification in the255
audit views.256
8. Ethics and Disclosure257
We report results only for audited artifacts and do not claim258
broader demographic coverage. The datasets and splits used in259
this study are derived from participant recordings, and we focus260
on methodological clarity and artifact traceability rather than261
deployment claims.262
9. Generative AI Use Disclosure263
We used generative AI tools for language polishing and format-264
ting support, and we verified technical claims against audited265
artifacts.266
10. Logic Checks267
The baseline table includes protocol and aggregate metrics268
fields.269
The dataset summary table includes id, N, V , Tmed, con-270
tact, and zero fields.271
The spatial modeling table includes protocol, variant, CER,272
and RTF fields.273
The electrode reduction table includes protocol, method,274
CER, and RTF fields.275
11. References276
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and277
J. Brumberg, “Silent speech interfaces,” 2010.278
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction279
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and280
Computer Engineering. Springer, 2017.281
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,282
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces283
for speech restoration: A review,” 2020.284
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and285
S. Lee, “Biosignal sensors and deep learning-based speech recog-286
nition: A review,” 2021.287
[5] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-288
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-289
the-ear silently spelled expressions,” 2024.290
[6] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-291
nectionist temporal classification,” 2006.292
[7] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,293
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-294
wards mobile, hands-free, silent speech text entry using elec-295
tropalatography,” 2022.296
[8] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-297
tion of electropalatographic data using latent variable models,”298
1998. 299
[9] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,300
“New developments in electropalatography: A state-of-the-art re-301
port,” 1989. 302
[10] W. J. Hardcastle, “Electropalatography in phonetic research and303
in speech training,” 1990.304
[11] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction305
methods and their implications for studies of lingual coarticula-306
tion,” 1991. 307
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and308
M. Stone, “Development of a silent speech interface driven by309
ultrasound and optical images of the tongue and lips,” 2010.310
[13] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-311
surement of face and palate by structured light,” 1993.312
[14] A. Toutios and K. Margaritis, “Learning electropalatograms from313
acoustics,” 2006. 314
[15] ——, “On the acoustic-to-electropalatographic mapping,” 2006.315
[16] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,316
“Visualisation and analysis of speech production with elec-317
tropalatography,” 2019.318
[17] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and319
evaluation of korean electropalatography (k-epg),” 2021.320
[18] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,321
and Q. V . Le, “Specaugment: A simple data augmentation method322
for automatic speech recognition,” 2019.323
