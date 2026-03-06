# Review Target (static checker input bundle)

## Metadata

```json
{
  "ai_tools_used": "unknown",
  "paper_type": "regular",
  "pdf": {
    "extracted_chars": 12926,
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
    "sha256": "1aa9019f697cdc0c49f069953b7ea6b88a61a5172b80664750eaec7aa4b5b4d0",
    "sha8": "1aa9019f",
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
    "sha256": "19f1c60ca36fa3f60cd20ae7976749c4fab1b3dd7dac5afce42cf982547fc047",
    "sha8": "19f1c60c"
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
      "extracted_chars": 12926,
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
      "sha256": "1aa9019f697cdc0c49f069953b7ea6b88a61a5172b80664750eaec7aa4b5b4d0",
      "sha8": "1aa9019f",
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
      "sha256": "19f1c60ca36fa3f60cd20ae7976749c4fab1b3dd7dac5afce42cf982547fc047",
      "sha8": "19f1c60c"
    }
  },
  "run_id": "INTSP2026_STATIC_1aa9019f_19f1c60c"
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
union. The cross participant protocol trains on a source partic-62
ipant and evaluates on a target participant under a shared vo-63
cabulary constraint. All split archives used in this study are64
enumerated with sizes and checksums in a manifest artifact.65
Labels are normalized by uppercasing and filtering to al-66
phabet characters, then represented as a space separated charac-67
ter sequence for CTC training and greedy decoding. This nor-68
malization is applied consistently during split construction and69
dataset preparation to avoid vocabulary drift.70
We report character error rate from greedy decoding and71
streaming speed using real time factor, defined as total infer-72
ence time divided by total input duration. For open-vocabulary73
decoding we also report lexicon projection error rates using a74
training lexicon and a full lexicon.75
4. Models76
Our baseline model encodes each frame as a vector of palate77
channels and applies a uni-directional recurrent decoder trained78
with a CTC objective. We compare two layout aware front ends:79
a row and column pooling front end that aggregates a proxy grid80
into one dimensional summaries, and a grid reconstruction front81
end that applies a convolutional spatial encoder. For the grid82
model we optionally enable a spatial augmentation that drops83
and shifts contiguous electrode blocks. [6, 18]84
5. Results85
The baseline recap table summarizes baseline performance un-86
der word holdout, instance holdout, and cross participant trans-87
fer. Lexicon projection reduces error rates relative to greedy88
decoding across protocols, highlighting the importance of open-89
vocabulary post processing for spelling.90

=== PAGE 2 ===
Table 1:Baseline recap across three evaluation protocols
(mean and standard deviation over groups).
protocol variant n cer m cer s lex all m lex all s
P1 vector 4 0.1796 0.0844 0.1018 0.0679
P2 vector 3 0.1451 0.0627 0.0747 0.0476
P3 vector 6 0.6909 0.1332 0.6442 0.0604
Table 2:Spatial modeling comparison at full channels (mean
and standard deviation over groups).
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
The spatial modeling table compares spatial inductive bias91
variants at full channels across protocols. The row and column92
front end tracks the vector baseline more closely than the con-93
volutional grid front end, and the grid front end increases real94
time factor. This trend is consistent with our single participant95
spatial analysis.96
The electrode reduction table evaluates a reduced chan-97
nel budget using several selection strategies. Across protocols,98
within participant selection and simple transfer selection yield99
similar performance, suggesting that a compact subset can pre-100
serve a large fraction of the vector baseline performance.101
6. Discussion102
Our results suggest that an explicit convolutional grid encoder103
is not automatically beneficial for electropalatography, despite104
its intuitive spatial structure. Spatial augmentation can improve105
robustness to synthetic electrode dropout, but it does not close106
the gap in our multi-participant accuracy results. Additional107
analyses on multi-source cross participant transfer and low shot108
adaptation are provided as artifact tables, and they highlight that109
cross participant performance remains challenging.110
7. Artifacts and Auditability111
This repository uses a strict paper registry that pins every ev-112
idence file by checksum and rejects unsupported manuscript113
blocks. The split manifest, aggregated metrics, and compact114
tables referenced in this paper are stored as deterministic ar-115
tifacts, enabling audit and reproduction within our repository116
environment.117
8. Ethics and Disclosure118
We report results only for audited artifacts and do not claim119
broader demographic coverage. The datasets and splits used in120
this study are derived from participant recordings, and we focus121
on methodological clarity and artifact traceability rather than122
Table 3:Electrode reduction methods under a reduced channel
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
deployment claims. 123
9. References124
[1] B. Denby, T. Schultz, K. Honda, T. Hueber, J. Gilbert,125
and J. Brumberg, “Silent speech interfaces,” 2010. [On-126
line]. Available: https://sciencedirect.com/science/article/pii/127
S0167639309001307128
[2] J. Freitas, A. Teixeira, M. S. Dias, and S. Silva,An Introduction129
to Silent Speech Interfaces, 2017. [Online]. Available: https:130
//link.springer.com/book/10.1007/978-3-319-40174-4131
[3] J. A. Gonzalez-Lopez, A. Gomez-Alanis, J. M. Martin Donas,132
J. L. Perez-Cordoba, and A. M. Gomez, “Silent speech interfaces133
for speech restoration: A review,” 2020. [Online]. Available:134
https://ieeexplore.ieee.org/document/9205294/135
[4] W. Lee, J. J. Seong, B. Ozlu, B. S. Shim, A. Marakhimov,136
and S. Lee, “Biosignal sensors and deep learning-based137
speech recognition: A review,” 2021. [Online]. Available:138
https://doi.org/10.3390/s21041399139
[5] X. Dong, Y . Chen, Y . Nishiyama, K. Sezaki, Y . Wang,140
K. Christofferson, and A. Mariakakis, “Rehearsse: Recognizing141
hidden-in-the-ear silently spelled expressions,” 2024. [Online].142
Available: https://dl.acm.org/doi/10.1145/3613904.3642095143
[6] A. Graves, S. Fern ´andez, F. Gomez, and J. Schmidhuber, “Con-144
nectionist temporal classification,” 2006. [Online]. Available:145
https://dl.acm.org/doi/10.1145/1143844.1143891146
[7] N. Kimura, T. Gemicioglu, J. Womack, R. Li, Y . Zhao,147
A. Bedri, Z. Su, A. Olwal, J. Rekimoto, and T. Starner,148
“Silentspeller: Towards mobile, hands-free, silent speech text149
entry using electropalatography,” 2022. [Online]. Available:150
https://dl.acm.org/doi/10.1145/3491102.3502015151
[8] M. ´A. Carreira-Perpi ˜n´an and S. Renals, “Dimensionality152
reduction of electropalatographic data using latent variable153
models,” 1998. [Online]. Available: https://sciencedirect.com/154
science/article/pii/S0167639398000594155
[9] W. Hardcastle, W. Jones, C. Knight, A. Trudgeon, and156
G. Calder, “New developments in electropalatography: A157
state-of-the-art report,” 1989. [Online]. Available: https:158
//doi.org/10.3109/02699208908985268159
[10] W. J. Hardcastle, “Electropalatography in phonetic research160
and in speech training,” 1990. [Online]. Available: https:161
//isca-archive.org/icslp 1990/hardcastle90b icslp.html162
[11] W. Hardcastle, F. Gibbon, and K. Nicolaidis, “Epg data163
reduction methods and their implications for studies of lingual164
coarticulation,” 1991. [Online]. Available: https://doi.org/10.165
1016/S0095-4470(19)30343-2166
[12] T. Hueber, E.-L. Benaroya, G. Chollet, B. Denby, G. Dreyfus,167
and M. Stone, “Development of a silent speech interface driven168

=== PAGE 3 ===
by ultrasound and optical images of the tongue and lips,” 2010.169
[Online]. Available: https://sciencedirect.com/science/article/pii/170
S0167639309001733171
[13] C. H. Shadle, J. N. Carter, T. P. Monks, and J. Field, “Depth172
measurement of face and palate by structured light,” 1993.173
[Online]. Available: https://isca-archive.org/eurospeech 1993/174
shadle93 eurospeech.html175
[14] A. Toutios and K. Margaritis, “Learning electropalatograms from176
acoustics.” [Online]. Available: https://doi.org/10.1109/ICASSP.177
2006.1660032178
[15] ——, “On the acoustic-to-electropalatographic mapping,” 2006.179
[Online]. Available: https://link.springer.com/chapter/10.1007/180
11613107 16181
[16] J. Verhoeven, N. R. Miller, L. Daems, and C. C. Reyes-182
Aldasoro, “Visualisation and analysis of speech production183
with electropalatography,” 2019. [Online]. Available: https:184
//doi.org/10.3390/jimaging5030040185
[17] S.-T. Woo, J.-W. Ha, S. Na, H. Choi, and S.-B. Pyun, “Design186
and evaluation of korean electropalatography (k-epg),” 2021.187
[Online]. Available: https://doi.org/10.3390/s21113802188
[18] D. S. Park, W. Chan, Y . Zhang, C.-C. Chiu, B. Zoph,189
E. D. Cubuk, and Q. V . Le, “Specaugment: A simple data190
augmentation method for automatic speech recognition,” 2019.191
[Online]. Available: https://isca-archive.org/interspeech 2019/192
park19 interspeech.html193
