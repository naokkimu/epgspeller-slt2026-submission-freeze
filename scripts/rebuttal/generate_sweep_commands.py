#!/usr/bin/env python3
"""
Generate one-command-at-a-time run commands from sweep CSV matrices.

This utility is PM-facing: it does not execute commands.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List


def _load_rows(csv_path: Path) -> List[Dict[str, str]]:
    with csv_path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _dataset_prep_cmd(row: Dict[str, str], python_bin: str) -> str:
    regions = row["electrode_regions"].strip()
    n_components = row["n_components"].strip()
    ds = row["downsample_factor"].strip()
    return (
        f"{python_bin} scripts/prepare_silentspeller_dataset.py "
        f"--split_path {row['split_npz']} "
        f"--n_components {n_components} "
        f"--downsample_factor {ds} "
        f"--electrode_regions {regions} "
        f"--output_path {row['dataset_pickle']}"
    )


def _train_cmd(row: Dict[str, str], python_bin: str) -> str:
    model_family = (row.get("model_family", "") or "gru").strip()
    cmd = [
        f"{python_bin} scripts/train.py",
        f"--dataset_path {row['dataset_pickle']}",
        f"--run_id {row['run_id']}",
        f"--model_family {model_family}",
        f"--n_units {row['n_units']}",
        f"--n_layers {row['n_layers']}",
        f"--stride_len {row['stride_len']}",
        f"--kernel_len {row['kernel_len']}",
        f"--n_batch {row['n_batch']}",
        f"--seed {row['train_seed']}",
        f"--white_noise_sd {row.get('white_noise_sd', '0.8') or '0.8'}",
        f"--constant_offset_sd {row.get('constant_offset_sd', '0.2') or '0.2'}",
        f"--gaussian_smooth_width {row.get('gaussian_smooth_width', '2.0') or '2.0'}",
        "--disable_day_embed",
    ]
    input_proj_dim = row.get("input_proj_dim", "").strip()
    if input_proj_dim:
        cmd.append(f"--input_proj_dim {input_proj_dim}")
    tcn_layers = row.get("tcn_layers", "").strip()
    if tcn_layers:
        cmd.append(f"--tcn_layers {tcn_layers}")
    tcn_kernel_size = row.get("tcn_kernel_size", "").strip()
    if tcn_kernel_size:
        cmd.append(f"--tcn_kernel_size {tcn_kernel_size}")
    transformer_heads = row.get("transformer_heads", "").strip()
    if transformer_heads:
        cmd.append(f"--transformer_heads {transformer_heads}")
    transformer_layers = row.get("transformer_layers", "").strip()
    if transformer_layers:
        cmd.append(f"--transformer_layers {transformer_layers}")
    transformer_ff_mult = row.get("transformer_ff_mult", "").strip()
    if transformer_ff_mult:
        cmd.append(f"--transformer_ff_mult {transformer_ff_mult}")
    if row["specaug_on"].strip() in {"1", "true", "True"}:
        cmd.append("--enable_online_specaug")
    return " ".join(cmd)


def _eval_cmds(row: Dict[str, str], python_bin: str) -> Iterable[str]:
    rid = row["run_id"]
    root = f"logs/{rid}"
    greedy_json = f"{root}/eval_greedy_test.json"
    frame_ms = row.get("frame_ms", "").strip() or "10.0"
    yield (
        f"{python_bin} scripts/rebuttal/eval_greedy_clean.py "
        f"--model_path {root} --partition test --device cuda --frame_ms {frame_ms} --out_json {greedy_json}"
    )
    yield (
        f"{python_bin} scripts/rebuttal/eval_lexicon_project.py "
        f"--pred_json {greedy_json} --lexicon_source train --out_json {root}/eval_lex_train.json"
    )
    yield (
        f"{python_bin} scripts/rebuttal/eval_lexicon_project.py "
        f"--pred_json {greedy_json} --lexicon_source all --out_json {root}/eval_lex_all.json"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate sweep commands from matrix CSV.")
    parser.add_argument("--matrix_csv", type=Path, required=True)
    parser.add_argument("--protocol", type=str, default=None, choices=["P1", "P2", "P3"])
    parser.add_argument("--run_id", type=str, default=None, help="Generate commands for one run only.")
    parser.add_argument("--python_bin", type=str, default=".venv/bin/python")
    args = parser.parse_args()

    rows = _load_rows(args.matrix_csv)
    if args.protocol:
        rows = [r for r in rows if r["protocol"] == args.protocol]
    if args.run_id:
        rows = [r for r in rows if r["run_id"] == args.run_id]

    if not rows:
        raise SystemExit("No rows matched filters.")

    for row in rows:
        print(f"# run_id={row['run_id']}")
        print(_dataset_prep_cmd(row, args.python_bin))
        print(_train_cmd(row, args.python_bin))
        for cmd in _eval_cmds(row, args.python_bin):
            print(cmd)
        print()


if __name__ == "__main__":
    main()
