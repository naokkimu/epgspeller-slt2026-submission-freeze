# ev_scripts_rebuttal_make_multi_source_cross_subject_instance_holdout_split_py

- kind: `data`
- path: `scripts/rebuttal/make_multi_source_cross_subject_instance_holdout_split.py`
- sha256: `4b831294d8fab58c02d485c6197ce3fdce4ab8104f7d771417b876dbc7254b34`
- size_bytes: 16396
- root_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- abs_path_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/scripts/rebuttal/make_multi_source_cross_subject_instance_holdout_split.py`

## Excerpt

```text
#!/usr/bin/env python3
"""Make multi-source cross-subject instance-holdout splits (Protocol-S, 2SRC -> 1TGT).

This is a leakage-free split constructor intended for *transparent* cross-subject experiments.
It does NOT perform any preprocessing (scaling/PCA). Those are handled downstream by dataset prep.

Construction (per word):
- Load raw datasets for SRC_A, SRC_B, and TGT.
- Apply optional exclusions independently (e.g., pinned all-zero trials).
- Restrict vocabulary to intersection(SRC_A ∩ SRC_B ∩ TGT).
- Keep only words with count >= 2 in both sources and count >= min_tgt_count in target.
- For each kept word, subsample exactly 2 renditions per dataset (deterministic given seed):
  - SRC_A: pick 1 as train-candidate (other unused)
  - SRC_B: pick 1 as train-candidate (other unused)
  - TGT: pick 1 as test (if >=2 are available we use a fixed "second pick"; if only 1 is
    available and min_tgt_count=1, we use that singleton).
- Sample n_competition_words from kept_vocab and move their train-candidates to competition.

Output NPZ keys:
  train_data, train_label, test_data, test_label, competition_data, competition_label
where:
  - train/competition contain 2 instances per word (one from SRC_A and one from SRC_B)
  - test contains 1 instance per word (from TGT)

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


def make_multi_source_cross_subject_instance_holdout_split(
    raw_npz_src_a: Path,
    raw_npz_src_b: Path,
    raw_npz_tgt: Path,
    *,
    seed: int,
    n_competition_words: int,
    min_tgt_count: int = 2,
    exclude_indices_src_a: Optional[Sequence[int]] = None,
    exclude_indices_src_b: Optional[Sequence[int]] = None,
    exclude_indices_tgt: Optional[Sequence[int]] = None,
) -> Tuple[Dict[str, np.ndarray], Dict[str, object]]:
    src_a_data_raw, src_a_labels_raw = _load_raw(raw_npz_src_a)
    src_b_data_raw, src_b_labels_raw = _load_raw(raw_npz_src_b)
    tgt_data_raw, tgt_labels_raw = _load_raw(raw_npz_tgt)

    src_a_orig = np.arange(len(src_a_data_raw), dtype=np.int64)
    src_b_orig = np.arange(len(src_b_data_raw), dtype=np.int64)
    tgt_orig = np.arange(len(tgt_data_raw), dtype=np.int64)

    src_a_data, src_a_labels, src_a_orig = _apply_exclusions(
        src_a_data_raw,
        src_a_labels_raw,
        src_a_orig,
        exclude_indices=list(exclude_indices_src_a or []),
        context=f"SRC_A:{raw_npz_src_a}",
    )
    src_b_data, src_b_labels, src_b_orig = _apply_exclusions(
        src_b_data_raw,
        src_b_labels_raw,
        src_b_orig,
        exclude_indices=list(exclude_indices_src_b or []),
        context=f"SRC_B:{raw_npz_src_b}",
    )
    tgt_data, tgt_labels, tgt_orig = _apply_exclusions(
        tgt_data_raw,
        tgt_labels_raw,
        tgt_orig,
        exclude_indices=list(exclude_indices_tgt or []),
        context=f"TGT:{raw_npz_tgt}",
    )

    src_a_groups = _group_indices_by_label(src_a_labels)
    src_b_groups = _group_indices_by_label(src_b_labels)
    tgt_groups = _group_indices_by_label(tgt_labels)

    vocab_a = set(src_a_groups.keys())
    vocab_b = set(src_b_groups.keys())
    vocab_t = set(tgt_groups.keys())

    vocab_intersection = sorted(vocab_a & vocab_b & vocab_t)

    if min_tgt_count < 1:
        raise ValueError(f"min_tgt_count must be >= 1, got {min_tgt_count}")

    kept_vocab = sorted(
        [
            w
            for w in vocab_intersection
            if (
                len(src_a_groups[w]) >= 2
                and len(src_b_groups[w]) >= 2
                and len(tgt_groups[w]) >= int(min_tgt_count)
            )
        ]
    )
    if not kept_vocab:
        raise ValueError("No intersection words meeting count constraints after exclusions.")
    if n_competition_words > len(kept_vocab):
        raise ValueError(
            f"Requested n_competition_words={n_competition_words} but only {len(kept_vocab)} kept words available."
        )

    rng = np.random.RandomState(seed)

    src_a_train_candidate: Dict[str, int] = {}
    src_b_train_candidate: Dict[str, int] = {}
    tgt_test_idx: Dict[str, int] = {}

    for w in kept_vocab:
        a_perm = rng.permutation(np.array(src_a_groups[w], dtype=np.int64))
        b_perm = rng.permutation(np.array(src_b_groups[w], dtype=np.int64))
        t_perm = rng.permutation(np.array(tgt_groups[w], dtype=np.int64))

        a_pick = a_perm[:2]
        b_pick = b_perm[:2]
        t_pick = t_perm[:2]

        src_a_train_candidate[w] = int(a_pick[0])
        src_b_train_candidate[w] = int(b_pick[0])
        if len(t_pick) >= 2:
            tgt_test_idx[w] = int(t_pick[1])  # "second pick" fixed for test
        else:
            tgt_test_idx[w] = int(t_pick[0])

    competition_words = set(_sample_unique_words(kept_vocab, n_competition_words, rng))
    train_word_set = set(kept_vocab) - competition_words

    # Two sources -> two instances per word.
    train_idxs_a = [src_a_train_candidate[w] for w in sorted(train_word_set)]
    train_idxs_b = [src_b_train_candidate[w] for w in sorted(train_word_set)]
    comp_idxs_a = [src_a_train_candidate[w] for w in sorted(competition_words)]
    comp_idxs_b = [src_b_train_candidate[w] for w in sorted(competition_words)]
    test_idxs_t = [tgt_test_idx[w] for w in kept_vocab]

    train_a_data, train_a_label = _materialize(src_a_data, src_a_labels, train_idxs_a)
    train_b_data, train_b_label = _materialize(src_b_data, src_b_labels, train_idxs_b)
    comp_a_data, comp_a_label = _materialize(src_a_data, src_a_labels, comp_idxs_a)
    comp_b_data, comp_b_label = _materialize(src_b_data, src_b_labels, comp_idxs_b)
    test_data, test_label = _materialize(tgt_data, tgt_labels, test_idxs_t)

    train_data = np.concatenate([train_a_data, train_b_data], axis=0)
    train_label = np.concatenate([train_a_label, train_b_label], axis=0)
    competition_data = np.concatenate([comp_a_data, comp_b_data], axis=0)
    competition_label = np.concatenate([comp_a_label, comp_b_label], axis=0)

    # Sanity asserts
    train_vocab = set(train_label.tolist())
    comp_vocab = set(competition_label.tolist())
    test_vocab = set(test_label.tolist())

    assert train_vocab.isdisjoint(comp_vocab), "Train and competition vocab must be disjoint (by construction)."
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

    # Dropped reasons (for auditability)
    missing_in_a = sorted((vocab_b & vocab_t) - vocab_a)
    missing_in_b = sorted((vocab_a & vocab_t) - vocab_b)
    missing_in_t = sorted((vocab_a & vocab_b) - vocab_t)

    insufficient_a = {w: len(src_a_groups[w]) for w in vocab_intersection if len(src_a_groups[w]) < 2}
    insufficient_b = {w: len(src_b_groups[w]) for w in vocab_intersection if len(src_b_groups[w]) < 2}
    insufficient_t = {w: len(tgt_groups[w]) for w in vocab_intersection if len(tgt_groups[w]) < int(min_tgt_count)}

    tgt_singleton_used = sorted([w for w in kept_vocab if len(tgt_groups[w]) == 1])

    meta = {
        "created_at": _dt.date.today().isoformat(),
        "raw_npz_src_a": str(raw_npz_src_a),
        "raw_npz_src_b": str(raw_npz_src_b),
        "raw_npz_tgt": str(raw_npz_tgt),
        "seed": int(seed),
        "n_competition_words": int(n_competition_words),
        "min_tgt_count": int(min_tgt_count),
        "n_samples_src_a_raw": int(len(src_a_data_raw)),
        "n_samples_src_b_raw": int(len(src_b_data_raw)),
        "n_samples_tgt_raw": int(len(tgt_data_raw)),
        "n_samples_src_a_after_exclusions": int(len(src_a_data)),
        "n_samples_src_b_after_exclusions": int(len(src_b_data)),
        "n_samples_tgt_after_exclusions": int(len(tgt_data)),
        "n_vocab_src_a_after_exclusions": int(len(vocab_a)),
        "n_vocab_src_b_after_exclusions": int(len(vocab_b)),
        "n_vocab_tgt_after_exclusions": int(len(vocab_t)),
        "n_vocab_intersection": int(len(vocab_intersection)),
        "n_vocab_kept": int(len(kept_vocab)),
        "n_tgt_singleton_words_in_kept_vocab": int(len(tgt_singleton_used)),
        "tgt_singleton_words_in_kept_vocab_examples": tgt_singleton_used[:20],
        "dropped_missing_in_src_a": missing_in_a,
        "dropped_missing_in_src_b": missing_in_b,
        "dropped_missing_in_tgt": missing_in_t,
        "dropped_insufficient_src_a": [
            {"label": w, "count": int(c)} for w, c in sorted(insufficient_a.items(), key=lambda kv: kv[0])
        ],
        "dropped_insufficient_src_b": [
            {"label": w, "count": int(c)} for w, c in sorted(insufficient_b.items(), key=lambda kv: kv[0])
        ],
        "dropped_insufficient_tgt": [
            {"label": w, "count": int(c)} for w, c in sorted(insufficient_t.items(), key=lambda kv: kv[0])
        ],
        "orig_indices_train_src_a": [
            int(x) for x in sorted(src_a_orig[np.array(train_idxs_a, dtype=np.int64)].tolist())
        ],
        "orig_indices_train_src_b": [
            int(x) for x in sorted(src_b_orig[np.array(train_idxs_b, dtype=np.int64)].tolist())
        ],
        "orig_indices_competition_src_a": [
            int(x) for x in sorted(src_a_orig[np.array(comp_idxs_a, dtype=np.int64)].tolist())
        ],
        "orig_indices_competition_src_b": [
            int(x) for x in sorted(src_b_orig[np.array(comp_idxs_b, dtype=np.int64)].tolist())
        ],
        "orig_indices_test_tgt": [int(x) for x in sorted(tgt_orig[np.array(test_idxs_t, dtype=np.int64)].tolist())],
    }

    return splits, meta


def main() -> None:
    ap = argparse.ArgumentParser(description="Make multi-source Protocol-S split NPZ (2SRC -> 1TGT).")
    ap.add_argument("--raw_npz_src_a", type=Path, required=True)
    ap.add_argument("--raw_npz_src_b", type=Path, required=True)
    ap.add_argument("--raw_npz_tgt", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n_competition_words", type=int, default=50)
    ap.add_argument(
        "--min_tgt_count",
        type=int,
        default=2,
        help="Minimum renditions per word required in target. Use 1 to allow singleton target words.",
    )
    ap.add_argument("--out_npz", type=Path, required=True)
    ap.add_argument("--exclude_indices_json_src_a", type=Path, default=None)
    ap.add_argument("--exclude_indices_json_src_b", type=Path, default=None)
    ap.add_argument("--exclude_indices_json_tgt", type=Path, default=None)
    args = ap.parse_args()

    repo_root = _find_repo_root()
    excl_a = _load_exclude_indices(args.exclude_indices_json_src_a)
    excl_b = _load_exclude_indices(args.exclude_indices_json_src_b)
    excl_t = _load_exclude_indices(args.exclude_indices_json_tgt)

    splits, meta = make_multi_source_cross_subject_instance_holdout_split(
        raw_npz_src_a=args.raw_npz_src_a,
        raw_npz_src_b=args.raw_npz_src_b,
        raw_npz_tgt=args.raw_npz_tgt,
        seed=args.seed,
        n_competition_words=args.n_competition_words,
        min_tgt_count=int(args.min_tgt_count),
        exclude_indices_src_a=excl_a,
        exclude_indices_src_b=excl_b,
        exclude_indices_tgt=excl_t,
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
    meta_out["exclude_indices_json_src_a"] = str(args.exclude_indices_json_src_a) if args.exclude_indices_json_src_a else ""
    meta_out["exclude_indices_json_src_b"] = str(args.exclude_indices_json_src_b) if args.exclude_indices_json_src_b else ""
    meta_out["exclude_indices_json_tgt"] = str(args.exclude_indices_json_tgt) if args.exclude_indices_json_tgt else ""
    meta_out["exclude_indices_src_a"] = [int(x) for x in excl_a]
    meta_out["exclude_indices_src_b"] = [int(x) for x in excl_b]
    meta_out["exclude_indices_tgt"] = [int(x) for x in excl_t]

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
```
