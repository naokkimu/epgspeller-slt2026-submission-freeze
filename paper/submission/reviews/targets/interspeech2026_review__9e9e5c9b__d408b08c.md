# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 28026,
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
    "sha256": "9e9e5c9b2e72569574989c490a2c147caa998e53496033a502bf7b49f16783bd",
    "sha8": "9e9e5c9b",
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
    "sha256": "d408b08ca0de67cb0941db88fa9bcd670304787da95526b708e60c5e5fc39c29",
    "sha8": "d408b08c"
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
        "positions": {
          "ack": null,
          "disclosure": 29438,
          "printbibliography": null,
          "references_heading": 29664,
          "refs": 29605,
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
      "extracted_chars": 28026,
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
      "sha256": "9e9e5c9b2e72569574989c490a2c147caa998e53496033a502bf7b49f16783bd",
      "sha8": "9e9e5c9b",
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
      "sha256": "d408b08ca0de67cb0941db88fa9bcd670304787da95526b708e60c5e5fc39c29",
      "sha8": "d408b08c"
    }
  },
  "run_id": "INTSP2026_STATIC_9e9e5c9b_d408b08c"
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
Claim: Audited protocol design enables comparable evalu-47
ation of EPG silent spelling and shows that layout-aware front48
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
ends do not consistently outperform a vector baseline under the49
tested protocols. 50
• We define protocols to evaluate word identity generalization51
and participant transfer, and we provide split archives with52
checksums. 53
• We run multi-participant experiments with character-level54
decoding and lexicon projection, tracked by a strict evidence55
registry. 56
• We compare a vector baseline with two layout aware front57
ends, and we report both accuracy and streaming speed met-58
rics. 59
• We provide deterministic scripts that export compact tables60
and manifests used by this manuscript.61
2. Data and Protocols62
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
We evaluate three primary protocols. The word holdout81
protocol uses disjoint vocabularies across train, test, and a com-82

=== PAGE 2 ===
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
participant datasets. They also show the fourth participant is102
target-only (not used as a source) in the cross-participant splits.103
This separation explains why the dataset summary includes all104
participant datasets even when a protocol uses only a subset.105
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
character-level decoding we also report lexicon projection error118
rates using a training lexicon and a full lexicon.119
Greedy decoding reports unconstrained character se-120
quences. Lexicon projection maps outputs to finite word sets121
derived from the training vocabulary or the full audited lexicon.122
This allows us to separate decoding quality from lexicon con-123
straints. We compute real time factor by dividing inference time124
by input duration under the same test harness. Tables summa-125
rize results over four split seeds as mean and standard deviation.126
We also report two sided t distribution confidence intervals for127
the mean, and paired t tests with Holm correction within each128
table and metric family.129
3. Models130
Our baseline model encodes each frame as a vector of palate131
channels and applies a uni-directional recurrent decoder trained132
with a CTC objective. We compare two layout aware front ends.133
One is a row and column pooling front end that aggregates a134
proxy grid into one dimensional summaries. The other is a grid135
front end that reconstructs a proxy grid and applies a convolu-136
tional spatial encoder. For the grid model we optionally enable a137
spatial augmentation that drops and shifts contiguous electrode138
blocks. [11, 19]139
The proxy grid is constructed from the palate channel lay-140
out. It supports row and column pooling or convolutional fea-141
ture extraction. We use a fixed layout file for the mapping so142
that row and column indices are consistent across splits. We143
augment spatially by perturbing contiguous electrode blocks to144
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
emulate missing contacts and minor spatial shifts.145
We fix core training hyperparameters across runs and record146
how we configure them in the metrics registry for auditability.147
4. Results148
We report greedy decoding error, lexicon-projected error, and149
streaming cost under a shared evaluation harness for all proto-150
cols. All metrics are derived from the same audited registry.151
We evaluate cross-participant transfer with the fourth par-152
ticipant as target under single-source and paired-source settings.153
Paired-source transfer is often lower error than single-154
source transfer, but direction-level outcomes are mixed.155
We compare vector, row/col, and grid-based front ends at156
full channels across protocols.157
Row/col tracks the vector baseline more closely than grid158
variants. Grid variants tend to worsen accuracy and increase159
latency, and patchpool reduces but does not remove this gap.160
We evaluate reduced-channel subsets using within-161
participant, transfer, and random selection strategies.162
Within-participant selection is similar to the vector base-163
line, while transfer and random subsets are generally lower and164
mixed across protocols.165
We evaluate paired-source cross-participant transfer under166
the same target and protocol constraints.167
Paired-source transfer is mixed across targets and front168
ends. 169
We evaluate low-shot adaptation by varying the number of170
training instances per word for a new participant.171
Two-shot generally improves over one-shot, while layout-172
aware variants remain mixed relative to the vector baseline.173
A compact statistics table summarizes confidence intervals174
and paired tests for the main comparisons.175
The interval estimates quantify uncertainty around the176
means, and the Holm adjusted paired tests distinguish clearer177
differences from comparisons that remain inconclusive under178
this analysis. 179
5. Discussion180
Across protocols, layout-aware front ends do not consistently181
outperform the vector baseline and often increase streaming182
cost; the patchpool grid reduces but does not eliminate the gap.183
Cross-participant transfer remains the main bottleneck. Source184
aggregation and low-shot adaptation help in some settings, but185
outcomes are mixed, and simple similarity indicators do not186

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
blocks. The split manifests, aggregated metrics, compact tables,198
and analysis summaries referenced in this paper are stored as199
deterministic artifacts, enabling audit and reproduction within200
our repository environment. The same artifacts are reused to201
build the manuscript tables and to support verification in the202
audit views.203
7. Ethics and Disclosure204
We report results only for audited artifacts and do not claim205
broader demographic coverage. The datasets and splits used in206
this study are derived from participant recordings, and we focus207
on methodological clarity and artifact traceability rather than208
deployment claims.209
8. Generative AI Use Disclosure210
We used generative AI tools for language polishing and format-211
ting support, and we verified technical claims against audited212
artifacts.213
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
9. References214
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and215
J. Brumberg, “Silent speech interfaces,” 2010.216
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction217
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and218
Computer Engineering. Springer, 2017.219
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,220
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces221
for speech restoration: A review,” 2020.222
[4] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,223
“New developments in electropalatography: A state-of-the-art re-224
port,” 1989. 225
[5] W. J. Hardcastle, “Electropalatography in phonetic research and226
in speech training,” 1990.227
[6] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and228
S. Lee, “Biosignal sensors and deep learning-based speech recog-229
nition: A review,” 2021.230
[7] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,231
“Visualisation and analysis of speech production with elec-232
tropalatography,” 2019.233

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
[8] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and234
evaluation of korean electropalatography (k-epg),” 2021.235
[9] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-236
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-237
the-ear silently spelled expressions,” 2024.238
[10] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fagan, R. Moore,239
and P. Green, “Isolated word recognition of silent speech240
using magnetic implants and sensors,” 2010. [Online]. Available:241
https://pubmed.ncbi.nlm.nih.gov/20863739/242
[11] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-243
nectionist temporal classification,” 2006.244
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and245
M. Stone, “Development of a silent speech interface driven by246
ultrasound and optical images of the tongue and lips,” 2010.247
[13] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,248
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-249
wards mobile, hands-free, silent speech text entry using elec-250
tropalatography,” 2022.251
[14] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-252
tion of electropalatographic data using latent variable models,”253
1998.254
[15] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction255
methods and their implications for studies of lingual coarticula-256
tion,” 1991.257
[16] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-258
surement of face and palate by structured light,” 1993.259
[17] A. Toutios and K. Margaritis, “Learning electropalatograms from260
acoustics,” 2006.261
[18] ——, “On the acoustic-to-electropalatographic mapping,” 2006.262
[19] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,263
and Q. V . Le, “Specaugment: A simple data augmentation method264
for automatic speech recognition,” 2019.265
Table 7:Statistical summary for the main comparisons;
columns report mean, standard deviation, t distribution confi-
dence interval bounds, and Holm adjusted paired test values
for each metric.
table group variant metric n mean std ci low ci high p adj
spatial all P1 vec cer 4 0.179598 0.084422 0.045265 0.313932
spatial all P1 vec rtf 4 0.000628 0.000232 0.000259 0.000997
spatial all P1 rowcol cer 4 0.201636 0.088598 0.060657 0.342615 0.098616
spatial all P1 rowcol rtf 4 0.002401 0.001106 0.000642 0.004160 0.086270
spatial all P1 grid cer 4 0.306225 0.149090 0.068989 0.543461 1.000000
spatial all P1 grid rtf 4 0.003564 0.001540 0.001114 0.006015 0.086270
spatial all P1 grid aug cer 4 0.309357 0.144027 0.080178 0.538536 0.768626
spatial all P1 grid aug rtf 4 0.003414 0.001054 0.001736 0.005091 0.047864
spatial all P1 patch cer 4 0.298153 0.066564 0.192235 0.404070 0.098616
spatial all P1 patch rtf 4 0.003795 0.001663 0.001149 0.006442 0.086270
spatial all P1 patch aug cer 4 0.298759 0.089136 0.156924 0.440594 0.536181
spatial all P1 patch aug rtf 4 0.003876 0.001709 0.001157 0.006595 0.086270
spatial all P2 vec cer 3 0.145064 0.062741 -0.010792 0.300920
spatial all P2 vec rtf 3 0.000107 0.000010 0.000083 0.000132
spatial all P2 rowcol cer 3 0.161288 0.078306 -0.033234 0.355810 1.000000
spatial all P2 rowcol rtf 3 0.000244 0.000037 0.000152 0.000337 0.066674
spatial all P2 grid cer 3 0.289352 0.212569 -0.238698 0.817402 1.000000
spatial all P2 grid rtf 3 0.000389 0.000047 0.000273 0.000505 0.045645
spatial all P2 grid aug cer 3 0.313884 0.243601 -0.291253 0.919022 1.000000
spatial all P2 grid aug rtf 3 0.000392 0.000045 0.000280 0.000503 0.045645
spatial all P2 patch cer 3 0.338431 0.232386 -0.238849 0.915711 1.000000
spatial all P2 patch rtf 3 0.000658 0.000088 0.000439 0.000876 0.046744
spatial all P2 patch aug cer 3 0.301369 0.162566 -0.102467 0.705206 1.000000
spatial all P2 patch aug rtf 3 0.000621 0.000038 0.000526 0.000716 0.010364
spatial all P3 vec cer 6 0.690876 0.133159 0.551134 0.830618
spatial all P3 vec rtf 6 0.000110 0.000014 0.000095 0.000125
spatial all P3 rowcol cer 6 0.682754 0.150993 0.524297 0.841212 1.000000
spatial all P3 rowcol rtf 6 0.000243 0.000033 0.000208 0.000278 0.000185
spatial all P3 grid cer 6 0.750726 0.089670 0.656624 0.844829 1.000000
spatial all P3 grid rtf 6 0.000393 0.000042 0.000349 0.000437 0.000041
spatial all P3 grid aug cer 6 0.755864 0.092047 0.659267 0.852462 1.000000
spatial all P3 grid aug rtf 6 0.000397 0.000046 0.000348 0.000445 0.000063
spatial all P3 patch cer 6 0.689754 0.110308 0.573993 0.805515 1.000000
spatial all P3 patch rtf 6 0.000631 0.000070 0.000558 0.000705 0.000063
spatial all P3 patch aug cer 6 0.699214 0.130453 0.562313 0.836116 1.000000
spatial all P3 patch aug rtf 6 0.000476 0.000079 0.000394 0.000559 0.000407
k64 all P1 topk cer 4 0.195201 0.082711 0.063589 0.326814
k64 all P1 topk rtf 4 0.000657 0.000210 0.000323 0.000991
k64 all P1 fps2k cer 4 0.191243 0.078133 0.066916 0.315570 1.000000
k64 all P1 fps2k rtf 4 0.000619 0.000229 0.000255 0.000984 1.000000
k64 all P1 xfer cer 4 0.205250 0.095069 0.053973 0.356527 1.000000
k64 all P1 xfer rtf 4 0.000586 0.000218 0.000239 0.000933 0.270712
k64 all P1 rand cer 4 0.197984 0.079337 0.071742 0.324226 1.000000
k64 all P1 rand rtf 4 0.000665 0.000282 0.000215 0.001114 1.000000
k64 all P2 topk cer 3 0.154361 0.059097 0.007557 0.301165
k64 all P2 topk rtf 3 0.000110 0.000011 0.000083 0.000137
k64 all P2 fps2k cer 3 0.153890 0.061687 0.000652 0.307128 1.000000
k64 all P2 fps2k rtf 3 0.000110 0.000010 0.000086 0.000134 1.000000
k64 all P2 xfer cer 3 0.158371 0.070931 -0.017831 0.334572 1.000000
k64 all P2 xfer rtf 3 0.000106 0.000009 0.000083 0.000128 0.616830
k64 all P2 rand cer 3 0.156604 0.066949 -0.009707 0.322915 1.000000
k64 all P2 rand rtf 3 0.000105 0.000011 0.000077 0.000132 0.012879
k64 all P3 topk cer 6 0.647323 0.130080 0.510812 0.783834
k64 all P3 topk rtf 6 0.000108 0.000009 0.000098 0.000118
k64 all P3 fps2k cer 6 0.656358 0.146547 0.502566 0.810150 1.000000
k64 all P3 fps2k rtf 6 0.000107 0.000010 0.000096 0.000117 1.000000
k64 all P3 xfer cer 6 0.656908 0.144089 0.505695 0.808120 1.000000
k64 all P3 xfer rtf 6 0.000109 0.000009 0.000100 0.000118 1.000000
k64 all P3 rand cer 6 0.644186 0.132838 0.504782 0.783591 1.000000
k64 all P3 rand rtf 6 0.000111 0.000010 0.000101 0.000121 0.949014
p3ms p23-¿p1 vec cer 4 0.473514 0.013627 0.451830 0.495198
p3ms p23-¿p1 vec rtf 4 0.000121 0.000017 0.000094 0.000148
p3ms p23-¿p1 rowcol cer 4 0.475860 0.013757 0.453969 0.497751 1.000000
p3ms p23-¿p1 rowcol rtf 4 0.000237 0.000007 0.000227 0.000248 0.000875
p3ms p23-¿p1 grid cer 4 0.601998 0.076465 0.480325 0.723671 0.335136
p3ms p23-¿p1 grid rtf 4 0.000389 0.000002 0.000385 0.000393 0.000305
p3ms p23-¿p1 grid aug cer 4 0.691091 0.164563 0.429234 0.952948 0.509728
p3ms p23-¿p1 grid aug rtf 4 0.000386 0.000007 0.000374 0.000397 0.000305
p3ms p13-¿p2 vec cer 4 0.520336 0.002870 0.515769 0.524903
p3ms p13-¿p2 vec rtf 4 0.000116 0.000002 0.000112 0.000120
p3ms p13-¿p2 rowcol cer 4 0.504160 0.011702 0.485540 0.522779 0.509728
p3ms p13-¿p2 rowcol rtf 4 0.000297 0.000024 0.000259 0.000336 0.000875
p3ms p13-¿p2 grid cer 4 0.510594 0.047368 0.435221 0.585968 1.000000
p3ms p13-¿p2 grid rtf 4 0.000435 0.000005 0.000428 0.000443 0.000007
p3ms p13-¿p2 grid aug cer 4 0.511412 0.016446 0.485242 0.537582 0.870281
p3ms p13-¿p2 grid aug rtf 4 0.000433 0.000006 0.000423 0.000442 0.000022
p3ms p12-¿p3 vec cer 4 0.838062 0.033612 0.784578 0.891545
p3ms p12-¿p3 vec rtf 4 0.000096 0.000002 0.000093 0.000099
p3ms p12-¿p3 rowcol cer 4 0.790280 0.032778 0.738123 0.842437 0.726887
p3ms p12-¿p3 rowcol rtf 4 0.000203 0.000004 0.000197 0.000210 0.000123
p3ms p12-¿p3 grid cer 4 0.736170 0.018227 0.707167 0.765174 0.107422
p3ms p12-¿p3 grid rtf 4 0.000343 0.000012 0.000324 0.000362 0.000205
p3ms p12-¿p3 grid aug cer 4 0.756115 0.019656 0.724838 0.787392 0.107422
p3ms p12-¿p3 grid aug rtf 4 0.000346 0.000009 0.000331 0.000360 0.000120
kshot p3 k1 vec cer 4 0.350280 0.059950 0.254886 0.445674
kshot p3 k1 vec rtf 4 0.000164 0.000009 0.000150 0.000177
kshot p3 k1 rowcol cer 4 0.334422 0.038622 0.272966 0.395877 0.241258
kshot p3 k1 rowcol rtf 4 0.000502 0.000022 0.000466 0.000537 0.000505
kshot p3 k1 grid cer 4 0.515275 0.050007 0.435703 0.594847 0.056663
kshot p3 k1 grid rtf 4 0.000712 0.000005 0.000704 0.000721 0.000002
kshot p3 k1 grid aug cer 4 0.610541 0.157183 0.360428 0.860654 0.152208
kshot p3 k1 grid aug rtf 4 0.001067 0.000637 0.000053 0.002080 0.067460
kshot p3 k2 vec cer 4 0.245802 0.008507 0.232266 0.259339
kshot p3 k2 vec rtf 4 0.000165 0.000002 0.000161 0.000168
kshot p3 k2 rowcol cer 4 0.278218 0.021655 0.243760 0.312677 0.130780
kshot p3 k2 rowcol rtf 4 0.000522 0.000007 0.000510 0.000533 0.000022
kshot p3 k2 grid cer 4 0.615555 0.132129 0.405309 0.825801 0.056663
kshot p3 k2 grid rtf 4 0.000769 0.000064 0.000667 0.000872 0.000685
kshot p3 k2 grid aug cer 4 0.688899 0.217916 0.342147 1.035651 0.102801
kshot p3 k2 grid aug rtf 4 0.000748 0.000038 0.000688 0.000808 0.000304
to4 P3:p1-¿p4 vec cer 4 0.665980 0.023669 0.628317 0.703643
to4 P3:p1-¿p4 vec lex 4 0.650824 0.026121 0.609260 0.692387
to4 P3:p2-¿p4 vec cer 4 0.809066 0.020709 0.776112 0.842019
to4 P3:p2-¿p4 vec lex 4 0.735943 0.021599 0.701575 0.770312
to4 P3:p3-¿p4 vec cer 4 0.583997 0.018010 0.555340 0.612655
to4 P3:p3-¿p4 vec lex 4 0.591077 0.028683 0.545436 0.636718
to4 P3:all-¿p4 vec cer 3 0.686348 0.113908 0.403384 0.969311
to4 P3:all-¿p4 vec lex 3 0.659281 0.072803 0.478430 0.840133
to4 P3MS:p12-¿p4 vec cer 4 0.654622 0.016130 0.628956 0.680287
to4 P3MS:p12-¿p4 vec lex 4 0.593178 0.016243 0.567332 0.619024
to4 P3MS:p13-¿p4 vec cer 4 0.536324 0.008931 0.522114 0.550535
to4 P3MS:p13-¿p4 vec lex 4 0.532695 0.008397 0.519334 0.546057
to4 P3MS:p23-¿p4 vec cer 4 0.554682 0.004553 0.547437 0.561927
to4 P3MS:p23-¿p4 vec lex 4 0.536573 0.011060 0.518974 0.554172
to4 P3MS:all-¿p4 vec cer 3 0.581876 0.063665 0.423724 0.740028
to4 P3MS:all-¿p4 vec lex 3 0.554149 0.033856 0.470047 0.638251
