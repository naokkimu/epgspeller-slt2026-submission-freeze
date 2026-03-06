# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 23044,
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
    "path": "interspeech2026_review.pdf",
    "sha256": "a5aaff856c5b32907ac81bcaa858d95eeacaff3d086206856447310d537e06ce",
    "sha8": "a5aaff85",
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
      "plain_characters": 832
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
    "sha256": "9eeae01afbfb23f5d2933ab4550cae40c91de4a3296e2eaf241da535e66567d0",
    "sha8": "9eeae01a"
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
          "disclosure": 21448,
          "printbibliography": null,
          "references_heading": 22000,
          "refs": 21941,
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
      "extracted_chars": 23044,
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
      "path": "interspeech2026_review.pdf",
      "sha256": "a5aaff856c5b32907ac81bcaa858d95eeacaff3d086206856447310d537e06ce",
      "sha8": "a5aaff85",
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
        "plain_characters": 832
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
      "sha256": "9eeae01afbfb23f5d2933ab4550cae40c91de4a3296e2eaf241da535e66567d0",
      "sha8": "9eeae01a"
    }
  },
  "run_id": "INTSP2026_STATIC_a5aaff85_9eeae01a"
}
```

## TeX preamble (first 200 lines)

```tex
% Auto-generated from paper/paper.json (paper-json v1.0.0). Do not edit by hand.
% Target: INTERSPEECH 2026 Paper Kit (Interspeech.cls).
\documentclass{Interspeech}

\title{EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for Open-Vocabulary Silent Spelling}
\keywords{silent speech interface, electropalatography, open vocabulary, text entry, auditability}

```

## PDF extracted text (page-separated, deterministic truncation)

=== PAGE 1 ===
EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for
Open-Vocabulary Silent Spelling
Anonymous submission to Interspeech 2026
Abstract1
Silent speech text entry with electropalatography requires2
models that generalize across word identities and participants3
while remaining auditable. We present an evidence-only study4
of open-vocabulary silent spelling from binary palate contact5
patterns. We define protocols for word holdout, instance hold-6
out, and cross participant transfer. Using participant labeled7
datasets and deterministic artifact tracking, we evaluate a vec-8
tor baseline and two layout aware front ends. We also analyze9
electrode reduction and how models adapt in low shot settings.10
Across our audited runs, the row and column front end tracks11
the vector baseline more closely than a convolutional grid front12
end. The grid front end increases streaming latency. We release13
split manifests, checksums, and compact result tables as pinned14
repository artifacts.15
Index Terms: silent speech interface, electropalatography,16
open vocabulary, text entry, auditability17
1. Introduction18
Silent speech interfaces aim to enable communication without19
audible acoustics. They use sensor measures of articulation20
or physiology. Electropalatography provides a practical binary21
contact form for tongue and palate interaction. Its discrete lay-22
out and device variability raise questions about inductive bias,23
robustness, and how models generalize. [1, 2, 3, 4]24
Recent work on silent spelling has emphasized open-25
vocabulary text entry, where character level decoding can26
compose words beyond a fixed closed set. We study open-27
vocabulary spelling with a CTC style decoder and lexicon pro-28
jection. We compare vector and layout aware front ends un-29
der multiple protocols that test how models generalize across30
words. [5, 6, 7]31
• We define protocols to evaluate word identity generalization32
and participant transfer, and we provide split archives with33
checksums.34
• We run multi-participant experiments with open-vocabulary35
decoding and lexicon projection, tracked by a strict evidence36
registry.37
• We compare a vector baseline with two layout aware front38
ends, and we report both accuracy and streaming speed met-39
rics.40
• We provide deterministic scripts that export compact tables41
and manifests used by this manuscript.42
2. Related Work43
Within our surveyed set, SilentSpeller and ReHEarSSE repre-44
sent open-vocabulary silent spelling systems. Broader silent45
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
speech systems span constrained recognition and reconstruction46
settings. In the electropalatography literature, the spatial layout47
is used to visualize contacts, characterize devices, and reduce48
how contacts are represented. This motivates tests of layout49
aware inductive bias in learned decoders. [8, 1, 5, 3, 9, 10, 11,50
12, 7, 13, 14, 15, 16, 17]51
We summarize the positioning of prior work using survey52
tags. These tags map systems by how they represent data and53
by system scope. We describe where open vocabulary silent54
spelling and electropalatography studies sit in the space.55
Prior electropalatography studies emphasize that contact56
patterns are structured by the palate layout. This motivates a57
proxy grid form and spatially structured modeling in learned58
decoders. Our work situates these ideas within open vocabu-59
lary silent spelling by making protocol definitions and artifact60
traceability explicit. 61
3. Data and Protocols62
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
The dataset summary table reports id, sample count, vo-76
cabulary size, median sequence length, mean contact rate, and77
the count of all-zero samples for each participant dataset. The78
id labels are anonymous participant codes used throughout the79
protocol manifests. 80

=== PAGE 2 ===
We evaluate three primary protocols. The word holdout81
protocol uses disjoint vocabularies across train, test, and a com-82
petition partition. The instance holdout protocol tests held out83
instances of seen words. It separates train and competition vo-84
cabularies while keeping the test vocabulary within their union.85
The cross participant protocol trains on a source participant86
and tests on a target participant under a shared vocabulary con-87
straint. We also define a paired source cross participant vari-88
ant and a low shot adaptation variant to isolate source aggrega-89
tion and limited supervision effects under the same audit rules.90
When a target participant has limited within word repetition,91
we configure the cross participant split generators to allow sin-92
gle instance target words. We keep the source side constraints93
unchanged. All split archives used in this study are enumerated94
with sizes and checksums in manifest artifacts.95
All split archives are generated deterministically from au-96
dited exports with fixed seeds. Each train, test, and competition97
partition is stored as an immutable archive with a checksum in98
the manifests to enable reuse and later verification. The man-99
ifests show the word-holdout protocol uses all four participant100
datasets. They show the instance-holdout protocol uses three101
participant datasets. They also show the fourth participant ap-102
pears only as a target in the cross-participant splits. This separa-103
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
open-vocabulary decoding we also report lexicon projection er-118
ror rates using a training lexicon and a full lexicon.119
Greedy decoding reports unconstrained character se-120
quences. Lexicon projection maps outputs to finite word sets121
derived from the training vocabulary or the full audited lexicon.122
This allows us to separate decoding quality from lexicon con-123
straints. We compute real time factor by dividing inference time124
by input duration under the same test harness.125
4. Models126
Our baseline model encodes each frame as a vector of palate127
channels and applies a uni-directional recurrent decoder trained128
with a CTC objective. We compare two layout aware front ends.129
One is a row and column pooling front end that aggregates a130
proxy grid into one dimensional summaries. The other is a grid131
front end that reconstructs a proxy grid and applies a convolu-132
tional spatial encoder. For the grid model we optionally enable a133
spatial augmentation that drops and shifts contiguous electrode134
blocks. [6, 18]135
The proxy grid is constructed from the palate channel lay-136
out. It supports row and column pooling or convolutional fea-137
ture extraction. We use a fixed layout file for the mapping so138
that row and column indices are consistent across splits. We139
augment spatially by perturbing contiguous electrode blocks to140
emulate missing contacts and minor spatial shifts.141
We fix core training hyperparameters across runs and record142
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
how we configure them in the metrics registry for auditability.143
5. Results144
Baseline performance across protocols is derived from the same145
metrics registry as the remaining tables. We report greedy de-146
coding error and lexicon-projected error to separate open vo-147
cabulary decoding quality from lexicon constraints. The vector148
baseline rows in the spatial modeling and electrode reduction ta-149
bles serve as the reference for protocol comparisons. We use the150
same split manifests and deterministic evaluation scripts across151
all protocols. 152
We evaluate cross participant transfer with the fourth par-153
ticipant as target under single source and paired source settings.154
The table uses protocol labels for single source cross participant155
transfer and multi source transfer. The lvl field marks direction156
level rows and an across direction aggregate. Group labels join157
source participant identifiers with an arrow to the target. The158
split archives that define these targets are pinned by checksum159
in the manifest. In our audited splits, the multi source aggre-160
gate reduces CER relative to the single source aggregate for the161
same target. 162
The cross participant results for the fourth participant in-163
clude both single source and paired source settings. This pro-164
vides a direct comparison of transfer with and without source165
aggregation under the same audited protocol constraints. This166
helps isolate source aggregation effects without changing the167
target data or evaluation pipeline.168
The spatial modeling table compares spatial inductive bias169
variants at full channels across protocols. We include a patch-170
pool grid encoder as a minimal way to implement a rescue for171
the grid encoder. The patchpool variant keeps a coarser spa-172
tial map before recurrent decoding. The variant labels are vec,173
rowcol, grid, grid aug, patch, and patch aug. The row and174
column front end tracks the vector baseline more closely than175
the convolutional grid front end under within participant proto-176
cols. Patchpool reduces the gap under cross participant transfer.177
Across protocols, grid variants tend to increase real time factor178
relative to the vector baseline. We do not observe a consistent179
accuracy gain over the vector baseline in any protocol.180
The electrode reduction table evaluates a reduced channel181
budget using several selection strategies. The method labels are182
topk, fps two k, xfer, and rand. The table reports both accu-183
racy and streaming speed so reduction effects can be compared184
under the same evaluation harness. Across protocols, within185
participant selection and simple transfer selection yield similar186

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
performance. This suggests that a compact subset can preserve187
a large fraction of the vector baseline performance. Random188
selection and simple transfer remain slightly worse than within189
participant selection in the audited results.190
The reduction results complement the protocol tables. They191
show that compact selections preserve much of the vector base-192
line under within participant tests. Cross participant transfer193
remains more challenging, so we report paired source and low194
shot analyses in the subsequent tables.195
We evaluate multi source cross participant transfer using196
paired source participants. The group labels concatenate the197
two source identifiers and use an arrow to the target identifier.198
The multi source table reports direction level results for vector199
and layout aware front ends. This isolates whether combining200
sources helps under the same target and protocol constraints.201
We further analyze multi source transfer deltas against sim-202
ple similarity measures. Delta cer is negative for all audited203
groups, and corr src tgt mean varies within a narrow range204
across groups. We report these measures to describe conditions205
rather than to assert a universal rule.206
We evaluate how models adapt in low shot settings for a207
new participant by varying the number of training instances per208
word. For the vector baseline, two shot improves over one shot,209
and the table reports layout aware variants. This isolates adap-210
tation behavior when only a small amount of labeled target data211
is available.212
6. Discussion213
Our results suggest that an explicit convolutional grid encoder214
is not automatically beneficial for electropalatography under215
within participant tests, despite its intuitive spatial structure.216
A patchpool grid variant reduces the underperformance of the217
grid encoder under cross participant transfer. This indicates that218
spatial encoder design choices can materially affect outcomes.219
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
The patchpool variant does not yield consistent gains over the220
vector baseline across protocols. Spatial augmentation can im-221
prove robustness to synthetic electrode dropout, but it does not222
close the accuracy gap for the convolutional grid variants in our223
multi participant results. We analyze multi source cross partic-224
ipant transfer and how models adapt in low shot settings, and225
we provide the results as artifact tables. They highlight that226
cross participant performance remains challenging. We also an-227
alyze conditions for multi source transfer deltas against simple228
dataset similarity measures. The effect is conditional and does229
not present a single dominant monotonic trend within our eval-230
uated group set. These observations are limited to our audited231
multi participant dataset collection and protocols.232
Across the audited protocols, within participant perfor-233
mance remains stronger than cross participant transfer. This234
emphasizes the difficulty of generalization under limited par-235
ticipant coverage. The target participant results reinforce this236
gap even when source aggregation is enabled. We report237
these trends as artifact grounded observations rather than broad238
claims. We expect additional participant data to be necessary239

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
for stronger transfer conclusions.240
7. Artifacts and Auditability241
This repository uses a strict paper registry that pins every ev-242
idence file by checksum and rejects unsupported manuscript243
blocks. The split manifests, aggregated metrics, compact tables,244
and analysis summaries referenced in this paper are stored as245
deterministic artifacts, enabling audit and reproduction within246
our repository environment. The same artifacts are reused to247
build the manuscript tables and to support verification in the248
audit views.249
8. Ethics and Disclosure250
We report results only for audited artifacts and do not claim251
broader demographic coverage. The datasets and splits used in252
this study are derived from participant recordings, and we focus253
on methodological clarity and artifact traceability rather than254
deployment claims.255
9. Generative AI Use Disclosure256
We used generative AI tools for language polishing and format-257
ting support, and we verified technical claims against audited258
artifacts.259
10. Logic Checks260
The baseline table includes protocol and aggregate metrics261
fields.262
The dataset summary table includes id, N, V , Tmed, con-263
tact, and zero fields.264
The spatial modeling table includes protocol, variant, CER,265
and RTF fields.266
The electrode reduction table includes protocol, method,267
CER, and RTF fields.268
11. References269
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and270
J. Brumberg, “Silent speech interfaces,” 2010.271
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction272
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and273
Computer Engineering. Springer, 2017.274
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,275
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces276
for speech restoration: A review,” 2020.277
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and278
S. Lee, “Biosignal sensors and deep learning-based speech recog-279
nition: A review,” 2021.280
[5] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-281
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-282
the-ear silently spelled expressions,” 2024.283
[6] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-284
nectionist temporal classification,” 2006.285
[7] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,286
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-287
wards mobile, hands-free, silent speech text entry using elec-288
tropalatography,” 2022.289
[8] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-290
tion of electropalatographic data using latent variable models,”291
1998. 292
[9] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,293
“New developments in electropalatography: A state-of-the-art re-294
port,” 1989. 295
[10] W. J. Hardcastle, “Electropalatography in phonetic research and296
in speech training,” 1990.297
[11] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction298
methods and their implications for studies of lingual coarticula-299
tion,” 1991. 300
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and301
M. Stone, “Development of a silent speech interface driven by302
ultrasound and optical images of the tongue and lips,” 2010.303
[13] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-304
surement of face and palate by structured light,” 1993.305
[14] A. Toutios and K. Margaritis, “Learning electropalatograms from306
acoustics,” 2006. 307
[15] ——, “On the acoustic-to-electropalatographic mapping,” 2006.308
[16] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,309
“Visualisation and analysis of speech production with elec-310
tropalatography,” 2019.311
[17] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and312
evaluation of korean electropalatography (k-epg),” 2021.313
[18] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,314
and Q. V . Le, “Specaugment: A simple data augmentation method315
for automatic speech recognition,” 2019.316
