- **Reviewable?** yes — **Score:** Weak Reject

**Major issues (novelty/positioning)**
1. **Related work is drastically underdeveloped** (2 sentences, 1 cite). As written, a reviewer cannot place the contribution within SSI/EPG literature, so novelty is not assessable.
2. **Positioning vs prior silent spelling/text-entry is unclear.** You cite SilentSpeller but do not state what is shared vs different (task framing, evaluation protocol, what you “contribute” beyond the baseline framing).
3. **“Open-vocabulary” risks overclaiming** unless explicitly defined as *lexicon-free character-level CTC under word-holdout* (no external lexicon/LM claims).
4. **EPG + “layout-aware proxy grid” lacks grounding.** The proxy mapping/dimensionality/visualization issues are introduced without citing EPG background or EPG representation/data-reduction work, making the mapping feel ad hoc (or implicitly novel).

**Minor issues**
1. Add 1–2 sentences explicitly stating **what you do not claim** (no new hardware, no new electrode geometry, no new objective), preferably in Related Work/Positioning.
2. Add minimal SSI context (one overview/review cite) so readers understand why EPG is one SSI modality among others.
3. Add a citation when first defining EPG in Sec. 1 to avoid “EPG explained from scratch with no anchor”.
4. Use consistent terms: “layout-aware two-dimensional reconstruction” vs “proxy grid” vs “electrode-to-grid proxy layout”.

**Concrete rewrite suggestions (TeX-ready) + citekeys to add**

1) **Abstract (tighten scope of “open-vocabulary”)**  
Replace the first sentence with:
```tex
We study lexicon-free (character-level) silent spelling from electropalatography (EPG) under a word-holdout protocol, and ask whether spatial inductive biases derived from a fixed electrode-to-grid proxy layout improve decoding.
```

2) **Problem setting (ground EPG + representation/data reduction)**  
After the first sentence of Sec. 1, add:
```tex
EPG has long been used to study and visualize tongue--palate contact patterns in phonetic research and speech training (e.g., \cite{hardcastle1989new,hardcastle1990electropalatography,verhoeven2019visualisation}), and prior work has explored EPG data reduction/representation \cite{hardcastle1991epg,carreira1998dimensionality}.
```
Citekeys to add: `hardcastle1989new, hardcastle1990electropalatography, verhoeven2019visualisation, hardcastle1991epg, carreira1998dimensionality`

3) **Replace Sec. 2 “Related work and positioning” with a minimal-but-sufficient paragraph**  
Replace the whole section with:
```tex
\section{Related work and positioning}
Silent speech interfaces (SSI) aim to infer linguistic content without relying on the acoustic speech signal \cite{denby2010silent,gonzalez2020silent,freitas2017an}.
SSI has been explored with multiple sensing modalities, including ultrasound/optical imaging of the tongue and lips \cite{hueber2010development} and implanted magnetic-sensor setups \cite{gilbert2010isolated}; in this work we focus specifically on electropalatography (EPG).
Within EPG-based SSI, silent spelling/text entry has been explored previously (e.g., \cite{kimura2022silentspeller}), and silent spelling has also been studied with other wearable sensors \cite{dong2024rehearsse}.
Our contribution is a controlled EPG representation study: under a fixed word-holdout protocol and a fixed CTC decoder, we isolate the effect of layout-agnostic (vector) versus layout-aware (proxy-grid 2D and row/column) front-ends, and we analyze robustness to fixed electrode dropouts via spatial augmentation.
We therefore scope claims to this protocol and proxy-layout assumption, and do not claim new hardware, a new electrode geometry, or a new decoding objective.
```
Citekeys to add: `denby2010silent, gonzalez2020silent, freitas2017an, hueber2010development, gilbert2010isolated, dong2024rehearsse` (plus existing `kimura2022silentspeller`)
