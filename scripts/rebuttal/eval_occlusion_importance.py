#!/usr/bin/env python3
"""Occlusion importance evaluation for SilentSpeller models.

This script evaluates how masking parts of the input features changes CER/WER.

Modes
- channel: mask one feature channel at a time (set to 0)
- region:  mask electrode regions (requires raw 124-dim features)

Outputs
- logs/<run_id>/occlusion_channel_importance.csv
- logs/<run_id>/occlusion_region_importance.csv

CSV files start with comment headers (# ...) containing baseline metrics.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import pickle
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader

# Make `src/` importable when running from a fresh checkout without editable install.
import sys


def _ensure_src_on_path() -> None:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        candidate = p / "src"
        if (candidate / "neural_decoder").is_dir():
            sys.path.insert(0, str(candidate))
            return


_ensure_src_on_path()

from neural_decoder.dataset import SpeechDataset
from neural_decoder.neural_decoder_trainer import loadModel


def numeric_to_string(nums: List[int]) -> str:
    return "".join(chr(ord("A") + n - 1) for n in nums if 1 <= n <= 26)


def calculate_edit_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    if len(s2) == 0:
        return len(s1)
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def greedy_decode(logits: torch.Tensor, lengths: torch.Tensor) -> List[List[int]]:
    batch_preds: List[List[int]] = []
    for i in range(logits.size(0)):
        seq_logits = logits[i, : lengths[i]]
        decoded = torch.argmax(seq_logits, dim=-1)
        decoded = torch.unique_consecutive(decoded, dim=-1)
        decoded = decoded[decoded != 0]  # remove blank
        batch_preds.append(decoded.cpu().tolist())
    return batch_preds


def padding_collate(batch):
    X, y, X_lens, y_lens, days = zip(*batch)
    X_padded = pad_sequence(X, batch_first=True, padding_value=0)
    y_padded = pad_sequence(y, batch_first=True, padding_value=0)
    return (
        X_padded,
        y_padded,
        torch.stack(X_lens),
        torch.stack(y_lens),
        torch.stack(days),
    )


def _load_prepare_module(repo_root: Path):
    prepare_py = repo_root / "scripts" / "prepare_silentspeller_dataset.py"
    if not prepare_py.exists():
        raise FileNotFoundError(f"prepare_silentspeller_dataset.py not found at {prepare_py}")
    spec = importlib.util.spec_from_file_location("prepare_silentspeller_dataset", str(prepare_py))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to import {prepare_py}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _evaluate_once(
    *,
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    mask_indices: Optional[Sequence[int]] = None,
    max_samples: Optional[int] = None,
) -> Dict[str, float]:
    total_chars = 0
    total_edits = 0
    total_words = 0
    total_word_errors = 0

    seen = 0
    with torch.no_grad():
        for X, y, X_len, y_len, days in loader:
            X = X.to(device)
            y = y.to(device)
            X_len = X_len.to(device)
            y_len = y_len.to(device)
            days = days.to(device)

            if mask_indices is not None:
                # Mask selected feature channels to 0.
                X[:, :, list(mask_indices)] = 0

            logits = model(X, days)
            adjusted_lens = ((X_len - model.kernelLen) / model.strideLen).to(torch.int32)
            preds = greedy_decode(logits, adjusted_lens)

            for i in range(len(preds)):
                pred_str = numeric_to_string(preds[i])
                true_seq = y[i][: y_len[i]].cpu().numpy().tolist()
                true_str = numeric_to_string(true_seq)

                dist = calculate_edit_distance(pred_str, true_str)
                total_edits += dist
                total_chars += len(true_str)
                total_words += 1
                total_word_errors += int(pred_str != true_str)

                seen += 1
                if max_samples is not None and seen >= max_samples:
                    break
            if max_samples is not None and seen >= max_samples:
                break

    cer = (total_edits / total_chars) if total_chars > 0 else 0.0
    wer = (total_word_errors / total_words) if total_words > 0 else 0.0
    return {
        "cer": float(cer),
        "wer": float(wer),
        "total_chars": float(total_chars),
        "total_edits": float(total_edits),
        "total_words": float(total_words),
        "total_word_errors": float(total_word_errors),
    }


def _write_csv_with_header(
    path: Path,
    *,
    header: Dict[str, str],
    fieldnames: List[str],
    rows: List[Dict[str, str]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        for k in sorted(header.keys()):
            f.write(f"# {k}={header[k]}\n")
        f.write("\n")
        f.write(",".join(fieldnames) + "\n")
        for r in rows:
            f.write(",".join(str(r.get(k, "")) for k in fieldnames) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Occlusion importance evaluation (channel/region).")
    ap.add_argument("--model_path", type=Path, required=True, help="Path like logs/<run_id>")
    ap.add_argument("--dataset_pickle", type=Path, required=True)
    ap.add_argument("--partition", type=str, default="test", choices=["test", "competition"])
    ap.add_argument("--mode", type=str, required=True, choices=["channel", "region"])
    ap.add_argument("--device", type=str, default="cuda")
    ap.add_argument("--batch_size", type=int, default=32)
    ap.add_argument("--max_samples", type=int, default=None, help="If set, evaluate only first N samples (debug).")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve()
    # scripts/rebuttal/eval_occlusion_importance.py -> repo root
    for p in repo_root.parents:
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            repo_root = p
            break

    if not args.model_path.exists():
        raise SystemExit(f"model_path not found: {args.model_path}")
    if not (args.model_path / "args").exists():
        raise SystemExit(f"model args file not found: {args.model_path / 'args'}")
    if not args.dataset_pickle.exists():
        raise SystemExit(f"dataset_pickle not found: {args.dataset_pickle}")

    with open(args.model_path / "args", "rb") as f:
        train_args = pickle.load(f)
    trained_dataset = Path(train_args.get("datasetPath", ""))
    if trained_dataset and trained_dataset != args.dataset_pickle:
        print(
            f"[WARN] dataset_pickle differs from trained datasetPath: trained={trained_dataset} provided={args.dataset_pickle}",
            file=sys.stderr,
        )

    with open(args.dataset_pickle, "rb") as f:
        dataset = pickle.load(f)

    n_days = len(dataset["train"])
    device = torch.device(args.device)
    model = loadModel(str(args.model_path), nInputLayers=n_days, device=device)
    model.eval()

    eval_dataset = SpeechDataset(dataset[args.partition])
    loader = DataLoader(
        eval_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
        collate_fn=padding_collate,
    )

    # Determine feature dim.
    sample_feat_dim = dataset["train"][0]["sentenceDat"][0].shape[1]

    baseline = _evaluate_once(model=model, loader=loader, device=device, mask_indices=None, max_samples=args.max_samples)

    out_rows: List[Dict[str, str]] = []
    out_path: Path

    if args.mode == "channel":
        for ch in range(int(sample_feat_dim)):
            masked = _evaluate_once(model=model, loader=loader, device=device, mask_indices=[ch], max_samples=args.max_samples)
            out_rows.append(
                {
                    "channel": str(ch),
                    "masked_cer": f"{masked['cer']:.6f}",
                    "delta_cer": f"{(masked['cer'] - baseline['cer']):.6f}",
                    "masked_wer": f"{masked['wer']:.6f}",
                    "delta_wer": f"{(masked['wer'] - baseline['wer']):.6f}",
                }
            )

        # Rank by delta_cer (descending)
        deltas = [float(r["delta_cer"]) for r in out_rows]
        order = sorted(range(len(out_rows)), key=lambda i: deltas[i], reverse=True)
        rank_by_idx = {order[i]: i + 1 for i in range(len(order))}
        for i, r in enumerate(out_rows):
            r["delta_cer_rank"] = str(rank_by_idx[i])

        out_rows.sort(key=lambda r: int(r["channel"]))
        out_path = args.model_path / "occlusion_channel_importance.csv"
        fieldnames = ["channel", "masked_cer", "delta_cer", "masked_wer", "delta_wer", "delta_cer_rank"]

    else:
        if int(sample_feat_dim) != 124:
            raise SystemExit(
                f"region mode requires raw 124-dim features (got {sample_feat_dim}). "
                "Use baseline raw runs (n_components=-1, electrode_regions=all)."
            )

        prep = _load_prepare_module(repo_root)
        region_levels = [
            "anterior",
            "middle",
            "posterior",
            "left",
            "right",
            "anterior middle",
            "middle posterior",
            "all",
        ]

        for reg in region_levels:
            idxs = sorted(prep.get_selected_electrodes(reg.split()))
            masked = _evaluate_once(model=model, loader=loader, device=device, mask_indices=idxs, max_samples=args.max_samples)
            out_rows.append(
                {
                    "region": reg,
                    "n_masked_channels": str(len(idxs)),
                    "masked_cer": f"{masked['cer']:.6f}",
                    "delta_cer": f"{(masked['cer'] - baseline['cer']):.6f}",
                    "masked_wer": f"{masked['wer']:.6f}",
                    "delta_wer": f"{(masked['wer'] - baseline['wer']):.6f}",
                }
            )

        deltas = [float(r["delta_cer"]) for r in out_rows]
        order = sorted(range(len(out_rows)), key=lambda i: deltas[i], reverse=True)
        rank_by_idx = {order[i]: i + 1 for i in range(len(order))}
        for i, r in enumerate(out_rows):
            r["delta_cer_rank"] = str(rank_by_idx[i])

        out_path = args.model_path / "occlusion_region_importance.csv"
        fieldnames = [
            "region",
            "n_masked_channels",
            "masked_cer",
            "delta_cer",
            "masked_wer",
            "delta_wer",
            "delta_cer_rank",
        ]

    header = {
        "model_path": str(args.model_path),
        "dataset_pickle": str(args.dataset_pickle),
        "partition": args.partition,
        "mode": args.mode,
        "baseline_cer": f"{baseline['cer']:.6f}",
        "baseline_wer": f"{baseline['wer']:.6f}",
        "n_samples": str(int(baseline["total_words"])),
        "feature_dim": str(int(sample_feat_dim)),
        "device": args.device,
        "batch_size": str(args.batch_size),
        "max_samples": str(args.max_samples) if args.max_samples is not None else "",
    }

    _write_csv_with_header(out_path, header=header, fieldnames=fieldnames, rows=out_rows)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
