#!/usr/bin/env python3
"""
Make word-holdout splits for Silent Speller rebuttal experiments.

Outputs an npz with keys:
  train_data, train_label, test_data, test_label, competition_data, competition_label
"""

import argparse
import numpy as np
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


def _group_indices_by_label(labels: Sequence[str]) -> Dict[str, List[int]]:
    groups: Dict[str, List[int]] = {}
    for idx, lab in enumerate(labels):
        groups.setdefault(lab, []).append(idx)
    return groups


def _sample_unique_words(
    words: List[str], n: int, rng: np.random.RandomState
) -> Tuple[List[str], List[str]]:
    """Return (picked, remaining)."""
    if n > len(words):
        raise ValueError(f"Requested {n} words but only {len(words)} available.")
    perm = rng.permutation(words)
    picked = list(perm[:n])
    remaining = list(perm[n:])
    return picked, remaining


def _materialize(
    data: np.ndarray,
    labels: np.ndarray,
    word_list: List[str],
    groups: Dict[str, List[int]],
) -> Tuple[np.ndarray, np.ndarray]:
    idxs: List[int] = []
    for w in word_list:
        idxs.extend(groups[w])
    idxs = sorted(idxs)
    return data[idxs], labels[idxs]


def make_splits(
    raw_npz: Path,
    n_competition_words: int,
    n_test_words: int,
    seed: int,
) -> Dict[str, np.ndarray]:
    raw = np.load(raw_npz, allow_pickle=True)
    data = raw["data"]
    labels = raw["label"]

    groups = _group_indices_by_label(labels)
    vocab = list(groups.keys())
    rng = np.random.RandomState(seed)

    comp_words, remaining = _sample_unique_words(vocab, n_competition_words, rng)
    test_words, train_words = _sample_unique_words(remaining, n_test_words, rng)

    # Materialize partitions
    competition_data, competition_label = _materialize(data, labels, comp_words, groups)
    test_data, test_label = _materialize(data, labels, test_words, groups)
    train_data, train_label = _materialize(data, labels, train_words, groups)

    # Sanity checks: vocab disjointness
    comp_set = set(comp_words)
    test_set = set(test_words)
    train_set = set(train_words)

    assert comp_set.isdisjoint(test_set)
    assert comp_set.isdisjoint(train_set)
    assert test_set.isdisjoint(train_set)

    return {
        "competition_data": competition_data,
        "competition_label": competition_label,
        "test_data": test_data,
        "test_label": test_label,
        "train_data": train_data,
        "train_label": train_label,
    }


def main():
    parser = argparse.ArgumentParser(description="Make word-holdout split npz.")
    parser.add_argument("--raw_npz", type=Path, required=True)
    parser.add_argument("--out_npz", type=Path, required=True)
    parser.add_argument("--n_competition_words", type=int, default=50)
    parser.add_argument("--n_test_words", type=int, default=50)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    splits = make_splits(
        raw_npz=args.raw_npz,
        n_competition_words=args.n_competition_words,
        n_test_words=args.n_test_words,
        seed=args.seed,
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

