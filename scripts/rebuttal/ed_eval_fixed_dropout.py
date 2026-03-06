#!/usr/bin/env python3
"""Evaluate a trained model under a fixed channel-dropout mask.

This simulates electrode failures: for a given drop_rate q and replicate rep,
we sample a fixed subset of feature channels and set them to 0 for all samples.

Outputs:
- logs/<run_id>/eval_dropout_q{q}_rep{rep}.json   (q uses 'p' instead of '.')
"""

from __future__ import annotations

import argparse
import json
import pickle
import random
import time
from pathlib import Path
from typing import Dict, List, Optional, Sequence

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
        decoded = decoded[decoded != 0]
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


def _evaluate(
    *,
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    masked_channels: Optional[Sequence[int]],
) -> Dict[str, float]:
    total_chars = 0
    total_edits = 0
    total_words = 0
    total_word_errors = 0
    total_input_frames = 0
    total_output_chunks = 0
    total_infer_seconds = 0.0

    with torch.no_grad():
        for X, y, X_len, y_len, days in loader:
            X = X.to(device)
            y = y.to(device)
            X_len = X_len.to(device)
            y_len = y_len.to(device)
            days = days.to(device)

            if masked_channels:
                X[:, :, list(masked_channels)] = 0

            if str(device).startswith("cuda"):
                torch.cuda.synchronize()
            t0 = time.perf_counter()
            logits = model(X, days)
            if str(device).startswith("cuda"):
                torch.cuda.synchronize()
            total_infer_seconds += max(0.0, time.perf_counter() - t0)

            adjusted_lens = ((X_len - model.kernelLen) / model.strideLen).to(torch.int32)
            preds = greedy_decode(logits, adjusted_lens)

            total_input_frames += int(X_len.sum().item())
            total_output_chunks += int(adjusted_lens.sum().item())

            for i in range(len(preds)):
                pred_str = numeric_to_string(preds[i])
                true_seq = y[i][: y_len[i]].cpu().numpy().tolist()
                true_str = numeric_to_string(true_seq)

                dist = calculate_edit_distance(pred_str, true_str)
                total_edits += dist
                total_chars += len(true_str)
                total_words += 1
                total_word_errors += int(pred_str != true_str)

    cer = (total_edits / total_chars) if total_chars > 0 else 0.0
    wer = (total_word_errors / total_words) if total_words > 0 else 0.0

    return {
        "cer": float(cer),
        "wer": float(wer),
        "total_words": float(total_words),
        "total_chars": float(total_chars),
        "total_edits": float(total_edits),
        "total_word_errors": float(total_word_errors),
        "total_input_frames": float(total_input_frames),
        "total_output_chunks": float(total_output_chunks),
        "total_infer_seconds": float(total_infer_seconds),
    }


def _q_tag(q: float) -> str:
    s = f"{q:.3f}".rstrip("0").rstrip(".")
    return s.replace(".", "p")


def main() -> None:
    ap = argparse.ArgumentParser(description="Evaluate with fixed channel-dropout mask.")
    ap.add_argument("--model_path", type=Path, required=True, help="logs/<run_id>")
    ap.add_argument("--dataset_pickle", type=Path, required=True)
    ap.add_argument("--partition", type=str, default="test", choices=["test", "competition"])
    ap.add_argument("--device", type=str, default="cuda")
    ap.add_argument("--drop_rate", type=float, required=True)
    ap.add_argument("--rep", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--batch_size", type=int, default=32)
    ap.add_argument("--out_json", type=Path, default=None)
    args = ap.parse_args()

    if not args.model_path.exists():
        raise SystemExit(f"model_path not found: {args.model_path}")
    if not (args.model_path / "args").exists():
        raise SystemExit(f"model args not found: {args.model_path / 'args'}")
    if not args.dataset_pickle.exists():
        raise SystemExit(f"dataset_pickle not found: {args.dataset_pickle}")
    if not (0.0 <= args.drop_rate <= 0.95):
        raise SystemExit("--drop_rate must be in [0,0.95]")
    if args.rep < 0:
        raise SystemExit("--rep must be >=0")

    # Baseline metrics from eval_greedy_test.json if present.
    baseline_cer = None
    baseline_wer = None
    greedy_json = args.model_path / "eval_greedy_test.json"
    if greedy_json.exists():
        payload = json.loads(greedy_json.read_text())
        baseline_cer = payload.get("cer")
        baseline_wer = payload.get("wer")

    with open(args.dataset_pickle, "rb") as f:
        dataset = pickle.load(f)

    feat_dim = int(dataset["train"][0]["sentenceDat"][0].shape[1])
    n_mask = int(args.drop_rate * feat_dim)
    rng = random.Random(args.seed * 1000 + args.rep)
    masked = sorted(rng.sample(list(range(feat_dim)), n_mask)) if n_mask > 0 else []

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

    masked_metrics = _evaluate(model=model, loader=loader, device=device, masked_channels=masked)

    out = {
        "run_id": args.model_path.name,
        "model_path": str(args.model_path),
        "dataset_pickle": str(args.dataset_pickle),
        "partition": args.partition,
        "device": args.device,
        "drop_rate": float(args.drop_rate),
        "rep": int(args.rep),
        "seed": int(args.seed),
        "feature_dim": int(feat_dim),
        "n_masked": int(n_mask),
        "masked_channels": masked,
        "baseline_cer": baseline_cer,
        "baseline_wer": baseline_wer,
        "masked_cer": masked_metrics["cer"],
        "masked_wer": masked_metrics["wer"],
        "delta_cer": (masked_metrics["cer"] - baseline_cer) if baseline_cer is not None else None,
        "delta_wer": (masked_metrics["wer"] - baseline_wer) if baseline_wer is not None else None,
        "n_samples": int(masked_metrics["total_words"]),
        "total_chars": int(masked_metrics["total_chars"]),
        "total_edits": int(masked_metrics["total_edits"]),
        "total_infer_seconds": float(masked_metrics["total_infer_seconds"]),
    }

    if args.out_json is None:
        qtag = _q_tag(args.drop_rate)
        args.out_json = args.model_path / f"eval_dropout_q{qtag}_rep{args.rep}.json"

    if args.out_json.exists():
        raise SystemExit(f"Refusing to overwrite existing out_json: {args.out_json}")

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Wrote {args.out_json}")


if __name__ == "__main__":
    main()

