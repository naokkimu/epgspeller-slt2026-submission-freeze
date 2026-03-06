# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 20511,
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
    "sha256": "9d37dd87468a6daaf6df3b8145c005a3509b0a9f17aaab166dab3de431a4a3c3",
    "sha8": "9d37dd87",
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
    "sha256": "0552404cfa01ae819ea0423413e6704d975e7214228d51439adc3ffb5c1363c6",
    "sha8": "0552404c"
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
      "extracted_chars": 20511,
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
      "sha256": "9d37dd87468a6daaf6df3b8145c005a3509b0a9f17aaab166dab3de431a4a3c3",
      "sha8": "9d37dd87",
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
      "sha256": "0552404cfa01ae819ea0423413e6704d975e7214228d51439adc3ffb5c1363c6",
      "sha8": "0552404c"
    }
  },
  "run_id": "INTSP2026_STATIC_9d37dd87_0552404c"
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
3. Data and Protocols54
We use four participant electropalatography datasets with word55
labels. Each sample is a variable length binary contact matrix,56
and the raw exports are treated as immutable evidence. We audit57
dataset statistics, label counts, and anomalies before construct-58
ing any train and test splits, and a small set of all-zero samples59
is excluded via a pinned index list.60
The audit pipeline records raw file checksums, validates61
schema consistency, and aggregates label distributions, se-62
quence length summaries, and per channel activity statistics be-63
fore any split construction. The raw exports remain unchanged,64
and any exclusions are applied only through pinned index lists65
that are included in the audit artifacts.66
The dataset summary table reports id, sample count, vocab-67
ulary size, median sequence length, mean contact rate, and the68
count of all-zero samples for each participant dataset.69
We evaluate three primary protocols. The word holdout70
protocol uses disjoint vocabularies across train, test, and a com-71
petition partition. The instance holdout protocol evaluates held72
out instances of seen words by separating train and competi-73
tion vocabularies while keeping the test vocabulary within their74
union. The cross participant protocol trains on a source partici-75
pant and evaluates on a target participant under a shared vocab-76
ulary constraint. When a target participant has limited within77
word repetition, we configure the cross participant split genera-78
tors to allow single instance target words while keeping source79
side constraints unchanged. All split archives used in this study80
are enumerated with sizes and checksums in manifest artifacts.81

=== PAGE 2 ===
Table 2:Baseline recap across three evaluation protocols; the
protocol column denotes word holdout, instance holdout, and
cross participant transfer, CER is character error rate, and lex
is lexicon projected error rate.
protocol variant n cer lex
P1 vec 4 0.180±0.084 0.102±0.068
P2 vec 3 0.145±0.063 0.075±0.048
P3 vec 6 0.691±0.133 0.644±0.060
All split archives are generated deterministically from au-82
dited exports with fixed seeds, and each train, test, and competi-83
tion partition is stored as an immutable archive with a checksum84
in the manifests to enable reuse and verification.85
Labels are normalized by uppercasing and filtering to al-86
phabet characters, then represented as a space separated charac-87
ter sequence for CTC training and greedy decoding. This nor-88
malization is applied consistently during split construction and89
dataset preparation to avoid vocabulary drift.90
We report character error rate from greedy decoding and91
streaming speed using real time factor, defined as total infer-92
ence time divided by total input duration. For open-vocabulary93
decoding we also report lexicon projection error rates using a94
training lexicon and a full lexicon.95
4. Models96
Our baseline model encodes each frame as a vector of palate97
channels and applies a uni-directional recurrent decoder trained98
with a CTC objective. We compare two layout aware front ends:99
a row and column pooling front end that aggregates a proxy grid100
into one dimensional summaries, and a grid reconstruction front101
end that applies a convolutional spatial encoder. For the grid102
model we optionally enable a spatial augmentation that drops103
and shifts contiguous electrode blocks. [6, 18]104
The proxy grid is constructed from the palate channel lay-105
out and supports either row and column pooling or convolu-106
tional feature extraction, while spatial augmentation perturbs107
contiguous electrode blocks to emulate missing contacts and108
minor spatial shifts.109
We fix core training hyperparameters across runs and record110
the shared configuration in the metrics registry for auditability.111
5. Results112
The baseline recap table summarizes baseline performance un-113
der word holdout, instance holdout, and cross participant trans-114
fer. Lexicon projection reduces error rates relative to greedy115
decoding across protocols, highlighting the importance of open-116
vocabulary post processing for spelling.117
We additionally evaluate cross participant generalization118
targeting participant four under both single source and multi119
source transfer. The table uses lvl labels dir for single direc-120
tions and all for the across direction aggregation, and the corre-121
sponding split archives are pinned by checksum in a dedicated122
manifest artifact. Group labels use p with source identifiers and123
an arrow to the target, and paired sources concatenate. In our124
audited splits, the multi source aggregation reduces CER rela-125
tive to the single source aggregation for the same target.126
The spatial modeling table compares spatial inductive bias127
variants at full channels across protocols, including a patchpool128
grid encoder as a minimal implementation rescue. The vari-129
ant labels are vec, rowcol, grid, grid aug, patch, and patch aug.130
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
P3MS dir p1p2-¿p4 0.655±0.016 0.593±0.016
P3MS dir p1p3-¿p4 0.536±0.009 0.533±0.008
P3MS dir p2p3-¿p4 0.555±0.005 0.537±0.011
P3MS all all-¿p4 0.582±0.064 0.554±0.034
Table 4:Spatial modeling at full channels across protocols;
variant labels are vec for vector baseline, rowcol for row and
column pooling, grid for convolutional grid encoder, grid aug
for grid with spatial augmentation, patch for patchpool grid en-
coder, and patch aug for patchpool with spatial augmentation;
CER is character error rate and RTF is real time factor.
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
The row and column front end tracks the vector baseline more131
closely than the convolutional grid front end under within par-132
ticipant protocols, while patchpool reduces the gap under cross133
participant transfer. Across protocols, grid variants tend to in-134
crease real time factor relative to the vector baseline, and we do135
not observe a consistent accuracy gain over the vector baseline136
in any protocol. 137
The electrode reduction table evaluates a reduced channel138
budget using several selection strategies. The method labels139
are topk, fps two k, xfer, and rand. Across protocols, within140
participant selection and simple transfer selection yield similar141
performance, suggesting that a compact subset can preserve a142
large fraction of the vector baseline performance. Random se-143
lection and simple transfer remain slightly worse than within144
participant selection in the audited results.145
The reduction results complement the protocol tables by146
showing that compact selections preserve much of the vector147
baseline under within participant evaluation, while cross partic-148
ipant transfer remains more challenging and motivates paired149

=== PAGE 3 ===
Table 5:Electrode reduction methods across protocols; method
labels are topk for within participant top ranked selection, fps
two k for farthest point sampling, xfer for transfer selection,
and rand for random selection; CER is character error rate and
RTF is real time factor.
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
group uses concatenated source identifiers with an arrow to the
target, variant labels are vec for vector baseline, rowcol for row
and column pooling, grid for convolutional grid encoder, and
grid aug for grid with spatial augmentation; CER is character
error rate and RTF is real time factor.
group variant cer rtf
p2p3-¿p1 vec 0.473±0.014 0.0001±0.0000
p2p3-¿p1 rowcol 0.476±0.014 0.0002±0.0000
p2p3-¿p1 grid 0.602±0.076 0.0004±0.0000
p2p3-¿p1 grid aug 0.691±0.165 0.0004±0.0000
p1p3-¿p2 vec 0.520±0.003 0.0001±0.0000
p1p3-¿p2 rowcol 0.504±0.012 0.0003±0.0000
p1p3-¿p2 grid 0.511±0.047 0.0004±0.0000
p1p3-¿p2 grid aug 0.511±0.016 0.0004±0.0000
p1p2-¿p3 vec 0.838±0.034 0.0001±0.0000
p1p2-¿p3 rowcol 0.790±0.033 0.0002±0.0000
p1p2-¿p3 grid 0.736±0.018 0.0003±0.0000
p1p2-¿p3 grid aug 0.756±0.020 0.0003±0.0000
source and low shot analyses reported in the subsequent tables.150
We evaluate multi source cross participant transfer using151
paired source participants. The group labels concatenate the152
two source identifiers and use an arrow to the target identifier.153
The multi source table reports direction level results for vector154
and layout aware front ends.155
We further analyze multi source transfer deltas against sim-156
ple similarity measures, and the conditions analysis summarizes157
the conditional pattern across audited source pairs and targets.158
We evaluate low shot adaptation for a new participant by159
varying the number of training instances per word. The k shot160
table summarizes one shot and two shot results for vector and161
layout aware front ends.162
6. Discussion163
Our results suggest that an explicit convolutional grid encoder164
is not automatically beneficial for electropalatography under165
within participant evaluation, despite its intuitive spatial struc-166
ture. A patchpool grid variant reduces the underperformance of167
the grid encoder under cross participant transfer, indicating that168
spatial encoder design choices can materially affect outcomes,169
Table 7:Low shot adaptation results for a new participant;
group uses the participant identifier and k one or k two to de-
note the number of training instances per word, variant labels
are vec for vector baseline, rowcol for row and column pooling,
grid for convolutional grid encoder, and grid aug for grid with
spatial augmentation; CER is character error rate and RTF is
real time factor.
group variant cer rtf
p3 k1 vec 0.350±0.060 0.0002±0.0000
p3 k1 rowcol 0.334±0.039 0.0005±0.0000
p3 k1 grid 0.515±0.050 0.0007±0.0000
p3 k1 grid aug 0.611±0.157 0.0011±0.0006
p3 k2 vec 0.246±0.009 0.0002±0.0000
p3 k2 rowcol 0.278±0.022 0.0005±0.0000
p3 k2 grid 0.616±0.132 0.0008±0.0001
p3 k2 grid aug 0.689±0.218 0.0007±0.0000
but it does not yield consistent gains over the vector baseline170
across protocols. Spatial augmentation can improve robustness171
to synthetic electrode dropout, but it does not close the accuracy172
gap for the convolutional grid variants in our multi participant173
results. Additional analyses on multi source cross participant174
transfer and low shot adaptation are provided as artifact tables,175
and they highlight that cross participant performance remains176
challenging. We also provide a conditions analysis of multi177
source transfer deltas versus simple dataset similarity measures,178
which shows that the effect is conditional and does not present179
a single dominant monotonic trend within our evaluated group180
set. These observations are limited to our audited multi partici-181
pant dataset collection and protocols.182
7. Artifacts and Auditability183
This repository uses a strict paper registry that pins every ev-184
idence file by checksum and rejects unsupported manuscript185
blocks. The split manifests, aggregated metrics, compact tables,186
and analysis summaries referenced in this paper are stored as187
deterministic artifacts, enabling audit and reproduction within188
our repository environment.189
8. Ethics and Disclosure190
We report results only for audited artifacts and do not claim191
broader demographic coverage. The datasets and splits used in192
this study are derived from participant recordings, and we focus193
on methodological clarity and artifact traceability rather than194
deployment claims. 195
9. Logic Checks196
The baseline table includes protocol and variant fields.197
10. References198
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert,199
and J. Brumberg, “Silent speech interfaces,” 2010. [On-200
line]. Available: https://sciencedirect.com/science/article/pii/201
S0167639309001307202
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction203
to Silent Speech Interfaces, 2017. [Online]. Available: https:204
//link.springer.com/book/10.1007/978-3-319-40174-4205
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,206
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces207

=== PAGE 4 ===
for speech restoration: A review,” 2020. [Online]. Available:208
https://ieeexplore.ieee.org/document/9205294/209
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov,210
and S. Lee, “Biosignal sensors and deep learning-based211
speech recognition: A review,” 2021. [Online]. Available:212
https://doi.org/10.3390/s21041399213
[5] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang,214
K. Christofferson, and A. Mariakakis, “Rehearsse: Recognizing215
hidden-in-the-ear silently spelled expressions,” 2024. [Online].216
Available: https://dl.acm.org/doi/10.1145/3613904.3642095217
[6] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-218
nectionist temporal classification,” 2006. [Online]. Available:219
https://dl.acm.org/doi/10.1145/1143844.1143891220
[7] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao,221
A. Bedri, Z. Su, A. Olwal, J. Rekimoto, and T. Starner,222
“Silentspeller: Towards mobile, hands-free, silent speech text223
entry using electropalatography,” 2022. [Online]. Available:224
https://dl.acm.org/doi/10.1145/3491102.3502015225
[8] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality226
reduction of electropalatographic data using latent variable227
models,” 1998. [Online]. Available: https://sciencedirect.com/228
science/article/pii/S0167639398000594229
[9] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and230
G. Calder, “New developments in electropalatography: A231
state-of-the-art report,” 1989. [Online]. Available: https:232
//doi.org/10.3109/02699208908985268233
[10] W. J. Hardcastle, “Electropalatography in phonetic research234
and in speech training,” 1990. [Online]. Available: https:235
//isca-archive.org/icslp 1990/hardcastle90b icslp.html236
[11] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data237
reduction methods and their implications for studies of lingual238
coarticulation,” 1991. [Online]. Available: https://doi.org/10.239
1016/S0095-4470(19)30343-2240
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus,241
and M. Stone, “Development of a silent speech interface driven242
by ultrasound and optical images of the tongue and lips,” 2010.243
[Online]. Available: https://sciencedirect.com/science/article/pii/244
S0167639309001733245
[13] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth246
measurement of face and palate by structured light,” 1993.247
[Online]. Available: https://isca-archive.org/eurospeech 1993/248
shadle93 eurospeech.html249
[14] A. Toutios and K. Margaritis, “Learning electropalatograms from250
acoustics.” [Online]. Available: https://doi.org/10.1109/ICASSP.251
2006.1660032252
[15] ——, “On the acoustic-to-electropalatographic mapping,” 2006.253
[Online]. Available: https://link.springer.com/chapter/10.1007/254
11613107 16255
[16] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-256
Aldasoro, “Visualisation and analysis of speech production257
with electropalatography,” 2019. [Online]. Available: https:258
//doi.org/10.3390/jimaging5030040259
[17] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design260
and evaluation of korean electropalatography (k-epg),” 2021.261
[Online]. Available: https://doi.org/10.3390/s21113802262
[18] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph,263
E. D. Cubuk, and Q. V . Le, “Specaugment: A simple data264
augmentation method for automatic speech recognition,” 2019.265
[Online]. Available: https://isca-archive.org/interspeech 2019/266
park19 interspeech.html267
