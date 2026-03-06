#!/usr/bin/env python3
from __future__ import annotations

"""Export a deterministic manifest (path/size/sha256) for split NPZ archives referenced by msx metrics.

This is evidence-only:
- Inputs are existing artifacts (metrics CSV + split NPZ files).
- No new learning/evaluation is performed.
"""

import argparse
import csv
import hashlib
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames))
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def main() -> None:
    ap = argparse.ArgumentParser(description="Export split NPZ manifest from msx metrics.")
    ap.add_argument(
        "--repo_root",
        type=Path,
        default=Path("."),
        help="Repo root (used to resolve split_npz paths).",
    )
    ap.add_argument(
        "--metrics_csv",
        type=Path,
        default=Path("sweeps/msx20260224/results/msx_all_metrics.csv"),
        help="Aggregated metrics CSV (must contain split_npz/protocol/split_id).",
    )
    ap.add_argument(
        "--out_csv",
        type=Path,
        default=Path("results/msx20260224/split_npz_manifest.csv"),
        help="Output CSV path.",
    )
    args = ap.parse_args()

    repo_root = args.repo_root.expanduser().resolve()
    metrics_csv = args.metrics_csv if args.metrics_csv.is_absolute() else (repo_root / args.metrics_csv)
    out_csv = args.out_csv if args.out_csv.is_absolute() else (repo_root / args.out_csv)

    if not metrics_csv.is_file():
        raise SystemExit(f"metrics_csv not found: {metrics_csv}")

    rows = _read_csv(metrics_csv)
    if not rows:
        raise SystemExit(f"metrics_csv is empty: {metrics_csv}")

    required_cols = ["protocol", "split_id", "split_npz"]
    missing = [c for c in required_cols if c not in rows[0]]
    if missing:
        raise SystemExit(f"metrics_csv missing columns: {missing}")

    # Deterministic: keep the first occurrence for metadata, de-duplicate by split_npz.
    first_by_npz: Dict[str, Tuple[str, str]] = {}
    for r in rows:
        rel = (r.get("split_npz") or "").strip()
        prot = (r.get("protocol") or "").strip()
        split_id = (r.get("split_id") or "").strip()
        if not rel or not prot or not split_id:
            raise SystemExit(f"metrics_csv contains empty required field(s): split_npz={rel!r} protocol={prot!r} split_id={split_id!r}")
        first_by_npz.setdefault(rel, (prot, split_id))

    out_rows: List[Dict[str, object]] = []
    for rel in sorted(first_by_npz.keys()):
        prot, split_id = first_by_npz[rel]
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts:
            raise SystemExit(f"split_npz path must be relative and safe: {rel}")
        abs_path = (repo_root / p).resolve()
        try:
            abs_path.relative_to(repo_root)
        except Exception:
            raise SystemExit(f"split_npz escapes repo_root: {rel}")
        if not abs_path.is_file():
            raise SystemExit(f"split_npz file missing: {rel} (resolved: {abs_path})")

        out_rows.append(
            {
                "protocol": prot,
                "split_id": split_id,
                "split_npz": rel,
                "size_bytes": abs_path.stat().st_size,
                "sha256": _sha256_file(abs_path),
            }
        )

    _write_csv(
        out_csv,
        out_rows,
        fieldnames=["protocol", "split_id", "split_npz", "size_bytes", "sha256"],
    )
    print(f"[OK] wrote: {out_csv}")


if __name__ == "__main__":
    main()

