#!/usr/bin/env python3
"""Create a subset dataset pickle by slicing feature channels.

This is a transparent, deterministic preprocessing step:
- input: an existing dataset pickle with raw 124-channel features
- output: a new dataset pickle where sentenceDat is sliced to selected channels

No learning happens here.
"""

from __future__ import annotations

import argparse
import pickle
from pathlib import Path
from typing import Dict, List

import numpy as np


def _parse_indices(s: str) -> List[int]:
    parts = [p for p in (s or "").strip().split() if p]
    if not parts:
        raise ValueError("--indices must be a non-empty space-separated list of ints")
    idxs = sorted({int(p) for p in parts})
    return idxs


def _slice_partition(partition: List[Dict], idxs: List[int]) -> List[Dict]:
    out: List[Dict] = []
    for day in partition:
        day_out = dict(day)
        sents = []
        for sample in day["sentenceDat"]:
            arr = np.asarray(sample)
            sents.append(arr[:, idxs])
        day_out["sentenceDat"] = sents
        out.append(day_out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Slice dataset pickle to a channel subset.")
    ap.add_argument("--in_pkl", type=Path, required=True)
    ap.add_argument("--out_pkl", type=Path, required=True)
    ap.add_argument("--subset_id", type=str, required=True)
    ap.add_argument("--indices", type=str, required=True, help='Space-separated channel indices, e.g. "0 5 8".')
    args = ap.parse_args()

    if not args.in_pkl.exists():
        raise SystemExit(f"in_pkl not found: {args.in_pkl}")
    if args.out_pkl.exists():
        raise SystemExit(f"Refusing to overwrite existing out_pkl: {args.out_pkl}")

    idxs = _parse_indices(args.indices)
    if min(idxs) < 0 or max(idxs) > 123:
        raise SystemExit(f"indices out of range [0,123]: min={min(idxs)} max={max(idxs)}")

    with args.in_pkl.open("rb") as f:
        dataset = pickle.load(f)

    if not isinstance(dataset, dict) or "train" not in dataset:
        raise SystemExit(f"Unexpected pickle structure: {args.in_pkl}")

    # Validate input feature dim.
    feat_dim = dataset["train"][0]["sentenceDat"][0].shape[1]
    if int(feat_dim) < max(idxs) + 1:
        raise SystemExit(f"Input feat_dim={feat_dim} is smaller than requested max index={max(idxs)}")

    out = dict(dataset)
    out["train"] = _slice_partition(dataset["train"], idxs)
    out["test"] = _slice_partition(dataset["test"], idxs)
    out["competition"] = _slice_partition(dataset["competition"], idxs)

    proc = dict(out.get("processing_info") or {})
    proc["subset_id"] = args.subset_id
    proc["selected_channel_indices"] = idxs
    proc["source_pkl"] = str(args.in_pkl)
    out["processing_info"] = proc

    args.out_pkl.parent.mkdir(parents=True, exist_ok=True)
    with args.out_pkl.open("wb") as f:
        pickle.dump(out, f)

    print(f"Wrote {args.out_pkl}")
    print(f"subset_id={args.subset_id} K={len(idxs)}")


if __name__ == "__main__":
    main()

