# ev_scripts_rebuttal_make_word_holdout_split_py

- kind: `data`
- path: `scripts/rebuttal/make_word_holdout_split.py`
- sha256: `29765a348234ddafcd7c0bb3aeedc3dad1813fa863da921039dcf2b5e4be5065`
- size_bytes: 5817
- root_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- abs_path_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/scripts/rebuttal/make_word_holdout_split.py`

## Excerpt

```text
#!/usr/bin/env python3
"""Make word-holdout splits for SilentSpeller experiments.

Outputs an NPZ with keys:
  train_data, train_label, test_data, test_label, competition_data, competition_label

Notes
- Optional exclusion list supports reproducible removal of known-bad samples
  (e.g., all-zero trials) without rewriting the raw NPZ.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np


def _group_indices_by_label(labels: Sequence[str]) -> Dict[str, List[int]]:
    groups: Dict[str, List[int]] = {}
    for idx, lab in enumerate(labels):
        groups.setdefault(str(lab), []).append(idx)
    return groups


def _sample_unique_words(words: List[str], n: int, rng: np.random.RandomState) -> Tuple[List[str], List[str]]:
    """Return (picked, remaining)."""
    if n < 0:
        raise ValueError(f"Requested n must be non-negative, got {n}.")
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
    idxs_sorted = np.array(sorted(idxs), dtype=np.int64)
    return data[idxs_sorted], labels[idxs_sorted]


def _load_exclude_indices(path: Optional[Path]) -> List[int]:
    if path is None:
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and "exclude_indices" in payload:
        xs = payload["exclude_indices"]
    else:
        xs = payload
    if not isinstance(xs, list):
        raise ValueError(f"exclude_indices_json must be a list or a dict with exclude_indices. Got: {type(xs)}")
    return [int(x) for x in xs]


def make_splits(
    raw_npz: Path,
    *,
    n_competition_words: int,
    n_test_words: int,
    seed: int,
    exclude_indices: Optional[List[int]] = None,
) -> Dict[str, np.ndarray]:
    raw = np.load(raw_npz, allow_pickle=True)
    if "data" not in raw:
        raise KeyError(f"raw_npz must contain key data. Available keys: {list(raw.keys())}")
    if "label" in raw:
        labels = raw["label"]
    elif "labels" in raw:
        labels = raw["labels"]
    else:
        raise KeyError(f"raw_npz must contain key label or labels. Available keys: {list(raw.keys())}")

    data = raw["data"]

    if len(data) != len(labels):
        raise ValueError(f"len(data) != len(label): {len(data)} vs {len(labels)}")

    if exclude_indices:
        n = len(data)
        bad = [i for i in exclude_indices if (i < 0 or i >= n)]
        if bad:
            raise ValueError(f"exclude index out of range for {raw_npz} (n={n}): examples={bad[:10]}")
        keep = np.ones(n, dtype=bool)
        keep[np.array(sorted(set(exclude_indices)), dtype=np.int64)] = False
        data = data[keep]
        labels = labels[keep]

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Make word-holdout split NPZ.")
    parser.add_argument("--raw_npz", type=Path, required=True)
    parser.add_argument("--out_npz", type=Path, required=True)
    parser.add_argument("--n_competition_words", type=int, default=50)
    parser.add_argument("--n_test_words", type=int, default=50)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--exclude_indices_json",
        type=Path,
        default=None,
        help="Optional JSON containing exclude_indices (0-based) to remove before splitting.",
    )
    args = parser.parse_args()

    exclude = _load_exclude_indices(args.exclude_indices_json)
    splits = make_splits(
        raw_npz=args.raw_npz,
        n_competition_words=args.n_competition_words,
        n_test_words=args.n_test_words,
        seed=args.seed,
        exclude_indices=exclude,
    )

    args.out_npz.parent.mkdir(parents=True, exist_ok=True)
    np.savez(args.out_npz, **splits)

    print("Saved split to", args.out_npz)
    if exclude:
        print(f"Applied exclusions: n_excluded={len(exclude)} (exclude_indices_json={args.exclude_indices_json})")
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
```
