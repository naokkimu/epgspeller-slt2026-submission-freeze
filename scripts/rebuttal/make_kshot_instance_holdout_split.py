#!/usr/bin/env python3
"""Make k-shot instance-holdout splits (Protocol-S variant, within-subject).

Goal: compare k=1 vs k=2 on *exactly the same vocabulary set* for a subject
that has multiple renditions per word (subj3=john_2328).

Construction (per word):
- Load raw dataset.
- Apply optional exclusions (e.g., pinned all-zero trials).
- Keep only words with count >= 3 (this is fixed even for k=1 to keep vocab identical).
- For each kept word, subsample exactly 3 renditions (deterministic given seed): [a, b, c]
  - test = b (fixed)
  - train-candidates = [a] for k=1, [a, c] for k=2
- Sample n_competition_words from kept_vocab and move their train-candidates to competition.

Output NPZ keys:
  train_data, train_label, test_data, test_label, competition_data, competition_label
with:
  - test: 1 instance/word
  - train/competition: k instances/word

Reproducibility metadata (repo-relative, created alongside split output):
- results/protocol_splits_2026-02-24/metadata/<out_npz_stem>.dropped_words.json
- results/protocol_splits_2026-02-24/metadata/<out_npz_stem>.kept_vocab.txt
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


def _canonicalize_label(x) -> str:
    return str(x).upper().strip()


def _load_raw(raw_npz: Path) -> Tuple[np.ndarray, np.ndarray]:
    raw = np.load(raw_npz, allow_pickle=True)
    if "data" not in raw:
        raise KeyError(f"raw_npz must contain key data. Available keys: {list(raw.keys())}")
    if "label" in raw:
        raw_labels = raw["label"]
    elif "labels" in raw:
        raw_labels = raw["labels"]
    else:
        raise KeyError(f"raw_npz must contain key label or labels. Available keys: {list(raw.keys())}")

    data = raw["data"]
    labels = np.array([_canonicalize_label(x) for x in raw_labels], dtype=object)
    if len(data) != len(labels):
        raise ValueError(f"len(data) != len(label): {len(data)} vs {len(labels)}")
    return data, labels


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


def _materialize(data: np.ndarray, labels: np.ndarray, idxs: Sequence[int]) -> Tuple[np.ndarray, np.ndarray]:
    idxs_sorted = np.array(sorted(int(i) for i in idxs), dtype=np.int64)
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


def _apply_exclusions(
    data: np.ndarray,
    labels: np.ndarray,
    orig_indices: np.ndarray,
    *,
    exclude_indices: Sequence[int],
    context: str,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if not exclude_indices:
        return data, labels, orig_indices

    n = len(data)
    bad = [i for i in exclude_indices if (i < 0 or i >= n)]
    if bad:
        raise ValueError(f"exclude index out of range for {context} (n={n}): examples={bad[:10]}")

    keep = np.ones(n, dtype=bool)
    keep[np.array(sorted(set(exclude_indices)), dtype=np.int64)] = False
    return data[keep], labels[keep], orig_indices[keep]


def make_kshot_instance_holdout_split(
    raw_npz: Path,
    *,
    seed: int,
    k_train: int,
    n_competition_words: int,
    exclude_indices: Optional[Sequence[int]] = None,
) -> Tuple[Dict[str, np.ndarray], Dict[str, object]]:
    if k_train not in (1, 2):
        raise ValueError(f"k_train must be 1 or 2, got {k_train}")

    data_raw, labels_raw = _load_raw(raw_npz)
    orig_indices = np.arange(len(data_raw), dtype=np.int64)

    data, labels, orig_indices = _apply_exclusions(
        data_raw,
        labels_raw,
        orig_indices,
        exclude_indices=list(exclude_indices or []),
        context=str(raw_npz),
    )

    groups = _group_indices_by_label(labels)

    dropped_words: Dict[str, int] = {w: len(idxs) for w, idxs in groups.items() if len(idxs) < 3}
    kept_vocab = sorted([w for w, idxs in groups.items() if len(idxs) >= 3])
    if not kept_vocab:
        raise ValueError("No words with count>=3 after exclusions; cannot construct k-shot split.")
    if n_competition_words > len(kept_vocab):
        raise ValueError(
            f"Requested n_competition_words={n_competition_words} but only {len(kept_vocab)} kept words available."
        )

    rng = np.random.RandomState(seed)

    test_idx: Dict[str, int] = {}
    train_candidate_idxs: Dict[str, List[int]] = {}

    for w in kept_vocab:
        idxs = np.array(groups[w], dtype=np.int64)
        perm = rng.permutation(idxs)
        pick3 = perm[:3]
        a = int(pick3[0])
        b = int(pick3[1])
        c = int(pick3[2])
        test_idx[w] = b
        train_candidate_idxs[w] = [a] if k_train == 1 else [a, c]

    competition_words = set(_sample_unique_words(kept_vocab, n_competition_words, rng))
    train_word_set = set(kept_vocab) - competition_words

    train_idxs: List[int] = []
    comp_idxs: List[int] = []
    for w in sorted(train_word_set):
        train_idxs.extend(train_candidate_idxs[w])
    for w in sorted(competition_words):
        comp_idxs.extend(train_candidate_idxs[w])

    test_idxs = [test_idx[w] for w in kept_vocab]

    train_data, train_label = _materialize(data, labels, train_idxs)
    competition_data, competition_label = _materialize(data, labels, comp_idxs)
    test_data, test_label = _materialize(data, labels, test_idxs)

    # Sanity asserts
    train_vocab = set(train_label.tolist())
    comp_vocab = set(competition_label.tolist())
    test_vocab = set(test_label.tolist())

    assert train_vocab.isdisjoint(comp_vocab), "Train and competition vocab must be disjoint."
    assert test_vocab == (train_vocab | comp_vocab), "Seen-word condition violated: test_vocab != train∪comp."
    assert len(test_label) == len(kept_vocab), "Expected exactly one test sample per kept word."

    splits = {
        "train_data": train_data,
        "train_label": train_label,
        "test_data": test_data,
        "test_label": test_label,
        "competition_data": competition_data,
        "competition_label": competition_label,
    }

    meta = {
        "created_at": _dt.date.today().isoformat(),
        "raw_npz": str(raw_npz),
        "seed": int(seed),
        "k_train": int(k_train),
        "n_competition_words": int(n_competition_words),
        "n_samples_raw": int(len(data_raw)),
        "n_samples_after_exclusions": int(len(data)),
        "n_vocab_after_exclusions": int(len(groups)),
        "n_vocab_kept": int(len(kept_vocab)),
        "n_vocab_dropped": int(len(dropped_words)),
        "dropped_words": [{"label": w, "count": int(c)} for w, c in sorted(dropped_words.items(), key=lambda kv: kv[0])],
        "orig_indices_train": [int(x) for x in sorted(orig_indices[np.array(train_idxs, dtype=np.int64)].tolist())],
        "orig_indices_test": [int(x) for x in sorted(orig_indices[np.array(test_idxs, dtype=np.int64)].tolist())],
        "orig_indices_competition": [int(x) for x in sorted(orig_indices[np.array(comp_idxs, dtype=np.int64)].tolist())],
    }

    return splits, meta


def main() -> None:
    ap = argparse.ArgumentParser(description="Make k-shot Protocol-S split NPZ (within-subject).")
    ap.add_argument("--raw_npz", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--k_train", type=int, required=True, choices=[1, 2])
    ap.add_argument("--n_competition_words", type=int, default=50)
    ap.add_argument("--out_npz", type=Path, required=True)
    ap.add_argument("--exclude_indices_json", type=Path, default=None)
    args = ap.parse_args()

    repo_root = _find_repo_root()
    exclude = _load_exclude_indices(args.exclude_indices_json)

    splits, meta = make_kshot_instance_holdout_split(
        raw_npz=args.raw_npz,
        seed=args.seed,
        k_train=args.k_train,
        n_competition_words=args.n_competition_words,
        exclude_indices=exclude,
    )

    args.out_npz.parent.mkdir(parents=True, exist_ok=True)
    np.savez(args.out_npz, **splits)

    meta_dir = repo_root / "results" / "protocol_splits_2026-02-24" / "metadata"
    meta_dir.mkdir(parents=True, exist_ok=True)

    stem = args.out_npz.stem
    (meta_dir / f"{stem}.kept_vocab.txt").write_text(
        "\n".join(sorted(set(splits["test_label"].tolist()))) + "\n", encoding="utf-8"
    )

    meta_out = dict(meta)
    meta_out["out_npz"] = str(args.out_npz)
    meta_out["exclude_indices_json"] = str(args.exclude_indices_json) if args.exclude_indices_json else ""
    meta_out["exclude_indices"] = [int(x) for x in exclude]

    (meta_dir / f"{stem}.dropped_words.json").write_text(
        json.dumps(meta_out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("Saved split to", args.out_npz)
    print(
        f"Sizes: train={len(splits['train_data'])}, test={len(splits['test_data'])}, competition={len(splits['competition_data'])}"
    )
    print(
        f"Vocab sizes: train={len(set(splits['train_label']))}, test={len(set(splits['test_label']))}, competition={len(set(splits['competition_label']))}"
    )
    print(f"Wrote metadata under: {meta_dir}")


if __name__ == "__main__":
    main()

