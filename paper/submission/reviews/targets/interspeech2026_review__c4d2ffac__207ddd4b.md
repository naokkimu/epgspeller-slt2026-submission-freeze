# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 22815,
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
    "sha256": "c4d2ffaccb252fcb5a5d8f8f7dc1de9278ccc1a66aeaf677225e2192adb89149",
    "sha8": "c4d2ffac",
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
    "sha256": "207ddd4b531e9e86b302c3aea2e45db39970292aa1c23a80a00ffbe92bbb2c01",
    "sha8": "207ddd4b"
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
          "disclosure": 21279,
          "printbibliography": null,
          "references_heading": 21505,
          "refs": 21446,
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
      "extracted_chars": 22815,
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
      "sha256": "c4d2ffaccb252fcb5a5d8f8f7dc1de9278ccc1a66aeaf677225e2192adb89149",
      "sha8": "c4d2ffac",
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
      "sha256": "207ddd4b531e9e86b302c3aea2e45db39970292aa1c23a80a00ffbe92bbb2c01",
      "sha8": "207ddd4b"
    }
  },
  "run_id": "INTSP2026_STATIC_c4d2ffac_207ddd4b"
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
Silent speech interfaces infer linguistic intent from non acous-20
tic signals, spanning articulatory sensing and other biosignals,21
and surveys emphasize variability, limited data, and evaluation22
protocol mismatches across systems. Electropalatography pro-23
vides a practical binary representation of tongue palate contact,24
but its discrete sensor layout and device specific geometry raise25
questions about inductive bias and cross participant generaliza-26
tion. [1, 2, 3, 4, 5, 6, 7, 8]27
We focus on silent spelling, an SSI interaction that decodes28
character strings rather than continuous speech recognition or29
reconstruction. Character level decoding with CTC supports30
lexicon scale spelling and evaluation on unseen words, while31
other SSI pipelines rely on constrained recognition or recon-32
struction formulations. Within our surveyed set, SilentSpeller33
and ReHEarSSE are the closest anchors for lexicon scale silent34
spelling. [1, 9, 10, 11, 12, 13]35
EPG contact patterns are spatially structured, and prior EPG36
studies examine dimensionality reduction and structured rep-37
resentations, motivating explicit evaluation of representation38
choices in learned decoders. We test layout aware front ends39
under protocols that distinguish generalization to held-out word40
identities, held-out instances of seen words, and cross partic-41
ipant transfer. We present an evidence tracked study of EPG42
silent spelling, define deterministic split protocols, compare a43
vector baseline to two layout aware front ends, and analyze elec-44
trode reduction and low shot adaptation under the same audit45
rules. [14, 15, 16, 17, 18]46
• We define protocols to evaluate word identity generalization47
and participant transfer, and we provide split archives with48
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
checksums. 49
• We run multi-participant experiments with character-level50
decoding and lexicon projection, tracked by a strict evidence51
registry. 52
• We compare a vector baseline with two layout aware front53
ends, and we report both accuracy and streaming speed met-54
rics. 55
• We provide deterministic scripts that export compact tables56
and manifests used by this manuscript.57
2. Data and Protocols58
We use four participant electropalatography datasets with word59
labels. Each sample is a variable length binary contact matrix,60
and the raw exports are treated as immutable evidence. We re-61
fer to participants with anonymous labels in all tables and split62
archives. We audit dataset statistics, label counts, and anoma-63
lies before we construct any train and test splits. We exclude a64
small set of all-zero samples via a pinned index list.65
The audit pipeline records raw file checksums. It vali-66
dates schema consistency. It summarizes label counts, sequence67
length summaries, and per channel activity statistics before any68
split construction. The raw exports remain unchanged. We ap-69
ply any exclusions only through pinned index lists that are in-70
cluded in the audit artifacts.71
The dataset summary table reports id, sample count, vo-72
cabulary size, median sequence length, mean contact rate, and73
the count of all-zero samples for each participant dataset. The74
id labels are anonymous participant codes used throughout the75
protocol manifests. 76
We evaluate three primary protocols. The word holdout77
protocol uses disjoint vocabularies across train, test, and a com-78
petition partition. The instance holdout protocol tests held out79
instances of seen words. It separates train and competition vo-80
cabularies while keeping the test vocabulary within their union.81
The cross participant protocol trains on a source participant82
and tests on a target participant under a shared vocabulary con-83

=== PAGE 2 ===
straint. We also define a paired source cross participant vari-84
ant and a low shot adaptation variant to isolate source aggrega-85
tion and limited supervision effects under the same audit rules.86
When a target participant has limited within word repetition,87
we configure the cross participant split generators to allow sin-88
gle instance target words. We keep the source side constraints89
unchanged. All split archives used in this study are enumerated90
with sizes and checksums in manifest artifacts.91
All split archives are generated deterministically from au-92
dited exports with fixed seeds. Each train, test, and competition93
partition is stored as an immutable archive with a checksum in94
the manifests to enable reuse and later verification. The man-95
ifests show the word-holdout protocol uses all four participant96
datasets. They show the instance-holdout protocol uses three97
participant datasets. They also show the fourth participant ap-98
pears only as a target in the cross-participant splits. This separa-99
tion explains why the dataset summary includes all participant100
datasets even when a protocol uses only a subset.101
We normalize labels by uppercasing and filtering to alpha-102
bet characters, then represent each label as a space separated103
character sequence for CTC training and greedy decoding. We104
apply this step consistently during split construction and dataset105
preparation to avoid vocabulary drift.106
We keep the label normalization step consistent across all107
splits and dataset preparation steps. This aligns the decoder108
vocabulary with the audited labels and reduces drift between109
training and artifacts used to evaluate.110
We report character error rate from greedy decoding and111
streaming speed using real time factor. We define real time fac-112
tor as total inference time divided by total input duration. For113
character-level decoding we also report lexicon projection error114
rates using a training lexicon and a full lexicon.115
Greedy decoding reports unconstrained character se-116
quences. Lexicon projection maps outputs to finite word sets117
derived from the training vocabulary or the full audited lexicon.118
This allows us to separate decoding quality from lexicon con-119
straints. We compute real time factor by dividing inference time120
by input duration under the same test harness.121
3. Models122
Our baseline model encodes each frame as a vector of palate123
channels and applies a uni-directional recurrent decoder trained124
with a CTC objective. We compare two layout aware front ends.125
One is a row and column pooling front end that aggregates a126
proxy grid into one dimensional summaries. The other is a grid127
front end that reconstructs a proxy grid and applies a convolu-128
tional spatial encoder. For the grid model we optionally enable a129
spatial augmentation that drops and shifts contiguous electrode130
blocks. [11, 19]131
The proxy grid is constructed from the palate channel lay-132
out. It supports row and column pooling or convolutional fea-133
ture extraction. We use a fixed layout file for the mapping so134
that row and column indices are consistent across splits. We135
augment spatially by perturbing contiguous electrode blocks to136
emulate missing contacts and minor spatial shifts.137
We fix core training hyperparameters across runs and record138
how we configure them in the metrics registry for auditability.139
4. Results140
Baseline performance across protocols is derived from the same141
metrics registry as the remaining tables. We report greedy de-142
coding error and lexicon-projected error to separate character-143
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
level decoding quality from lexicon constraints. The vector144
baseline rows in the spatial modeling and electrode reduction ta-145
bles serve as the reference for protocol comparisons. We use the146
same split manifests and deterministic evaluation scripts across147
all protocols. 148
We evaluate cross participant transfer with the fourth par-149
ticipant as target under single source and paired source settings.150
The table uses protocol labels for single source cross participant151
transfer and multi source transfer. The lvl field marks direction152
level rows and an across direction aggregate. Group labels join153
source participant identifiers with an arrow to the target. The154
split archives that define these targets are pinned by checksum155
in the manifest. In our audited splits, the multi source aggre-156
gate reduces CER relative to the single source aggregate for the157
same target. 158
The cross participant results for the fourth participant in-159
clude both single source and paired source settings. This pro-160
vides a direct comparison of transfer with and without source161
aggregation under the same audited protocol constraints. This162
helps isolate source aggregation effects without changing the163
target data or evaluation pipeline.164
The spatial modeling table compares spatial inductive bias165
variants at full channels across protocols. We include a patch-166
pool grid encoder as a minimal way to implement a rescue for167
the grid encoder. The patchpool variant keeps a coarser spa-168
tial map before recurrent decoding. The variant labels are vec,169
rowcol, grid, grid aug, patch, and patch aug. The row and170
column front end tracks the vector baseline more closely than171
the convolutional grid front end under within participant proto-172
cols. Patchpool reduces the gap under cross participant transfer.173
Across protocols, grid variants tend to increase real time factor174
relative to the vector baseline. We do not observe a consistent175
accuracy gain over the vector baseline in any protocol.176
The electrode reduction table evaluates a reduced channel177
budget using several selection strategies. The method labels are178
topk, fps two k, xfer, and rand. The table reports both accu-179
racy and streaming speed so reduction effects can be compared180
under the same evaluation harness. Across protocols, within181
participant selection and simple transfer selection yield similar182
performance. This suggests that a compact subset can preserve183
a large fraction of the vector baseline performance. Random184
selection and simple transfer remain slightly worse than within185
participant selection in the audited results.186
The reduction results complement the protocol tables. They187
show that compact selections preserve much of the vector base-188
line under within participant tests. Cross participant transfer189

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
remains more challenging, so we report paired source and low190
shot analyses in the subsequent tables.191
We evaluate multi source cross participant transfer using192
paired source participants. The group labels concatenate the193
two source identifiers and use an arrow to the target identifier.194
The multi source table reports direction level results for vector195
and layout aware front ends. This isolates whether combining196
sources helps under the same target and protocol constraints.197
We further analyze multi source transfer deltas against sim-198
ple similarity measures. Delta cer is negative for all audited199
groups, and corr src tgt mean varies within a narrow range200
across groups. We report these measures to describe conditions201
rather than to assert a universal rule.202
We evaluate how models adapt in low shot settings for a203
new participant by varying the number of training instances per204
word. For the vector baseline, two shot improves over one shot,205
and the table reports layout aware variants. This isolates adap-206
tation behavior when only a small amount of labeled target data207
is available.208
5. Discussion209
Our results suggest that an explicit convolutional grid encoder210
is not automatically beneficial for electropalatography under211
within participant tests, despite its intuitive spatial structure.212
A patchpool grid variant reduces the underperformance of the213
grid encoder under cross participant transfer. This indicates that214
spatial encoder design choices can materially affect outcomes.215
The patchpool variant does not yield consistent gains over the216
vector baseline across protocols. Spatial augmentation can im-217
prove robustness to synthetic electrode dropout, but it does not218
close the accuracy gap for the convolutional grid variants in our219
multi participant results. We analyze multi source cross partic-220
ipant transfer and how models adapt in low shot settings, and221
we provide the results as artifact tables. They highlight that222
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
cross participant performance remains challenging. We also an-223
alyze conditions for multi source transfer deltas against simple224
dataset similarity measures. The effect is conditional and does225
not present a single dominant monotonic trend within our eval-226
uated group set. These observations are limited to our audited227
multi participant dataset collection and protocols.228
Across the audited protocols, within participant perfor-229
mance remains stronger than cross participant transfer. This230
emphasizes the difficulty of generalization under limited par-231
ticipant coverage. The target participant results reinforce this232
gap even when source aggregation is enabled. We report233
these trends as artifact grounded observations rather than broad234
claims. We expect additional participant data to be necessary235
for stronger transfer conclusions.236
6. Artifacts and Auditability237
This repository uses a strict paper registry that pins every ev-238
idence file by checksum and rejects unsupported manuscript239
blocks. The split manifests, aggregated metrics, compact tables,240
and analysis summaries referenced in this paper are stored as241

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
deterministic artifacts, enabling audit and reproduction within242
our repository environment. The same artifacts are reused to243
build the manuscript tables and to support verification in the244
audit views.245
7. Ethics and Disclosure246
We report results only for audited artifacts and do not claim247
broader demographic coverage. The datasets and splits used in248
this study are derived from participant recordings, and we focus249
on methodological clarity and artifact traceability rather than250
deployment claims.251
8. Generative AI Use Disclosure252
We used generative AI tools for language polishing and format-253
ting support, and we verified technical claims against audited254
artifacts.255
9. References256
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and257
J. Brumberg, “Silent speech interfaces,” 2010.258
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction259
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and260
Computer Engineering. Springer, 2017.261
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,262
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces263
for speech restoration: A review,” 2020.264
[4] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,265
“New developments in electropalatography: A state-of-the-art re-266
port,” 1989.267
[5] W. J. Hardcastle, “Electropalatography in phonetic research and268
in speech training,” 1990.269
[6] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and270
S. Lee, “Biosignal sensors and deep learning-based speech recog-271
nition: A review,” 2021.272
[7] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,273
“Visualisation and analysis of speech production with elec-274
tropalatography,” 2019.275
[8] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and276
evaluation of korean electropalatography (k-epg),” 2021.277
[9] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-278
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-279
the-ear silently spelled expressions,” 2024.280
[10] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fagan, R. Moore,281
and P. Green, “Isolated word recognition of silent speech282
using magnetic implants and sensors,” 2010. [Online]. Available:283
https://pubmed.ncbi.nlm.nih.gov/20863739/284
[11] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-285
nectionist temporal classification,” 2006.286
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and287
M. Stone, “Development of a silent speech interface driven by288
ultrasound and optical images of the tongue and lips,” 2010.289
[13] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,290
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-291
wards mobile, hands-free, silent speech text entry using elec-292
tropalatography,” 2022.293
[14] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-294
tion of electropalatographic data using latent variable models,”295
1998. 296
[15] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction297
methods and their implications for studies of lingual coarticula-298
tion,” 1991. 299
[16] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-300
surement of face and palate by structured light,” 1993.301
[17] A. Toutios and K. Margaritis, “Learning electropalatograms from302
acoustics,” 2006. 303
[18] ——, “On the acoustic-to-electropalatographic mapping,” 2006.304
[19] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,305
and Q. V . Le, “Specaugment: A simple data augmentation method306
for automatic speech recognition,” 2019.307
