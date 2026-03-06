# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 20854,
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
    "sha256": "448a8a16496cf7e8783e664e3d0ffa192a0cdf470d863c5de995024ab4a6d36d",
    "sha8": "448a8a16",
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
    "sha256": "2ade2f99901f3d1c026fbe7711eae4226dd062a580f6a5ed6c9cda7e8be298ec",
    "sha8": "2ade2f99"
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
      "extracted_chars": 20854,
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
      "sha256": "448a8a16496cf7e8783e664e3d0ffa192a0cdf470d863c5de995024ab4a6d36d",
      "sha8": "448a8a16",
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
      "sha256": "2ade2f99901f3d1c026fbe7711eae4226dd062a580f6a5ed6c9cda7e8be298ec",
      "sha8": "2ade2f99"
    }
  },
  "run_id": "INTSP2026_STATIC_448a8a16_2ade2f99"
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
We evaluate three primary protocols. The word holdout75
protocol uses disjoint vocabularies across train, test, and a com-76
petition partition. The instance holdout protocol tests held out77
instances of seen words. It separates train and competition vo-78
cabularies while keeping the test vocabulary within their union.79
The cross participant protocol trains on a source participant80
and tests on a target participant under a shared vocabulary con-81
straint. We also define a paired source cross participant vari-82
ant and a low shot adaptation variant to isolate source aggrega-83
tion and limited supervision effects under the same audit rules.84
When a target participant has limited within word repetition,85
we configure the cross participant split generators to allow sin-86
gle instance target words. We keep the source side constraints87
unchanged. All split archives used in this study are enumerated88
with sizes and checksums in manifest artifacts.89
All split archives are generated deterministically from au-90
dited exports with fixed seeds. Each train, test, and competition91
partition is stored as an immutable archive with a checksum in92
the manifests to enable reuse and later verification. The man-93
ifests show the word-holdout protocol uses all four participant94
datasets. They show the instance-holdout protocol uses three95

=== PAGE 2 ===
participant datasets. They also show the fourth participant is96
target-only (not used as a source) in the cross-participant splits.97
The audited label histogram for the fourth participant is dom-98
inated by single-instance labels, so we restrict that participant99
to target-only use in cross-participant evaluation. This separa-100
tion explains why the dataset summary includes all participant101
datasets even when a protocol uses only a subset.102
We normalize labels by uppercasing and filtering to alpha-103
bet characters, then represent each label as a space separated104
character sequence for CTC training and greedy decoding. We105
apply this step consistently during split construction and dataset106
preparation to avoid vocabulary drift.107
We keep the label normalization step consistent across all108
splits and dataset preparation steps. This aligns the decoder109
vocabulary with the audited labels and reduces drift between110
training and artifacts used to evaluate.111
We report character error rate from greedy decoding and112
streaming speed using real time factor. We define real time fac-113
tor as total inference time divided by total input duration. For114
character-level decoding we also report lexicon projection error115
rates using a training lexicon and a full lexicon.116
Greedy decoding reports unconstrained character se-117
quences. Lexicon projection maps outputs to finite word sets118
derived from the training vocabulary or the full audited lexicon.119
This allows us to separate decoding quality from lexicon con-120
straints. We compute real time factor by dividing inference time121
by input duration under the same test harness. Tables summa-122
rize results over four split seeds as mean and standard devia-123
tion. We compute two sided t distribution confidence intervals124
for the primary accuracy metric and paired t tests with Holm125
correction; the compact statistical summary table is provided in126
the supplementary archive.127
3. Models128
Our baseline model encodes each frame as a vector of palate129
channels and applies a uni-directional recurrent decoder trained130
with a CTC objective. We compare two layout aware front ends.131
One is a row and column pooling front end that aggregates a132
proxy grid into one dimensional summaries. The other is a grid133
front end that reconstructs a proxy grid and applies a convolu-134
tional spatial encoder. For the grid model we optionally enable a135
spatial augmentation that drops and shifts contiguous electrode136
blocks. [11, 19]137
The proxy grid is constructed from the palate channel lay-138
out. It supports row and column pooling or convolutional fea-139
ture extraction. We use a fixed layout file for the mapping so140
that row and column indices are consistent across splits. We141
augment spatially by perturbing contiguous electrode blocks to142
emulate missing contacts and minor spatial shifts.143
We fix core training hyperparameters across runs and record144
how we configure them in the metrics registry for auditability.145
4. Results146
We report greedy decoding error, lexicon-projected error, and147
streaming cost under a shared evaluation harness for all proto-148
cols. The fourth participant is target-only in cross-participant149
evaluation due to single-instance label dominance. All metrics150
are derived from the same audited registry.151
We summarize baseline performance across the three eval-152
uation protocols.153
Baseline error is lowest for word and instance holdout and154
highest for cross participant transfer, consistent with the proto-155
Table 1:Baseline recap across evaluation protocols; the proto-
col column denotes word holdout, instance holdout, and cross
participant transfer, n counts split aggregates, CER is character
error rate, and lex is lexicon projected error rate.
protocol n cer lex
P1 4 0.180±0.084 0.102±0.068
P2 3 0.145±0.063 0.075±0.048
P3 6 0.691±0.133 0.644±0.060
Table 2:Spatial modeling at full channels across protocols
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
col difficulty ordering.156
We compare vector, row/col, and grid-based front ends at157
full channels across protocols.158
Row and column pooling tends to track the vector baseline159
more closely, while grid variants increase error and streaming160
cost across protocols.161
We evaluate cross-participant transfer with the fourth par-162
ticipant as target under single-source and paired-source settings.163
Paired-source transfer is often lower error than single-164
source transfer, but direction-level outcomes are mixed.165
We evaluate low-shot adaptation by varying the number of166
training instances per word for a new participant.167
Two-shot generally improves over one-shot, while layout-168
aware variants remain mixed relative to the vector baseline.169
We evaluate paired-source cross-participant transfer under170
the same target and protocol constraints.171
Paired-source transfer is mixed across targets and front172
ends. 173
We evaluate reduced-channel subsets across protocols using174
within-participant, transfer, and random selection strategies.175
Within-participant selection tends to track the full-channel176
baseline more closely than transfer or random subsets, though177
patterns remain mixed across protocols.178
We visualize how accuracy and streaming cost vary with179
electrode budget for the word holdout protocol.180
Accuracy improves as electrode budget increases, random181
selection remains weaker than within participant selection, and182
streaming cost varies less than error.183

=== PAGE 3 ===
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
Table 4:Low shot adaptation results for a new participant;
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
Table 6:Electrode reduction methods across protocols (proto-
col one word holdout, protocol two instance holdout, protocol
three cross participant).
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
5. Discussion184
Across protocols, layout-aware front ends do not consistently185
outperform the vector baseline and often increase streaming186
cost; the patchpool grid reduces but does not eliminate the gap.187
The pattern suggests spatial structure alone is insufficient with-188
out careful capacity and regularization choices. Row and col-189
umn pooling offers the most stable compromise within our au-190
dited runs. Cross-participant transfer remains the main bottle-191
neck. Source aggregation and low-shot adaptation help in some192
settings, but outcomes are mixed, and simple similarity indica-193
tors do not yield a single rule for when multi-source helps. This194
variability argues for protocol-specific validation rather than as-195
suming transfer will generalize. As a result, cross-participant196
evaluation remains the most conservative stress test for new par-197
ticipants. Design implication: when low latency is the priority,198
the vector or row/col front ends are safer choices; when robust-199
ness to electrode dropout or spatial priors is desired, grid-based200
options require careful tuning and validation. In practice, the201
safest workflow is to benchmark both families under the au-202
dited split definitions before committing to a deployment path.203
If deployment constraints allow, a small validation sweep across204
the audited protocols provides a more reliable basis than se-205
lecting by architecture alone. These takeaways depend on the206
audited datasets, split protocols, and evaluation pipeline, and207
they may not transfer to other sensors, labeling schemes, or par-208
ticipant populations. Broader participant coverage and longer-209
term recording stability remain outside the current evidence en-210
velope. We do not claim transfer beyond the audited protocol211
definitions.212
6. Artifacts and Auditability213
This repository uses a strict paper registry that pins every ev-214
idence file by checksum and rejects unsupported manuscript215
blocks. The split manifests, aggregated metrics, compact ta-216
bles, statistical summaries, and analysis reports referenced in217
this paper are stored as deterministic artifacts, enabling audit218
and reproduction within our repository environment. A supple-219
mentary archive includes the compact statistical summary table220
for reviewers.221
7. Ethics and Disclosure222
We report results only for audited artifacts and do not claim223
broader demographic coverage. The datasets and splits used in224
this study are derived from participant recordings, and we focus225
on methodological clarity and artifact traceability rather than226
deployment claims. We used generative AI tools for language227
polishing and verified technical claims against audited artifacts.228

=== PAGE 5 ===
8. References229
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and230
J. Brumberg, “Silent speech interfaces,” 2010.231
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction232
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and233
Computer Engineering. Springer, 2017.234
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,235
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces236
for speech restoration: A review,” 2020.237
[4] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,238
“New developments in electropalatography: A state-of-the-art re-239
port,” 1989.240
[5] W. J. Hardcastle, “Electropalatography in phonetic research and241
in speech training,” 1990.242
[6] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and243
S. Lee, “Biosignal sensors and deep learning-based speech recog-244
nition: A review,” 2021.245
[7] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,246
“Visualisation and analysis of speech production with elec-247
tropalatography,” 2019.248
[8] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and249
evaluation of korean electropalatography (k-epg),” 2021.250
[9] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-251
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-252
the-ear silently spelled expressions,” 2024.253
[10] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fagan, R. Moore,254
and P. Green, “Isolated word recognition of silent speech255
using magnetic implants and sensors,” 2010. [Online]. Available:256
https://pubmed.ncbi.nlm.nih.gov/20863739/257
[11] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-258
nectionist temporal classification,” 2006.259
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and260
M. Stone, “Development of a silent speech interface driven by261
ultrasound and optical images of the tongue and lips,” 2010.262
[13] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,263
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-264
wards mobile, hands-free, silent speech text entry using elec-265
tropalatography,” 2022.266
[14] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-267
tion of electropalatographic data using latent variable models,”268
1998.269
[15] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction270
methods and their implications for studies of lingual coarticula-271
tion,” 1991.272
[16] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-273
surement of face and palate by structured light,” 1993.274
[17] A. Toutios and K. Margaritis, “Learning electropalatograms from275
acoustics,” 2006.276
[18] ——, “On the acoustic-to-electropalatographic mapping,” 2006.277
[19] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,278
and Q. V . Le, “Specaugment: A simple data augmentation method279
for automatic speech recognition,” 2019.280
