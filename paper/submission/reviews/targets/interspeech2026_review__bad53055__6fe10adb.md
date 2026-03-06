# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 21718,
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
    "sha256": "bad530559e87393487684fcb1c3b23c351798a168b518d632ff5f966ceea1183",
    "sha8": "bad53055",
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
    "path": "interspeech2026_review.tex",
    "sha256": "6fe10adb72197c0a3d8d6f15a122fda21f0728bd78e5719a4ab1a345beb96a37",
    "sha8": "6fe10adb"
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
          "disclosure": 21289,
          "printbibliography": null,
          "references_heading": 21515,
          "refs": 21456,
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
      "extracted_chars": 21718,
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
      "sha256": "bad530559e87393487684fcb1c3b23c351798a168b518d632ff5f966ceea1183",
      "sha8": "bad53055",
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
      "path": "interspeech2026_review.tex",
      "sha256": "6fe10adb72197c0a3d8d6f15a122fda21f0728bd78e5719a4ab1a345beb96a37",
      "sha8": "6fe10adb"
    }
  },
  "run_id": "INTSP2026_STATIC_bad53055_6fe10adb"
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
system decodes character strings rather than attempting contin-28
uous speech recognition or reconstruction. This framing helps29
separate within word variation from word identity generaliza-30
tion and makes evaluation protocol choices central, because a31
system can appear to scale by expanding a fixed lexicon or by32
generalizing to held-out word identities with character-level de-33
coding. [1, 2, 3, 4]34
Within our surveyed set, SilentSpeller and ReHEarSSE rep-35
resent silent spelling systems that move beyond small com-36
mand vocabularies and evaluate unseen words under lexicon37
constraints. Broader silent speech systems span constrained38
recognition and reconstruction settings. In the electropalatog-39
raphy literature, contact patterns are treated as spatially struc-40
tured by the palate layout, motivating layout aware representa-41
tions. [5, 1, 6, 7, 8]42
Motivated by this, we test layout aware front ends under43
protocols that distinguish generalization to held-out word iden-44
tities, held-out instances of seen words, and cross participant45
transfer. We present an evidence tracked study of EPG silent46
spelling, define deterministic split protocols, compare a vector47
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
baseline to two layout aware front ends, and analyze electrode48
reduction and low shot adaptation under the same audit rules.49
• We define protocols to evaluate word identity generalization50
and participant transfer, and we provide split archives with51
checksums. 52
• We run multi-participant experiments with character-level53
decoding and lexicon projection, tracked by a strict evidence54
registry. 55
• We compare a vector baseline with two layout aware front56
ends, and we report both accuracy and streaming speed met-57
rics. 58
• We provide deterministic scripts that export compact tables59
and manifests used by this manuscript.60
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
The dataset summary table reports id, sample count, vo-75
cabulary size, median sequence length, mean contact rate, and76
the count of all-zero samples for each participant dataset. The77
id labels are anonymous participant codes used throughout the78
protocol manifests. 79
We evaluate three primary protocols. The word holdout80
protocol uses disjoint vocabularies across train, test, and a com-81

=== PAGE 2 ===
petition partition. The instance holdout protocol tests held out82
instances of seen words. It separates train and competition vo-83
cabularies while keeping the test vocabulary within their union.84
The cross participant protocol trains on a source participant85
and tests on a target participant under a shared vocabulary con-86
straint. We also define a paired source cross participant vari-87
ant and a low shot adaptation variant to isolate source aggrega-88
tion and limited supervision effects under the same audit rules.89
When a target participant has limited within word repetition,90
we configure the cross participant split generators to allow sin-91
gle instance target words. We keep the source side constraints92
unchanged. All split archives used in this study are enumerated93
with sizes and checksums in manifest artifacts.94
All split archives are generated deterministically from au-95
dited exports with fixed seeds. Each train, test, and competition96
partition is stored as an immutable archive with a checksum in97
the manifests to enable reuse and later verification. The man-98
ifests show the word-holdout protocol uses all four participant99
datasets. They show the instance-holdout protocol uses three100
participant datasets. They also show the fourth participant ap-101
pears only as a target in the cross-participant splits. This separa-102
tion explains why the dataset summary includes all participant103
datasets even when a protocol uses only a subset.104
We normalize labels by uppercasing and filtering to alpha-105
bet characters, then represent each label as a space separated106
character sequence for CTC training and greedy decoding. We107
apply this step consistently during split construction and dataset108
preparation to avoid vocabulary drift.109
We keep the label normalization step consistent across all110
splits and dataset preparation steps. This aligns the decoder111
vocabulary with the audited labels and reduces drift between112
training and artifacts used to evaluate.113
We report character error rate from greedy decoding and114
streaming speed using real time factor. We define real time fac-115
tor as total inference time divided by total input duration. For116
character-level decoding we also report lexicon projection error117
rates using a training lexicon and a full lexicon.118
Greedy decoding reports unconstrained character se-119
quences. Lexicon projection maps outputs to finite word sets120
derived from the training vocabulary or the full audited lexicon.121
This allows us to separate decoding quality from lexicon con-122
straints. We compute real time factor by dividing inference time123
by input duration under the same test harness.124
3. Models125
Our baseline model encodes each frame as a vector of palate126
channels and applies a uni-directional recurrent decoder trained127
with a CTC objective. We compare two layout aware front ends.128
One is a row and column pooling front end that aggregates a129
proxy grid into one dimensional summaries. The other is a grid130
front end that reconstructs a proxy grid and applies a convolu-131
tional spatial encoder. For the grid model we optionally enable a132
spatial augmentation that drops and shifts contiguous electrode133
blocks. [9, 10]134
The proxy grid is constructed from the palate channel lay-135
out. It supports row and column pooling or convolutional fea-136
ture extraction. We use a fixed layout file for the mapping so137
that row and column indices are consistent across splits. We138
augment spatially by perturbing contiguous electrode blocks to139
emulate missing contacts and minor spatial shifts.140
We fix core training hyperparameters across runs and record141
how we configure them in the metrics registry for auditability.142
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
4. Results143
Baseline performance across protocols is derived from the same144
metrics registry as the remaining tables. We report greedy de-145
coding error and lexicon-projected error to separate character-146
level decoding quality from lexicon constraints. The vector147
baseline rows in the spatial modeling and electrode reduction ta-148
bles serve as the reference for protocol comparisons. We use the149
same split manifests and deterministic evaluation scripts across150
all protocols. 151
We evaluate cross participant transfer with the fourth par-152
ticipant as target under single source and paired source settings.153
The table uses protocol labels for single source cross participant154
transfer and multi source transfer. The lvl field marks direction155
level rows and an across direction aggregate. Group labels join156
source participant identifiers with an arrow to the target. The157
split archives that define these targets are pinned by checksum158
in the manifest. In our audited splits, the multi source aggre-159
gate reduces CER relative to the single source aggregate for the160
same target. 161
The cross participant results for the fourth participant in-162
clude both single source and paired source settings. This pro-163
vides a direct comparison of transfer with and without source164
aggregation under the same audited protocol constraints. This165
helps isolate source aggregation effects without changing the166
target data or evaluation pipeline.167
The spatial modeling table compares spatial inductive bias168
variants at full channels across protocols. We include a patch-169
pool grid encoder as a minimal way to implement a rescue for170
the grid encoder. The patchpool variant keeps a coarser spa-171
tial map before recurrent decoding. The variant labels are vec,172
rowcol, grid, grid aug, patch, and patch aug. The row and173
column front end tracks the vector baseline more closely than174
the convolutional grid front end under within participant proto-175
cols. Patchpool reduces the gap under cross participant transfer.176
Across protocols, grid variants tend to increase real time factor177
relative to the vector baseline. We do not observe a consistent178
accuracy gain over the vector baseline in any protocol.179
The electrode reduction table evaluates a reduced channel180
budget using several selection strategies. The method labels are181
topk, fps two k, xfer, and rand. The table reports both accu-182
racy and streaming speed so reduction effects can be compared183
under the same evaluation harness. Across protocols, within184
participant selection and simple transfer selection yield similar185
performance. This suggests that a compact subset can preserve186
a large fraction of the vector baseline performance. Random187

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
selection and simple transfer remain slightly worse than within188
participant selection in the audited results.189
The reduction results complement the protocol tables. They190
show that compact selections preserve much of the vector base-191
line under within participant tests. Cross participant transfer192
remains more challenging, so we report paired source and low193
shot analyses in the subsequent tables.194
We evaluate multi source cross participant transfer using195
paired source participants. The group labels concatenate the196
two source identifiers and use an arrow to the target identifier.197
The multi source table reports direction level results for vector198
and layout aware front ends. This isolates whether combining199
sources helps under the same target and protocol constraints.200
We further analyze multi source transfer deltas against sim-201
ple similarity measures. Delta cer is negative for all audited202
groups, and corr src tgt mean varies within a narrow range203
across groups. We report these measures to describe conditions204
rather than to assert a universal rule.205
We evaluate how models adapt in low shot settings for a206
new participant by varying the number of training instances per207
word. For the vector baseline, two shot improves over one shot,208
and the table reports layout aware variants. This isolates adap-209
tation behavior when only a small amount of labeled target data210
is available.211
5. Discussion212
Our results suggest that an explicit convolutional grid encoder213
is not automatically beneficial for electropalatography under214
within participant tests, despite its intuitive spatial structure.215
A patchpool grid variant reduces the underperformance of the216
grid encoder under cross participant transfer. This indicates that217
spatial encoder design choices can materially affect outcomes.218
The patchpool variant does not yield consistent gains over the219
vector baseline across protocols. Spatial augmentation can im-220
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
prove robustness to synthetic electrode dropout, but it does not221
close the accuracy gap for the convolutional grid variants in our222
multi participant results. We analyze multi source cross partic-223
ipant transfer and how models adapt in low shot settings, and224
we provide the results as artifact tables. They highlight that225
cross participant performance remains challenging. We also an-226
alyze conditions for multi source transfer deltas against simple227
dataset similarity measures. The effect is conditional and does228
not present a single dominant monotonic trend within our eval-229
uated group set. These observations are limited to our audited230
multi participant dataset collection and protocols.231
Across the audited protocols, within participant perfor-232
mance remains stronger than cross participant transfer. This233
emphasizes the difficulty of generalization under limited par-234
ticipant coverage. The target participant results reinforce this235
gap even when source aggregation is enabled. We report236
these trends as artifact grounded observations rather than broad237
claims. We expect additional participant data to be necessary238
for stronger transfer conclusions.239

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
6. Artifacts and Auditability240
This repository uses a strict paper registry that pins every ev-241
idence file by checksum and rejects unsupported manuscript242
blocks. The split manifests, aggregated metrics, compact tables,243
and analysis summaries referenced in this paper are stored as244
deterministic artifacts, enabling audit and reproduction within245
our repository environment. The same artifacts are reused to246
build the manuscript tables and to support verification in the247
audit views.248
7. Ethics and Disclosure249
We report results only for audited artifacts and do not claim250
broader demographic coverage. The datasets and splits used in251
this study are derived from participant recordings, and we focus252
on methodological clarity and artifact traceability rather than253
deployment claims.254
8. Generative AI Use Disclosure255
We used generative AI tools for language polishing and format-256
ting support, and we verified technical claims against audited257
artifacts.258
9. References259
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and260
J. Brumberg, “Silent speech interfaces,” 2010.261
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction262
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and263
Computer Engineering. Springer, 2017.264
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,265
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces266
for speech restoration: A review,” 2020.267
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and268
S. Lee, “Biosignal sensors and deep learning-based speech recog-269
nition: A review,” 2021.270
[5] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-271
tion of electropalatographic data using latent variable models,”272
1998.273
[6] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-274
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-275
the-ear silently spelled expressions,” 2024.276
[7] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,277
“New developments in electropalatography: A state-of-the-art re-278
port,” 1989.279
[8] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,280
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-281
wards mobile, hands-free, silent speech text entry using elec-282
tropalatography,” 2022.283
[9] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-284
nectionist temporal classification,” 2006.285
[10] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,286
and Q. V . Le, “Specaugment: A simple data augmentation method287
for automatic speech recognition,” 2019.288
