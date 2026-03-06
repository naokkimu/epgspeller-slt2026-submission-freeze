#!/usr/bin/env python3
"""
Pre-experiment preflight checks for ICASSP/Interspeech ablation runs.

This script is read-only: it validates dataset/split availability and
summarizes split statistics before launching expensive training jobs.
"""

import argparse
from pathlib import Path
from typing import Dict, List

import numpy as np


def _npz_stats(path: Path) -> Dict[str, int]:
    data = np.load(path, allow_pickle=True)
    required = [
        "train_data",
        "train_label",
        "test_data",
        "test_label",
        "competition_data",
        "competition_label",
    ]
    for key in required:
        if key not in data:
            raise KeyError(f"{path} is missing required key: {key}")

    train_labels = np.array([str(x).upper().strip() for x in data["train_label"]], dtype=object)
    test_labels = np.array([str(x).upper().strip() for x in data["test_label"]], dtype=object)
    comp_labels = np.array([str(x).upper().strip() for x in data["competition_label"]], dtype=object)

    return {
        "train_samples": int(len(data["train_data"])),
        "test_samples": int(len(data["test_data"])),
        "competition_samples": int(len(data["competition_data"])),
        "train_vocab": int(len(set(train_labels.tolist()))),
        "test_vocab": int(len(set(test_labels.tolist()))),
        "competition_vocab": int(len(set(comp_labels.tolist()))),
    }


def _exists_or_warn(path: Path, warnings: List[str], label: str) -> bool:
    if path.exists():
        return True
    warnings.append(f"[MISSING] {label}: {path}")
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Preflight checks for ablation experiments.")
    parser.add_argument(
        "--repo_root",
        type=Path,
        default=Path("."),
        help="Repository root (default: current directory).",
    )
    parser.add_argument(
        "--raw_root",
        type=Path,
        default=Path("raw/silentspeller_dataset"),
        help="Root path for raw datasets.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    raw_root = (repo_root / args.raw_root).resolve() if not args.raw_root.is_absolute() else args.raw_root

    raw_dataset_expected = [
        raw_root / "p1_2328_old_dataset.npz",
        raw_root / "thad_2328_old_dataset.npz",
    ]

    split_dir = repo_root / "raw_dataset"
    p1_splits = [split_dir / f"train_test_competition_split_seed{s}.npz" for s in [0, 1, 2, 3]]
    p2_splits = [
        split_dir / f"protocolS_split_seed{s}_subj{subj}_ds1.npz"
        for s in [0, 1, 2, 3]
        for subj in [1, 2]
    ]
    p3_splits = [
        split_dir / "protocolSx_split_seed0_subj1to2_ds1.npz",
        split_dir / "protocolSx_split_seed0_subj2to1_ds1.npz",
    ]

    writable_dirs = [repo_root / "data", repo_root / "logs", repo_root / "sweeps"]

    warnings: List[str] = []
    print("=== Preflight: path checks ===")
    _exists_or_warn(split_dir, warnings, "split directory")
    for p in raw_dataset_expected:
        _exists_or_warn(p, warnings, "raw dataset")
    for p in p1_splits + p2_splits + p3_splits:
        _exists_or_warn(p, warnings, "split file")

    print("\n=== Preflight: writable directories ===")
    for d in writable_dirs:
        d.mkdir(parents=True, exist_ok=True)
        ok = d.exists() and d.is_dir()
        print(f"[{'OK' if ok else 'ERR'}] {d}")
        if not ok:
            warnings.append(f"[DIR] Could not create/access {d}")

    print("\n=== Preflight: split statistics ===")
    for section_name, files in [("P1 word-holdout", p1_splits), ("P2 Protocol-S", p2_splits), ("P3 CrossSubject", p3_splits)]:
        print(f"\n[{section_name}]")
        for f in files:
            if not f.exists():
                print(f"- {f.name}: SKIP (missing)")
                continue
            try:
                st = _npz_stats(f)
            except Exception as exc:  # pragma: no cover - defensive
                warnings.append(f"[BROKEN] {f}: {exc}")
                print(f"- {f.name}: ERROR ({exc})")
                continue
            print(
                f"- {f.name}: "
                f"train/test/comp={st['train_samples']}/{st['test_samples']}/{st['competition_samples']} | "
                f"vocab={st['train_vocab']}/{st['test_vocab']}/{st['competition_vocab']}"
            )

    print("\n=== Summary ===")
    if warnings:
        print("Preflight finished with warnings:")
        for w in warnings:
            print(f"- {w}")
    else:
        print("Preflight passed with no warnings.")


if __name__ == "__main__":
    main()

