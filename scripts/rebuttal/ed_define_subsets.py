#!/usr/bin/env python3
"""Define electrode subsets for EPG design experiments (P1, K-curve).

Inputs
- Channel importance CSV produced by ed_aggregate_occlusion.py
- SmartPalate map CSV (16x16 grid) for spatial diversification

Outputs
- sweeps/ed20260217/subsets/P1_subset_defs.csv
  columns: subset_id, method, K, random_seed, indices_space_separated
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import math
import random
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple


K_LIST = [16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120]


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Failed to locate repo root (expected dirs: scripts/, src/).")


def _load_prepare_module(repo_root: Path):
    prepare_py = repo_root / "scripts" / "prepare_silentspeller_dataset.py"
    spec = importlib.util.spec_from_file_location("prepare_silentspeller_dataset", str(prepare_py))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to import {prepare_py}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_smartpalate_map(repo_root: Path, csv_path: Path):
    mod_path = repo_root / "scripts" / "rebuttal" / "ed_smartpalate_map.py"
    spec = importlib.util.spec_from_file_location("ed_smartpalate_map", str(mod_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to import {mod_path}")
    mod = importlib.util.module_from_spec(spec)
    # dataclasses relies on the module being present in sys.modules during exec.
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod.load_map(csv_path)


def _read_importance(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _parse_order(importance_rows: List[Dict[str, str]]) -> List[int]:
    scored: List[Tuple[float, int]] = []
    for r in importance_rows:
        ch_s = (r.get("channel") or "").strip()
        s_s = (r.get("mean_delta_cer") or "").strip()
        if not ch_s or not s_s:
            continue
        ch = int(ch_s)
        score = float(s_s)
        scored.append((score, ch))
    # sort by score desc, then channel asc
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [ch for _, ch in scored]


def _parse_importance_map(importance_rows: List[Dict[str, str]]) -> Dict[int, Dict[str, float]]:
    out: Dict[int, Dict[str, float]] = {}
    for r in importance_rows:
        ch_s = (r.get("channel") or "").strip()
        if not ch_s:
            continue
        ch = int(ch_s)
        out[ch] = {
            "mean_delta_cer": float(r.get("mean_delta_cer") or "nan"),
            "frac_negative": float(r.get("frac_negative") or "nan"),
        }
    return out


def _sorted_unique(indices: Sequence[int]) -> List[int]:
    return sorted(set(int(i) for i in indices))


def _fps_select(
    *,
    candidate_by_importance: Sequence[int],
    K: int,
    coords: Dict[int, Tuple[int, int]],
) -> List[int]:
    """Farthest-point sampling over coordinates, using importance order for candidate pool.

    Strategy:
    - Candidate pool = first 2K channels by importance (passed in)
    - Start from the most important mapped channel.
    - Iteratively add the channel that maximizes the min distance to selected.
    - If mapped candidates are insufficient, fill by remaining candidates in importance order.
    """
    if K <= 0:
        return []

    candidates = list(candidate_by_importance)
    mapped = [ch for ch in candidates if ch in coords]
    unmapped = [ch for ch in candidates if ch not in coords]

    if not mapped:
        # No coordinates: fall back to importance order.
        return _sorted_unique(candidates[:K])

    selected: List[int] = []
    selected.append(mapped[0])

    def dist2(a: int, b: int) -> float:
        ra, ca = coords[a]
        rb, cb = coords[b]
        dr = float(ra - rb)
        dc = float(ca - cb)
        return dr * dr + dc * dc

    mapped_set = set(mapped)
    while len(selected) < min(K, len(mapped)):
        best_ch = None
        best_min_d = -1.0
        sel_set = set(selected)
        for ch in mapped:
            if ch in sel_set:
                continue
            md = min(dist2(ch, s) for s in selected)
            if md > best_min_d:
                best_min_d = md
                best_ch = ch
        if best_ch is None:
            break
        selected.append(best_ch)

    # Fill remaining from candidate pool in importance order (includes unmapped).
    if len(selected) < K:
        sel_set = set(selected)
        for ch in candidates:
            if ch in sel_set:
                continue
            selected.append(ch)
            sel_set.add(ch)
            if len(selected) >= K:
                break

    return _sorted_unique(selected)


def _topk_within(order: Sequence[int], allowed: Set[int], K: int) -> List[int]:
    out: List[int] = []
    for ch in order:
        if ch in allowed:
            out.append(ch)
            if len(out) >= K:
                break
    return _sorted_unique(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Define P1 electrode subsets for design sweeps.")
    ap.add_argument("--importance_csv", type=Path, required=True)
    ap.add_argument("--smartpalate_csv", type=Path, default=Path("scripts/smartpalate_distribution.csv"))
    ap.add_argument("--out_csv", type=Path, default=Path("sweeps/ed20260217/subsets/P1_subset_defs.csv"))
    args = ap.parse_args()

    imp_rows = _read_importance(args.importance_csv)
    if not imp_rows:
        raise SystemExit(f"No rows in importance_csv: {args.importance_csv}")

    order = _parse_order(imp_rows)
    if len(order) < 10:
        raise SystemExit(f"Too few channels in importance order (got {len(order)})")

    imp_map = _parse_importance_map(imp_rows)

    repo_root = _repo_root()
    smartpalate_csv = args.smartpalate_csv
    if not smartpalate_csv.is_absolute():
        smartpalate_csv = repo_root / smartpalate_csv

    # Load spatial map.
    sp = _load_smartpalate_map(repo_root, smartpalate_csv)
    coords = sp.channel_to_rc

    # Load region definitions from prepare script.
    prep = _load_prepare_module(repo_root)
    front_allowed = set(prep.get_selected_electrodes(["anterior", "middle"]))
    post_allowed_strict = set(prep.get_selected_electrodes(["posterior"]))
    post_allowed_wide = set(prep.get_selected_electrodes(["middle", "posterior"]))

    all_ch = list(range(124))

    out_rows: List[Dict[str, str]] = []

    # topK and fps2k K-curve
    for K in K_LIST:
        topk = _sorted_unique(order[:K])
        out_rows.append(
            {
                "subset_id": f"topk_k{K}",
                "method": "topk",
                "K": str(K),
                "random_seed": "",
                "indices_space_separated": " ".join(str(i) for i in topk),
            }
        )

        cand2k = order[: min(len(order), 2 * K)]
        fps = _fps_select(candidate_by_importance=cand2k, K=K, coords=coords)
        out_rows.append(
            {
                "subset_id": f"fps2k_k{K}",
                "method": "fps2k",
                "K": str(K),
                "random_seed": "",
                "indices_space_separated": " ".join(str(i) for i in fps),
            }
        )

        # random replicates
        for r in range(5):
            seed = 1000 + K * 10 + r
            rr = random.Random(seed)
            sample = rr.sample(all_ch, K)
            sample = _sorted_unique(sample)
            out_rows.append(
                {
                    "subset_id": f"rand_k{K}_r{r}",
                    "method": "random",
                    "K": str(K),
                    "random_seed": str(seed),
                    "indices_space_separated": " ".join(str(i) for i in sample),
                }
            )

    # Front/back comparison subsets
    for K in (32, 64):
        front = _topk_within(order, front_allowed, K)
        out_rows.append(
            {
                "subset_id": f"front_topk_k{K}",
                "method": "front_topk",
                "K": str(K),
                "random_seed": "",
                "indices_space_separated": " ".join(str(i) for i in front),
            }
        )

        # Posterior strict may have fewer channels than K (posterior=40 in current definitions).
        allowed = post_allowed_strict if K <= len(post_allowed_strict) else post_allowed_wide
        post = _topk_within(order, allowed, K)
        out_rows.append(
            {
                "subset_id": f"post_topk_k{K}",
                "method": "post_topk",
                "K": str(K),
                "random_seed": "",
                "indices_space_separated": " ".join(str(i) for i in post),
            }
        )

    # Harmful channels pruning: mean_delta_cer <= -0.001 and frac_negative >= 0.75
    harmful: Set[int] = set()
    for ch in all_ch:
        m = imp_map.get(ch)
        if not m:
            continue
        mean = float(m.get("mean_delta_cer", float("nan")))
        frac_neg = float(m.get("frac_negative", float("nan")))
        if math.isnan(mean) or math.isnan(frac_neg):
            continue
        if mean <= -0.001 and frac_neg >= 0.75:
            harmful.add(ch)

    pruned = [ch for ch in all_ch if ch not in harmful]
    pruned = _sorted_unique(pruned)
    out_rows.append(
        {
            "subset_id": "prune_harmful",
            "method": "prune_harmful",
            "K": str(len(pruned)),
            "random_seed": "",
            "indices_space_separated": " ".join(str(i) for i in pruned),
        }
    )

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", newline="") as f:
        fieldnames = ["subset_id", "method", "K", "random_seed", "indices_space_separated"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in out_rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    print(f"Wrote {args.out_csv} ({len(out_rows)} subsets)")
    print(f"harmful_channels={len(harmful)} prune_harmful_K={len(pruned)}")


if __name__ == "__main__":
    main()
