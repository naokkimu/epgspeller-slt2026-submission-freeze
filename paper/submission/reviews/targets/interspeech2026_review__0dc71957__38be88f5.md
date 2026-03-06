# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 19685,
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
    "sha256": "0dc7195735d9c8be72705855c0061737c89629da572b2320bb6d1a6e1dca9617",
    "sha8": "0dc71957",
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
    "sha256": "38be88f56321947a98acdde8f54f322f6d707173a8a946e2097795434e107091",
    "sha8": "38be88f5"
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
          "disclosure": 18334,
          "printbibliography": null,
          "references_heading": 18574,
          "refs": 18515,
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
      "extracted_chars": 19685,
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
      "sha256": "0dc7195735d9c8be72705855c0061737c89629da572b2320bb6d1a6e1dca9617",
      "sha8": "0dc71957",
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
      "sha256": "38be88f56321947a98acdde8f54f322f6d707173a8a946e2097795434e107091",
      "sha8": "38be88f5"
    }
  },
  "run_id": "INTSP2026_STATIC_0dc71957_38be88f5"
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
We compute two sided t distribution confidence intervals for the127
primary accuracy metric and paired t tests with Holm correc-128
tion; the compact statistical summary is provided as a pinned129
artifact.130
3. Models131
Our baseline model encodes each frame as a vector of palate132
channels and applies a uni-directional recurrent decoder trained133
with a CTC objective. We compare two layout aware front ends.134
One is a row and column pooling front end that aggregates a135
proxy grid into one dimensional summaries. The other is a grid136
front end that reconstructs a proxy grid and applies a convolu-137
tional spatial encoder. For the grid model we optionally enable a138
spatial augmentation that drops and shifts contiguous electrode139
blocks. [11, 19]140
The proxy grid is constructed from the palate channel lay-141
out. It supports row and column pooling or convolutional fea-142
ture extraction. We use a fixed layout file for the mapping so143
that row and column indices are consistent across splits. We144
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
augment spatially by perturbing contiguous electrode blocks to145
emulate missing contacts and minor spatial shifts.146
We fix core training hyperparameters across runs and record147
how we configure them in the metrics registry for auditability.148
4. Results149
We report greedy decoding error, lexicon-projected error, and150
streaming cost under a shared evaluation harness for all proto-151
cols. All metrics are derived from the same audited registry.152
We evaluate cross-participant transfer with the fourth par-153
ticipant as target under single-source and paired-source settings.154
Paired-source transfer is often lower error than single-155
source transfer, but direction-level outcomes are mixed.156
We compare vector, row/col, and grid-based front ends at157
full channels across protocols.158
Row/col tracks the vector baseline more closely than grid159
variants. Grid variants tend to worsen accuracy and increase160
latency, and patchpool reduces but does not remove this gap.161
We evaluate reduced-channel subsets using within-162
participant, transfer, and random selection strategies.163
Within-participant selection is similar to the vector base-164
line, while transfer and random subsets are generally lower and165
mixed across protocols.166
We evaluate paired-source cross-participant transfer under167
the same target and protocol constraints.168
Paired-source transfer is mixed across targets and front169
ends. 170
We evaluate low-shot adaptation by varying the number of171
training instances per word for a new participant.172
Two-shot generally improves over one-shot, while layout-173
aware variants remain mixed relative to the vector baseline.174
5. Discussion175
Across protocols, layout-aware front ends do not consistently176
outperform the vector baseline and often increase streaming177
cost; the patchpool grid reduces but does not eliminate the gap.178
Cross-participant transfer remains the main bottleneck. Source179
aggregation and low-shot adaptation help in some settings, but180
outcomes are mixed, and simple similarity indicators do not181
yield a single rule for when multi-source helps. Design implica-182
tion: when low latency is the priority, the vector or row/col front183
ends are safer choices; when robustness to electrode dropout184
or spatial priors is desired, grid-based options require careful185
tuning and validation. These takeaways depend on the audited186

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
datasets, split protocols, and evaluation pipeline, and they may187
not transfer to other sensors, labeling schemes, or participant188
populations.189
6. Artifacts and Auditability190
This repository uses a strict paper registry that pins every ev-191
idence file by checksum and rejects unsupported manuscript192
blocks. The split manifests, aggregated metrics, compact ta-193
bles, statistical summaries, and analysis reports referenced in194
this paper are stored as deterministic artifacts, enabling audit195
and reproduction within our repository environment. A supple-196
mentary archive includes the compact statistical summary table197
for reviewers.198
7. Ethics and Disclosure199
We report results only for audited artifacts and do not claim200
broader demographic coverage. The datasets and splits used in201
this study are derived from participant recordings, and we focus202
on methodological clarity and artifact traceability rather than203
deployment claims.204
8. Generative AI Use Disclosure205
We used generative AI tools for language polishing and format-206
ting support, and we verified technical claims against audited207
artifacts.208
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
9. References209
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert, and210
J. Brumberg, “Silent speech interfaces,” 2010.211
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction212
to Silent Speech Interfaces, ser. SpringerBriefs in Electrical and213
Computer Engineering. Springer, 2017.214
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,215
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces216
for speech restoration: A review,” 2020.217
[4] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and G. Calder,218
“New developments in electropalatography: A state-of-the-art re-219
port,” 1989.220
[5] W. J. Hardcastle, “Electropalatography in phonetic research and221
in speech training,” 1990.222
[6] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov, and223
S. Lee, “Biosignal sensors and deep learning-based speech recog-224
nition: A review,” 2021.225
[7] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-Aldasoro,226
“Visualisation and analysis of speech production with elec-227
tropalatography,” 2019.228
[8] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design and229
evaluation of korean electropalatography (k-epg),” 2021.230
[9] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang, K. Christof-231
ferson, and A. Mariakakis, “Rehearsse: Recognizing hidden-in-232
the-ear silently spelled expressions,” 2024.233
[10] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fagan, R. Moore,234
and P. Green, “Isolated word recognition of silent speech235
using magnetic implants and sensors,” 2010. [Online]. Available:236
https://pubmed.ncbi.nlm.nih.gov/20863739/237
[11] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-238
nectionist temporal classification,” 2006.239
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus, and240
M. Stone, “Development of a silent speech interface driven by241
ultrasound and optical images of the tongue and lips,” 2010.242
[13] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao, A. Bedri,243
Z. Su, A. Olwal, J. Rekimoto, and T. Starner, “Silentspeller: To-244
wards mobile, hands-free, silent speech text entry using elec-245
tropalatography,” 2022.246
[14] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality reduc-247
tion of electropalatographic data using latent variable models,”248
1998.249
[15] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data reduction250
methods and their implications for studies of lingual coarticula-251
tion,” 1991.252
[16] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth mea-253
surement of face and palate by structured light,” 1993.254
[17] A. Toutios and K. Margaritis, “Learning electropalatograms from255
acoustics,” 2006. 256
[18] ——, “On the acoustic-to-electropalatographic mapping,” 2006.257
[19] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph, E. D. Cubuk,258
and Q. V . Le, “Specaugment: A simple data augmentation method259
for automatic speech recognition,” 2019.260
