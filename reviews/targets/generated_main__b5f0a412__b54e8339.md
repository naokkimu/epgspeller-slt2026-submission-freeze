# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 21206,
    "max_chars": 120000,
    "media_boxes": [
      {
        "height_pt": 792.0,
        "page": 1,
        "width_pt": 612.0
      },
      {
        "height_pt": 792.0,
        "page": 2,
        "width_pt": 612.0
      },
      {
        "height_pt": 792.0,
        "page": 3,
        "width_pt": 612.0
      },
      {
        "height_pt": 792.0,
        "page": 4,
        "width_pt": 612.0
      },
      {
        "height_pt": 792.0,
        "page": 5,
        "width_pt": 612.0
      },
      {
        "height_pt": 792.0,
        "page": 6,
        "width_pt": 612.0
      },
      {
        "height_pt": 792.0,
        "page": 7,
        "width_pt": 612.0
      }
    ],
    "page_count": 7,
    "path": "paper/manuscript/generated_main.pdf",
    "sha256": "b5f0a412fc2a25c461e438bbaffdd2296916a82d2a0dbf584e3006697f997a04",
    "sha8": "b5f0a412",
    "truncated": false
  },
  "rules": "/Users/naokkimu/.codex/skills/paperjson/assets/toolkit/references/interspeech2026_rules.yaml",
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
      "plain_characters": 878
    },
    "documentclass": {
      "class": "article",
      "found": true,
      "has_cameraready": false,
      "is_interspeech": false,
      "options": [
        "10pt",
        "twocolumn"
      ],
      "options_raw": "[10pt,twocolumn]"
    },
    "path": "paper/manuscript/generated_main.tex",
    "sha256": "b54e8339f49061100e5fce2ffba8cd8e49435b19fe7ef9961272439bab5ee316",
    "sha8": "b54e8339"
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
      "message": "abstract contains non-ASCII characters",
      "ok": false,
      "severity": "warn"
    },
    {
      "evidence": {
        "abstract_chars": 878,
        "max_characters": 1000
      },
      "id": "abstract_length",
      "message": "abstract_chars=878 <= max_characters=1000",
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
          "class": "article",
          "found": true,
          "has_cameraready": false,
          "is_interspeech": false,
          "options": [
            "10pt",
            "twocolumn"
          ],
          "options_raw": "[10pt,twocolumn]"
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
        "page_count": 7
      },
      "id": "page_limit",
      "message": "page_count=7 <= max_pages=6",
      "ok": false,
      "severity": "error"
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
      "extracted_chars": 21206,
      "max_chars": 120000,
      "media_boxes": [
        {
          "height_pt": 792.0,
          "page": 1,
          "width_pt": 612.0
        },
        {
          "height_pt": 792.0,
          "page": 2,
          "width_pt": 612.0
        },
        {
          "height_pt": 792.0,
          "page": 3,
          "width_pt": 612.0
        },
        {
          "height_pt": 792.0,
          "page": 4,
          "width_pt": 612.0
        },
        {
          "height_pt": 792.0,
          "page": 5,
          "width_pt": 612.0
        },
        {
          "height_pt": 792.0,
          "page": 6,
          "width_pt": 612.0
        },
        {
          "height_pt": 792.0,
          "page": 7,
          "width_pt": 612.0
        }
      ],
      "page_count": 7,
      "path": "paper/manuscript/generated_main.pdf",
      "sha256": "b5f0a412fc2a25c461e438bbaffdd2296916a82d2a0dbf584e3006697f997a04",
      "sha8": "b5f0a412",
      "truncated": false
    },
    "rules": "/Users/naokkimu/.codex/skills/paperjson/assets/toolkit/references/interspeech2026_rules.yaml",
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
        "plain_characters": 878
      },
      "documentclass": {
        "class": "article",
        "found": true,
        "has_cameraready": false,
        "is_interspeech": false,
        "options": [
          "10pt",
          "twocolumn"
        ],
        "options_raw": "[10pt,twocolumn]"
      },
      "path": "paper/manuscript/generated_main.tex",
      "sha256": "b54e8339f49061100e5fce2ffba8cd8e49435b19fe7ef9961272439bab5ee316",
      "sha8": "b54e8339"
    }
  },
  "run_id": "INTSP2026_STATIC_b5f0a412_b54e8339"
}
```

## TeX preamble (first 200 lines)

```tex
% Auto-generated from paper/paper.json (paper-json v1.0.0). Do not edit by hand.
% Note: this entry uses a portable LaTeX preamble (article class).
% If you want the official Interspeech kit styling, replace the documentclass/preamble accordingly.
\documentclass[10pt,twocolumn]{article}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{float}
\usepackage{graphicx}
\usepackage{microtype}
\usepackage{hyperref}
\usepackage{url}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}

\title{EPGSpeller: Lexicon-Free Silent Spelling Recognition}
\author{Anonymous}
\date{}

```

## PDF extracted text (page-separated, deterministic truncation)

=== PAGE 1 ===
EPGSpeller: Lexicon-Free Silent Spelling Recognition
Anonymous
Abstract
Protocol mixing still obscures progress in EPG silent
spelling when word holdout, seen-word instance hold-
out, and cross-participant transfer are reported to-
gether. We present EPGSpeller, an evidence-tracked
benchmark for lexicon-free character decoding with
deterministic split generation, checksum-pinned man-
ifests, and a shared metric harness. Across audited
runs, CER is 0.180±0.084 in P1 and 0.145±0.063
in P2, but rises to 0.691±0.133 in P3, identify-
ing cross-participant transfer as the dominant bot-
tleneck. At full channels, rowcol tracks vec more
closely than grid variants in most settings. For the
p4 target aggregate, paired-source transfer lowers
CER from 0.686±0.114 to 0.582±0.064 and LEX
from 0.659±0.073 to 0.554±0.034, while direction-
level gains remain mixed. These findings provide a
reproducible baseline within our audited datasets and
protocol definitions.
1 Introduction
Silent speech interfaces (SSI) infer linguistic intent
from non-acoustic signals, including articulatory sens-
ing and other biosignals. For silent spelling with elec-
tropalatography (EPG), a practical failure remains:
many evaluations mix word-identity holdout, repeated-
instance holdout, and cross-participant transfer, so
reported gains can reflect protocol differences rather
than decoder differences. [1, 2, 3, 4, 5, 6, 7, 8]
Recent systems such as SilentSpeller and Re-
HEarSSE show lexicon-scale character-level spelling
beyond small command sets. However, these lines
of work do not provide a unified, auditable protocol
stack that isolates each generalization regime under
a shared artifact trace. In parallel, prior EPG stud-
ies motivate structured representations and spatial
inductive bias, but their evaluation settings are het-
erogeneous across datasets and tasks. [ 9, 1, 10, 11, 12,
13, 14, 15, 16, 17, 18]
To address this gap, we introduce EPGSpeller, an
evidence-tracked evaluation framework for EPG silent
spelling. EPGSpeller fixes deterministic split gener-
ation, pinned split manifests, and a common metric
harness for greedy decoding, lexicon projection, and
streaming cost. It explicitly separates word hold-
out, instance holdout, and cross-participant transfer
so model comparisons remain protocol-specific and
reproducible. We validate EPGSpeller with four par-
ticipant datasets and compare a vector baseline with
row-column and grid-based front ends under matched
settings. We also evaluate electrode reduction and low-
shot adaptation under the same audit rules. Across
our audited runs, row-column pooling tracks the vec-
tor baseline more consistently than grid variants, while
cross-participant transfer remains the dominant bot-
tleneck. [9, 13, 16, 17, 18]
Within our audited datasets and protocol defini-
tions, protocol-level auditability is required for com-
parable benchmarking.
• We define deterministic protocol families that
isolate word-identity, instance-level, and cross-
participant generalization.
• We provide checksum-pinned split archives and
manifests so each reported result is reproducible
from audited artifacts.
• We benchmark vector, row-column, and grid front
ends under a shared evaluation harness with ac-
curacy and streaming metrics.
• We report electrode-reduction and low-shot anal-
yses under the same protocol constraints.
1

=== PAGE 2 ===
2 Data and Protocols
We use four participant electropalatography datasets
with word labels. Each sample is a variable length
binary contact matrix, and the raw exports are treated
as immutable evidence. We refer to participants with
anonymous labels in all tables and split archives. We
audit dataset statistics, label counts, and anomalies
before we construct any train and test splits. We
exclude a small set of all-zero samples via a pinned
index list.
The audit pipeline records raw file checksums. It
validates schema consistency. It summarizes label
counts, sequence length summaries, and per channel
activity statistics before any split construction. The
raw exports remain unchanged. We apply any exclu-
sions only through pinned index lists that are included
in the audit artifacts.
We evaluate three primary protocols. The word
holdout protocol uses disjoint vocabularies across
train, test, and a competition partition. The instance
holdout protocol tests held out instances of seen words.
It separates train and competition vocabularies while
keeping the test vocabulary within their union. The
cross participant protocol trains on a source partici-
pant and tests on a target participant under a shared
vocabulary constraint. We also define a paired source
cross participant variant and a low shot adaptation
variant to isolate source aggregation and limited su-
pervision effects under the same audit rules. When a
target participant has limited within word repetition,
we configure the cross participant split generators to
allow single instance target words. We keep the source
side constraints unchanged. All split archives used in
this study are enumerated with sizes and checksums
in manifest artifacts.
All split archives are generated deterministically
from audited exports with fixed seeds. Each train,
test, and competition partition is stored as an im-
mutable archive with a checksum in the manifests
to enable reuse and later verification. The manifests
show the word-holdout protocol uses all four partici-
pant datasets. They show the instance-holdout proto-
col uses three participant datasets. They also show
the fourth participant is target-only (not used as a
source) in the cross-participant splits. The audited la-
bel histogram for the fourth participant is dominated
by single-instance labels, so we restrict that partici-
pant to target-only use in cross-participant evaluation.
This separation explains why the dataset summary
includes all participant datasets even when a protocol
uses only a subset.
We normalize labels by uppercasing and filtering
to alphabet characters, then represent each label as a
space separated character sequence for CTC training
and greedy decoding. We apply this step consistently
during split construction and dataset preparation to
avoid vocabulary drift.
We keep the label normalization step consistent
across all splits and dataset preparation steps. This
aligns the decoder vocabulary with the audited labels
and reduces drift between training and artifacts used
to evaluate.
We report character error rate from greedy decoding
and streaming speed using real time factor. We define
real time factor as total inference time divided by
total input duration. For character-level decoding
we also report lexicon projection error rates using a
training lexicon and a full lexicon.
Greedy decoding reports unconstrained character
sequences. Lexicon projection maps outputs to finite
word sets derived from the training vocabulary or
the full audited lexicon. This allows us to separate
decoding quality from lexicon constraints. We com-
pute real time factor by dividing inference time by
input duration under the same test harness. Tables
summarize results over four split seeds as mean and
standard deviation. We compute two sided t distri-
bution confidence intervals for the primary accuracy
metric and paired t tests with Holm correction; the
compact statistical summary table is provided in the
supplementary archive.
3 Models
Our baseline model encodes each frame as a vector of
palate channels and applies a uni-directional recurrent
decoder trained with a CTC objective. We compare
two layout aware front ends. One is a row and col-
umn pooling front end that aggregates a proxy grid
into one dimensional summaries. The other is a grid
2

=== PAGE 3 ===
Table 1: Baseline recap across protocols; P1 means
word holdout, P2 means instance holdout, and P3
means cross-participant transfer. n is the number of
split-seed aggregates. CER is character error rate and
LEX is lexicon-projected error rate.
protocol n cer lex
P1 4 0.180±0.084 0.102±0.068
P2 3 0.145±0.063 0.075±0.048
P3 6 0.691±0.133 0.644±0.060
front end that reconstructs a proxy grid and applies a
convolutional spatial encoder. For the grid model we
optionally enable a spatial augmentation that drops
and shifts contiguous electrode blocks. [12, 19]
The proxy grid is constructed from the palate chan-
nel layout. It supports row and column pooling or
convolutional feature extraction. We use a fixed layout
file for the mapping so that row and column indices
are consistent across splits. We augment spatially
by perturbing contiguous electrode blocks to emulate
missing contacts and minor spatial shifts.
We fix core training hyperparameters across runs
and record how we configure them in the metrics
registry for auditability.
4 Results
We report greedy decoding error, lexicon-projected er-
ror, and streaming cost under a shared evaluation
harness for all protocols. The fourth participant
is target-only in cross-participant evaluation due to
single-instance label dominance. All metrics are de-
rived from the same audited registry.
Table tab:main summarizes baseline performance
across the three evaluation protocols.
Table tab:main shows a clear protocol ordering:
CER is 0.145 to 0.180 for within-participant protocols
(P2 and P1) and 0.691 for cross-participant P3, while
LEX rises from 0.075 to 0.102 up to 0.644. Transfer
difficulty, not within-participant decoding, drives the
largest residual error.
Table tab:spatial all compares vector, row/col, and
grid-based front ends at full channels across protocols.
Table 2: Spatial modeling at full channels across P1,
P2, and P3; P1 means word holdout, P2 means in-
stance holdout, and P3 means cross-participant trans-
fer. CER is character error rate and RTF is real time
factor.
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
From Table tab:spatial all, rowcol tracks vec across
protocols (P1: 0.20 vs 0.18, P2: 0.16 vs 0.15, P3: 0.68
vs 0.69 CER). Grid and grid aug are usually higher
in CER and RTF, and patch variants only partially
close this gap. The compact statistical summary in
supplementary material shows broad interval overlap,
so we treat these as directional trends rather than
universal winners.
Table tab:tofour evaluates cross-participant transfer
with participant p4 as target under single-source and
paired-source settings.
Table tab:tofour shows an aggregate gain for p4
target transfer: CER drops from 0.686±0.114 in P3
all-¿p4 to 0.582±0.064 in P3MS all-¿p4, and LEX
drops from 0.659±0.073 to 0.554±0.034. Direction
rows remain heterogeneous, so source-pair selection
stays condition dependent.
Table tab:kshot evaluates low-shot adaptation by
varying the number of training instances per word for
3

=== PAGE 4 ===
Table 3: Cross-participant transfer targeting par-
ticipant p4. Proto marks P3 single-source transfer
or P3MS paired-source transfer. Lvl marks direc-
tion rows or all-direction aggregates. Group encodes
source-to-target participant IDs p1 to p4. CER is
character error rate and LEX is lexicon-projected er-
ror rate.
proto lvl group cer lex
P3 dir p1-¿p4 0.666±0.024 0.651±0.026
P3 dir p2-¿p4 0.809±0.021 0.736±0.022
P3 dir p3-¿p4 0.584±0.018 0.591±0.029
P3 all all-¿p4 0.686±0.114 0.659±0.073
P3MS dir p12-¿p4 0.655±0.016 0.593±0.016
P3MS dir p13-¿p4 0.536±0.009 0.533±0.008
P3MS dir p23-¿p4 0.555±0.005 0.537±0.011
P3MS all all-¿p4 0.582±0.064 0.554±0.034
a new participant.
From Table tab:kshot, increasing from k1 to k2
improves vec (0.350-¿0.246) and rowcol (0.334-¿0.278),
but worsens grid (0.515-¿0.616) and grid aug (0.611-
¿0.689). Low-shot gain is architecture dependent, not
automatic.
Table tab:k64 all evaluates reduced-channel subsets
across protocols using within-participant, transfer,
and random selection strategies.
Table 4: Low-shot adaptation for participant p3 with
k1 or k2 training instances per word. vec is vector
baseline, rowcol is row-column pooling, grid is a con-
volutional grid encoder, and grid aug adds spatial
augmentation. CER is character error rate and RTF
is real time factor.
group variant cer rtf
p3 k1 vec 0.350±0.060 0.0002±0.0000
p3 k1 rowcol 0.334±0.039 0.0005±0.0000
p3 k1 grid 0.515±0.050 0.0007±0.0000
p3 k1 grid aug 0.611±0.157 0.0011±0.0006
p3 k2 vec 0.246±0.009 0.0002±0.0000
p3 k2 rowcol 0.278±0.022 0.0005±0.0000
p3 k2 grid 0.616±0.132 0.0008±0.0001
p3 k2 grid aug 0.689±0.218 0.0007±0.0000
Table 5: Electrode-reduction methods at K=64 across
P1, P2, and P3; P1 means word holdout, P2 means in-
stance holdout, and P3 means cross-participant trans-
fer. topk and fps2k are within-participant selections,
xfer transfers a source ranking, and rand is a fixed
random subset. CER is character error rate and RTF
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
Table tab:k64 all shows small method deltas at
K=64: P1 CER ranges 0.191-0.205, P2 ranges 0.154-
0.158, and P3 ranges 0.644-0.657. Because these
ranges overlap strongly, we avoid a universal ranking
among topk, fps2k, xfer, and rand.
Figure fig:kcurve visualizes how accuracy and
streaming cost vary with electrode budget for the
4

=== PAGE 5 ===
word holdout protocol.
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
Figure 1: Electrode-budget trends for P1 word hold-
out; topk uses within-participant importance ranking,
diversity corresponds to fps2k, and random is a fixed
random subset. CER is character error rate and RTF
is real time factor.
Figure fig:kcurve shows CER improving as K in-
creases toward full channels, while RTF changes
less steeply. Random subsets remain below within-
participant selections across most K, although the
absolute gap narrows at larger budgets.
Table tab:p3ms evaluates paired-source cross-
participant transfer under the same target and proto-
col constraints.
Table 6: Paired-source cross-participant results by
source pair; group denotes source participants to tar-
get participant with participant IDs p1 to p4. vec is
vector baseline, rowcol is row-column pooling, grid
is a convolutional grid encoder, and grid aug adds
spatial augmentation. CER is character error rate
and RTF is real time factor.
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
Table tab:p3ms is target dependent: for p23-¿p1,
vec 0.473 and rowcol 0.476 outperform grid 0.602 and
grid aug 0.691, while for p12-¿p3, grid 0.736 outper-
forms vec 0.838 and rowcol 0.790. Multi-source benefit
is therefore conditional rather than universal.
5 Discussion
The dominant and most stable signal is the protocol
gap: P3 CER is 0.691±0.133, versus 0.180±0.084 for
P1 and 0.145±0.063 for P2. This ordering persists un-
der front-end swaps, channel reduction, and low-shot
settings, so cross-participant mismatch remains the
primary error source in this audited setup. Layout-
aware bias alone is insufficient. Rowcol remains close
to vec across P1-P3, while grid variants often increase
CER and RTF; patch pooling narrows some gaps but
does not create a consistent winner. Spatial encoders
therefore need protocol-specific validation against ex-
plicit latency constraints. Source aggregation helps
at the p4 aggregate level (CER 0.686 to 0.582), but
direction-level outcomes remain heterogeneous. To-
gether with k-shot behavior (vec and rowcol improve
5

=== PAGE 6 ===
from k1 to k2 while grid variants worsen), this indi-
cates that transfer benefit depends on source-target
compatibility and model family. Our practical rule
is protocol-specific selection under matched audited
splits and manifests. We limit all claims to these
datasets, this normalization pipeline, and these proto-
col definitions, and we do not extrapolate to unaudited
populations or sensing setups.
6 Conclusion
EPGSpeller provides a reproducible benchmark for
lexicon-free silent spelling under deterministic au-
dited protocols. Within this audited setting, cross-
participant transfer remains the hardest regime (P3
CER 0.691±0.133), and paired-source aggregation can
reduce aggregate p4 error (0.686 to 0.582) without
removing direction dependence. Deployment claims
should therefore be validated per protocol, per target,
and per latency constraint.
7 Artifacts and Auditability
This repository uses a strict paper registry that pins
every evidence file by checksum and rejects unsup-
ported manuscript blocks. The split manifests, aggre-
gated metrics, compact tables, statistical summaries,
and analysis reports referenced in this paper are stored
as deterministic artifacts, enabling audit and repro-
duction within our repository environment. A sup-
plementary archive includes the compact statistical
summary table for reviewers.
8 Ethics and Disclosure
We report results only for audited artifacts and do not
claim broader demographic coverage. The datasets
and splits used in this study are derived from par-
ticipant recordings, and we focus on methodological
clarity and artifact traceability rather than deploy-
ment claims. We used generative AI tools for language
polishing and verified technical claims against audited
artifacts.
References
[1] B. Denby, T. Schultz, K. Honda, T. Hueber,
J. Gilbert, and J. Brumberg, “Silent speech in-
terfaces,” 2010.
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,
An Introduction to Silent Speech Interfaces, ser.
SpringerBriefs in Electrical and Computer Engi-
neering. Springer, 2017.
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M.
Martin Donas, J. L. Perez-Cordoba, and A. M.
Gomez, “Silent speech interfaces for speech
restoration: A review,” 2020.
[4] W. Hardcastle, W. Jones, C. Knight, A. Trud-
geon, and G. Calder, “New developments in
electropalatography: A state-of-the-art report,”
1989.
[5] W. J. Hardcastle, “Electropalatography in pho-
netic research and in speech training,” 1990.
[6] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim,
A. Marakhimov, and S. Lee, “Biosignal sensors
and deep learning-based speech recognition: A
review,” 2021.
[7] J. Verhoeven, N. R. Miller, L. Daems, and
C. C. Reyes-Aldasoro, “Visualisation and anal-
ysis of speech production with electropalatogra-
phy,” 2019.
[8] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B.
Pyun, “Design and evaluation of korean elec-
tropalatography (k-epg),” 2021.
[9] M. ´A. Carreira-Perpi˜ n´ an and S. Renals, “Dimen-
sionality reduction of electropalatographic data
using latent variable models,” 1998.
[10] X. Dong, Y. Chen, Y. Nishiyama, K. Sezaki,
Y. Wang, K. Christofferson, and A. Mariakakis,
“Rehearsse: Recognizing hidden-in-the-ear silently
spelled expressions,” 2024.
[11] J. Gilbert, S. Rybchenko, R. Hofe, S. Ell, M. Fa-
gan, R. Moore, and P. Green, “Isolated word
6

=== PAGE 7 ===
recognition of silent speech using magnetic im-
plants and sensors,” 2010.
[12] A. Graves, S. Fern´ andez, F. Gomez, and
J. Schmidhuber, “Connectionist temporal classi-
fication,” 2006.
[13] W. Hardcastle, F. Gibbon, and K. Nicolaidis,
“Epg data reduction methods and their implica-
tions for studies of lingual coarticulation,” 1991.
[14] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby,
G. Dreyfus, and M. Stone, “Development of a
silent speech interface driven by ultrasound and
optical images of the tongue and lips,” 2010.
[15] N. Kimura, T. Gemicioglu, J. Womack, R. Li,
Y. Zhao, A. Bedri, Z. Su, A. Olwal, J. Reki-
moto, and T. Starner, “Silentspeller: Towards
mobile, hands-free, silent speech text entry using
electropalatography,” 2022.
[16] C. H. Shadle, J. N. Carter, T. P. Monks, and
J. Field, “Depth measurement of face and palate
by structured light,” 1993.
[17] A. Toutios and K. Margaritis, “Learning elec-
tropalatograms from acoustics,” 2006.
[18] ——, “On the acoustic-to-electropalatographic
mapping,” 2006.
[19] D. S. Park, W. Chan, Y. Zhang, C.-C. Chiu,
B. Zoph, E. D. Cubuk, and Q. V. Le, “Specaug-
ment: A simple data augmentation method for
automatic speech recognition,” 2019.
7
