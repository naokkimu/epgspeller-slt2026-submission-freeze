# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 18939,
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
    "sha256": "0be8cd3db3bf1e7e2653d754fa4154d260a880fb81945bf3624d46fc0577588e",
    "sha8": "0be8cd3d",
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
    "sha256": "cce356ec5c6579d960c12516680afde2113909b9759998e813388dcdeba77fbc",
    "sha8": "cce356ec"
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
      "extracted_chars": 18939,
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
      "sha256": "0be8cd3db3bf1e7e2653d754fa4154d260a880fb81945bf3624d46fc0577588e",
      "sha8": "0be8cd3d",
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
      "sha256": "cce356ec5c6579d960c12516680afde2113909b9759998e813388dcdeba77fbc",
      "sha8": "cce356ec"
    }
  },
  "run_id": "INTSP2026_STATIC_0be8cd3d_cce356ec"
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
dataset id n samples n unique labels T median total frames mean contact all zero samples exclude indices n
p1 2328 old 2328 1164 234.000 570750 0.1876 0 0
thad 2328 old 2328 1164 196.000 484586 0.2029 0 0
john 2328 2797 1164 283.000 810375 0.1221 4 4
su 1167 old 1167 1162 229.000 287808 0.1855 0 0
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
The dataset summary table reports raw sample counts, vo-57
cabulary sizes, median sequence length, total frames, mean58
contact rate, and excluded all-zero counts for each participant59
dataset. 60
We evaluate three primary protocols. The word holdout61
protocol uses disjoint vocabularies across train, test, and a com-62
petition partition. The instance holdout protocol evaluates held63
out instances of seen words by separating train and competi-64
tion vocabularies while keeping the test vocabulary within their65
union. The cross participant protocol trains on a source partici-66
pant and evaluates on a target participant under a shared vocab-67
ulary constraint. When a target participant has limited within68
word repetition, we configure the cross participant split genera-69
tors to allow single instance target words while keeping source70
side constraints unchanged. All split archives used in this study71
are enumerated with sizes and checksums in manifest artifacts.72
Labels are normalized by uppercasing and filtering to al-73
phabet characters, then represented as a space separated charac-74
ter sequence for CTC training and greedy decoding. This nor-75
malization is applied consistently during split construction and76
dataset preparation to avoid vocabulary drift.77
We report character error rate from greedy decoding and78
streaming speed using real time factor, defined as total infer-79
ence time divided by total input duration. For open-vocabulary80
decoding we also report lexicon projection error rates using a81
training lexicon and a full lexicon.82

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
protocol variant n cer m cer s lex all m lex all s
P1 vector 4 0.1796 0.0844 0.1018 0.0679
P2 vector 3 0.1451 0.0627 0.0747 0.0476
P3 vector 6 0.6909 0.1332 0.6442 0.0604
4. Models83
Our baseline model encodes each frame as a vector of palate84
channels and applies a uni-directional recurrent decoder trained85
with a CTC objective. We compare two layout aware front ends:86
a row and column pooling front end that aggregates a proxy grid87
into one dimensional summaries, and a grid reconstruction front88
end that applies a convolutional spatial encoder. For the grid89
model we optionally enable a spatial augmentation that drops90
and shifts contiguous electrode blocks. [6, 18]91
We fix core training hyperparameters across runs; the train-92
ing configuration table lists the shared values extracted from the93
metrics registry.94
5. Results95
The baseline recap table summarizes baseline performance un-96
der word holdout, instance holdout, and cross participant trans-97
fer. Lexicon projection reduces error rates relative to greedy98
decoding across protocols, highlighting the importance of open-99
vocabulary post processing for spelling.100
We additionally evaluate cross participant generalization101
targeting participant four under both single source and multi102
source transfer. The to participant four generalization table103
summarizes direction level seed statistics, and the correspond-104
ing split archives are pinned by checksum in a dedicated mani-105
fest artifact.106
The spatial modeling tables compare spatial inductive bias107
variants at full channels across protocols, including a patchpool108
grid encoder as a minimal implementation rescue. The row and109
column front end tracks the vector baseline more closely than110
the convolutional grid front end under within participant pro-111
tocols, while patchpool reduces the gap under cross participant112
transfer. Across protocols, grid variants tend to increase real113
time factor relative to the vector baseline.114
Table 4:Cross participant generalization targeting participant
four (direction wise mean and standard deviation over seeds,
plus across direction aggregation).
protocol level group cer lex all rtf
P3 direction subj1to4 0.6660 +/- 0.0237 0.6508 +/- 0.0261 0.000192 +/- 0.000088
P3 direction subj2to4 0.8091 +/- 0.0207 0.7359 +/- 0.0216 0.000145 +/- 0.000010
P3 direction subj3to4 0.5840 +/- 0.0180 0.5911 +/- 0.0287 0.000140 +/- 0.000007
P3 across directions ALL to4 0.6863 +/- 0.1139 0.6593 +/- 0.0728 0.000159 +/- 0.000029
P3MS direction subj12to4 0.6546 +/- 0.0161 0.5932 +/- 0.0162 0.000138 +/- 0.000011
P3MS direction subj13to4 0.5363 +/- 0.0089 0.5327 +/- 0.0084 0.000148 +/- 0.000010
P3MS direction subj23to4 0.5547 +/- 0.0046 0.5366 +/- 0.0111 0.000144 +/- 0.000007
P3MS across directions ALL to4 0.5819 +/- 0.0637 0.5541 +/- 0.0339 0.000143 +/- 0.000005
Table 5:Spatial modeling at full channels for the word holdout
protocol.
variant cer lex all rtf
vector 0.1796 +/- 0.0844 0.1018 +/- 0.0679 0.000628 +/- 0.000232
rowcol 0.2016 +/- 0.0886 0.1285 +/- 0.0810 0.002401 +/- 0.001106
spatial2d 0.3062 +/- 0.1491 0.2536 +/- 0.1797 0.003564 +/- 0.001540
spatial2d aug 0.3094 +/- 0.1440 0.2605 +/- 0.1681 0.003414 +/- 0.001054
patchpool 0.2982 +/- 0.0666 0.2373 +/- 0.0732 0.003795 +/- 0.001663
patchpool aug 0.2988 +/- 0.0891 0.2338 +/- 0.0920 0.003876 +/- 0.001709
The electrode reduction table evaluates a reduced chan-115
nel budget using several selection strategies. Across protocols,116
within participant selection and simple transfer selection yield117
similar performance, suggesting that a compact subset can pre-118
serve a large fraction of the vector baseline performance.119
We evaluate multi source cross participant transfer using120
paired source participants. The multi source table reports direc-121
tion level results for vector and layout aware front ends.122
We evaluate low shot adaptation for a new participant by123
varying the number of training instances per word. The k shot124
table summarizes results for vector and layout aware front ends.125
6. Discussion126
Our results suggest that an explicit convolutional grid encoder127
is not automatically beneficial for electropalatography under128
within participant evaluation, despite its intuitive spatial struc-129
ture. A patchpool grid variant reduces the underperformance of130
the grid encoder under cross participant transfer, indicating that131
spatial encoder design choices can materially affect outcomes,132
but it does not yield consistent gains over the vector baseline133
across protocols. Spatial augmentation can improve robustness134
to synthetic electrode dropout, but it does not close the accuracy135
gap for the convolutional grid variants in our multi participant136
results. Additional analyses on multi source cross participant137
transfer and low shot adaptation are provided as artifact tables,138
and they highlight that cross participant performance remains139
challenging. We also provide a conditions analysis of multi140
source transfer deltas versus simple dataset similarity measures,141
which shows that the effect is conditional and does not present142
a single dominant monotonic trend within our evaluated group143
set. 144
7. Artifacts and Auditability145
This repository uses a strict paper registry that pins every ev-146
idence file by checksum and rejects unsupported manuscript147
blocks. The split manifests, aggregated metrics, compact tables,148

=== PAGE 3 ===
Table 6:Spatial modeling at full channels for the instance hold-
out protocol.
variant cer lex all rtf
vector 0.1451 +/- 0.0627 0.0747 +/- 0.0476 0.000107 +/- 0.000010
rowcol 0.1613 +/- 0.0783 0.0893 +/- 0.0636 0.000244 +/- 0.000037
spatial2d 0.2894 +/- 0.2126 0.2321 +/- 0.2530 0.000389 +/- 0.000047
spatial2d aug 0.3139 +/- 0.2436 0.2611 +/- 0.2879 0.000392 +/- 0.000045
patchpool 0.3384 +/- 0.2324 0.2850 +/- 0.2689 0.000658 +/- 0.000088
patchpool aug 0.3014 +/- 0.1626 0.2438 +/- 0.1897 0.000621 +/- 0.000038
Table 7:Spatial modeling at full channels for the cross partici-
pant protocol.
variant cer lex all rtf
vector 0.6909 +/- 0.1332 0.6442 +/- 0.0604 0.000110 +/- 0.000014
rowcol 0.6828 +/- 0.1510 0.6260 +/- 0.0850 0.000243 +/- 0.000033
spatial2d 0.7507 +/- 0.0897 0.7434 +/- 0.0699 0.000393 +/- 0.000042
spatial2d aug 0.7559 +/- 0.0920 0.7474 +/- 0.0803 0.000397 +/- 0.000046
patchpool 0.6898 +/- 0.1103 0.6840 +/- 0.0819 0.000631 +/- 0.000070
patchpool aug 0.6992 +/- 0.1305 0.6749 +/- 0.1076 0.000476 +/- 0.000079
and analysis summaries referenced in this paper are stored as149
deterministic artifacts, enabling audit and reproduction within150
our repository environment.151
8. Ethics and Disclosure152
We report results only for audited artifacts and do not claim153
broader demographic coverage. The datasets and splits used in154
this study are derived from participant recordings, and we focus155
on methodological clarity and artifact traceability rather than156
deployment claims.157
9. Logic Checks158
The baseline table includes protocol and variant fields.159
10. References160
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert,161
and J. Brumberg, “Silent speech interfaces,” 2010. [On-162
line]. Available: https://sciencedirect.com/science/article/pii/163
S0167639309001307164
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction165
to Silent Speech Interfaces, 2017. [Online]. Available: https:166
//link.springer.com/book/10.1007/978-3-319-40174-4167
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,168
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces169
for speech restoration: A review,” 2020. [Online]. Available:170
https://ieeexplore.ieee.org/document/9205294/171
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov,172
and S. Lee, “Biosignal sensors and deep learning-based173
speech recognition: A review,” 2021. [Online]. Available:174
https://doi.org/10.3390/s21041399175
[5] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang,176
K. Christofferson, and A. Mariakakis, “Rehearsse: Recognizing177
hidden-in-the-ear silently spelled expressions,” 2024. [Online].178
Available: https://dl.acm.org/doi/10.1145/3613904.3642095179
[6] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-180
nectionist temporal classification,” 2006. [Online]. Available:181
https://dl.acm.org/doi/10.1145/1143844.1143891182
[7] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao,183
A. Bedri, Z. Su, A. Olwal, J. Rekimoto, and T. Starner,184
Table 8:Electrode reduction methods for word and instance
holdout protocols.
protocol method cer rtf
P1 within topk 0.1952 +/- 0.0827 0.000657 +/- 0.000210
P1 within fps2k 0.1912 +/- 0.0781 0.000619 +/- 0.000229
P1 transfer topk 0.2053 +/- 0.0951 0.000586 +/- 0.000218
P1 random 0.1980 +/- 0.0793 0.000665 +/- 0.000282
P2 within topk 0.1544 +/- 0.0591 0.000110 +/- 0.000011
P2 within fps2k 0.1539 +/- 0.0617 0.000110 +/- 0.000010
P2 transfer topk 0.1584 +/- 0.0709 0.000106 +/- 0.000009
P2 random 0.1566 +/- 0.0669 0.000105 +/- 0.000011
Table 9:Electrode reduction methods for the cross participant
protocol.
method cer rtf
within topk 0.6473 +/- 0.1301 0.000108 +/- 0.000009
within fps2k 0.6564 +/- 0.1465 0.000107 +/- 0.000010
transfer topk 0.6569 +/- 0.1441 0.000109 +/- 0.000009
random 0.6442 +/- 0.1328 0.000111 +/- 0.000010
“Silentspeller: Towards mobile, hands-free, silent speech text185
entry using electropalatography,” 2022. [Online]. Available:186
https://dl.acm.org/doi/10.1145/3491102.3502015187
[8] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality188
reduction of electropalatographic data using latent variable189
models,” 1998. [Online]. Available: https://sciencedirect.com/190
science/article/pii/S0167639398000594191
[9] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and192
G. Calder, “New developments in electropalatography: A193
state-of-the-art report,” 1989. [Online]. Available: https:194
//doi.org/10.3109/02699208908985268195
[10] W. J. Hardcastle, “Electropalatography in phonetic research196
and in speech training,” 1990. [Online]. Available: https:197
//isca-archive.org/icslp 1990/hardcastle90b icslp.html198
[11] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data199
reduction methods and their implications for studies of lingual200
coarticulation,” 1991. [Online]. Available: https://doi.org/10.201
1016/S0095-4470(19)30343-2202
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus,203
and M. Stone, “Development of a silent speech interface driven204
by ultrasound and optical images of the tongue and lips,” 2010.205
[Online]. Available: https://sciencedirect.com/science/article/pii/206
S0167639309001733207
[13] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth208
measurement of face and palate by structured light,” 1993.209
[Online]. Available: https://isca-archive.org/eurospeech 1993/210
shadle93 eurospeech.html211
[14] A. Toutios and K. Margaritis, “Learning electropalatograms from212
acoustics.” [Online]. Available: https://doi.org/10.1109/ICASSP.213
2006.1660032 214
[15] ——, “On the acoustic-to-electropalatographic mapping,” 2006.215
[Online]. Available: https://link.springer.com/chapter/10.1007/216
11613107 16 217
[16] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-218
Aldasoro, “Visualisation and analysis of speech production219
with electropalatography,” 2019. [Online]. Available: https:220
//doi.org/10.3390/jimaging5030040221
[17] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design222
and evaluation of korean electropalatography (k-epg),” 2021.223
[Online]. Available: https://doi.org/10.3390/s21113802224
[18] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph,225
E. D. Cubuk, and Q. V . Le, “Specaugment: A simple data226

=== PAGE 4 ===
Table 10:Multi source cross participant results by source pair.
group variant cer rtf
subj23to1 vector 0.4735 +/- 0.0136 0.000121 +/- 0.000017
subj23to1 rowcol 0.4759 +/- 0.0138 0.000237 +/- 0.000007
subj23to1 spatial2d 0.6020 +/- 0.0765 0.000389 +/- 0.000002
subj23to1 spatial2d aug 0.6911 +/- 0.1646 0.000386 +/- 0.000007
subj13to2 vector 0.5203 +/- 0.0029 0.000116 +/- 0.000002
subj13to2 rowcol 0.5042 +/- 0.0117 0.000297 +/- 0.000024
subj13to2 spatial2d 0.5106 +/- 0.0474 0.000435 +/- 0.000005
subj13to2 spatial2d aug 0.5114 +/- 0.0164 0.000433 +/- 0.000006
subj12to3 vector 0.8381 +/- 0.0336 0.000096 +/- 0.000002
subj12to3 rowcol 0.7903 +/- 0.0328 0.000203 +/- 0.000004
subj12to3 spatial2d 0.7362 +/- 0.0182 0.000343 +/- 0.000012
subj12to3 spatial2d aug 0.7561 +/- 0.0197 0.000346 +/- 0.000009
Table 11:Low shot adaptation results for a new participant.
group variant cer rtf
subj3 k1 vector 0.3503 +/- 0.0599 0.000164 +/- 0.000009
subj3 k1 rowcol 0.3344 +/- 0.0386 0.000502 +/- 0.000022
subj3 k1 spatial2d 0.5153 +/- 0.0500 0.000712 +/- 0.000005
subj3 k1 spatial2d aug 0.6105 +/- 0.1572 0.001067 +/- 0.000637
subj3 k2 vector 0.2458 +/- 0.0085 0.000165 +/- 0.000002
subj3 k2 rowcol 0.2782 +/- 0.0217 0.000522 +/- 0.000007
subj3 k2 spatial2d 0.6156 +/- 0.1321 0.000769 +/- 0.000064
subj3 k2 spatial2d aug 0.6889 +/- 0.2179 0.000748 +/- 0.000038
augmentation method for automatic speech recognition,” 2019.227
[Online]. Available: https://isca-archive.org/interspeech 2019/228
park19 interspeech.html229
