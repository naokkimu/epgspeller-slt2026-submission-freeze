**Reviewable?** yes — **Score:** Weak Accept

**Major issues (novelty/positioning)**
- Related work remains thin at the EPG-SSI “system” level (only one EPG text-entry system cited), which can make novelty look like a single-paper comparison.
- Strengthen framing: controlled test of a common intuition (proxy-grid spatial bias helps), emphasizing negative result (2D conv) + robustness gain (spatial aug) without broad generalization.

**Minor issues**
- Add a parenthetical tying “Open-Vocabulary” to lexicon-free greedy CTC under word-holdout.
- Add an SSI/biosignal review anchor (`lee2021biosignal`).
- Optionally cite EPG multimodal learning beyond text entry (`a8287fa9`).
- Add a scoping sentence in Results that proxy-layout is not true geometry.

**TeX-ready rewrite suggestions (citekeys to add)**
- In Related Work: add `lee2021biosignal` to the SSI overview sentence and optionally add `a8287fa9` as an example of EPG in other ML settings.
- Add “(lexicon-free decoding)” parenthetical when describing word-holdout protocol.
- Add one sentence in Results scope: proxy-layout scope is inductive-bias only.
