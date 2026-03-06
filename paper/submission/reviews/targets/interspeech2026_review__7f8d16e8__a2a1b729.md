# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 15198,
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
      }
    ],
    "page_count": 3,
    "path": "interspeech2026_review.pdf",
    "sha256": "7f8d16e887e7db14a545b44222c5e04ec0c17a29d046889321eee6d4ce0f8b73",
    "sha8": "7f8d16e8",
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
    "sha256": "a2a1b72913ffd91a7155d666bdafc030b6531f7720e5519b3b92828933595131",
    "sha8": "a2a1b729"
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
        "page_count": 3
      },
      "id": "page_limit",
      "message": "page_count=3 <= max_pages=6",
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
      "extracted_chars": 15198,
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
        }
      ],
      "page_count": 3,
      "path": "interspeech2026_review.pdf",
      "sha256": "7f8d16e887e7db14a545b44222c5e04ec0c17a29d046889321eee6d4ce0f8b73",
      "sha8": "7f8d16e8",
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
      "sha256": "a2a1b72913ffd91a7155d666bdafc030b6531f7720e5519b3b92828933595131",
      "sha8": "a2a1b729"
    }
  },
  "run_id": "INTSP2026_STATIC_7f8d16e8_a2a1b729"
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
We evaluate three primary protocols. The word holdout57
protocol uses disjoint vocabularies across train, test, and a com-58
petition partition. The instance holdout protocol evaluates held59
out instances of seen words by separating train and competi-60
tion vocabularies while keeping the test vocabulary within their61
union. The cross participant protocol trains on a source partici-62
pant and evaluates on a target participant under a shared vocab-63
ulary constraint. When a target participant has limited within64
word repetition, we configure the cross participant split genera-65
tors to allow single instance target words while keeping source66
side constraints unchanged. All split archives used in this study67
are enumerated with sizes and checksums in manifest artifacts.68
Labels are normalized by uppercasing and filtering to al-69
phabet characters, then represented as a space separated charac-70
ter sequence for CTC training and greedy decoding. This nor-71
malization is applied consistently during split construction and72
dataset preparation to avoid vocabulary drift.73
We report character error rate from greedy decoding and74
streaming speed using real time factor, defined as total infer-75
ence time divided by total input duration. For open-vocabulary76
decoding we also report lexicon projection error rates using a77
training lexicon and a full lexicon.78
4. Models79
Our baseline model encodes each frame as a vector of palate80
channels and applies a uni-directional recurrent decoder trained81
with a CTC objective. We compare two layout aware front ends:82
a row and column pooling front end that aggregates a proxy grid83
into one dimensional summaries, and a grid reconstruction front84
end that applies a convolutional spatial encoder. For the grid85
model we optionally enable a spatial augmentation that drops86
and shifts contiguous electrode blocks. [6, 18]87
5. Results88
The baseline recap table summarizes baseline performance un-89
der word holdout, instance holdout, and cross participant trans-90

=== PAGE 2 ===
Table 1:Baseline recap across three evaluation protocols
(mean and standard deviation over groups).
protocol variant n cer m cer s lex all m lex all s
P1 vector 4 0.1796 0.0844 0.1018 0.0679
P2 vector 3 0.1451 0.0627 0.0747 0.0476
P3 vector 6 0.6909 0.1332 0.6442 0.0604
Table 2:Cross participant generalization targeting participant
four (direction wise mean and standard deviation over seeds,
plus across direction aggregation).
protocol level group variant n cer m cer s
P3 direction subj1to4 vector 4 0.6660 0.0237
P3 direction subj2to4 vector 4 0.8091 0.0207
P3 direction subj3to4 vector 4 0.5840 0.0180
P3 across directions ALL to4 vector 3 0.6863 0.1139
P3MS direction subj12to4 vector 4 0.6546 0.0161
P3MS direction subj13to4 vector 4 0.5363 0.0089
P3MS direction subj23to4 vector 4 0.5547 0.0046
P3MS across directions ALL to4 vector 3 0.5819 0.0637
fer. Lexicon projection reduces error rates relative to greedy91
decoding across protocols, highlighting the importance of open-92
vocabulary post processing for spelling.93
We additionally evaluate cross participant generalization94
targeting participant four under both single source and multi95
source transfer. The to participant four generalization table96
summarizes direction level seed statistics, and the correspond-97
ing split archives are pinned by checksum in a dedicated mani-98
fest artifact.99
The spatial modeling table compares spatial inductive bias100
variants at full channels across protocols, including a patchpool101
grid encoder as a minimal implementation rescue. The row and102
column front end tracks the vector baseline more closely than103
the convolutional grid front end under within participant pro-104
tocols, while patchpool reduces the gap under cross participant105
transfer. Across protocols, grid variants tend to increase real106
time factor relative to the vector baseline. These trends are con-107
sistent with our single participant spatial analysis.108
The electrode reduction table evaluates a reduced chan-109
nel budget using several selection strategies. Across protocols,110
within participant selection and simple transfer selection yield111
similar performance, suggesting that a compact subset can pre-112
serve a large fraction of the vector baseline performance.113
6. Discussion114
Our results suggest that an explicit convolutional grid encoder115
is not automatically beneficial for electropalatography under116
within participant evaluation, despite its intuitive spatial struc-117
ture. A patchpool grid variant reduces the underperformance of118
the grid encoder under cross participant transfer, indicating that119
spatial encoder design choices can materially affect outcomes,120
but it does not yield consistent gains over the vector baseline121
across protocols. Spatial augmentation can improve robustness122
to synthetic electrode dropout, but it does not close the accuracy123
gap for the convolutional grid variants in our multi participant124
results. Additional analyses on multi source cross participant125
transfer and low shot adaptation are provided as artifact tables,126
and they highlight that cross participant performance remains127
challenging. We also provide a conditions analysis of multi128
source transfer deltas versus simple dataset similarity measures,129
Table 3:Spatial modeling comparison at full channels in-
cluding patchpool variants (mean and standard deviation over
groups).
protocol variant n cer m cer s lex all m lex all s
P1 vector 4 0.1796 0.0844 0.1018 0.0679
P1 rowcol 4 0.2016 0.0886 0.1285 0.0810
P1 spatial2d 4 0.3062 0.1491 0.2536 0.1797
P1 spatial2d aug 4 0.3094 0.1440 0.2605 0.1681
P1 patchpool 4 0.2982 0.0666 0.2373 0.0732
P1 patchpool aug 4 0.2988 0.0891 0.2338 0.0920
P2 vector 3 0.1451 0.0627 0.0747 0.0476
P2 rowcol 3 0.1613 0.0783 0.0893 0.0636
P2 spatial2d 3 0.2894 0.2126 0.2321 0.2530
P2 spatial2d aug 3 0.3139 0.2436 0.2611 0.2879
P2 patchpool 3 0.3384 0.2324 0.2850 0.2689
P2 patchpool aug 3 0.3014 0.1626 0.2438 0.1897
P3 vector 6 0.6909 0.1332 0.6442 0.0604
P3 rowcol 6 0.6828 0.1510 0.6260 0.0850
P3 spatial2d 6 0.7507 0.0897 0.7434 0.0699
P3 spatial2d aug 6 0.7559 0.0920 0.7474 0.0803
P3 patchpool 6 0.6898 0.1103 0.6840 0.0819
P3 patchpool aug 6 0.6992 0.1305 0.6749 0.1076
Table 4:Electrode reduction methods under a reduced channel
budget (mean and standard deviation over groups).
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
which shows that the effect is conditional and does not present130
a single dominant monotonic trend within our evaluated group131
set. 132
7. Artifacts and Auditability133
This repository uses a strict paper registry that pins every ev-134
idence file by checksum and rejects unsupported manuscript135
blocks. The split manifests, aggregated metrics, compact tables,136
and analysis summaries referenced in this paper are stored as137
deterministic artifacts, enabling audit and reproduction within138
our repository environment.139
8. Ethics and Disclosure140
We report results only for audited artifacts and do not claim141
broader demographic coverage. The datasets and splits used in142
this study are derived from participant recordings, and we focus143
on methodological clarity and artifact traceability rather than144
deployment claims. 145

=== PAGE 3 ===
9. References146
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert,147
and J. Brumberg, “Silent speech interfaces,” 2010. [On-148
line]. Available: https://sciencedirect.com/science/article/pii/149
S0167639309001307150
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction151
to Silent Speech Interfaces, 2017. [Online]. Available: https:152
//link.springer.com/book/10.1007/978-3-319-40174-4153
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,154
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces155
for speech restoration: A review,” 2020. [Online]. Available:156
https://ieeexplore.ieee.org/document/9205294/157
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov,158
and S. Lee, “Biosignal sensors and deep learning-based159
speech recognition: A review,” 2021. [Online]. Available:160
https://doi.org/10.3390/s21041399161
[5] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang,162
K. Christofferson, and A. Mariakakis, “Rehearsse: Recognizing163
hidden-in-the-ear silently spelled expressions,” 2024. [Online].164
Available: https://dl.acm.org/doi/10.1145/3613904.3642095165
[6] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-166
nectionist temporal classification,” 2006. [Online]. Available:167
https://dl.acm.org/doi/10.1145/1143844.1143891168
[7] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao,169
A. Bedri, Z. Su, A. Olwal, J. Rekimoto, and T. Starner,170
“Silentspeller: Towards mobile, hands-free, silent speech text171
entry using electropalatography,” 2022. [Online]. Available:172
https://dl.acm.org/doi/10.1145/3491102.3502015173
[8] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality174
reduction of electropalatographic data using latent variable175
models,” 1998. [Online]. Available: https://sciencedirect.com/176
science/article/pii/S0167639398000594177
[9] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and178
G. Calder, “New developments in electropalatography: A179
state-of-the-art report,” 1989. [Online]. Available: https:180
//doi.org/10.3109/02699208908985268181
[10] W. J. Hardcastle, “Electropalatography in phonetic research182
and in speech training,” 1990. [Online]. Available: https:183
//isca-archive.org/icslp 1990/hardcastle90b icslp.html184
[11] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data185
reduction methods and their implications for studies of lingual186
coarticulation,” 1991. [Online]. Available: https://doi.org/10.187
1016/S0095-4470(19)30343-2188
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus,189
and M. Stone, “Development of a silent speech interface driven190
by ultrasound and optical images of the tongue and lips,” 2010.191
[Online]. Available: https://sciencedirect.com/science/article/pii/192
S0167639309001733193
[13] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth194
measurement of face and palate by structured light,” 1993.195
[Online]. Available: https://isca-archive.org/eurospeech 1993/196
shadle93 eurospeech.html197
[14] A. Toutios and K. Margaritis, “Learning electropalatograms from198
acoustics.” [Online]. Available: https://doi.org/10.1109/ICASSP.199
2006.1660032200
[15] ——, “On the acoustic-to-electropalatographic mapping,” 2006.201
[Online]. Available: https://link.springer.com/chapter/10.1007/202
11613107 16203
[16] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-204
Aldasoro, “Visualisation and analysis of speech production205
with electropalatography,” 2019. [Online]. Available: https:206
//doi.org/10.3390/jimaging5030040207
[17] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design208
and evaluation of korean electropalatography (k-epg),” 2021.209
[Online]. Available: https://doi.org/10.3390/s21113802210
[18] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph,211
E. D. Cubuk, and Q. V . Le, “Specaugment: A simple data212
augmentation method for automatic speech recognition,” 2019.213
[Online]. Available: https://isca-archive.org/interspeech 2019/214
park19 interspeech.html215
