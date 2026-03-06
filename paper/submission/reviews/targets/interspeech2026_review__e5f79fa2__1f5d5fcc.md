# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 24494,
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
    "sha256": "e5f79fa2e23868ae95437efae0413c4cd5b976d8b1b8fdc987478ed1c5349832",
    "sha8": "e5f79fa2",
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
    "sha256": "1f5d5fcc575d2c63809432a773a586c56129dcedde989c0462bcb39ec26055c5",
    "sha8": "1f5d5fcc"
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
          "disclosure": 22899,
          "printbibliography": null,
          "references_heading": 23125,
          "refs": 23066,
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
      "extracted_chars": 24494,
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
      "sha256": "e5f79fa2e23868ae95437efae0413c4cd5b976d8b1b8fdc987478ed1c5349832",
      "sha8": "e5f79fa2",
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
      "sha256": "1f5d5fcc575d2c63809432a773a586c56129dcedde989c0462bcb39ec26055c5",
      "sha8": "1f5d5fcc"
    }
  },
  "run_id": "INTSP2026_STATIC_e5f79fa2_1f5d5fcc"
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
2. Related Work61
Silent speech interfaces infer linguistic intent from non acoustic62
signals. Surveys describe a wide range of sensing modalities63
and emphasize variability, limited data, and evaluation protocol64
mismatches, which make system level comparisons sensitive to65
vocabulary and subject conditions. [1, 2, 3, 4]66
Electropalatography measures tongue palate contact with67
an instrumented palate, and foundational instrumentation68
and visualization work define what EPG captures and how69
palatograms are represented. Modern device designs are lay-70
out specific, so electrode geometry is a meaningful design con-71
straint when comparing models. Within SSI, SilentSpeller ex-72
emplifies EPG based silent spelling with letter level decoding73
and unseen word evaluation. EPG is also used as an articula-74
tory modality in multimodal mapping tasks. [9, 7, 10, 8, 11, 12]75
Character level sequence decoding with CTC supports lex-76
icon scale silent spelling and evaluation on unseen words,77
while other SSI pipelines use constrained recognition or re-78
construction formulations. Prior EPG studies investigate di-79
mensionality reduction and structured representations, motivat-80
ing explicit evaluation of representation choices in learned de-81
coders. [5, 1, 6, 13, 14, 15, 16, 8, 17, 18]82
3. Data and Protocols83
We use four participant electropalatography datasets with word84
labels. Each sample is a variable length binary contact matrix,85
and the raw exports are treated as immutable evidence. We re-86
fer to participants with anonymous labels in all tables and split87
archives. We audit dataset statistics, label counts, and anoma-88
lies before we construct any train and test splits. We exclude a89
small set of all-zero samples via a pinned index list.90
The audit pipeline records raw file checksums. It vali-91
dates schema consistency. It summarizes label counts, sequence92
length summaries, and per channel activity statistics before any93

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
split construction. The raw exports remain unchanged. We ap-94
ply any exclusions only through pinned index lists that are in-95
cluded in the audit artifacts.96
The dataset summary table reports id, sample count, vo-97
cabulary size, median sequence length, mean contact rate, and98
the count of all-zero samples for each participant dataset. The99
id labels are anonymous participant codes used throughout the100
protocol manifests.101
We evaluate three primary protocols. The word holdout102
protocol uses disjoint vocabularies across train, test, and a com-103
petition partition. The instance holdout protocol tests held out104
instances of seen words. It separates train and competition vo-105
cabularies while keeping the test vocabulary within their union.106
The cross participant protocol trains on a source participant107
and tests on a target participant under a shared vocabulary con-108
straint. We also define a paired source cross participant vari-109
ant and a low shot adaptation variant to isolate source aggrega-110
tion and limited supervision effects under the same audit rules.111
When a target participant has limited within word repetition,112
we configure the cross participant split generators to allow sin-113
gle instance target words. We keep the source side constraints114
unchanged. All split archives used in this study are enumerated115
with sizes and checksums in manifest artifacts.116
All split archives are generated deterministically from au-117
dited exports with fixed seeds. Each train, test, and competition118
partition is stored as an immutable archive with a checksum in119
the manifests to enable reuse and later verification. The man-120
ifests show the word-holdout protocol uses all four participant121
datasets. They show the instance-holdout protocol uses three122
participant datasets. They also show the fourth participant ap-123
pears only as a target in the cross-participant splits. This separa-124
tion explains why the dataset summary includes all participant125
datasets even when a protocol uses only a subset.126
We normalize labels by uppercasing and filtering to alpha-127
bet characters, then represent each label as a space separated128
character sequence for CTC training and greedy decoding. We129
apply this step consistently during split construction and dataset130
preparation to avoid vocabulary drift.131
We keep the label normalization step consistent across all132
splits and dataset preparation steps. This aligns the decoder133
vocabulary with the audited labels and reduces drift between134
training and artifacts used to evaluate.135
We report character error rate from greedy decoding and136
streaming speed using real time factor. We define real time fac-137
tor as total inference time divided by total input duration. For138
character-level decoding we also report lexicon projection error139
rates using a training lexicon and a full lexicon.140
Greedy decoding reports unconstrained character se-141
quences. Lexicon projection maps outputs to finite word sets142
derived from the training vocabulary or the full audited lexicon.143
This allows us to separate decoding quality from lexicon con-144
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
straints. We compute real time factor by dividing inference time145
by input duration under the same test harness.146
4. Models147
Our baseline model encodes each frame as a vector of palate148
channels and applies a uni-directional recurrent decoder trained149
with a CTC objective. We compare two layout aware front ends.150
One is a row and column pooling front end that aggregates a151
proxy grid into one dimensional summaries. The other is a grid152
front end that reconstructs a proxy grid and applies a convolu-153
tional spatial encoder. For the grid model we optionally enable a154
spatial augmentation that drops and shifts contiguous electrode155
blocks. [14, 19] 156
The proxy grid is constructed from the palate channel lay-157
out. It supports row and column pooling or convolutional fea-158
ture extraction. We use a fixed layout file for the mapping so159
that row and column indices are consistent across splits. We160
augment spatially by perturbing contiguous electrode blocks to161
emulate missing contacts and minor spatial shifts.162
We fix core training hyperparameters across runs and record163
how we configure them in the metrics registry for auditability.164
5. Results165
Baseline performance across protocols is derived from the same166
metrics registry as the remaining tables. We report greedy de-167
coding error and lexicon-projected error to separate character-168
level decoding quality from lexicon constraints. The vector169
baseline rows in the spatial modeling and electrode reduction ta-170
bles serve as the reference for protocol comparisons. We use the171
same split manifests and deterministic evaluation scripts across172
all protocols. 173
We evaluate cross participant transfer with the fourth par-174
ticipant as target under single source and paired source settings.175
The table uses protocol labels for single source cross participant176
transfer and multi source transfer. The lvl field marks direction177
level rows and an across direction aggregate. Group labels join178
source participant identifiers with an arrow to the target. The179
split archives that define these targets are pinned by checksum180
in the manifest. In our audited splits, the multi source aggre-181
gate reduces CER relative to the single source aggregate for the182
same target. 183
The cross participant results for the fourth participant in-184
clude both single source and paired source settings. This pro-185
vides a direct comparison of transfer with and without source186

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
aggregation under the same audited protocol constraints. This187
helps isolate source aggregation effects without changing the188
target data or evaluation pipeline.189
The spatial modeling table compares spatial inductive bias190
variants at full channels across protocols. We include a patch-191
pool grid encoder as a minimal way to implement a rescue for192
the grid encoder. The patchpool variant keeps a coarser spa-193
tial map before recurrent decoding. The variant labels are vec,194
rowcol, grid, grid aug, patch, and patch aug. The row and195
column front end tracks the vector baseline more closely than196
the convolutional grid front end under within participant proto-197
cols. Patchpool reduces the gap under cross participant transfer.198
Across protocols, grid variants tend to increase real time factor199
relative to the vector baseline. We do not observe a consistent200
accuracy gain over the vector baseline in any protocol.201
The electrode reduction table evaluates a reduced channel202
budget using several selection strategies. The method labels are203
topk, fps two k, xfer, and rand. The table reports both accu-204
racy and streaming speed so reduction effects can be compared205
under the same evaluation harness. Across protocols, within206
participant selection and simple transfer selection yield similar207
performance. This suggests that a compact subset can preserve208
a large fraction of the vector baseline performance. Random209
selection and simple transfer remain slightly worse than within210
participant selection in the audited results.211
The reduction results complement the protocol tables. They212
show that compact selections preserve much of the vector base-213
line under within participant tests. Cross participant transfer214
remains more challenging, so we report paired source and low215
shot analyses in the subsequent tables.216
We evaluate multi source cross participant transfer using217
paired source participants. The group labels concatenate the218
two source identifiers and use an arrow to the target identifier.219
The multi source table reports direction level results for vector220
and layout aware front ends. This isolates whether combining221
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
sources helps under the same target and protocol constraints.222
We further analyze multi source transfer deltas against sim-223
ple similarity measures. Delta cer is negative for all audited224
groups, and corr src tgt mean varies within a narrow range225
across groups. We report these measures to describe conditions226
rather than to assert a universal rule.227
We evaluate how models adapt in low shot settings for a228
new participant by varying the number of training instances per229
word. For the vector baseline, two shot improves over one shot,230
and the table reports layout aware variants. This isolates adap-231
tation behavior when only a small amount of labeled target data232
is available. 233
6. Discussion234
Our results suggest that an explicit convolutional grid encoder235
is not automatically beneficial for electropalatography under236
within participant tests, despite its intuitive spatial structure.237
A patchpool grid variant reduces the underperformance of the238
grid encoder under cross participant transfer. This indicates that239
spatial encoder design choices can materially affect outcomes.240

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
The patchpool variant does not yield consistent gains over the241
vector baseline across protocols. Spatial augmentation can im-242
prove robustness to synthetic electrode dropout, but it does not243
close the accuracy gap for the convolutional grid variants in our244
multi participant results. We analyze multi source cross partic-245
ipant transfer and how models adapt in low shot settings, and246
we provide the results as artifact tables. They highlight that247
cross participant performance remains challenging. We also an-248
alyze conditions for multi source transfer deltas against simple249
dataset similarity measures. The effect is conditional and does250
not present a single dominant monotonic trend within our eval-251
uated group set. These observations are limited to our audited252
multi participant dataset collection and protocols.253
Across the audited protocols, within participant perfor-254
mance remains stronger than cross participant transfer. This255
emphasizes the difficulty of generalization under limited par-256
ticipant coverage. The target participant results reinforce this257
gap even when source aggregation is enabled. We report258
these trends as artifact grounded observations rather than broad259
claims. We expect additional participant data to be necessary260
for stronger transfer conclusions.261
7. Artifacts and Auditability262
This repository uses a strict paper registry that pins every ev-263
idence file by checksum and rejects unsupported manuscript264
blocks. The split manifests, aggregated metrics, compact tables,265
and analysis summaries referenced in this paper are stored as266
deterministic artifacts, enabling audit and reproduction within267
our repository environment. The same artifacts are reused to268
build the manuscript tables and to support verification in the269
audit views.270
8. Ethics and Disclosure271
We report results only for audited artifacts and do not claim272
broader demographic coverage. The datasets and splits used in273
this study are derived from participant recordings, and we focus274
on methodological clarity and artifact traceability rather than275
deployment claims.276
9. Generative AI Use Disclosure277
We used generative AI tools for language polishing and format-278
ting support, and we verified technical claims against audited279
artifacts.280
10. References281
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and282
J. Brumberg, “Silent speech interfaces,” 2010.283
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction284
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and285
Computer Engineering. Springer, 2017.286
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,287
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces288
for speech restoration: A review,” 2020.289
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and290
S. Lee, “Biosignal sensors and deep learning-based speech recog-291
nition: A review,” 2021.292
[5] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-293
tion of electropalatographic data using latent variable models,”294
1998. 295
[6] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-296
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-297
the-ear silently spelled expressions,” 2024.298
[7] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,299
“New developments in electropalatography: A state-of-the-art re-300
port,” 1989. 301
[8] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,302
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-303
wards mobile, hands-free, silent speech text entry using elec-304
tropalatography,” 2022.305
[9] L.-C. Chen, P.-H. Chen, R. T.-H. Tsai, and Y . Tsao, “arxiv:306
Epg2s: Speech generation and speech enhancement based307
on electropalatography and audio signals using multimodal308
learning,” 2022. [Online]. Available: https://arxiv.org/abs/2206.309
07860 310
[10] W. J. Hardcastle, “Electropalatography in phonetic research and311
in speech training,” 1990.312
[11] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,313
“Visualisation and analysis of speech production with elec-314
tropalatography,” 2019.315
[12] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and316
evaluation of korean electropalatography (k-epg),” 2021.317
[13] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fagan, R. Moore,318
and P. Green, “Isolated word recognition of silent speech319
using magnetic implants and sensors,” 2010. [Online]. Available:320
https://pubmed.ncbi.nlm.nih.gov/20863739/321
[14] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-322
nectionist temporal classification,” 2006.323
[15] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction324
methods and their implications for studies of lingual coarticula-325
tion,” 1991. 326
[16] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and327
M. Stone, “Development of a silent speech interface driven by328
ultrasound and optical images of the tongue and lips,” 2010.329
[17] A. Toutios and K. Margaritis, “Learning electropalatograms from330
acoustics,” 2006. 331
[18] ——, “On the acoustic-to-electropalatographic mapping,” 2006.332
[19] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,333
and Q. V . Le, “Specaugment: A simple data augmentation method334
for automatic speech recognition,” 2019.335
