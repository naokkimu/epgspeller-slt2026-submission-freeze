# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 12332,
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
      }
    ],
    "page_count": 4,
    "path": "paper/manuscript/generated_main.pdf",
    "sha256": "ca7e094ca75aaa546c288ab777e06f77d8eab59711b218a1df5a9ff4dae3d7ba",
    "sha8": "ca7e094c",
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
    "sha256": "d8553a4c63ec87ba8df83939df5a9dfb9279904e9eda76850a27292caf5ca699",
    "sha8": "d8553a4c"
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
      "extracted_chars": 12332,
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
        }
      ],
      "page_count": 4,
      "path": "paper/manuscript/generated_main.pdf",
      "sha256": "ca7e094ca75aaa546c288ab777e06f77d8eab59711b218a1df5a9ff4dae3d7ba",
      "sha8": "ca7e094c",
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
      "sha256": "d8553a4c63ec87ba8df83939df5a9dfb9279904e9eda76850a27292caf5ca699",
      "sha8": "d8553a4c"
    }
  },
  "run_id": "INTSP2026_STATIC_ca7e094c_d8553a4c"
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
train and test splits, and a small set of all-zero samples
is excluded via a pinned index list.
We evaluate three primary protocols. The word
holdout protocol uses disjoint vocabularies across
train, test, and a competition partition. The instance
holdout protocol evaluates held out instances of seen
words by separating train and competition vocabu-
laries while keeping the test vocabulary within their
union. The cross participant protocol trains on a
source participant and evaluates on a target partici-
pant under a shared vocabulary constraint. All split
archives used in this study are enumerated with sizes
and checksums in a manifest artifact.
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
5 Results
The baseline recap table summarizes baseline perfor-
mance under word holdout, instance holdout, and
cross participant transfer. Lexicon projection reduces
Table 1: Baseline recap across three evaluation proto-
cols (mean and standard deviation over groups).
protocol variant n cer m cer s lex all m lex all s
P1 vector 4 0.1796 0.0844 0.1018 0.0679
P2 vector 3 0.1451 0.0627 0.0747 0.0476
P3 vector 6 0.6909 0.1332 0.6442 0.0604
Table 2: Spatial modeling comparison at full channels
(mean and standard deviation over groups).
protocol variant n cer m cer s rtf m rtf s
P1 vector 4 0.1796 0.0844 0.000628 0.000232
P1 rowcol 4 0.2016 0.0886 0.002401 0.001106
P1 spatial2d 4 0.3062 0.1491 0.003564 0.001540
P1 spatial2d aug 4 0.3094 0.1440 0.003414 0.001054
P2 vector 3 0.1451 0.0627 0.000107 0.000010
P2 rowcol 3 0.1613 0.0783 0.000244 0.000037
P2 spatial2d 3 0.2894 0.2126 0.000389 0.000047
P2 spatial2d aug 3 0.3139 0.2436 0.000392 0.000045
P3 vector 6 0.6909 0.1332 0.000110 0.000014
P3 rowcol 6 0.6828 0.1510 0.000243 0.000033
P3 spatial2d 6 0.7507 0.0897 0.000393 0.000042
P3 spatial2d aug 6 0.7559 0.0920 0.000397 0.000046
error rates relative to greedy decoding across proto-
cols, highlighting the importance of open-vocabulary
post processing for spelling.
The spatial modeling table compares spatial induc-
tive bias variants at full channels across protocols.
The row and column front end tracks the vector base-
line more closely than the convolutional grid front
end, and the grid front end increases real time factor.
This trend is consistent with our single participant
spatial analysis.
The electrode reduction table evaluates a reduced
channel budget using several selection strategies.
Across protocols, within participant selection and
simple transfer selection yield similar performance,
suggesting that a compact subset can preserve a large
fraction of the vector baseline performance.
2

=== PAGE 3 ===
Table 3: Electrode reduction methods under a reduced
channel budget (mean and standard deviation over
groups).
protocol method n cer m cer s rtf m rtf s
P1 within topk 4 0.1952 0.0827 0.000657 0.000210
P1 within fps2k 4 0.1912 0.0781 0.000619 0.000229
P1 transfer topk 4 0.2053 0.0951 0.000586 0.000218
P1 random 4 0.1980 0.0793 0.000665 0.000282
P2 within topk 3 0.1544 0.0591 0.000110 0.000011
P2 within fps2k 3 0.1539 0.0617 0.000110 0.000010
P2 transfer topk 3 0.1584 0.0709 0.000106 0.000009
P2 random 3 0.1566 0.0669 0.000105 0.000011
P3 within topk 6 0.6473 0.1301 0.000108 0.000009
P3 within fps2k 6 0.6564 0.1465 0.000107 0.000010
P3 transfer topk 6 0.6569 0.1441 0.000109 0.000009
P3 random 6 0.6442 0.1328 0.000111 0.000010
6 Discussion
Our results suggest that an explicit convolutional
grid encoder is not automatically beneficial for elec-
tropalatography, despite its intuitive spatial structure.
Spatial augmentation can improve robustness to syn-
thetic electrode dropout, but it does not close the gap
in our multi-participant accuracy results. Additional
analyses on multi-source cross participant transfer and
low shot adaptation are provided as artifact tables,
and they highlight that cross participant performance
remains challenging.
7 Artifacts and Auditability
This repository uses a strict paper registry that pins
every evidence file by checksum and rejects unsup-
ported manuscript blocks. The split manifest, ag-
gregated metrics, and compact tables referenced in
this paper are stored as deterministic artifacts, en-
abling audit and reproduction within our repository
environment.
8 Ethics and Disclosure
We report results only for audited artifacts and do not
claim broader demographic coverage. The datasets
and splits used in this study are derived from par-
ticipant recordings, and we focus on methodological
clarity and artifact traceability rather than deploy-
ment claims.
References
[1] B. Denby, T. Schultz, K. Honda, T. Hue-
ber, J. Gilbert, and J. Brumberg, “Silent
speech interfaces,” 2010. [Online]. Avail-
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
3

=== PAGE 4 ===
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
4
