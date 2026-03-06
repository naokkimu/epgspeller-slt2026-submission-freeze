# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 18253,
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
      }
    ],
    "page_count": 6,
    "path": "paper/manuscript/generated_main.pdf",
    "sha256": "ba786f15cdfad0993e2cac2681d6d0b9678f0301fe9793ff129b2b6ed24d7f14",
    "sha8": "ba786f15",
    "truncated": false
  },
  "rules": "/Users/naokkimu/.codex/skills/paperjson-init/assets/toolkit/references/interspeech2026_rules.yaml",
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
    "sha256": "5556de5b800abed3fd627958d0d29ab60cf569960dae775a8b4f7ca4f2a77641",
    "sha8": "5556de5b"
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
        "page_count": 6
      },
      "id": "page_limit",
      "message": "page_count=6 <= max_pages=6",
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
      "extracted_chars": 18253,
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
        }
      ],
      "page_count": 6,
      "path": "paper/manuscript/generated_main.pdf",
      "sha256": "ba786f15cdfad0993e2cac2681d6d0b9678f0301fe9793ff129b2b6ed24d7f14",
      "sha8": "ba786f15",
      "truncated": false
    },
    "rules": "/Users/naokkimu/.codex/skills/paperjson-init/assets/toolkit/references/interspeech2026_rules.yaml",
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
      "sha256": "5556de5b800abed3fd627958d0d29ab60cf569960dae775a8b4f7ca4f2a77641",
      "sha8": "5556de5b"
    }
  },
  "run_id": "INTSP2026_STATIC_ba786f15_5556de5b"
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
\usepackage{graphicx}
\usepackage{microtype}
\usepackage{hyperref}
\usepackage{url}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}

\title{EPGSpeller: Evidence-Only Protocols and Multi-Participant Evaluation for Open-Vocabulary Silent Spelling}
\author{Anonymous}
\date{}

```

## PDF extracted text (page-separated, deterministic truncation)

=== PAGE 1 ===
EPGSpeller: Evidence-Only Protocols and Multi-Participant
Evaluation for Open-Vocabulary Silent Spelling
Anonymous
Abstract
Silent speech text entry with electropalatography
requires models that generalize across word identi-
ties and participants while remaining auditable. We
present an evidence-only study of open-vocabulary
silent spelling from binary palate contact patterns,
with protocols for word holdout, instance holdout, and
cross participant transfer. Using four participants and
deterministic artifact tracking, we evaluate a vector
baseline and two layout aware front ends, and we
analyze electrode reduction and low shot adaptation.
Across our audited runs, the row and column front
end tracks the vector baseline more closely than a
convolutional grid front end, while the grid front end
increases streaming latency. We release split mani-
fests, checksums, and compact result tables as pinned
repository artifacts.
1 Introduction
Silent speech interfaces aim to enable communication
without audible acoustics, using sensor measurements
of articulation or physiology. Electropalatography
provides a practical binary contact representation of
tongue and palate interaction, but its discrete layout
and device variability raise questions about inductive
bias, robustness, and generalization. [1, 2, 3, 4]
Recent work on silent spelling has emphasized open-
vocabulary text entry, where character level decoding
can compose words beyond a fixed closed set. We
study open-vocabulary spelling with a CTC style de-
coder and lexicon projection, and we compare vector
and layout aware front ends under multiple general-
ization protocols. [5, 6, 7]
• We define evaluation protocols that separate word
identity generalization and participant transfer,
and we provide split archives with checksums.
• We run multi-participant experiments with open-
vocabulary decoding and lexicon projection,
tracked by a strict evidence registry.
• We compare a vector baseline with two layout
aware front ends, and we report both accuracy
and streaming speed metrics.
• We provide deterministic scripts that export
compact tables and manifests used by this
manuscript.
2 Related Work
Within our surveyed set, open-vocabulary silent
spelling systems are represented by SilentSpeller and
ReHEarSSE, while broader silent speech systems span
constrained recognition and reconstruction settings.
In the electropalatography literature, the spatial lay-
out has been used for visualization, device charac-
terization, and representation reduction, motivating
tests of layout aware inductive bias in learned de-
coders. [8, 1, 5, 3, 9, 10, 11, 12, 7, 13, 14, 15, 16, 17]
3 Data and Protocols
We use four participant electropalatography datasets
with word labels. Each sample is a variable length
binary contact matrix, and the raw exports are treated
as immutable evidence. We audit dataset statistics,
label counts, and anomalies before constructing any
1

=== PAGE 2 ===
Table 1: Raw dataset summary for each participant
dataset.
dataset id n samples n unique labels T median total frames mean contact all zero samples exclude indices n
p1 2328 old 2328 1164 234.000 570750 0.1876 0 0
thad 2328 old 2328 1164 196.000 484586 0.2029 0 0
john 2328 2797 1164 283.000 810375 0.1221 4 4
su 1167 old 1167 1162 229.000 287808 0.1855 0 0
train and test splits, and a small set of all-zero samples
is excluded via a pinned index list.
The dataset summary table reports raw sample
counts, vocabulary sizes, median sequence length, to-
tal frames, mean contact rate, and excluded all-zero
counts for each participant dataset.
We evaluate three primary protocols. The word
holdout protocol uses disjoint vocabularies across
train, test, and a competition partition. The instance
holdout protocol evaluates held out instances of seen
words by separating train and competition vocabu-
laries while keeping the test vocabulary within their
union. The cross participant protocol trains on a
source participant and evaluates on a target partici-
pant under a shared vocabulary constraint. When a
target participant has limited within word repetition,
we configure the cross participant split generators to
allow single instance target words while keeping source
side constraints unchanged. All split archives used in
this study are enumerated with sizes and checksums
in manifest artifacts.
Labels are normalized by uppercasing and filtering
to alphabet characters, then represented as a space
separated character sequence for CTC training and
greedy decoding. This normalization is applied con-
sistently during split construction and dataset prepa-
ration to avoid vocabulary drift.
We report character error rate from greedy decoding
and streaming speed using real time factor, defined as
total inference time divided by total input duration.
For open-vocabulary decoding we also report lexicon
projection error rates using a training lexicon and a
full lexicon.
Table 2: Shared training configuration across all re-
ported runs.
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
4 Models
Our baseline model encodes each frame as a vector of
palate channels and applies a uni-directional recurrent
decoder trained with a CTC objective. We compare
two layout aware front ends: a row and column pool-
ing front end that aggregates a proxy grid into one
dimensional summaries, and a grid reconstruction
front end that applies a convolutional spatial encoder.
For the grid model we optionally enable a spatial aug-
mentation that drops and shifts contiguous electrode
blocks. [6, 18]
We fix core training hyperparameters across runs;
the training configuration table lists the shared values
extracted from the metrics registry.
5 Results
The baseline recap table summarizes baseline perfor-
mance under word holdout, instance holdout, and
cross participant transfer. Lexicon projection reduces
error rates relative to greedy decoding across proto-
cols, highlighting the importance of open-vocabulary
post processing for spelling.
2

=== PAGE 3 ===
Table 3: Baseline recap across three evaluation proto-
cols (mean and standard deviation over groups).
protocol variant n cer m cer s lex all m lex all s
P1 vector 4 0.1796 0.0844 0.1018 0.0679
P2 vector 3 0.1451 0.0627 0.0747 0.0476
P3 vector 6 0.6909 0.1332 0.6442 0.0604
Table 4: Cross participant generalization targeting
participant four (direction wise mean and standard
deviation over seeds, plus across direction aggrega-
tion).
protocol level group cer lex all rtf
P3 direction subj1to4 0.6660 +/- 0.0237 0.6508 +/- 0.0261 0.000192 +/- 0.000088
P3 direction subj2to4 0.8091 +/- 0.0207 0.7359 +/- 0.0216 0.000145 +/- 0.000010
P3 direction subj3to4 0.5840 +/- 0.0180 0.5911 +/- 0.0287 0.000140 +/- 0.000007
P3 across directions ALL to4 0.6863 +/- 0.1139 0.6593 +/- 0.0728 0.000159 +/- 0.000029
P3MS direction subj12to4 0.6546 +/- 0.0161 0.5932 +/- 0.0162 0.000138 +/- 0.000011
P3MS direction subj13to4 0.5363 +/- 0.0089 0.5327 +/- 0.0084 0.000148 +/- 0.000010
P3MS direction subj23to4 0.5547 +/- 0.0046 0.5366 +/- 0.0111 0.000144 +/- 0.000007
P3MS across directions ALL to4 0.5819 +/- 0.0637 0.5541 +/- 0.0339 0.000143 +/- 0.000005
We additionally evaluate cross participant general-
ization targeting participant four under both single
source and multi source transfer. The to participant
four generalization table summarizes direction level
seed statistics, and the corresponding split archives
are pinned by checksum in a dedicated manifest arti-
fact.
The spatial modeling tables compare spatial induc-
tive bias variants at full channels across protocols,
including a patchpool grid encoder as a minimal im-
plementation rescue. The row and column front end
tracks the vector baseline more closely than the con-
volutional grid front end under within participant pro-
tocols, while patchpool reduces the gap under cross
participant transfer. Across protocols, grid variants
tend to increase real time factor relative to the vector
baseline.
The electrode reduction table evaluates a reduced
channel budget using several selection strategies.
Across protocols, within participant selection and
simple transfer selection yield similar performance,
suggesting that a compact subset can preserve a large
Table 5: Spatial modeling at full channels for the
word holdout protocol.
variant cer lex all rtf
vector 0.1796 +/- 0.0844 0.1018 +/- 0.0679 0.000628 +/- 0.000232
rowcol 0.2016 +/- 0.0886 0.1285 +/- 0.0810 0.002401 +/- 0.001106
spatial2d 0.3062 +/- 0.1491 0.2536 +/- 0.1797 0.003564 +/- 0.001540
spatial2d aug 0.3094 +/- 0.1440 0.2605 +/- 0.1681 0.003414 +/- 0.001054
patchpool 0.2982 +/- 0.0666 0.2373 +/- 0.0732 0.003795 +/- 0.001663
patchpool aug 0.2988 +/- 0.0891 0.2338 +/- 0.0920 0.003876 +/- 0.001709
Table 6: Spatial modeling at full channels for the
instance holdout protocol.
variant cer lex all rtf
vector 0.1451 +/- 0.0627 0.0747 +/- 0.0476 0.000107 +/- 0.000010
rowcol 0.1613 +/- 0.0783 0.0893 +/- 0.0636 0.000244 +/- 0.000037
spatial2d 0.2894 +/- 0.2126 0.2321 +/- 0.2530 0.000389 +/- 0.000047
spatial2d aug 0.3139 +/- 0.2436 0.2611 +/- 0.2879 0.000392 +/- 0.000045
patchpool 0.3384 +/- 0.2324 0.2850 +/- 0.2689 0.000658 +/- 0.000088
patchpool aug 0.3014 +/- 0.1626 0.2438 +/- 0.1897 0.000621 +/- 0.000038
fraction of the vector baseline performance.
We evaluate multi source cross participant transfer
using paired source participants. The multi source
table reports direction level results for vector and
layout aware front ends.
We evaluate low shot adaptation for a new partici-
pant by varying the number of training instances per
word. The k shot table summarizes results for vector
and layout aware front ends.
6 Discussion
Our results suggest that an explicit convolutional
grid encoder is not automatically beneficial for elec-
tropalatography under within participant evaluation,
despite its intuitive spatial structure. A patchpool
grid variant reduces the underperformance of the grid
encoder under cross participant transfer, indicating
that spatial encoder design choices can materially af-
fect outcomes, but it does not yield consistent gains
over the vector baseline across protocols. Spatial aug-
mentation can improve robustness to synthetic elec-
trode dropout, but it does not close the accuracy gap
3

=== PAGE 4 ===
Table 7: Spatial modeling at full channels for the cross
participant protocol.
variant cer lex all rtf
vector 0.6909 +/- 0.1332 0.6442 +/- 0.0604 0.000110 +/- 0.000014
rowcol 0.6828 +/- 0.1510 0.6260 +/- 0.0850 0.000243 +/- 0.000033
spatial2d 0.7507 +/- 0.0897 0.7434 +/- 0.0699 0.000393 +/- 0.000042
spatial2d aug 0.7559 +/- 0.0920 0.7474 +/- 0.0803 0.000397 +/- 0.000046
patchpool 0.6898 +/- 0.1103 0.6840 +/- 0.0819 0.000631 +/- 0.000070
patchpool aug 0.6992 +/- 0.1305 0.6749 +/- 0.1076 0.000476 +/- 0.000079
Table 8: Electrode reduction methods for word and
instance holdout protocols.
protocol method cer rtf
P1 within topk 0.1952 +/- 0.0827 0.000657 +/- 0.000210
P1 within fps2k 0.1912 +/- 0.0781 0.000619 +/- 0.000229
P1 transfer topk 0.2053 +/- 0.0951 0.000586 +/- 0.000218
P1 random 0.1980 +/- 0.0793 0.000665 +/- 0.000282
P2 within topk 0.1544 +/- 0.0591 0.000110 +/- 0.000011
P2 within fps2k 0.1539 +/- 0.0617 0.000110 +/- 0.000010
P2 transfer topk 0.1584 +/- 0.0709 0.000106 +/- 0.000009
P2 random 0.1566 +/- 0.0669 0.000105 +/- 0.000011
for the convolutional grid variants in our multi par-
ticipant results. Additional analyses on multi source
cross participant transfer and low shot adaptation
are provided as artifact tables, and they highlight
that cross participant performance remains challeng-
ing. We also provide a conditions analysis of multi
source transfer deltas versus simple dataset similarity
measures, which shows that the effect is conditional
and does not present a single dominant monotonic
trend within our evaluated group set.
7 Artifacts and Auditability
This repository uses a strict paper registry that pins
every evidence file by checksum and rejects unsup-
ported manuscript blocks. The split manifests, aggre-
gated metrics, compact tables, and analysis summaries
referenced in this paper are stored as deterministic
artifacts, enabling audit and reproduction within our
repository environment.
Table 9: Electrode reduction methods for the cross
participant protocol.
method cer rtf
within topk 0.6473 +/- 0.1301 0.000108 +/- 0.000009
within fps2k 0.6564 +/- 0.1465 0.000107 +/- 0.000010
transfer topk 0.6569 +/- 0.1441 0.000109 +/- 0.000009
random 0.6442 +/- 0.1328 0.000111 +/- 0.000010
Table 10: Multi source cross participant results by
source pair.
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
8 Ethics and Disclosure
We report results only for audited artifacts and do not
claim broader demographic coverage. The datasets
and splits used in this study are derived from par-
ticipant recordings, and we focus on methodological
clarity and artifact traceability rather than deploy-
ment claims.
9 Logic Checks
The baseline table includes protocol and variant fields.
References
[1] B. Denby, T. Schultz, K. Honda, T. Hue-
ber, J. Gilbert, and J. Brumberg, “Silent
speech interfaces,” 2010. [Online]. Avail-
4

=== PAGE 5 ===
Table 11: Low shot adaptation results for a new par-
ticipant.
group variant cer rtf
subj3 k1 vector 0.3503 +/- 0.0599 0.000164 +/- 0.000009
subj3 k1 rowcol 0.3344 +/- 0.0386 0.000502 +/- 0.000022
subj3 k1 spatial2d 0.5153 +/- 0.0500 0.000712 +/- 0.000005
subj3 k1 spatial2d aug 0.6105 +/- 0.1572 0.001067 +/- 0.000637
subj3 k2 vector 0.2458 +/- 0.0085 0.000165 +/- 0.000002
subj3 k2 rowcol 0.2782 +/- 0.0217 0.000522 +/- 0.000007
subj3 k2 spatial2d 0.6156 +/- 0.1321 0.000769 +/- 0.000064
subj3 k2 spatial2d aug 0.6889 +/- 0.2179 0.000748 +/- 0.000038
able: https://sciencedirect.com/science/article/
pii/S0167639309001307
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,
An Introduction to Silent Speech Interfaces, 2017.
[Online]. Available: https://link.springer.com/
book/10.1007/978-3-319-40174-4
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M.
Martin Donas, J. L. Perez-Cordoba, and A. M.
Gomez, “Silent speech interfaces for speech
restoration: A review,” 2020. [Online]. Available:
https://ieeexplore.ieee.org/document/9205294/
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim,
A. Marakhimov, and S. Lee, “Biosignal sensors
and deep learning-based speech recognition:
A review,” 2021. [Online]. Available: https:
//doi.org/10.3390/s21041399
[5] X. Dong, Y. Chen, Y. Nishiyama,
K. Sezaki, Y. Wang, K. Christofferson,
and A. Mariakakis, “Rehearsse: Recog-
nizing hidden-in-the-ear silently spelled ex-
pressions,” 2024. [Online]. Available: https:
//dl.acm.org/doi/10.1145/3613904.3642095
[6] A. Graves, S. Fern´ andez, F. Gomez, and
J. Schmidhuber, “Connectionist temporal clas-
sification,” 2006. [Online]. Available: https:
//dl.acm.org/doi/10.1145/1143844.1143891
[7] N. Kimura, T. Gemicioglu, J. Womack,
R. Li, Y. Zhao, A. Bedri, Z. Su, A. Olwal,
J. Rekimoto, and T. Starner, “Silentspeller:
Towards mobile, hands-free, silent speech
text entry using electropalatography,” 2022.
[Online]. Available: https://dl.acm.org/doi/10.
1145/3491102.3502015
[8] M. ´A. Carreira-Perpi˜ n´ an and S. Renals,
“Dimensionality reduction of electropalatographic
data using latent variable models,” 1998.
[Online]. Available: https://sciencedirect.com/
science/article/pii/S0167639398000594
[9] W. Hardcastle, W. Jones, C. Knight,
A. Trudgeon, and G. Calder, “New devel-
opments in electropalatography: A state-
of-the-art report,” 1989. [Online]. Available:
https://doi.org/10.3109/02699208908985268
[10] W. J. Hardcastle, “Electropalatography in
phonetic research and in speech training,” 1990.
[Online]. Available: https://isca-archive.org/
icslp 1990/hardcastle90b icslp.html
[11] W. Hardcastle, F. Gibbon, and K. Nico-
laidis, “Epg data reduction methods and
their implications for studies of lingual coar-
ticulation,” 1991. [Online]. Available: https:
//doi.org/10.1016/S0095-4470(19)30343-2
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby,
G. Dreyfus, and M. Stone, “Development of a
silent speech interface driven by ultrasound and
optical images of the tongue and lips,” 2010.
[Online]. Available: https://sciencedirect.com/
science/article/pii/S0167639309001733
[13] C. H. Shadle, J. N. Carter, T. P. Monks,
and J. Field, “Depth measurement of face
and palate by structured light,” 1993. [Online].
Available: https://isca-archive.org/eurospeech
1993/shadle93 eurospeech.html
[14] A. Toutios and K. Margaritis, “Learning
electropalatograms from acoustics.” [Online].
Available: https://doi.org/10.1109/ICASSP.
2006.1660032
[15] ——, “On the acoustic-to-electropalatographic
mapping,” 2006. [Online]. Available: https://
link.springer.com/chapter/10.1007/11613107 16
5

=== PAGE 6 ===
[16] J. Verhoeven, N. R. Miller, L. Daems, and C. C.
Reyes-Aldasoro, “Visualisation and analysis of
speech production with electropalatography,”
2019. [Online]. Available: https://doi.org/10.
3390/jimaging5030040
[17] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and
S.-B. Pyun, “Design and evaluation of korean
electropalatography (k-epg),” 2021. [Online].
Available: https://doi.org/10.3390/s21113802
[18] D. S. Park, W. Chan, Y. Zhang, C.-C.
Chiu, B. Zoph, E. D. Cubuk, and Q. V. Le,
“Specaugment: A simple data augmentation
method for automatic speech recognition,” 2019.
[Online]. Available: https://isca-archive.org/
interspeech 2019/park19 interspeech.html
6
