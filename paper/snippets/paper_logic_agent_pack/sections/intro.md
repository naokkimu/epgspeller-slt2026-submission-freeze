# Introduction (intro)

- pack_index: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/snippets/paper_logic_agent_pack/index.md`
- narrative: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/paper/snippets/paper_logic_agent_pack/narrative.md`

## Blocks
- [b_intro_1](../blocks/b_intro_1.md) kind=`paragraph`
- [b_intro_2](../blocks/b_intro_2.md) kind=`paragraph`
- [b_contrib](../blocks/b_contrib.md) kind=`bullets`

## Narrative

## Introduction (intro)

### [b_intro_1](../blocks/b_intro_1.md) (paragraph)
Silent speech interfaces aim to enable communication without audible acoustics. They use sensor measures of articulation or physiology. Electropalatography provides a practical binary contact form for tongue and palate interaction. Its discrete layout and device variability raise questions about inductive bias, robustness, and how models generalize. ~\\cite{denby2010silent,freitas2017an,gonzalez2020silent,lee2021biosignal}

### [b_intro_2](../blocks/b_intro_2.md) (paragraph)
Recent work on silent spelling has emphasized open-vocabulary text entry, where character level decoding can compose words beyond a fixed closed set. We study open-vocabulary spelling with a CTC style decoder and lexicon projection. We compare vector and layout aware front ends under multiple protocols that test how models generalize across words. ~\\cite{dong2024rehearsse,graves2006connectionist,kimura2022silentspeller}

### [b_contrib](../blocks/b_contrib.md) (bullets)
- We define protocols to evaluate word identity generalization and participant transfer, and we provide split archives with checksums.
- We run multi-participant experiments with open-vocabulary decoding and lexicon projection, tracked by a strict evidence registry.
- We compare a vector baseline with two layout aware front ends, and we report both accuracy and streaming speed metrics.
- We provide deterministic scripts that export compact tables and manifests used by this manuscript.
