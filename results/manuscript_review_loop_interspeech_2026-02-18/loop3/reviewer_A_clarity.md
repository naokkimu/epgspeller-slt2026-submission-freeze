**Reviewable?** yes — clarity/definitions score: **4/5**.

**Major issues (<=5)**
- **L32–36**: The “pinned SmartPalate distribution snapshot” → proxy mapping $\pi$ construction is not concretely described (what kind of artifact it is, and how it yields grid coordinates); add one short operational sentence.
- **L33 + L58–62**: Treatment of *unmapped* channels is underspecified/“optional”, making it unclear what each front-end actually consumes and whether comparisons are strictly matched.
- **L67–68**: TopK and FPS-diverse TopK lack minimal operational definitions (“occlusion-derived importance score”, “bounded candidate pool”), so the baseline meaning is not fully reviewable from the text.
- **L51 + L70–73**: “Streaming RTF” risks misinterpretation; the definition is forward-pass time, but “streaming” suggests online/latency constraints. Tighten terminology and measurement description.
- **L21–24 vs L102–105**: Abstract robustness claim is broader than the later definition (fixed evaluation-time dropout masks; “spatial augmentation” defined on proxy grid). Align wording.

**Minor issues (<=10)**
- **L22**: “open-vocabulary” and “lexicon-free (character-level)” overlap; define once and use one term consistently.
- **L23–24**: The abstract’s three-way list is dense; add a brief parenthetical for “row/column compression” (row/column pooling on proxy grid).
- **L30**: First mention of “SmartPalate” could use a one-phrase definition (what it refers to in this paper: device/channel indexing scheme).
- **L34**: Mask channel is introduced but not re-anchored in the model descriptions; remind where it enters the network.
- **L38–39**: “As a result” is not logically tight; better to explicitly state “no lexicon/LM constraint at decoding”.
- **L45**: Terminology drift (“proxy-grid two-dimensional” vs “two-dimensional reconstruction” vs “two-dimensional convolutional front-end”); standardize labels.
- **L51**: “temporal unfolding operator” is jargon; prefer a simpler phrasing (“sliding-window stacking/chunking”) plus one clause.
- **L65**: “SpecAugment-inspired masking” is vague for EPG; specify the axis at a high level (time/channel/grid).
- **L81–82**: Replace “worse/slower” with “higher CER/higher RTF” for precision.
- **L103**: “fixed electrode-dropout masks” could be read as time-varying; one clarifying clause would help.

**TeX-ready rewrite suggestions**
- **Abstract (L22–24)**:
```tex
We study open-vocabulary (character-level) silent spelling from electropalatography (EPG) under a word-holdout protocol (test-word identities excluded from training) and ask whether a fixed proxy electrode-to-grid mapping provides a useful spatial inductive bias for character-level decoding.
We evaluate three EPG front-end representations under matched training conditions: (i) a layout-agnostic channel vector encoder, (ii) a proxy-grid reconstruction consumed by a two-dimensional convolutional front-end, and (iii) row/column pooling on the same proxy grid.
In this setting, the proxy-grid convolutional front-end yields higher greedy CER than the vector baseline and higher forward-pass RTF, while proxy-grid spatial augmentation improves robustness to fixed electrode dropouts.
```

- **Proxy mapping + unmapped channels (L32–35)**:
```tex
To introduce spatial structure, we define a fixed proxy mapping $\pi$ from SmartPalate channel indices to grid coordinates on a $\GridRows\times\GridCols$ proxy grid, derived from the pinned layout snapshot \texttt{\EvSmartpalateDistribution} (\texttt{\ShaSmartpalateDistribution}).
Mapped channels contribute to the proxy grid; channels for which $\pi(c)$ is undefined are treated as \emph{unmapped} and retained as separate non-grid features.
If multiple mapped channels share a grid cell, we aggregate them deterministically by averaging, and we provide an electrode-presence mask as an additional grid channel.
```

- **Word-holdout + decoding (replace L38–39)**:
```tex
In the word-holdout protocol, training and test sets are disjoint at the word-identity level: all examples of each test word are excluded from training.
We decode with greedy CTC and do not apply a lexicon constraint or an external language model.
```

- **TopK/FPS baselines (rewrite L67–68)**:
```tex
We compare two electrode-selection baselines for budgeted subsets of size $K$: \emph{TopK}, which selects the $K$ highest-ranked channels under an occlusion-based importance score (the performance degradation induced by masking a channel), and \emph{FPS-diverse TopK}, which adds a proxy-grid spatial-diversity constraint via farthest-point sampling from a high-scoring candidate pool.
We treat both as baselines and do not claim novelty for these heuristics.
```

- **RTF terminology (rewrite L70)**:
```tex
We report character error rate (CER) from greedy CTC decoding and forward-pass real-time factor (RTF).
```
