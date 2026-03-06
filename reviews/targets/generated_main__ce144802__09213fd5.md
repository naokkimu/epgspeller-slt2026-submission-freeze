# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 17413,
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
    "sha256": "ce1448026e5ce31afbf91846c83b5ca8e8f2aef920dae520bf1bc2315679ac11",
    "sha8": "ce144802",
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
    "sha256": "09213fd562ea1b3458af706d10316ed7976f03b02cdc5910fbc5a1c4fb208a9c",
    "sha8": "09213fd5"
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
      "extracted_chars": 17413,
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
      "sha256": "ce1448026e5ce31afbf91846c83b5ca8e8f2aef920dae520bf1bc2315679ac11",
      "sha8": "ce144802",
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
      "sha256": "09213fd562ea1b3458af706d10316ed7976f03b02cdc5910fbc5a1c4fb208a9c",
      "sha8": "09213fd5"
    }
  },
  "run_id": "INTSP2026_STATIC_ce144802_09213fd5"
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
We summarize the positioning of prior work using
survey tags that map systems by representation and
system scope, describing where open vocabulary silent
spelling and electropalatography studies sit in the
space.
1

=== PAGE 2 ===
Table 1: Raw dataset summary for each participant
dataset; N is sample count, V is vocabulary size, Tmed
is median sequence length, contact is mean contact
rate, and zero is the count of all zero samples.
id N V Tmed contact zero
p1 2328 1164 234 0.19 0
p2 2328 1164 196 0.20 0
p3 2797 1164 283 0.12 4
p4 1167 1162 229 0.19 0
3 Data and Protocols
We use four participant electropalatography datasets
with word labels. Each sample is a variable length
binary contact matrix, and the raw exports are treated
as immutable evidence. We audit dataset statistics,
label counts, and anomalies before constructing any
train and test splits, and a small set of all-zero samples
is excluded via a pinned index list.
The dataset summary table reports id, sample
count, vocabulary size, median sequence length, mean
contact rate, and the count of all-zero samples for
each participant dataset.
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
Table 2: Baseline recap across three evaluation pro-
tocols; CER is character error rate and lex is lexicon
projected error rate.
protocol variant n cer lex
P1 vec 4 0.180±0.084 0.102±0.068
P2 vec 3 0.145±0.063 0.075±0.048
P3 vec 6 0.691±0.133 0.644±0.060
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
We fix core training hyperparameters across runs
and record the shared configuration in the metrics
registry for auditability.
5 Results
The baseline recap table summarizes baseline perfor-
mance under word holdout, instance holdout, and
cross participant transfer. Lexicon projection reduces
error rates relative to greedy decoding across proto-
cols, highlighting the importance of open-vocabulary
post processing for spelling.
We additionally evaluate cross participant general-
ization targeting participant four under both single
source and multi source transfer. The table uses lvl
labels dir for single directions and all for the across
2

=== PAGE 3 ===
Table 3: Cross participant generalization targeting
participant four; proto denotes the protocol abbrevia-
tion, lvl marks direction level or aggregate, and lex is
lexicon projected error rate.
proto lvl group cer lex
P3 dir s1-4 0.666±0.024 0.651±0.026
P3 dir s2-4 0.809±0.021 0.736±0.022
P3 dir s3-4 0.584±0.018 0.591±0.029
P3 all all 0.686±0.114 0.659±0.073
P3MS dir s12-4 0.655±0.016 0.593±0.016
P3MS dir s13-4 0.536±0.009 0.533±0.008
P3MS dir s23-4 0.555±0.005 0.537±0.011
P3MS all all 0.582±0.064 0.554±0.034
direction aggregation, and the corresponding split
archives are pinned by checksum in a dedicated mani-
fest artifact. Group labels use sX-Y for single source
and sXY-Y for paired sources. In our audited splits,
the multi source aggregation reduces CER relative to
the single source aggregation for the same target.
The spatial modeling table compares spatial induc-
tive bias variants at full channels across protocols,
including a patchpool grid encoder as a minimal im-
plementation rescue. The variant labels are vec, row-
col, grid, grid aug, patch, and patch aug. The row
and column front end tracks the vector baseline more
closely than the convolutional grid front end under
within participant protocols, while patchpool reduces
the gap under cross participant transfer. Across pro-
tocols, grid variants tend to increase real time factor
relative to the vector baseline, and we do not observe
a consistent accuracy gain over the vector baseline in
any protocol.
The electrode reduction table evaluates a reduced
channel budget using several selection strategies. The
method labels are topk, fps two k, xfer, and rand.
Across protocols, within participant selection and
simple transfer selection yield similar performance,
suggesting that a compact subset can preserve a large
fraction of the vector baseline performance. Random
selection and simple transfer remain slightly worse
than within participant selection in the audited re-
sults.
We evaluate multi source cross participant transfer
Table 4: Spatial modeling at full channels across
protocols; CER is character error rate and RTF is
real time factor.
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
using paired source participants. The group labels
indicate the two source participants followed by the
target participant. The multi source table reports
direction level results for vector and layout aware
front ends.
We further analyze multi source transfer deltas
against simple similarity measures, and the conditions
analysis summarizes the conditional pattern across
audited source pairs and targets.
We evaluate low shot adaptation for a new partici-
pant by varying the number of training instances per
word. The k shot table summarizes one shot and two
shot results for vector and layout aware front ends.
6 Discussion
Our results suggest that an explicit convolutional
grid encoder is not automatically beneficial for elec-
tropalatography under within participant evaluation,
despite its intuitive spatial structure. A patchpool
grid variant reduces the underperformance of the grid
3

=== PAGE 4 ===
Table 5: Electrode reduction methods across protocols;
CER is character error rate and RTF is real time
factor.
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
encoder under cross participant transfer, indicating
that spatial encoder design choices can materially af-
fect outcomes, but it does not yield consistent gains
over the vector baseline across protocols. Spatial aug-
mentation can improve robustness to synthetic elec-
trode dropout, but it does not close the accuracy gap
for the convolutional grid variants in our multi par-
ticipant results. Additional analyses on multi source
cross participant transfer and low shot adaptation are
provided as artifact tables, and they highlight that
cross participant performance remains challenging.
We also provide a conditions analysis of multi source
transfer deltas versus simple dataset similarity mea-
sures, which shows that the effect is conditional and
does not present a single dominant monotonic trend
within our evaluated group set. These observations
are limited to our audited multi participant dataset
collection and protocols.
7 Artifacts and Auditability
This repository uses a strict paper registry that pins
every evidence file by checksum and rejects unsup-
ported manuscript blocks. The split manifests, aggre-
gated metrics, compact tables, and analysis summaries
referenced in this paper are stored as deterministic
artifacts, enabling audit and reproduction within our
Table 6: Multi source cross participant results by
source pair; CER is character error rate and RTF is
real time factor.
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
Table 7: Low shot adaptation results for a new par-
ticipant; CER is character error rate and RTF is real
time factor.
group variant cer rtf
subj3 k1 vec 0.350±0.060 0.0002±0.0000
subj3 k1 rowcol 0.334±0.039 0.0005±0.0000
subj3 k1 grid 0.515±0.050 0.0007±0.0000
subj3 k1 grid aug 0.611±0.157 0.0011±0.0006
subj3 k2 vec 0.246±0.009 0.0002±0.0000
subj3 k2 rowcol 0.278±0.022 0.0005±0.0000
subj3 k2 grid 0.616±0.132 0.0008±0.0001
subj3 k2 grid aug 0.689±0.218 0.0007±0.0000
repository environment.
8 Ethics and Disclosure
We report results only for audited artifacts and do not
claim broader demographic coverage. The datasets
and splits used in this study are derived from par-
ticipant recordings, and we focus on methodological
clarity and artifact traceability rather than deploy-
ment claims.
4

=== PAGE 5 ===
Figure 1: Multi source transfer delta versus similarity
across audited groups.
9 Logic Checks
The baseline table includes protocol and variant fields.
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
5

=== PAGE 6 ===
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
6
