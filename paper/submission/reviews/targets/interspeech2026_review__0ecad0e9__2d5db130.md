# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 17984,
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
    "sha256": "0ecad0e9c891feb7caba428419a3e49eb9aeb1694476cac0bff200d8efefe401",
    "sha8": "0ecad0e9",
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
    "sha256": "2d5db130538f5ffc43ca516ee5e3cf0b25a25a521c94e91e62280f81a52f2b52",
    "sha8": "2d5db130"
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
      "extracted_chars": 17984,
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
      "sha256": "0ecad0e9c891feb7caba428419a3e49eb9aeb1694476cac0bff200d8efefe401",
      "sha8": "0ecad0e9",
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
      "sha256": "2d5db130538f5ffc43ca516ee5e3cf0b25a25a521c94e91e62280f81a52f2b52",
      "sha8": "2d5db130"
    }
  },
  "run_id": "INTSP2026_STATIC_0ecad0e9_2d5db130"
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
Table 1:Raw dataset summary for each participant dataset.
id N V Tmed contact zero
p1 2328 old 2328 1164 234 0.19 0
thad 2328 old 2328 1164 196 0.20 0
john 2328 2797 1164 283 0.12 4
su 1167 old 1167 1162 229 0.19 0
the spatial layout has been used for visualization, device char-46
acterization, and representation reduction, motivating tests of47
layout aware inductive bias in learned decoders. [8, 1, 5, 3, 9,48
10, 11, 12, 7, 13, 14, 15, 16, 17]49
3. Data and Protocols50
We use four participant electropalatography datasets with word51
labels. Each sample is a variable length binary contact matrix,52
and the raw exports are treated as immutable evidence. We audit53
dataset statistics, label counts, and anomalies before construct-54
ing any train and test splits, and a small set of all-zero samples55
is excluded via a pinned index list.56
The dataset summary table reports id, sample count, vocab-57
ulary size, median sequence length, mean contact rate, and the58
count of all-zero samples for each participant dataset.59
We evaluate three primary protocols. The word holdout60
protocol uses disjoint vocabularies across train, test, and a com-61
petition partition. The instance holdout protocol evaluates held62
out instances of seen words by separating train and competi-63
tion vocabularies while keeping the test vocabulary within their64
union. The cross participant protocol trains on a source partici-65
pant and evaluates on a target participant under a shared vocab-66
ulary constraint. When a target participant has limited within67
word repetition, we configure the cross participant split genera-68
tors to allow single instance target words while keeping source69
side constraints unchanged. All split archives used in this study70
are enumerated with sizes and checksums in manifest artifacts.71
Labels are normalized by uppercasing and filtering to al-72
phabet characters, then represented as a space separated charac-73
ter sequence for CTC training and greedy decoding. This nor-74
malization is applied consistently during split construction and75
dataset preparation to avoid vocabulary drift.76
We report character error rate from greedy decoding and77
streaming speed using real time factor, defined as total infer-78
ence time divided by total input duration. For open-vocabulary79
decoding we also report lexicon projection error rates using a80
training lexicon and a full lexicon.81

=== PAGE 2 ===
Table 2:Shared training configuration across all reported runs.
parameter value
n units 512
n layers 5
stride len 4
kernel len 32
input proj dim 64
specaug on 1
white noise sd 0.8
constant offset sd 0.2
gaussian smooth width 2.0
frame ms 10.0
n batch 10000
train seed 0
n components -1
downsample factor 1
electrode regions all
apply ts2vec 0
Table 3:Baseline recap across three evaluation protocols
(mean and standard deviation over groups).
protocol variant n cer lex
P1 vec 4 0.180±0.084 0.102±0.068
P2 vec 3 0.145±0.063 0.075±0.048
P3 vec 6 0.691±0.133 0.644±0.060
4. Models82
Our baseline model encodes each frame as a vector of palate83
channels and applies a uni-directional recurrent decoder trained84
with a CTC objective. We compare two layout aware front ends:85
a row and column pooling front end that aggregates a proxy grid86
into one dimensional summaries, and a grid reconstruction front87
end that applies a convolutional spatial encoder. For the grid88
model we optionally enable a spatial augmentation that drops89
and shifts contiguous electrode blocks. [6, 18]90
We fix core training hyperparameters across runs; the train-91
ing configuration table lists the shared values extracted from the92
metrics registry.93
5. Results94
The baseline recap table summarizes baseline performance un-95
der word holdout, instance holdout, and cross participant trans-96
fer. Lexicon projection reduces error rates relative to greedy97
decoding across protocols, highlighting the importance of open-98
vocabulary post processing for spelling.99
We additionally evaluate cross participant generalization100
targeting participant four under both single source and multi101
source transfer. The table uses lvl labels dir for single direc-102
tions and all for the across direction aggregation, and the corre-103
sponding split archives are pinned by checksum in a dedicated104
manifest artifact. In our audited splits, the multi source aggre-105
gation reduces CER relative to the single source aggregation for106
the same target.107
The spatial modeling tables compare spatial inductive bias108
variants at full channels across protocols, including a patchpool109
grid encoder as a minimal implementation rescue. The vari-110
ant labels are vec, rowcol, grid, grid aug, patch, and patch aug.111
The row and column front end tracks the vector baseline more112
closely than the convolutional grid front end under within par-113
Table 4:Cross participant generalization targeting participant
four (direction wise mean and standard deviation over seeds,
plus across direction aggregation).
proto lvl group cer lex
P3 dir s1-4 0.666±0.024 0.651±0.026
P3 dir s2-4 0.809±0.021 0.736±0.022
P3 dir s3-4 0.584±0.018 0.591±0.029
P3 all all 0.686±0.114 0.659±0.073
P3MS dir s12-4 0.655±0.016 0.593±0.016
P3MS dir s13-4 0.536±0.009 0.533±0.008
P3MS dir s23-4 0.555±0.005 0.537±0.011
P3MS all all 0.582±0.064 0.554±0.034
Table 5:Spatial modeling at full channels for the word holdout
protocol.
variant cer lex rtf
vec 0.18±0.08 0.10±0.07 0.0006±0.0002
rowcol 0.20±0.09 0.13±0.08 0.0024±0.0011
grid 0.31±0.15 0.25±0.18 0.0036±0.0015
grid aug 0.31±0.14 0.26±0.17 0.0034±0.0011
patch 0.30±0.07 0.24±0.07 0.0038±0.0017
patch aug 0.30±0.09 0.23±0.09 0.0039±0.0017
ticipant protocols, while patchpool reduces the gap under cross114
participant transfer. Across protocols, grid variants tend to in-115
crease real time factor relative to the vector baseline, and we do116
not observe a consistent accuracy gain over the vector baseline117
in any protocol. 118
The electrode reduction tables evaluate a reduced channel119
budget using several selection strategies. The method labels120
are topk, fps two k, xfer, and rand. Across protocols, within121
participant selection and simple transfer selection yield similar122
performance, suggesting that a compact subset can preserve a123
large fraction of the vector baseline performance. Random se-124
lection and simple transfer remain slightly worse than within125
participant selection in the audited results.126
We evaluate multi source cross participant transfer using127
paired source participants. The group labels indicate the two128
source participants followed by the target participant. The multi129
source table reports direction level results for vector and layout130
aware front ends. 131
We evaluate low shot adaptation for a new participant by132
varying the number of training instances per word. The k shot133
table summarizes one shot and two shot results for vector and134
layout aware front ends.135
6. Discussion136
Our results suggest that an explicit convolutional grid encoder137
is not automatically beneficial for electropalatography under138
within participant evaluation, despite its intuitive spatial struc-139
ture. A patchpool grid variant reduces the underperformance of140
the grid encoder under cross participant transfer, indicating that141
spatial encoder design choices can materially affect outcomes,142
but it does not yield consistent gains over the vector baseline143
across protocols. Spatial augmentation can improve robustness144
to synthetic electrode dropout, but it does not close the accuracy145
gap for the convolutional grid variants in our multi participant146
results. Additional analyses on multi source cross participant147
transfer and low shot adaptation are provided as artifact tables,148
and they highlight that cross participant performance remains149

=== PAGE 3 ===
Table 6:Spatial modeling at full channels for the instance hold-
out protocol.
variant cer lex rtf
vec 0.15±0.06 0.07±0.05 0.0001±0.0000
rowcol 0.16±0.08 0.09±0.06 0.0002±0.0000
grid 0.29±0.21 0.23±0.25 0.0004±0.0000
grid aug 0.31±0.24 0.26±0.29 0.0004±0.0000
patch 0.34±0.23 0.28±0.27 0.0007±0.0001
patch aug 0.30±0.16 0.24±0.19 0.0006±0.0000
Table 7:Spatial modeling at full channels for the cross partici-
pant protocol.
variant cer lex rtf
vec 0.69±0.13 0.64±0.06 0.0001±0.0000
rowcol 0.68±0.15 0.63±0.09 0.0002±0.0000
grid 0.75±0.09 0.74±0.07 0.0004±0.0000
grid aug 0.76±0.09 0.75±0.08 0.0004±0.0000
patch 0.69±0.11 0.68±0.08 0.0006±0.0001
patch aug 0.70±0.13 0.67±0.11 0.0005±0.0001
challenging. We also provide a conditions analysis of multi150
source transfer deltas versus simple dataset similarity measures,151
which shows that the effect is conditional and does not present152
a single dominant monotonic trend within our evaluated group153
set. These observations are limited to our audited multi partici-154
pant dataset collection and protocols.155
7. Artifacts and Auditability156
This repository uses a strict paper registry that pins every ev-157
idence file by checksum and rejects unsupported manuscript158
blocks. The split manifests, aggregated metrics, compact tables,159
and analysis summaries referenced in this paper are stored as160
deterministic artifacts, enabling audit and reproduction within161
our repository environment.162
8. Ethics and Disclosure163
We report results only for audited artifacts and do not claim164
broader demographic coverage. The datasets and splits used in165
this study are derived from participant recordings, and we focus166
on methodological clarity and artifact traceability rather than167
deployment claims.168
9. Logic Checks169
The baseline table includes protocol and variant fields.170
10. References171
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert,172
and J. Brumberg, “Silent speech interfaces,” 2010. [On-173
line]. Available: https://sciencedirect.com/science/article/pii/174
S0167639309001307175
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction176
to Silent Speech Interfaces, 2017. [Online]. Available: https:177
//link.springer.com/book/10.1007/978-3-319-40174-4178
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,179
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces180
for speech restoration: A review,” 2020. [Online]. Available:181
https://ieeexplore.ieee.org/document/9205294/182
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov,183
Table 8:Electrode reduction methods for word and instance
holdout protocols.
protocol method cer rtf
P1 topk 0.195±0.083 0.0007±0.0002
P1 fps2k 0.191±0.078 0.0006±0.0002
P1 xfer 0.205±0.095 0.0006±0.0002
P1 rand 0.198±0.079 0.0007±0.0003
P2 topk 0.154±0.059 0.0001±0.0000
P2 fps2k 0.154±0.062 0.0001±0.0000
P2 xfer 0.158±0.071 0.0001±0.0000
P2 rand 0.157±0.067 0.0001±0.0000
Table 9:Electrode reduction methods for the cross participant
protocol.
method cer rtf
topk 0.647±0.130 0.0001±0.0000
fps2k 0.656±0.146 0.0001±0.0000
xfer 0.657±0.144 0.0001±0.0000
rand 0.644±0.133 0.0001±0.0000
and S. Lee, “Biosignal sensors and deep learning-based184
speech recognition: A review,” 2021. [Online]. Available:185
https://doi.org/10.3390/s21041399186
[5] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang,187
K. Christofferson, and A. Mariakakis, “Rehearsse: Recognizing188
hidden-in-the-ear silently spelled expressions,” 2024. [Online].189
Available: https://dl.acm.org/doi/10.1145/3613904.3642095190
[6] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-191
nectionist temporal classification,” 2006. [Online]. Available:192
https://dl.acm.org/doi/10.1145/1143844.1143891193
[7] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao,194
A. Bedri, Z. Su, A. Olwal, J. Rekimoto, and T. Starner,195
“Silentspeller: Towards mobile, hands-free, silent speech text196
entry using electropalatography,” 2022. [Online]. Available:197
https://dl.acm.org/doi/10.1145/3491102.3502015198
[8] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality199
reduction of electropalatographic data using latent variable200
models,” 1998. [Online]. Available: https://sciencedirect.com/201
science/article/pii/S0167639398000594202
[9] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and203
G. Calder, “New developments in electropalatography: A204
state-of-the-art report,” 1989. [Online]. Available: https:205
//doi.org/10.3109/02699208908985268206
[10] W. J. Hardcastle, “Electropalatography in phonetic research207
and in speech training,” 1990. [Online]. Available: https:208
//isca-archive.org/icslp 1990/hardcastle90b icslp.html209
[11] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data210
reduction methods and their implications for studies of lingual211
coarticulation,” 1991. [Online]. Available: https://doi.org/10.212
1016/S0095-4470(19)30343-2213
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus,214
and M. Stone, “Development of a silent speech interface driven215
by ultrasound and optical images of the tongue and lips,” 2010.216
[Online]. Available: https://sciencedirect.com/science/article/pii/217
S0167639309001733218
[13] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth219
measurement of face and palate by structured light,” 1993.220
[Online]. Available: https://isca-archive.org/eurospeech 1993/221
shadle93 eurospeech.html222
[14] A. Toutios and K. Margaritis, “Learning electropalatograms from223
acoustics.” [Online]. Available: https://doi.org/10.1109/ICASSP.224
2006.1660032 225

=== PAGE 4 ===
Table 10:Multi source cross participant results by source pair.
group variant cer rtf
subj23to1 vec 0.473±0.014 0.0001±0.0000
subj23to1 rowcol 0.476±0.014 0.0002±0.0000
subj23to1 grid 0.602±0.076 0.0004±0.0000
subj23to1 grid aug 0.691±0.165 0.0004±0.0000
subj13to2 vec 0.520±0.003 0.0001±0.0000
subj13to2 rowcol 0.504±0.012 0.0003±0.0000
subj13to2 grid 0.511±0.047 0.0004±0.0000
subj13to2 grid aug 0.511±0.016 0.0004±0.0000
subj12to3 vec 0.838±0.034 0.0001±0.0000
subj12to3 rowcol 0.790±0.033 0.0002±0.0000
subj12to3 grid 0.736±0.018 0.0003±0.0000
subj12to3 grid aug 0.756±0.020 0.0003±0.0000
Table 11:Low shot adaptation results for a new participant.
group variant cer rtf
subj3 k1 vec 0.350±0.060 0.0002±0.0000
subj3 k1 rowcol 0.334±0.039 0.0005±0.0000
subj3 k1 grid 0.515±0.050 0.0007±0.0000
subj3 k1 grid aug 0.611±0.157 0.0011±0.0006
subj3 k2 vec 0.246±0.009 0.0002±0.0000
subj3 k2 rowcol 0.278±0.022 0.0005±0.0000
subj3 k2 grid 0.616±0.132 0.0008±0.0001
subj3 k2 grid aug 0.689±0.218 0.0007±0.0000
[15] ——, “On the acoustic-to-electropalatographic mapping,” 2006.226
[Online]. Available: https://link.springer.com/chapter/10.1007/227
11613107 16228
[16] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-229
Aldasoro, “Visualisation and analysis of speech production230
with electropalatography,” 2019. [Online]. Available: https:231
//doi.org/10.3390/jimaging5030040232
[17] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design233
and evaluation of korean electropalatography (k-epg),” 2021.234
[Online]. Available: https://doi.org/10.3390/s21113802235
[18] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph,236
E. D. Cubuk, and Q. V . Le, “Specaugment: A simple data237
augmentation method for automatic speech recognition,” 2019.238
[Online]. Available: https://isca-archive.org/interspeech 2019/239
park19 interspeech.html240
