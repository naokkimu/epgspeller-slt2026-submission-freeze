#!/usr/bin/env python3
"""Make cross-subject instance-holdout splits (Protocol-S cross-subject / XSUB).

Goal (leakage-free preprocessing; enforced downstream by dataset prep):
- Fit scaler/PCA on source TRAIN only.
- Apply the same transform to source competition and target test (no fitting on target).

This script defines XSUB at the *split* level to support raw datasets that may
have variable renditions per word.

Construction:
- Load SRC and TGT raw datasets.
- Apply optional exclusions independently (e.g., known all-zero trials).
- Restrict vocabulary to intersection (SRC ∩ TGT).
- Keep only words with count >= 2 in SRC and count >= min_tgt_count in TGT.
- For each kept word, subsample exactly 2 renditions per subject (deterministic given seed).
  - SRC: pick 1 as train-candidate (the other unused)
  - TGT: pick 1 as test (if >=2 are available we use a fixed "second pick"; if only 1 is
    available and min_tgt_count=1, we use that singleton).
- Randomly select n_competition_words and move their SRC train-candidate to competition.

Outputs an NPZ with keys:
  train_data, train_label, test_data, test_label, competition_data, competition_label
where train/competition come from SRC and test comes from TGT.

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


def make_cross_subject_instance_holdout_split(
    raw_npz_src: Path,
    raw_npz_tgt: Path,
    *,
    seed: int,
    n_competition_words: int,
    min_tgt_count: int = 2,
    exclude_indices_src: Optional[Sequence[int]] = None,
    exclude_indices_tgt: Optional[Sequence[int]] = None,
) -> Tuple[Dict[str, np.ndarray], Dict[str, object]]:
    src_data_raw, src_labels_raw = _load_raw(raw_npz_src)
    tgt_data_raw, tgt_labels_raw = _load_raw(raw_npz_tgt)

    src_orig_indices = np.arange(len(src_data_raw), dtype=np.int64)
    tgt_orig_indices = np.arange(len(tgt_data_raw), dtype=np.int64)

    src_data, src_labels, src_orig_indices = _apply_exclusions(
        src_data_raw,
        src_labels_raw,
        src_orig_indices,
        exclude_indices=list(exclude_indices_src or []),
        context=f"SRC:{raw_npz_src}",
    )
    tgt_data, tgt_labels, tgt_orig_indices = _apply_exclusions(
        tgt_data_raw,
        tgt_labels_raw,
        tgt_orig_indices,
        exclude_indices=list(exclude_indices_tgt or []),
        context=f"TGT:{raw_npz_tgt}",
    )

    src_groups = _group_indices_by_label(src_labels)
    tgt_groups = _group_indices_by_label(tgt_labels)

    src_vocab = set(src_groups.keys())
    tgt_vocab = set(tgt_groups.keys())

    vocab_intersection = sorted(src_vocab & tgt_vocab)

    if min_tgt_count < 1:
        raise ValueError(f"min_tgt_count must be >= 1, got {min_tgt_count}")

    # Keep only words with >=2 renditions in SRC and >=min_tgt_count in TGT.
    kept_vocab = sorted(
        [w for w in vocab_intersection if (len(src_groups[w]) >= 2 and len(tgt_groups[w]) >= min_tgt_count)]
    )

    if not kept_vocab:
        raise ValueError("No intersection words meeting count constraints after exclusions.")

    if n_competition_words > len(kept_vocab):
        raise ValueError(
            f"Requested n_competition_words={n_competition_words} but only {len(kept_vocab)} kept words available."
        )

    rng = np.random.RandomState(seed)

    src_train_candidate: Dict[str, int] = {}
    tgt_test_idx: Dict[str, int] = {}

    # Per-word subsampling to exactly 2 renditions (per subject).
    for w in kept_vocab:
        src_perm = rng.permutation(np.array(src_groups[w], dtype=np.int64))
        tgt_perm = rng.permutation(np.array(tgt_groups[w], dtype=np.int64))

        src_pick = src_perm[:2]
        tgt_pick = tgt_perm[:2]

        src_train_candidate[w] = int(src_pick[0])
        # Use the second pick for test to mirror the within-subject Protocol-S pattern.
        # If only a singleton exists in TGT (min_tgt_count=1), use it.
        if len(tgt_pick) >= 2:
            tgt_test_idx[w] = int(tgt_pick[1])
        else:
            tgt_test_idx[w] = int(tgt_pick[0])

    competition_words = set(_sample_unique_words(kept_vocab, n_competition_words, rng))
    train_word_set = set(kept_vocab) - competition_words

    train_idxs = [src_train_candidate[w] for w in sorted(train_word_set)]
    competition_idxs = [src_train_candidate[w] for w in sorted(competition_words)]
    test_idxs = [tgt_test_idx[w] for w in kept_vocab]

    train_data, train_label = _materialize(src_data, src_labels, train_idxs)
    competition_data, competition_label = _materialize(src_data, src_labels, competition_idxs)
    test_data, test_label = _materialize(tgt_data, tgt_labels, test_idxs)

    # Sanity asserts
    train_vocab = set(train_label.tolist())
    competition_vocab = set(competition_label.tolist())
    test_vocab = set(test_label.tolist())

    assert len(test_label) == len(kept_vocab), "Expected exactly one test sample per kept vocabulary word."
    assert len(test_vocab) == len(kept_vocab), "Test vocabulary should cover all kept words exactly once."
    assert test_vocab.issubset(train_vocab.union(competition_vocab)), "Seen-word condition violated."
    assert train_vocab.isdisjoint(competition_vocab), "Train and competition vocab should be disjoint."

    splits = {
        "train_data": train_data,
        "train_label": train_label,
        "test_data": test_data,
        "test_label": test_label,
        "competition_data": competition_data,
        "competition_label": competition_label,
    }

    # Dropped reasons (for auditability)
    missing_in_tgt = sorted(src_vocab - tgt_vocab)
    missing_in_src = sorted(tgt_vocab - src_vocab)
    insufficient_src = {w: len(src_groups[w]) for w in vocab_intersection if len(src_groups[w]) < 2}
    insufficient_tgt = {w: len(tgt_groups[w]) for w in vocab_intersection if len(tgt_groups[w]) < min_tgt_count}

    tgt_singleton_used = sorted([w for w in kept_vocab if len(tgt_groups[w]) == 1])

    meta = {
        "created_at": _dt.date.today().isoformat(),
        "raw_npz_src": str(raw_npz_src),
        "raw_npz_tgt": str(raw_npz_tgt),
        "seed": int(seed),
        "n_competition_words": int(n_competition_words),
        "min_tgt_count": int(min_tgt_count),
        "n_samples_src_raw": int(len(src_data_raw)),
        "n_samples_tgt_raw": int(len(tgt_data_raw)),
        "n_samples_src_after_exclusions": int(len(src_data)),
        "n_samples_tgt_after_exclusions": int(len(tgt_data)),
        "n_vocab_src_after_exclusions": int(len(src_vocab)),
        "n_vocab_tgt_after_exclusions": int(len(tgt_vocab)),
        "n_vocab_intersection": int(len(vocab_intersection)),
        "n_vocab_kept": int(len(kept_vocab)),
        "n_tgt_singleton_words_in_kept_vocab": int(len(tgt_singleton_used)),
        "tgt_singleton_words_in_kept_vocab_examples": tgt_singleton_used[:20],
        "dropped_missing_in_tgt": missing_in_tgt,
        "dropped_missing_in_src": missing_in_src,
        "dropped_insufficient_src": [
            {"label": w, "count": int(c)} for w, c in sorted(insufficient_src.items(), key=lambda kv: kv[0])
        ],
        "dropped_insufficient_tgt": [
            {"label": w, "count": int(c)} for w, c in sorted(insufficient_tgt.items(), key=lambda kv: kv[0])
        ],
        "orig_indices_train_src": [
            int(x) for x in sorted(src_orig_indices[np.array(train_idxs, dtype=np.int64)].tolist())
        ],
        "orig_indices_competition_src": [
            int(x) for x in sorted(src_orig_indices[np.array(competition_idxs, dtype=np.int64)].tolist())
        ],
        "orig_indices_test_tgt": [int(x) for x in sorted(tgt_orig_indices[np.array(test_idxs, dtype=np.int64)].tolist())],
    }

    return splits, meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Make cross-subject Protocol-S split NPZ (XSUB).")
    parser.add_argument("--raw_npz_src", type=Path, required=True)
    parser.add_argument("--raw_npz_tgt", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--n_competition_words", type=int, default=50)
    parser.add_argument(
        "--min_tgt_count",
        type=int,
        default=2,
        help="Minimum renditions per word required in target. Use 1 to allow singleton target words.",
    )
    parser.add_argument("--out_npz", type=Path, required=True)
    parser.add_argument(
        "--exclude_indices_json_src",
        type=Path,
        default=None,
        help="Optional JSON containing exclude_indices (0-based) to remove from SRC before splitting.",
    )
    parser.add_argument(
        "--exclude_indices_json_tgt",
        type=Path,
        default=None,
        help="Optional JSON containing exclude_indices (0-based) to remove from TGT before splitting.",
    )
    args = parser.parse_args()

    repo_root = _find_repo_root()
    excl_src = _load_exclude_indices(args.exclude_indices_json_src)
    excl_tgt = _load_exclude_indices(args.exclude_indices_json_tgt)

    splits, meta = make_cross_subject_instance_holdout_split(
        raw_npz_src=args.raw_npz_src,
        raw_npz_tgt=args.raw_npz_tgt,
        seed=args.seed,
        n_competition_words=args.n_competition_words,
        min_tgt_count=int(args.min_tgt_count),
        exclude_indices_src=excl_src,
        exclude_indices_tgt=excl_tgt,
    )

    args.out_npz.parent.mkdir(parents=True, exist_ok=True)
    np.savez(args.out_npz, **splits)

    meta_dir = repo_root / "results" / "protocol_splits_2026-02-24" / "metadata"
    meta_dir.mkdir(parents=True, exist_ok=True)

    stem = args.out_npz.stem
    (meta_dir / f"{stem}.kept_vocab.txt").write_text(
        "\n".join(sorted(set(splits['test_label'].tolist()))) + "\n", encoding="utf-8"
    )

    meta_out = dict(meta)
    meta_out["out_npz"] = str(args.out_npz)
    meta_out["exclude_indices_json_src"] = str(args.exclude_indices_json_src) if args.exclude_indices_json_src else ""
    meta_out["exclude_indices_json_tgt"] = str(args.exclude_indices_json_tgt) if args.exclude_indices_json_tgt else ""
    meta_out["exclude_indices_src"] = [int(x) for x in excl_src]
    meta_out["exclude_indices_tgt"] = [int(x) for x in excl_tgt]

    (meta_dir / f"{stem}.dropped_words.json").write_text(
        json.dumps(meta_out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("Saved split to", args.out_npz)
    if excl_src:
        print(f"Applied SRC exclusions: n_excluded={len(excl_src)} (exclude_indices_json_src={args.exclude_indices_json_src})")
    if excl_tgt:
        print(f"Applied TGT exclusions: n_excluded={len(excl_tgt)} (exclude_indices_json_tgt={args.exclude_indices_json_tgt})")
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
    print(f"Wrote metadata under: {meta_dir}")


if __name__ == "__main__":
    main()
