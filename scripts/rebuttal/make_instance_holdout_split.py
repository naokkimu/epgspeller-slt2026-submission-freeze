#!/usr/bin/env python3
"""
Make instance-holdout splits (Protocol-S: seen-word / instance holdout).

Assumption (minimal design for SilentSpeller raw dataset):
  - Each word appears exactly 2 times (2 renditions / word).
  - For each word, one instance goes to test and the other is a train-candidate.
  - For early-stopping "competition" split, we move train-candidates for
    n_competition_words words from train to competition (removing them from train).

Outputs an npz with keys:
  train_data, train_label, test_data, test_label, competition_data, competition_label
"""

import argparse
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np


def _canonicalize_label(x) -> str:
    # Normalize to uppercase to align with downstream greedy decoding / lexicon.
    return str(x).upper().strip()


def _group_indices_by_label(labels: Sequence[str]) -> Dict[str, List[int]]:
    groups: Dict[str, List[int]] = {}
    for idx, lab in enumerate(labels):
        groups.setdefault(lab, []).append(idx)
    return groups


def _sample_unique_words(words: List[str], n: int, rng: np.random.RandomState) -> List[str]:
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}.")
    if n > len(words):
        raise ValueError(f"Requested {n} words but only {len(words)} available.")
    perm = rng.permutation(words)
    return list(perm[:n])


def _materialize(data: np.ndarray, labels: np.ndarray, idxs: List[int]) -> Tuple[np.ndarray, np.ndarray]:
    idxs_sorted = np.array(sorted(idxs), dtype=np.int64)
    return data[idxs_sorted], labels[idxs_sorted]


def make_instance_holdout_split(
    raw_npz: Path,
    seed: int,
    n_competition_words: int,
) -> Dict[str, np.ndarray]:
    raw = np.load(raw_npz, allow_pickle=True)

    if "data" not in raw:
        raise KeyError(f"raw_npz must contain key 'data'. Available keys: {list(raw.keys())}")
    if "label" in raw:
        raw_labels = raw["label"]
    elif "labels" in raw:
        raw_labels = raw["labels"]
    else:
        raise KeyError(f"raw_npz must contain key 'label' or 'labels'. Available keys: {list(raw.keys())}")

    data = raw["data"]
    labels = np.array([_canonicalize_label(x) for x in raw_labels], dtype=object)

    groups = _group_indices_by_label(labels)
    vocab = sorted(groups.keys())
    rng = np.random.RandomState(seed)

    # Assert 2 renditions / word (minimal Protocol-S design).
    bad = {w: len(idxs) for w, idxs in groups.items() if len(idxs) != 2}
    if bad:
        examples = list(sorted(bad.items(), key=lambda kv: (-kv[1], kv[0])))[:10]
        raise ValueError(
            "Protocol-S expects exactly 2 samples per word. "
            f"Found {len(bad)} words violating this. Examples: {examples}"
        )

    train_candidate_idxs: Dict[str, int] = {}
    test_idxs: Dict[str, int] = {}
    for w in vocab:
        idxs = groups[w]
        perm = rng.permutation(idxs)
        train_candidate_idxs[w] = int(perm[0])
        test_idxs[w] = int(perm[1])

    competition_words = set(_sample_unique_words(vocab, n_competition_words, rng))

    train_word_set = set(vocab) - competition_words

    train_idxs_list = [train_candidate_idxs[w] for w in sorted(train_word_set)]
    competition_idxs_list = [train_candidate_idxs[w] for w in sorted(competition_words)]
    test_idxs_list = [test_idxs[w] for w in vocab]

    # Materialize partitions
    train_data, train_label = _materialize(data, labels, train_idxs_list)
    competition_data, competition_label = _materialize(data, labels, competition_idxs_list)
    test_data, test_label = _materialize(data, labels, test_idxs_list)

    # Sanity asserts
    train_vocab = set(train_label.tolist())
    competition_vocab = set(competition_label.tolist())
    test_vocab = set(test_label.tolist())

    # seen-word condition: every test word exists in (train ∪ competition).
    assert test_vocab.issubset(train_vocab.union(competition_vocab))

    # instance holdout: exactly 1 test instance per word.
    assert len(test_label) == len(vocab), "Expected exactly one test sample per vocabulary word."
    assert len(test_vocab) == len(vocab), "Test vocabulary should cover all words exactly once."

    # word-disjointness between train and competition (by construction).
    assert train_vocab.isdisjoint(competition_vocab), "Train and competition vocab should be disjoint."

    # index-level disjointness
    train_set = set(train_idxs_list)
    comp_set = set(competition_idxs_list)
    test_set = set(test_idxs_list)
    assert train_set.isdisjoint(comp_set)
    assert train_set.isdisjoint(test_set)
    assert comp_set.isdisjoint(test_set)

    return {
        "train_data": train_data,
        "train_label": train_label,
        "test_data": test_data,
        "test_label": test_label,
        "competition_data": competition_data,
        "competition_label": competition_label,
    }


def main():
    parser = argparse.ArgumentParser(description="Make instance-holdout split npz (Protocol-S).")
    parser.add_argument("--raw_npz", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--n_competition_words", type=int, default=50)
    parser.add_argument("--out_npz", type=Path, required=True)
    args = parser.parse_args()

    splits = make_instance_holdout_split(
        raw_npz=args.raw_npz,
        seed=args.seed,
        n_competition_words=args.n_competition_words,
    )

    args.out_npz.parent.mkdir(parents=True, exist_ok=True)
    np.savez(args.out_npz, **splits)

    print("Saved split to", args.out_npz)
    print(
        f"Sizes: train={len(splits['train_data'])}, "
        f"test={len(splits['test_data'])}, "
        f"competition={len(splits['competition_data'])}"
    )
    print(
        f"Vocab sizes: train={len(set(splits['train_label']))}, "
        f"test={len(set(splits['test_label']))}, "
        f"competition={len(set(splits['competition_label']))}"
    )


if __name__ == "__main__":
    main()


