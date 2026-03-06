#!/usr/bin/env python3
"""Define K=64 electrode subsets for msx20260224.

Inputs
- Per-subject importance CSVs:
    <importance_dir>/subj{1..4}_channel_importance.csv
- SmartPalate map CSV (16x16 proxy):
    scripts/smartpalate_distribution.csv

Outputs
- <out_dir>/k64_subset_defs.json (source of truth)
- <out_dir>/k64_subset_defs.csv  (human-readable)

Definitions (decision complete)
- within_topk64(subjN): top-64 channels by mean_delta_cer (desc)
- within_fps2k64(subjN): farthest-point sampling on SmartPalate coords from top-128 candidate pool (2K)
- transfer_subj1_topk64: within_topk64(subj1)
- random64_seed{seed}: fixed random 64-subset over [0,123]
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import random
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


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
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [ch for _, ch in scored]


def _sorted_unique(xs: Sequence[int]) -> List[int]:
    return sorted(set(int(x) for x in xs))


def _load_smartpalate_coords(csv_path: Path) -> Dict[int, Tuple[int, int]]:
    # Use the same deterministic rules as ed_smartpalate_map.py
    lines = csv_path.read_text(encoding="utf-8-sig").splitlines()
    grid: List[List[int]] = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        grid.append([int(x) for x in s.split(",")])
    if not grid:
        raise ValueError(f"Empty grid: {csv_path}")
    n_cols = len(grid[0])
    if any(len(r) != n_cols for r in grid):
        raise ValueError(f"Non-rectangular grid in {csv_path}")

    coords: Dict[int, Tuple[int, int]] = {}
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v in (-1, 124):
                continue
            if not (0 <= v <= 123):
                continue
            if v not in coords:
                coords[v] = (r, c)
    return coords


def _fps_select(*, candidate_by_importance: Sequence[int], K: int, coords: Dict[int, Tuple[int, int]]) -> List[int]:
    """Farthest-point sampling over coordinates, using importance order for candidate pool."""
    if K <= 0:
        return []

    candidates = list(candidate_by_importance)
    mapped = [ch for ch in candidates if ch in coords]
    unmapped = [ch for ch in candidates if ch not in coords]

    if not mapped:
        return _sorted_unique(candidates[:K])

    selected: List[int] = [mapped[0]]

    def dist2(a: int, b: int) -> float:
        ra, ca = coords[a]
        rb, cb = coords[b]
        dr = float(ra - rb)
        dc = float(ca - cb)
        return dr * dr + dc * dc

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

    # Fill remaining from candidate pool (importance order; includes unmapped).
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


def main() -> None:
    ap = argparse.ArgumentParser(description="Define K=64 subsets for msx20260224")
    ap.add_argument("--importance_dir", type=Path, required=True)
    ap.add_argument("--smartpalate_csv", type=Path, default=Path("scripts/smartpalate_distribution.csv"))
    ap.add_argument("--out_dir", type=Path, default=Path("sweeps/msx20260224/importance"))
    ap.add_argument("--random_seed", type=int, default=20260224)
    args = ap.parse_args()

    repo_root = _find_repo_root()
    importance_dir = args.importance_dir if args.importance_dir.is_absolute() else (repo_root / args.importance_dir)
    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)
    sp_csv = args.smartpalate_csv if args.smartpalate_csv.is_absolute() else (repo_root / args.smartpalate_csv)

    if not importance_dir.exists():
        raise SystemExit(f"importance_dir not found: {importance_dir}")
    if not sp_csv.exists():
        raise SystemExit(f"smartpalate_csv not found: {sp_csv}")

    coords = _load_smartpalate_coords(sp_csv)

    subj_defs: Dict[str, Dict[str, List[int]]] = {}
    for subj in range(1, 5):
        imp_path = importance_dir / f"subj{subj}_channel_importance.csv"
        if not imp_path.exists():
            raise SystemExit(f"Missing importance CSV: {imp_path}")
        rows = _read_importance(imp_path)
        order = _parse_order(rows)
        if len(order) < 64:
            raise SystemExit(f"subj{subj}: importance order too short (got {len(order)})")

        topk64 = _sorted_unique(order[:64])
        cand = order[: min(len(order), 128)]
        fps2k64 = _fps_select(candidate_by_importance=cand, K=64, coords=coords)

        if len(topk64) != 64 or len(fps2k64) != 64:
            raise SystemExit(f"subj{subj}: expected 64 indices but got topk={len(topk64)} fps2k={len(fps2k64)}")

        subj_defs[f"subj{subj}"] = {"topk64": topk64, "fps2k64": fps2k64}

    transfer = list(subj_defs["subj1"]["topk64"])

    rr = random.Random(int(args.random_seed))
    random64 = _sorted_unique(rr.sample(list(range(124)), 64))

    payload = {
        "created_at": _dt.date.today().isoformat(),
        "random_seed": int(args.random_seed),
        "smartpalate_csv": str(args.smartpalate_csv),
        "subjects": subj_defs,
        "transfer_subj1_topk64": transfer,
        "random64_seed20260224": random64,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "k64_subset_defs.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # CSV view
    csv_rows: List[Dict[str, str]] = []
    for subj in range(1, 5):
        sid = f"subj{subj}"
        csv_rows.append(
            {
                "subset_id": f"within_topk64_{sid}",
                "method": "within_topk64",
                "K": "64",
                "subject": sid,
                "indices_space_separated": " ".join(str(i) for i in subj_defs[sid]["topk64"]),
            }
        )
        csv_rows.append(
            {
                "subset_id": f"within_fps2k64_{sid}",
                "method": "within_fps2k64",
                "K": "64",
                "subject": sid,
                "indices_space_separated": " ".join(str(i) for i in subj_defs[sid]["fps2k64"]),
            }
        )
    csv_rows.append(
        {
            "subset_id": "transfer_subj1_topk64",
            "method": "transfer_subj1_topk64",
            "K": "64",
            "subject": "subj1",
            "indices_space_separated": " ".join(str(i) for i in transfer),
        }
    )
    csv_rows.append(
        {
            "subset_id": "random64_seed20260224",
            "method": "random64_seed20260224",
            "K": "64",
            "subject": "",
            "indices_space_separated": " ".join(str(i) for i in random64),
        }
    )

    out_csv = out_dir / "k64_subset_defs.csv"
    with out_csv.open("w", newline="") as f:
        fieldnames = ["subset_id", "method", "K", "subject", "indices_space_separated"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in csv_rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    print(f"[OK] wrote {out_dir / 'k64_subset_defs.json'}")
    print(f"[OK] wrote {out_csv}")


if __name__ == "__main__":
    main()

