## Reviewable?
Yes — **Score: Weak Reject**

## Major issues (clarity/definitions)
1. **Key terms/acronyms are used without definition**, making the method hard to parse quickly (CTC, CER, RTF, FPS, “temporal unfolding operator”, “SpecAugment-inspired masking”, “spatial augmentation”). (MAIN.TEX:36, 46, 60, 62, 65, 96)
2. **Proxy layout mapping is under-specified as a definition**: what exactly is the mapping object (a table/function), what artifact encodes it, and what “aggregated deterministically” means operationally; likewise “masked” and “combined” are not defined at the representation level. (MAIN.TEX:32–34, 52–54)
3. **Word-holdout protocol is only stated, not defined**: “test words are unseen” is not enough to understand the split unit and exclusion rule (e.g., whether *all* examples of a held-out word are excluded) and how this interacts with “open-vocabulary”. (MAIN.TEX:22, 37–38, 59)
4. **Electrode-budgeting and selection heuristics are not defined as procedures**: “TopK” and “FPS-diverse TopK” are described impressionistically; the reader cannot tell what inputs they take or how they produce a subset, nor what “budget” means in the model descriptions (“selected channels”). (MAIN.TEX:52, 62–63)
5. **Streaming RTF is asserted as “slower/faster” without a definition of how it is computed/what is included**, so the speed conclusions are hard to interpret even if the table is correct. (MAIN.TEX:65, 73–74, 84–85)

## Minor issues
- Abstract includes an auditability/process sentence that reads like metadata rather than scientific content. Consider moving it to Sec. 7. (MAIN.TEX:25, 107–110)
- “proxy spatial map” phrasing is vague; define it as a mapping object (e.g., function/table) once, then reuse. (MAIN.TEX:32)
- Line 33 is grammatically dense (“\\DuplicatedChannels mapped channels…”); split into two sentences for readability. (MAIN.TEX:33)
- “temporal backbone produces \\InputProjDim-dimensional…” is slightly awkward; “\\InputProjDim-dim” or “\\InputProjDim-dimensional” but tighten. (MAIN.TEX:45)
- “frame rate at \\FrameMs ms” risks confusion; “frame shift/hop” would be clearer. (MAIN.TEX:60)
- “Grid cells … are masked” should clarify whether this is a value mask, an attention/mask tensor, or both. (MAIN.TEX:53)
- “optionally with the unmapped channels” leaves the reader unsure which variant is reported; state whether unmapped channels are always included for layout-aware models. (MAIN.TEX:56)
- Results prose relies on qualitative adjectives (“worse”, “close”); consider pointing to the specific metric direction per table in one compact clause. (MAIN.TEX:73–74, 84–85)
- Consider adding a citation for the EPG/SmartPalate hardware/layout claim using one of the included EPG-related citekeys, if appropriate. (MAIN.TEX:29–32)

## TeX-ready rewrite suggestions (exact replacements)
1. **Define the proxy mapping more concretely and point to the pinned artifact**
   - Replace MAIN.TEX lines 32–34 with:
```tex
To introduce spatial structure, we define a fixed proxy mapping $\pi$ from SmartPalate channel indices to grid coordinates on a \GridRows$\times$\GridCols grid. The mapping is derived from the pinned SmartPalate distribution snapshot \texttt{\EvSmartpalateDistribution} (\texttt{\ShaSmartpalateDistribution}).
A channel is \emph{mapped} if $\pi(c)$ is defined (\MappedChannels) and \emph{unmapped} otherwise (\UnmappedChannels). When multiple mapped channels share a grid cell (\DuplicatedChannels channels), we resolve the collision deterministically when constructing each grid frame.
This proxy mapping is used only as an inductive bias for layout-aware representations; we do not interpret it as a geometric tongue model.
```

2. **Make the word-holdout definition explicit**
   - Replace MAIN.TEX lines 37–38 with:
```tex
In the word-holdout protocol, training and test sets are disjoint at the word-identity level: all examples of each test word are excluded from training. As a result, greedy CTC decoding is not constrained to a fixed training lexicon.
```

3. **Spell out CTC on first use**
   - Replace MAIN.TEX line 36 with:
```tex
We use a character-level connectionist temporal classification (CTC) formulation~\cite{graves2006connectionist}.
```

4. **Define electrode-budgeting heuristics as procedures (without adding new numeric facts)**
   - Replace MAIN.TEX lines 62–63 with:
```tex
We compare two electrode-selection baselines for budgeted subsets of size $K$: \emph{TopK}, which selects the $K$ highest-ranked channels under an importance score, and \emph{FPS-diverse TopK}, which augments the TopK ranking with a proxy-grid spatial-diversity constraint. We treat both as baselines and do not claim novelty for these heuristics.
```

5. **Expand CER/RTF (and reduce parenthetical repetition)**
   - Replace MAIN.TEX line 65 with:
```tex
We report character error rate (CER) from greedy CTC decoding and streaming real-time factor (RTF); lower is better for both.
```
