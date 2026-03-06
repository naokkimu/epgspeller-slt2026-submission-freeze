# ev_scripts_rebuttal_make_instance_holdout_split_py

- kind: `data`
- path: `scripts/rebuttal/make_instance_holdout_split.py`
- sha256: `07041c24ac0120a854ca55921017f9e628510b7e0b783e8bf74b55f3b6c783e2`
- size_bytes: 10763
- root_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- abs_path_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/scripts/rebuttal/make_instance_holdout_split.py`

## Excerpt

```text
#!/usr/bin/env python3
"""Make instance-holdout splits (Protocol-S: seen-word / instance holdout).

This script defines Protocol-S at the *split* level to support raw datasets that
may have variable renditions per word.

Construction (per word):
- Apply optional exclusions (e.g., known all-zero trials).
- Keep only words with count >= 2.
- Subsample exactly 2 renditions per kept word (deterministic given seed).
- One instance goes to test; the other becomes a train-candidate.
- For early-stopping "competition" split, we move train-candidates for
  n_competition_words words from train to competition (removing them from train).

Outputs an NPZ with keys:
  train_data, train_label, test_data, test_label, competition_data, competition_label

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


def make_instance_holdout_split(
    raw_npz: Path,
    *,
    seed: int,
    n_competition_words: int,
    exclude_indices: Optional[Sequence[int]] = None,
) -> Tuple[Dict[str, np.ndarray], Dict[str, object]]:
    raw = np.load(raw_npz, allow_pickle=True)

    if "data" not in raw:
        raise KeyError(f"raw_npz must contain key data. Available keys: {list(raw.keys())}")
    if "label" in raw:
        raw_labels = raw["label"]
    elif "labels" in raw:
        raw_labels = raw["labels"]
    else:
        raise KeyError(f"raw_npz must contain key label or labels. Available keys: {list(raw.keys())}")

    data_raw = raw["data"]
    labels_raw = np.array([_canonicalize_label(x) for x in raw_labels], dtype=object)

    if len(data_raw) != len(labels_raw):
        raise ValueError(f"len(data) != len(label): {len(data_raw)} vs {len(labels_raw)}")

    orig_indices = np.arange(len(data_raw), dtype=np.int64)

    data, labels, orig_indices = _apply_exclusions(
        data_raw,
        labels_raw,
        orig_indices,
        exclude_indices=list(exclude_indices or []),
        context=str(raw_npz),
    )

    groups = _group_indices_by_label(labels)

    dropped_words: Dict[str, int] = {w: len(idxs) for w, idxs in groups.items() if len(idxs) < 2}
    kept_vocab = sorted([w for w, idxs in groups.items() if len(idxs) >= 2])

    if not kept_vocab:
        raise ValueError("No words with count>=2 after exclusions; cannot construct Protocol-S split.")

    if n_competition_words > len(kept_vocab):
        raise ValueError(
            f"Requested n_competition_words={n_competition_words} but only {len(kept_vocab)} words have count>=2."
        )

    rng = np.random.RandomState(seed)

    train_candidate_idxs: Dict[str, int] = {}
    test_idxs: Dict[str, int] = {}

    # Per-word subsampling to exactly 2 renditions.
    for w in kept_vocab:
        idxs = np.array(groups[w], dtype=np.int64)
        perm = rng.permutation(idxs)
        pick = perm[:2]
        train_candidate_idxs[w] = int(pick[0])
        test_idxs[w] = int(pick[1])

    competition_words = set(_sample_unique_words(kept_vocab, n_competition_words, rng))
    train_word_set = set(kept_vocab) - competition_words

    train_idxs_list = [train_candidate_idxs[w] for w in sorted(train_word_set)]
    competition_idxs_list = [train_candidate_idxs[w] for w in sorted(competition_words)]
    test_idxs_list = [test_idxs[w] for w in kept_vocab]

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
    assert len(test_label) == len(kept_vocab), "Expected exactly one test sample per kept vocabulary word."
    assert len(test_vocab) == len(kept_vocab), "Test vocabulary should cover all kept words exactly once."

    # word-disjointness between train and competition (by construction).
    assert train_vocab.isdisjoint(competition_vocab), "Train and competition vocab should be disjoint."

    # index-level disjointness
    assert set(train_idxs_list).isdisjoint(set(competition_idxs_list))
    assert set(train_idxs_list).isdisjoint(set(test_idxs_list))
    assert set(competition_idxs_list).isdisjoint(set(test_idxs_list))

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
        "n_competition_words": int(n_competition_words),
        "n_samples_raw": int(len(data_raw)),
        "n_samples_after_exclusions": int(len(data)),
        "n_vocab_after_exclusions": int(len(groups)),
        "n_vocab_kept": int(len(kept_vocab)),
        "n_vocab_dropped": int(len(dropped_words)),
        "dropped_words": [
            {"label": w, "count": int(c)} for w, c in sorted(dropped_words.items(), key=lambda kv: (kv[0]))
        ],
        "orig_indices_train": [int(x) for x in sorted(orig_indices[np.array(train_idxs_list, dtype=np.int64)].tolist())],
        "orig_indices_test": [int(x) for x in sorted(orig_indices[np.array(test_idxs_list, dtype=np.int64)].tolist())],
        "orig_indices_competition": [
            int(x) for x in sorted(orig_indices[np.array(competition_idxs_list, dtype=np.int64)].tolist())
        ],
    }

    return splits, meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Make instance-holdout split NPZ (Protocol-S).")
    parser.add_argument("--raw_npz", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--n_competition_words", type=int, default=50)
    parser.add_argument("--out_npz", type=Path, required=True)
    parser.add_argument(
        "--exclude_indices_json",
        type=Path,
        default=None,
        help="Optional JSON containing exclude_indices (0-based) to remove before splitting.",
    )
    args = parser.parse_args()

    repo_root = _find_repo_root()
    exclude = _load_exclude_indices(args.exclude_indices_json)

    splits, meta = make_instance_holdout_split(
        raw_npz=args.raw_npz,
        seed=args.seed,
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
    print(f"Wrote metadata under: {meta_dir}")


if __name__ == "__main__":
    main()
```
