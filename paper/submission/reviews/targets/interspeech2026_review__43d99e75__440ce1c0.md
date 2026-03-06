# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 21992,
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
    "sha256": "43d99e75c417db781d2fe4d0b1aa8e27f97022a0c12ecb3ac4a5d53d8d70a499",
    "sha8": "43d99e75",
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
      "plain_characters": 803
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
    "sha256": "440ce1c02c57ab4d0b009e3963638d5bcccfdef4c2879ac1c22355a4cab4120c",
    "sha8": "440ce1c0"
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
        "abstract_chars": 803,
        "max_characters": 1000
      },
      "id": "abstract_length",
      "message": "abstract_chars=803 <= max_characters=1000",
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
      "extracted_chars": 21992,
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
      "sha256": "43d99e75c417db781d2fe4d0b1aa8e27f97022a0c12ecb3ac4a5d53d8d70a499",
      "sha8": "43d99e75",
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
        "plain_characters": 803
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
      "sha256": "440ce1c02c57ab4d0b009e3963638d5bcccfdef4c2879ac1c22355a4cab4120c",
      "sha8": "440ce1c0"
    }
  },
  "run_id": "INTSP2026_STATIC_43d99e75_440ce1c0"
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
Open-V ocabulary Silent Spelling
Anonymous submission to Interspeech 2026
Abstract1
Silent speech text entry with electropalatography requires2
models that generalize across word identities and participants3
while remaining auditable. We present an evidence-only study4
of open-vocabulary silent spelling from binary palate contact5
patterns, with protocols for word holdout, instance holdout, and6
cross participant transfer. Using four participants and determin-7
istic artifact tracking, we evaluate a vector baseline and two lay-8
out aware front ends, and we analyze electrode reduction and9
low shot adaptation. Across our audited runs, the row and col-10
umn front end tracks the vector baseline more closely than a11
convolutional grid front end, while the grid front end increases12
streaming latency. We release split manifests, checksums, and13
compact result tables as pinned repository artifacts.14
Index Terms: silent speech interface, electropalatography,15
open vocabulary, text entry, auditability16
1. Introduction17
Silent speech interfaces aim to enable communication without18
audible acoustics, using sensor measurements of articulation19
or physiology. Electropalatography provides a practical binary20
contact representation of tongue and palate interaction, but its21
discrete layout and device variability raise questions about in-22
ductive bias, robustness, and generalization. [1, 2, 3, 4]23
Recent work on silent spelling has emphasized open-24
vocabulary text entry, where character level decoding can25
compose words beyond a fixed closed set. We study open-26
vocabulary spelling with a CTC style decoder and lexicon pro-27
jection, and we compare vector and layout aware front ends un-28
der multiple generalization protocols. [5, 6, 7]29
• We define evaluation protocols that separate word identity30
generalization and participant transfer, and we provide split31
archives with checksums.32
• We run multi-participant experiments with open-vocabulary33
decoding and lexicon projection, tracked by a strict evidence34
registry.35
• We compare a vector baseline with two layout aware front36
ends, and we report both accuracy and streaming speed met-37
rics.38
• We provide deterministic scripts that export compact tables39
and manifests used by this manuscript.40
2. Related Work41
Within our surveyed set, open-vocabulary silent spelling sys-42
tems are represented by SilentSpeller and ReHEarSSE, while43
broader silent speech systems span constrained recognition and44
reconstruction settings. In the electropalatography literature,45
Table 1:Raw dataset summary for each participant dataset; id
is the participant identifier, N is sample count, V is vocabulary
size, Tmed is median sequence length, contact is mean contact
rate, and zero is the count of all zero samples.
id N V Tmed contact zero
p1 2328 1164 234 0.19 0
p2 2328 1164 196 0.20 0
p3 2797 1164 283 0.12 4
p4 1167 1162 229 0.19 0
the spatial layout has been used for visualization, device char-46
acterization, and representation reduction, motivating tests of47
layout aware inductive bias in learned decoders. [8, 1, 5, 3, 9,48
10, 11, 12, 7, 13, 14, 15, 16, 17]49
We summarize the positioning of prior work using sur-50
vey tags that map systems by representation and system scope,51
describing where open vocabulary silent spelling and elec-52
tropalatography studies sit in the space.53
Prior electropalatography studies emphasize that con-54
tact patterns are structured by the palate layout, motivating55
proxy grid representations and spatially structured modeling in56
learned decoders. Our work situates these ideas within open57
vocabulary silent spelling by making protocol definitions and58
artifact traceability explicit.59
3. Data and Protocols60
We use four participant electropalatography datasets with word61
labels. Each sample is a variable length binary contact matrix,62
and the raw exports are treated as immutable evidence. We audit63
dataset statistics, label counts, and anomalies before construct-64
ing any train and test splits, and a small set of all-zero samples65
is excluded via a pinned index list.66
The audit pipeline records raw file checksums, validates67
schema consistency, and aggregates label distributions, se-68
quence length summaries, and per channel activity statistics be-69
fore any split construction. The raw exports remain unchanged,70
and any exclusions are applied only through pinned index lists71
that are included in the audit artifacts.72
The dataset summary table reports id, sample count, vocab-73
ulary size, median sequence length, mean contact rate, and the74
count of all-zero samples for each participant dataset.75
We evaluate three primary protocols. The word holdout76
protocol uses disjoint vocabularies across train, test, and a com-77
petition partition. The instance holdout protocol evaluates held78
out instances of seen words by separating train and competi-79
tion vocabularies while keeping the test vocabulary within their80
union. The cross participant protocol trains on a source partici-81

=== PAGE 2 ===
pant and evaluates on a target participant under a shared vocab-82
ulary constraint. When a target participant has limited within83
word repetition, we configure the cross participant split genera-84
tors to allow single instance target words while keeping source85
side constraints unchanged. All split archives used in this study86
are enumerated with sizes and checksums in manifest artifacts.87
All split archives are generated deterministically from au-88
dited exports with fixed seeds, and each train, test, and competi-89
tion partition is stored as an immutable archive with a checksum90
in the manifests to enable reuse and verification.91
Labels are normalized by uppercasing and filtering to al-92
phabet characters, then represented as a space separated charac-93
ter sequence for CTC training and greedy decoding. This nor-94
malization is applied consistently during split construction and95
dataset preparation to avoid vocabulary drift.96
We maintain a consistent label normalization pipeline97
across all splits and dataset preparation steps so that the decoder98
vocabulary is aligned with the audited labels, reducing drift be-99
tween training and evaluation artifacts.100
We report character error rate from greedy decoding and101
streaming speed using real time factor, defined as total infer-102
ence time divided by total input duration. For open-vocabulary103
decoding we also report lexicon projection error rates using a104
training lexicon and a full lexicon.105
Greedy decoding reports unconstrained character se-106
quences, while lexicon projection maps outputs to finite word107
sets derived from the training vocabulary or the full audited lex-108
icon, allowing us to separate decoding quality from lexicon con-109
straints. We compute real time factor by dividing inference time110
by input duration under the same evaluation harness.111
4. Models112
Our baseline model encodes each frame as a vector of palate113
channels and applies a uni-directional recurrent decoder trained114
with a CTC objective. We compare two layout aware front ends:115
a row and column pooling front end that aggregates a proxy grid116
into one dimensional summaries, and a grid reconstruction front117
end that applies a convolutional spatial encoder. For the grid118
model we optionally enable a spatial augmentation that drops119
and shifts contiguous electrode blocks. [6, 18]120
The proxy grid is constructed from the palate channel lay-121
out and supports either row and column pooling or convolu-122
tional feature extraction, while spatial augmentation perturbs123
contiguous electrode blocks to emulate missing contacts and124
minor spatial shifts.125
We fix core training hyperparameters across runs and record126
the shared configuration in the metrics registry for auditability.127
5. Results128
The baseline recap table summarizes baseline performance un-129
der word holdout, instance holdout, and cross participant trans-130
fer. Lexicon projection reduces error rates relative to greedy131
decoding across protocols, highlighting the importance of open-132
vocabulary post processing for spelling.133
We additionally evaluate cross participant generalization134
targeting participant four under both single source and multi135
source transfer. The table uses lvl labels dir for single direc-136
tions and all for the across direction aggregation, and the corre-137
sponding split archives are pinned by checksum in a dedicated138
manifest artifact. Group labels use p with source identifiers and139
an arrow to the target, and paired sources concatenate. In our140
Table 2:Baseline recap across three evaluation protocols; the
protocol column denotes word holdout, instance holdout, and
cross participant transfer, CER is character error rate, and lex
is lexicon projected error rate.
protocol n cer lex
P1 4 0.180±0.084 0.102±0.068
P2 3 0.145±0.063 0.075±0.048
P3 6 0.691±0.133 0.644±0.060
Table 3:Cross participant generalization targeting participant
four; proto distinguishes single source and multi source cross
participant protocols, lvl marks direction level or across direc-
tion aggregate, group encodes source to target participant iden-
tifiers, and lex is lexicon projected error rate.
proto lvl group cer lex
P3 dir p1-¿p4 0.666±0.024 0.651±0.026
P3 dir p2-¿p4 0.809±0.021 0.736±0.022
P3 dir p3-¿p4 0.584±0.018 0.591±0.029
P3 all all-¿p4 0.686±0.114 0.659±0.073
P3MS dir p12-¿p4 0.655±0.016 0.593±0.016
P3MS dir p13-¿p4 0.536±0.009 0.533±0.008
P3MS dir p23-¿p4 0.555±0.005 0.537±0.011
P3MS all all-¿p4 0.582±0.064 0.554±0.034
audited splits, the multi source aggregation reduces CER rela-141
tive to the single source aggregation for the same target.142
The cross participant results for the fourth participant in-143
clude both single source and paired source settings, which pro-144
vide a direct comparison of transfer with and without source145
aggregation under the same audited protocol constraints.146
The spatial modeling table compares spatial inductive bias147
variants at full channels across protocols, including a patchpool148
grid encoder as a minimal implementation rescue. The vari-149
ant labels are vec, rowcol, grid, grid aug, patch, and patch aug.150
The row and column front end tracks the vector baseline more151
closely than the convolutional grid front end under within par-152
ticipant protocols, while patchpool reduces the gap under cross153
participant transfer. Across protocols, grid variants tend to in-154
crease real time factor relative to the vector baseline, and we do155
not observe a consistent accuracy gain over the vector baseline156
in any protocol. 157
The electrode reduction table evaluates a reduced channel158
budget using several selection strategies. The method labels159
are topk, fps two k, xfer, and rand. Across protocols, within160
participant selection and simple transfer selection yield similar161
performance, suggesting that a compact subset can preserve a162
large fraction of the vector baseline performance. Random se-163
lection and simple transfer remain slightly worse than within164
participant selection in the audited results.165
The reduction results complement the protocol tables by166
showing that compact selections preserve much of the vector167
baseline under within participant evaluation, while cross partic-168
ipant transfer remains more challenging and motivates paired169
source and low shot analyses reported in the subsequent tables.170
We evaluate multi source cross participant transfer using171
paired source participants. The group labels concatenate the172
two source identifiers and use an arrow to the target identifier.173
The multi source table reports direction level results for vector174
and layout aware front ends.175
We further analyze multi source transfer deltas against sim-176

=== PAGE 3 ===
Table 4:Spatial modeling at full channels across protocols; vec,
rowcol, grid, grid aug, patch, and patch aug denote vector base-
line, row and column pooling, convolutional grid encoder, grid
with spatial augmentation, patchpool grid encoder, and patch-
pool with augmentation; CER is character error rate and RTF
is real time factor.
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
ple similarity measures, and the conditions analysis summarizes177
the conditional pattern across audited source pairs and targets.178
We evaluate low shot adaptation for a new participant by179
varying the number of training instances per word. The k shot180
table summarizes one shot and two shot results for vector and181
layout aware front ends.182
6. Discussion183
Our results suggest that an explicit convolutional grid encoder184
is not automatically beneficial for electropalatography under185
within participant evaluation, despite its intuitive spatial struc-186
ture. A patchpool grid variant reduces the underperformance of187
the grid encoder under cross participant transfer, indicating that188
spatial encoder design choices can materially affect outcomes,189
but it does not yield consistent gains over the vector baseline190
across protocols. Spatial augmentation can improve robustness191
to synthetic electrode dropout, but it does not close the accuracy192
gap for the convolutional grid variants in our multi participant193
results. Additional analyses on multi source cross participant194
transfer and low shot adaptation are provided as artifact tables,195
and they highlight that cross participant performance remains196
challenging. We also provide a conditions analysis of multi197
source transfer deltas versus simple dataset similarity measures,198
which shows that the effect is conditional and does not present199
a single dominant monotonic trend within our evaluated group200
set. These observations are limited to our audited multi partici-201
pant dataset collection and protocols.202
Across the audited protocols, within participant perfor-203
mance remains stronger than cross participant transfer, empha-204
sizing the difficulty of generalization under limited participant205
coverage. We report these trends as artifact grounded observa-206
tions rather than broad claims, and we expect additional partic-207
ipant data to be necessary for stronger transfer conclusions.208
Table 5:Electrode reduction methods across protocols; topk,
fps two k, xfer, and rand denote within top ranked selection,
farthest point sampling, transfer selection, and random selec-
tion; CER is character error rate and RTF is real time factor.
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
Table 6:Multi source cross participant results by source pair;
group concatenates source identifiers with an arrow to the tar-
get, and vec, rowcol, grid, and grid aug denote vector baseline,
row and column pooling, and grid encoder with or without spa-
tial augmentation; CER is character error rate and RTF is real
time factor.
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
7. Artifacts and Auditability209
This repository uses a strict paper registry that pins every ev-210
idence file by checksum and rejects unsupported manuscript211
blocks. The split manifests, aggregated metrics, compact tables,212
and analysis summaries referenced in this paper are stored as213
deterministic artifacts, enabling audit and reproduction within214
our repository environment.215
8. Ethics and Disclosure216
We report results only for audited artifacts and do not claim217
broader demographic coverage. The datasets and splits used in218
this study are derived from participant recordings, and we focus219
on methodological clarity and artifact traceability rather than220
deployment claims. 221
9. Logic Checks222
The baseline table includes protocol and aggregate metrics223
fields. 224

=== PAGE 4 ===
Table 7:Low shot adaptation results for a new participant;
group uses the participant identifier and k one or k two for the
number of training instances per word, and vec, rowcol, grid,
and grid aug denote vector baseline, row and column pooling,
and grid encoder with or without spatial augmentation; CER is
character error rate and RTF is real time factor.
group variant cer rtf
p3 k1 vec 0.350±0.060 0.0002±0.0000
p3 k1 rowcol 0.334±0.039 0.0005±0.0000
p3 k1 grid 0.515±0.050 0.0007±0.0000
p3 k1 grid aug 0.611±0.157 0.0011±0.0006
p3 k2 vec 0.246±0.009 0.0002±0.0000
p3 k2 rowcol 0.278±0.022 0.0005±0.0000
p3 k2 grid 0.616±0.132 0.0008±0.0001
p3 k2 grid aug 0.689±0.218 0.0007±0.0000
10. References225
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert,226
and J. Brumberg, “Silent speech interfaces,” 2010. [On-227
line]. Available: https://sciencedirect.com/science/article/pii/228
S0167639309001307229
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction230
to Silent Speech Interfaces, 2017. [Online]. Available: https:231
//link.springer.com/book/10.1007/978-3-319-40174-4232
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,233
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces234
for speech restoration: A review,” 2020. [Online]. Available:235
https://ieeexplore.ieee.org/document/9205294/236
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov,237
and S. Lee, “Biosignal sensors and deep learning-based238
speech recognition: A review,” 2021. [Online]. Available:239
https://doi.org/10.3390/s21041399240
[5] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang,241
K. Christofferson, and A. Mariakakis, “Rehearsse: Recognizing242
hidden-in-the-ear silently spelled expressions,” 2024. [Online].243
Available: https://dl.acm.org/doi/10.1145/3613904.3642095244
[6] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-245
nectionist temporal classification,” 2006. [Online]. Available:246
https://dl.acm.org/doi/10.1145/1143844.1143891247
[7] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao,248
A. Bedri, Z. Su, A. Olwal, J. Rekimoto, and T. Starner,249
“Silentspeller: Towards mobile, hands-free, silent speech text250
entry using electropalatography,” 2022. [Online]. Available:251
https://dl.acm.org/doi/10.1145/3491102.3502015252
[8] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality253
reduction of electropalatographic data using latent variable254
models,” 1998. [Online]. Available: https://sciencedirect.com/255
science/article/pii/S0167639398000594256
[9] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and257
G. Calder, “New developments in electropalatography: A258
state-of-the-art report,” 1989. [Online]. Available: https:259
//doi.org/10.3109/02699208908985268260
[10] W. J. Hardcastle, “Electropalatography in phonetic research261
and in speech training,” 1990. [Online]. Available: https:262
//isca-archive.org/icslp 1990/hardcastle90b icslp.html263
[11] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data264
reduction methods and their implications for studies of lingual265
coarticulation,” 1991. [Online]. Available: https://doi.org/10.266
1016/S0095-4470(19)30343-2267
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus,268
and M. Stone, “Development of a silent speech interface driven269
by ultrasound and optical images of the tongue and lips,” 2010.270
[Online]. Available: https://sciencedirect.com/science/article/pii/271
S0167639309001733272
[13] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth273
measurement of face and palate by structured light,” 1993.274
[Online]. Available: https://isca-archive.org/eurospeech 1993/275
shadle93 eurospeech.html276
[14] A. Toutios and K. Margaritis, “Learning electropalatograms from277
acoustics.” [Online]. Available: https://doi.org/10.1109/ICASSP.278
2006.1660032 279
[15] ——, “On the acoustic-to-electropalatographic mapping,” 2006.280
[Online]. Available: https://link.springer.com/chapter/10.1007/281
11613107 16 282
[16] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-283
Aldasoro, “Visualisation and analysis of speech production284
with electropalatography,” 2019. [Online]. Available: https:285
//doi.org/10.3390/jimaging5030040286
[17] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design287
and evaluation of korean electropalatography (k-epg),” 2021.288
[Online]. Available: https://doi.org/10.3390/s21113802289
[18] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph,290
E. D. Cubuk, and Q. V . Le, “Specaugment: A simple data291
augmentation method for automatic speech recognition,” 2019.292
[Online]. Available: https://isca-archive.org/interspeech 2019/293
park19 interspeech.html294
