#!/usr/bin/env python3
"""Make additional msx20260224 splits (P3MS + subj3 k-shot) and audit them.

This script is transparent and fail-fast.
It does NOT run training/evaluation.

What it does
- P3MS (2SRC -> 1TGT):
  - seed0..3 for targets {subj1,subj2,subj3} with two remaining subjects as sources:
      subj23to1, subj13to2, subj12to3
- P2K (subj3 k-shot):
  - seed0..3 for k=1 and k=2: protocolSkshot_split_seed{seed}_subj3_k{k}_ds1.npz

Then, audit all generated split NPZs via scripts/rebuttal/da_audit_split_npz.py
using protocol tags P3MS and P2K.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
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


def _p3ms_specs() -> List[Tuple[str, str, str]]:
    # (direction_id, src_a, src_b, tgt) encoded in id.
    return [
        ("subj23to1", "subj2", "subj3", "subj1"),
        ("subj13to2", "subj1", "subj3", "subj2"),
        ("subj12to3", "subj1", "subj2", "subj3"),
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description="Make msx additional splits (P3MS + subj3 k-shot) and audit them")
    ap.add_argument("--raw_dir", type=Path, default=Path("raw/silentspeller_dataset"))
    ap.add_argument("--out_dir", type=Path, default=Path("raw_dataset"))
    ap.add_argument("--seeds", type=str, default="0,1,2,3")
    ap.add_argument("--n_competition_words", type=int, default=50)
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

    # --- P3MS ---
    p3ms_py = repo_root / "scripts" / "rebuttal" / "make_multi_source_cross_subject_instance_holdout_split.py"
    for direction_id, src_a, src_b, tgt in _p3ms_specs():
        for seed in seeds:
            out_npz = out_dir / f"protocolSxms_split_seed{seed}_{direction_id}_ds1.npz"
            if out_npz.exists():
                continue
            cmd = [
                str(py),
                str(p3ms_py),
                "--raw_npz_src_a",
                str(raw[src_a]),
                "--raw_npz_src_b",
                str(raw[src_b]),
                "--raw_npz_tgt",
                str(raw[tgt]),
                "--seed",
                str(seed),
                "--n_competition_words",
                str(args.n_competition_words),
                "--out_npz",
                str(out_npz),
            ]
            if src_a == "subj3":
                cmd += ["--exclude_indices_json_src_a", str(excl_subj3)]
            if src_b == "subj3":
                cmd += ["--exclude_indices_json_src_b", str(excl_subj3)]
            if tgt == "subj3":
                cmd += ["--exclude_indices_json_tgt", str(excl_subj3)]
            _run(cmd)

    # --- k-shot (subj3 only) ---
    kshot_py = repo_root / "scripts" / "rebuttal" / "make_kshot_instance_holdout_split.py"
    for k in (1, 2):
        for seed in seeds:
            out_npz = out_dir / f"protocolSkshot_split_seed{seed}_subj3_k{k}_ds1.npz"
            if out_npz.exists():
                continue
            cmd = [
                str(py),
                str(kshot_py),
                "--raw_npz",
                str(raw["subj3"]),
                "--seed",
                str(seed),
                "--k_train",
                str(k),
                "--n_competition_words",
                str(args.n_competition_words),
                "--out_npz",
                str(out_npz),
                "--exclude_indices_json",
                str(excl_subj3),
            ]
            _run(cmd)

    # --- Audit all new split NPZs ---
    audit_py = repo_root / "scripts" / "rebuttal" / "da_audit_split_npz.py"
    fig_dir = audit_out_dir / "figures" / "protocol_splits"
    fig_dir.mkdir(parents=True, exist_ok=True)

    split_specs: List[Tuple[str, str, int, str, Path]] = []  # (split_id, protocol, seed, subject, path)

    for direction_id, _, _, _ in _p3ms_specs():
        for seed in seeds:
            split_specs.append(
                (
                    f"P3MS_{direction_id}_seed{seed}",
                    "P3MS",
                    seed,
                    direction_id,
                    out_dir / f"protocolSxms_split_seed{seed}_{direction_id}_ds1.npz",
                )
            )

    for k in (1, 2):
        for seed in seeds:
            split_specs.append(
                (
                    f"P2K_subj3_seed{seed}_k{k}",
                    "P2K",
                    seed,
                    "subj3",
                    out_dir / f"protocolSkshot_split_seed{seed}_subj3_k{k}_ds1.npz",
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

    print("[OK] additional splits generated + audited")


if __name__ == "__main__":
    main()

