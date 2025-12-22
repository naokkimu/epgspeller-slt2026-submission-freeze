#!/usr/bin/env python3
"""
Make cross-subject instance-holdout splits (Protocol-S cross-subject).

Goal (leakage-free preprocessing):
  - Fit scaler/PCA on source TRAIN only.
  - Apply the same transform to source competition and target test (no fitting on target).

Assumptions (minimal design for SilentSpeller raw dataset):
  - Each subject dataset contains exactly 2 samples per word (2 renditions/word).
  - Source and target share the same vocabulary set.

Construction:
  - For each word, pick 1 source instance as train-candidate.
  - Randomly select n_competition_words and move their source train-candidate to competition.
  - For each word, pick 1 target instance as test.

Outputs an npz with keys:
  train_data, train_label, test_data, test_label, competition_data, competition_label
where train/competition come from SRC and test comes from TGT.
"""

import argparse
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np


def _canonicalize_label(x) -> str:
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


def _load_raw(raw_npz: Path) -> Tuple[np.ndarray, np.ndarray]:
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
    return data, labels


def make_cross_subject_instance_holdout_split(
    raw_npz_src: Path,
    raw_npz_tgt: Path,
    seed: int,
    n_competition_words: int,
) -> Dict[str, np.ndarray]:
    src_data, src_labels = _load_raw(raw_npz_src)
    tgt_data, tgt_labels = _load_raw(raw_npz_tgt)

    src_groups = _group_indices_by_label(src_labels)
    tgt_groups = _group_indices_by_label(tgt_labels)

    src_vocab = sorted(src_groups.keys())
    tgt_vocab = sorted(tgt_groups.keys())
    if set(src_vocab) != set(tgt_vocab):
        missing_in_tgt = sorted(set(src_vocab) - set(tgt_vocab))[:10]
        missing_in_src = sorted(set(tgt_vocab) - set(src_vocab))[:10]
        raise ValueError(
            "Source/target vocabulary mismatch. "
            f"missing_in_tgt(examples)={missing_in_tgt} missing_in_src(examples)={missing_in_src}"
        )
    vocab = src_vocab  # canonical ordering

    # Assert 2 renditions / word for both subjects.
    bad_src = {w: len(idxs) for w, idxs in src_groups.items() if len(idxs) != 2}
    bad_tgt = {w: len(idxs) for w, idxs in tgt_groups.items() if len(idxs) != 2}
    if bad_src or bad_tgt:
        raise ValueError(
            "Protocol-S cross-subject expects exactly 2 samples per word for both subjects. "
            f"bad_src={len(bad_src)} bad_tgt={len(bad_tgt)}"
        )

    rng = np.random.RandomState(seed)

    # Per-word instance selection (within subject)
    src_train_candidate: Dict[str, int] = {}
    tgt_test_idx: Dict[str, int] = {}
    for w in vocab:
        src_perm = rng.permutation(src_groups[w])
        tgt_perm = rng.permutation(tgt_groups[w])
        src_train_candidate[w] = int(src_perm[0])
        tgt_test_idx[w] = int(tgt_perm[1])

    competition_words = set(_sample_unique_words(vocab, n_competition_words, rng))
    train_word_set = set(vocab) - competition_words

    train_idxs = [src_train_candidate[w] for w in sorted(train_word_set)]
    competition_idxs = [src_train_candidate[w] for w in sorted(competition_words)]
    test_idxs = [tgt_test_idx[w] for w in vocab]

    train_data, train_label = _materialize(src_data, src_labels, train_idxs)
    competition_data, competition_label = _materialize(src_data, src_labels, competition_idxs)
    test_data, test_label = _materialize(tgt_data, tgt_labels, test_idxs)

    # Sanity asserts
    train_vocab = set(train_label.tolist())
    competition_vocab = set(competition_label.tolist())
    test_vocab = set(test_label.tolist())

    assert len(test_label) == len(vocab), "Expected exactly one test sample per vocabulary word."
    assert len(test_vocab) == len(vocab), "Test vocabulary should cover all words exactly once."
    assert test_vocab.issubset(train_vocab.union(competition_vocab)), "Seen-word condition violated."
    assert train_vocab.isdisjoint(competition_vocab), "Train and competition vocab should be disjoint."

    return {
        "train_data": train_data,
        "train_label": train_label,
        "test_data": test_data,
        "test_label": test_label,
        "competition_data": competition_data,
        "competition_label": competition_label,
    }


def main():
    parser = argparse.ArgumentParser(description="Make cross-subject Protocol-S split npz.")
    parser.add_argument("--raw_npz_src", type=Path, required=True)
    parser.add_argument("--raw_npz_tgt", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--n_competition_words", type=int, default=50)
    parser.add_argument("--out_npz", type=Path, required=True)
    args = parser.parse_args()

    splits = make_cross_subject_instance_holdout_split(
        raw_npz_src=args.raw_npz_src,
        raw_npz_tgt=args.raw_npz_tgt,
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


