#!/usr/bin/env python3
"""Make multi-subject splits (P1/P2/P3) for subj1..subj4 and audit them.

This script is intentionally transparent and fail-fast.
It does NOT run training/evaluation.

What it does
- P1 word-holdout:
  - Ensure subj1 split files exist under the new naming scheme via symlinks.
  - Generate subj2/subj3/subj4 split NPZs (subj3 applies the pinned exclusion list).
- P2 Protocol-S (instance holdout):
  - Keep existing subj1/subj2 split NPZs.
  - Generate subj3 split NPZs using subsample-to-2 construction (exclusions applied).
  - subj4 is excluded (insufficient renditions in raw; see dataset audit).
- P3 Protocol-S cross-subject (XSUB):
  - Keep existing subj1<->subj2.
  - Generate new directions involving subj3 for seed0..3 (exclusions applied for subj3).

Then, audit ALL split NPZs (P1/P2/P3) via da_audit_split_npz.py and write results
under the dataset-audit output directory.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


def _parse_int_list(s: str) -> List[int]:
    out: List[int] = []
    for part in (s or "").split(","):
        part = part.strip()
        if not part:
            continue
        out.append(int(part))
    if not out:
        raise SystemExit("--seeds must be a non-empty comma-separated list")
    return out


def _run(cmd: Sequence[str]) -> None:
    print("[RUN]", " ".join(map(str, cmd)))
    subprocess.run(list(cmd), check=True)


def _ensure_symlink(link_path: Path, target_path: Path) -> None:
    if not target_path.exists():
        raise SystemExit(f"Symlink target missing: {target_path}")

    if link_path.exists() or link_path.is_symlink():
        # Allow if already correct.
        try:
            if link_path.is_symlink() and link_path.resolve() == target_path.resolve():
                return
            if link_path.exists() and link_path.samefile(target_path):
                return
        except Exception:
            pass
        raise SystemExit(f"Refusing to overwrite existing path (not the expected link): {link_path}")

    link_path.parent.mkdir(parents=True, exist_ok=True)
    # Relative symlink within the same directory.
    link_path.symlink_to(target_path.name)


def _maybe_write_default_exclusions(path: Path) -> None:
    if path.exists():
        return
    payload = {
        "dataset_id": "john_2328",
        "exclude_indices": [509, 674, 1631, 1941],
        "reason": "all-zero samples detected in audit; prefer re-export if possible",
        "created_at": _dt.date.today().isoformat(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _raw_paths(raw_dir: Path) -> Dict[str, Path]:
    return {
        "subj1": raw_dir / "p1_2328_old_dataset.npz",
        "subj2": raw_dir / "thad_2328_old_dataset.npz",
        "subj3": raw_dir / "john_2328_dataset.npz",
        "subj4": raw_dir / "su_1167_old_dataset.npz",
    }


def _direction_pairs() -> List[str]:
    return [
        "subj1to2",
        "subj2to1",
        "subj1to3",
        "subj3to1",
        "subj2to3",
        "subj3to2",
    ]


def _direction_to_src_tgt(direction: str) -> Tuple[str, str]:
    m = re.match(r"^subj(?P<src>[1-3])to(?P<tgt>[1-3])$", direction)
    if not m:
        raise ValueError(direction)
    return f"subj{m.group('src')}", f"subj{m.group('tgt')}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Make multi-subject splits (P1/P2/P3) and audit them")
    ap.add_argument("--raw_dir", type=Path, default=Path("raw/silentspeller_dataset"))
    ap.add_argument("--out_dir", type=Path, default=Path("raw_dataset"))
    ap.add_argument("--seeds", type=str, default="0,1,2,3")
    ap.add_argument("--n_competition_words", type=int, default=50)
    ap.add_argument("--n_test_words", type=int, default=50)
    ap.add_argument(
        "--exclude_indices_json_subj3",
        type=Path,
        default=Path("results/dataset_audit_silentspeller_2026-02-24/exclusions/john_2328_exclude_indices.json"),
    )
    ap.add_argument("--smartpalate_csv", type=Path, default=Path("scripts/smartpalate_distribution.csv"))
    ap.add_argument(
        "--audit_out_dir",
        type=Path,
        default=Path("results/dataset_audit_silentspeller_2026-02-24"),
        help="Output directory for split EDA CSVs/figures (reuses dataset audit directory).",
    )
    args = ap.parse_args()

    repo_root = _find_repo_root()
    py = repo_root / ".venv" / "bin" / "python"
    if not py.exists():
        raise SystemExit(f"python not found: {py}")

    raw_dir = args.raw_dir if args.raw_dir.is_absolute() else (repo_root / args.raw_dir)
    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)
    sp_csv = args.smartpalate_csv if args.smartpalate_csv.is_absolute() else (repo_root / args.smartpalate_csv)
    audit_out_dir = args.audit_out_dir if args.audit_out_dir.is_absolute() else (repo_root / args.audit_out_dir)

    seeds = _parse_int_list(args.seeds)

    if not raw_dir.exists():
        raise SystemExit(f"raw_dir not found: {raw_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    excl_subj3 = args.exclude_indices_json_subj3
    excl_subj3 = excl_subj3 if excl_subj3.is_absolute() else (repo_root / excl_subj3)
    _maybe_write_default_exclusions(excl_subj3)

    if not sp_csv.exists():
        raise SystemExit(f"Missing smartpalate CSV: {sp_csv}")

    raw = _raw_paths(raw_dir)
    for k, p in raw.items():
        if not p.exists():
            raise SystemExit(f"Missing raw dataset for {k}: {p}")

    # --- P1: ensure subj1 naming scheme (symlinks) ---
    for seed in seeds:
        base = out_dir / f"train_test_competition_split_seed{seed}.npz"
        link = out_dir / f"train_test_competition_split_seed{seed}_subj1_ds1.npz"
        _ensure_symlink(link, base)

    # --- P1: generate subj2/subj3/subj4 ---
    word_split_py = repo_root / "scripts" / "rebuttal" / "make_word_holdout_split.py"

    for subj in ["subj2", "subj3", "subj4"]:
        for seed in seeds:
            out_npz = out_dir / f"train_test_competition_split_seed{seed}_{subj}_ds1.npz"
            if out_npz.exists():
                continue
            cmd = [
                str(py),
                str(word_split_py),
                "--raw_npz",
                str(raw[subj]),
                "--n_competition_words",
                str(args.n_competition_words),
                "--n_test_words",
                str(args.n_test_words),
                "--seed",
                str(seed),
                "--out_npz",
                str(out_npz),
            ]
            if subj == "subj3":
                cmd += ["--exclude_indices_json", str(excl_subj3)]
            _run(cmd)

    # --- P2: generate subj3 Protocol-S instance-holdout ---
    inst_split_py = repo_root / "scripts" / "rebuttal" / "make_instance_holdout_split.py"

    for subj in ["subj1", "subj2", "subj3"]:
        for seed in seeds:
            out_npz = out_dir / f"protocolS_split_seed{seed}_{subj}_ds1.npz"
            if out_npz.exists():
                continue
            if subj in ("subj1", "subj2"):
                raise SystemExit(f"Expected existing Protocol-S split missing: {out_npz}")
            cmd = [
                str(py),
                str(inst_split_py),
                "--raw_npz",
                str(raw[subj]),
                "--seed",
                str(seed),
                "--n_competition_words",
                str(args.n_competition_words),
                "--out_npz",
                str(out_npz),
                "--exclude_indices_json",
                str(excl_subj3),
            ]
            _run(cmd)

    # --- P3: generate directions over subj1..subj3 ---
    xsub_split_py = repo_root / "scripts" / "rebuttal" / "make_cross_subject_instance_holdout_split.py"

    for direction in _direction_pairs():
        src_subj, tgt_subj = _direction_to_src_tgt(direction)
        if src_subj not in raw or tgt_subj not in raw:
            raise SystemExit(f"Unknown direction subjects: {direction}")
        for seed in seeds:
            out_npz = out_dir / f"protocolSx_split_seed{seed}_{direction}_ds1.npz"
            if out_npz.exists():
                continue
            cmd = [
                str(py),
                str(xsub_split_py),
                "--raw_npz_src",
                str(raw[src_subj]),
                "--raw_npz_tgt",
                str(raw[tgt_subj]),
                "--seed",
                str(seed),
                "--n_competition_words",
                str(args.n_competition_words),
                "--out_npz",
                str(out_npz),
            ]
            if src_subj == "subj3":
                cmd += ["--exclude_indices_json_src", str(excl_subj3)]
            if tgt_subj == "subj3":
                cmd += ["--exclude_indices_json_tgt", str(excl_subj3)]
            _run(cmd)

    # --- Audit all split NPZs ---
    audit_py = repo_root / "scripts" / "rebuttal" / "da_audit_split_npz.py"
    fig_dir = audit_out_dir / "figures" / "protocol_splits"
    fig_dir.mkdir(parents=True, exist_ok=True)

    split_specs: List[Tuple[str, str, int, str, Path]] = []  # (split_id, protocol, seed, subject, path)

    # P1
    for subj in ["subj1", "subj2", "subj3", "subj4"]:
        for seed in seeds:
            split_specs.append(
                (
                    f"P1_{subj}_seed{seed}",
                    "P1",
                    seed,
                    subj,
                    out_dir / f"train_test_competition_split_seed{seed}_{subj}_ds1.npz",
                )
            )

    # P2
    for subj in ["subj1", "subj2", "subj3"]:
        for seed in seeds:
            split_specs.append(
                (
                    f"P2_{subj}_seed{seed}",
                    "P2",
                    seed,
                    subj,
                    out_dir / f"protocolS_split_seed{seed}_{subj}_ds1.npz",
                )
            )

    # P3
    for direction in _direction_pairs():
        for seed in seeds:
            split_specs.append(
                (
                    f"P3_{direction}_seed{seed}",
                    "P3",
                    seed,
                    direction,
                    out_dir / f"protocolSx_split_seed{seed}_{direction}_ds1.npz",
                )
            )

    for _, _, _, _, p in split_specs:
        if not p.exists():
            raise SystemExit(f"Missing split NPZ file: {p}")

    for split_id, protocol, seed, subject, p in split_specs:
        cmd = [
            str(py),
            str(audit_py),
            "--split_npz",
            str(p),
            "--split_id",
            split_id,
            "--protocol",
            protocol,
            "--seed",
            str(seed),
            "--subject",
            subject,
            "--smartpalate_csv",
            str(sp_csv),
            "--out_dir",
            str(audit_out_dir),
            "--fig_dir",
            str(fig_dir),
        ]
        _run(cmd)

    print("[OK] all splits generated + audited")


if __name__ == "__main__":
    main()
