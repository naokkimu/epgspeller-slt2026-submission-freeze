# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 18753,
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
      },
      {
        "height_pt": 841.89,
        "page": 5,
        "width_pt": 595.276
      }
    ],
    "page_count": 5,
    "path": "interspeech2026_review.pdf",
    "sha256": "204058f98de0bfdd35f96ba49f44b818b0a1e54348d2f2ce4923849d73e0fb8a",
    "sha8": "204058f9",
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
      "plain_characters": 913
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
    "sha256": "d8de0917ace83a57aa8f51a9010fe021eac8e4f8e044579315473aa7e88e1970",
    "sha8": "d8de0917"
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
        "abstract_chars": 913,
        "max_characters": 1000
      },
      "id": "abstract_length",
      "message": "abstract_chars=913 <= max_characters=1000",
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
        "page_count": 5
      },
      "id": "page_limit",
      "message": "page_count=5 <= max_pages=6",
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
      "extracted_chars": 18753,
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
        },
        {
          "height_pt": 841.89,
          "page": 5,
          "width_pt": 595.276
        }
      ],
      "page_count": 5,
      "path": "interspeech2026_review.pdf",
      "sha256": "204058f98de0bfdd35f96ba49f44b818b0a1e54348d2f2ce4923849d73e0fb8a",
      "sha8": "204058f9",
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
        "plain_characters": 913
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
      "sha256": "d8de0917ace83a57aa8f51a9010fe021eac8e4f8e044579315473aa7e88e1970",
      "sha8": "d8de0917"
    }
  },
  "run_id": "INTSP2026_STATIC_204058f9_d8de0917"
}
```

## TeX preamble (first 200 lines)

```tex
% Auto-generated from paper/paper.json (paper-json v1.0.0). Do not edit by hand.
% Target: INTERSPEECH 2026 Paper Kit (Interspeech.cls).
\documentclass{Interspeech}
\usepackage{placeins}

\title{EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for Character-Level Silent Spelling}
\keywords{silent speech interface, electropalatography, character-level decoding, text entry, auditability}

```

## PDF extracted text (page-separated, deterministic truncation)

=== PAGE 1 ===
EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for
Character-Level Silent Spelling
Anonymous submission to Interspeech 2026
Abstract1
Claim: Audited protocol design enables comparable evalu-2
ation of EPG silent spelling and shows that layout-aware front3
ends do not consistently outperform a vector baseline under the4
tested protocols. Silent speech text entry with electropalatogra-5
phy requires models that generalize across word identities and6
participants while remaining auditable. We present an evidence-7
only study of silent spelling from binary palate contact pat-8
terns using character-level decoding and lexicon-projected eval-9
uation. We define protocols for word holdout, instance holdout,10
and cross participant transfer. Using participant labeled datasets11
and deterministic artifact tracking, we evaluate a vector baseline12
and two layout aware front ends, and analyze electrode reduc-13
tion and low shot adaptation. Across our audited runs, the row14
and column front end tracks the vector baseline more closely15
than a convolutional grid front end.16
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
Claim: Audited protocols enable comparable evaluation of47
EPG silent spelling and show that layout-aware front ends do48
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
not consistently beat a vector baseline.49
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
petition partition. The instance holdout protocol tests held out82

=== PAGE 2 ===
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
participant datasets. They also show the fourth participant is101
target-only (not used as a source) in the cross-participant splits.102
The audited label histogram for the fourth participant is dom-103
inated by single-instance labels, so we restrict that participant104
to target-only use in cross-participant evaluation. This separa-105
tion explains why the dataset summary includes all participant106
datasets even when a protocol uses only a subset.107
We normalize labels by uppercasing and filtering to alpha-108
bet characters, then represent each label as a space separated109
character sequence for CTC training and greedy decoding. We110
apply this step consistently during split construction and dataset111
preparation to avoid vocabulary drift.112
We keep the label normalization step consistent across all113
splits and dataset preparation steps. This aligns the decoder114
vocabulary with the audited labels and reduces drift between115
training and artifacts used to evaluate.116
We report character error rate from greedy decoding and117
streaming speed using real time factor. We define real time fac-118
tor as total inference time divided by total input duration. For119
character-level decoding we also report lexicon projection error120
rates using a training lexicon and a full lexicon.121
Greedy decoding reports unconstrained character se-122
quences. Lexicon projection maps outputs to finite word sets123
derived from the training vocabulary or the full audited lexicon.124
This allows us to separate decoding quality from lexicon con-125
straints. We compute real time factor by dividing inference time126
by input duration under the same test harness. Tables summa-127
rize results over four split seeds as mean and standard devia-128
tion. We compute two sided t distribution confidence intervals129
for the primary accuracy metric and paired t tests with Holm130
correction; the compact statistical summary table is provided in131
the supplementary archive.132
3. Models133
Our baseline model encodes each frame as a vector of palate134
channels and applies a uni-directional recurrent decoder trained135
with a CTC objective. We compare two layout aware front ends.136
One is a row and column pooling front end that aggregates a137
proxy grid into one dimensional summaries. The other is a grid138
front end that reconstructs a proxy grid and applies a convolu-139
tional spatial encoder. For the grid model we optionally enable a140
spatial augmentation that drops and shifts contiguous electrode141
blocks. [11, 19]142
The proxy grid is constructed from the palate channel lay-143
out. It supports row and column pooling or convolutional fea-144
Table 2:Baseline recap across evaluation protocols; the proto-
col column denotes word holdout, instance holdout, and cross
participant transfer, n counts split aggregates, CER is character
error rate, and lex is lexicon projected error rate.
protocol n cer lex
P1 4 0.180±0.084 0.102±0.068
P2 3 0.145±0.063 0.075±0.048
P3 6 0.691±0.133 0.644±0.060
Table 3:Cross participant generalization targeting the fourth
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
ture extraction. We use a fixed layout file for the mapping so145
that row and column indices are consistent across splits. We146
augment spatially by perturbing contiguous electrode blocks to147
emulate missing contacts and minor spatial shifts.148
We fix core training hyperparameters across runs and record149
how we configure them in the metrics registry for auditability.150
4. Results151
We report greedy decoding error, lexicon-projected error, and152
streaming cost under a shared evaluation harness for all proto-153
cols. The fourth participant is target-only in cross-participant154
evaluation due to single-instance label dominance. All metrics155
are derived from the same audited registry.156
We summarize baseline performance across the three eval-157
uation protocols. 158
Baseline error is lowest for word and instance holdout and159
highest for cross participant transfer, consistent with the proto-160
col difficulty ordering.161
We evaluate cross-participant transfer with the fourth par-162
ticipant as target under single-source and paired-source settings.163
Paired-source transfer is often lower error than single-164
source transfer, but direction-level outcomes are mixed.165
We evaluate paired-source cross-participant transfer under166
the same target and protocol constraints.167
Paired-source transfer is mixed across targets and front168
ends. 169
We visualize how accuracy and streaming cost vary with170
electrode budget for the word holdout protocol.171
Accuracy improves as electrode budget increases, random172
selection remains weaker than within participant selection, and173
streaming cost varies less than error.174
We compare vector, row/col, and grid-based front ends at175
full channels across protocols.176
Row and column pooling tends to track the vector baseline177
more closely, while grid variants increase error and streaming178

=== PAGE 3 ===
Table 4:Multi source cross participant results by source pair;
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
cost across protocols.179
0.10
0.15
0.20
CER
topk
fps2k
random
full budget
16 32 48 64 80 96 112
Electrode budget (K)
0.0004
0.0005
0.0006
0.0007
streaming RTF
Figure 1:Electrode budget trends for word holdout comparing
topk, diversity, and random selection, showing accuracy and
streaming cost.

=== PAGE 4 ===
Table 5:Spatial modeling at full channels across protocols
(protocol one word holdout, protocol two instance holdout, pro-
tocol three cross participant).
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
5. Discussion180
Across protocols, layout-aware front ends do not consistently181
outperform the vector baseline and often increase streaming182
cost; the patchpool grid reduces but does not eliminate the gap.183
Cross-participant transfer remains the main bottleneck. Source184
aggregation and low-shot adaptation help in some settings, but185
outcomes are mixed, and simple similarity indicators do not186
yield a single rule for when multi-source helps. Design implica-187
tion: when low latency is the priority, the vector or row/col front188
ends are safer choices; when robustness to electrode dropout189
or spatial priors is desired, grid-based options require careful190
tuning and validation. These takeaways depend on the audited191
datasets, split protocols, and evaluation pipeline, and they may192
not transfer to other sensors, labeling schemes, or participant193
populations.194
6. Artifacts and Auditability195
This repository uses a strict paper registry that pins every ev-196
idence file by checksum and rejects unsupported manuscript197
blocks. The split manifests, aggregated metrics, compact ta-198
bles, statistical summaries, and analysis reports referenced in199
this paper are stored as deterministic artifacts, enabling audit200
and reproduction within our repository environment. A supple-201
mentary archive includes the compact statistical summary table202
for reviewers.203
7. Ethics and Disclosure204
We report results only for audited artifacts and do not claim205
broader demographic coverage. The datasets and splits used in206
this study are derived from participant recordings, and we focus207
on methodological clarity and artifact traceability rather than208
deployment claims. We used generative AI tools for language209
polishing and verified technical claims against audited artifacts.210

=== PAGE 5 ===
8. References211
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and212
J. Brumberg, “Silent speech interfaces,” 2010.213
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction214
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and215
Computer Engineering. Springer, 2017.216
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,217
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces218
for speech restoration: A review,” 2020.219
[4] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,220
“New developments in electropalatography: A state-of-the-art re-221
port,” 1989.222
[5] W. J. Hardcastle, “Electropalatography in phonetic research and223
in speech training,” 1990.224
[6] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and225
S. Lee, “Biosignal sensors and deep learning-based speech recog-226
nition: A review,” 2021.227
[7] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,228
“Visualisation and analysis of speech production with elec-229
tropalatography,” 2019.230
[8] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and231
evaluation of korean electropalatography (k-epg),” 2021.232
[9] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-233
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-234
the-ear silently spelled expressions,” 2024.235
[10] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fagan, R. Moore,236
and P. Green, “Isolated word recognition of silent speech237
using magnetic implants and sensors,” 2010. [Online]. Available:238
https://pubmed.ncbi.nlm.nih.gov/20863739/239
[11] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-240
nectionist temporal classification,” 2006.241
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and242
M. Stone, “Development of a silent speech interface driven by243
ultrasound and optical images of the tongue and lips,” 2010.244
[13] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,245
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-246
wards mobile, hands-free, silent speech text entry using elec-247
tropalatography,” 2022.248
[14] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-249
tion of electropalatographic data using latent variable models,”250
1998.251
[15] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction252
methods and their implications for studies of lingual coarticula-253
tion,” 1991.254
[16] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-255
surement of face and palate by structured light,” 1993.256
[17] A. Toutios and K. Margaritis, “Learning electropalatograms from257
acoustics,” 2006.258
[18] ——, “On the acoustic-to-electropalatographic mapping,” 2006.259
[19] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,260
and Q. V . Le, “Specaugment: A simple data augmentation method261
for automatic speech recognition,” 2019.262
