#!/usr/bin/env python3
"""
Greedy CTC evaluation for rebuttal numbers (open-vocab, no LM).
"""

import argparse
import json
import pickle
from pathlib import Path
from typing import List, Tuple

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
    """
    logits: [B, T, C]
    lengths: [B] actual time steps after stride adjustment
    """
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


def evaluate(model_path: Path, partition: str, device: str, out_json: Path = None):
    # Load args and dataset
    with open(model_path / "args", "rb") as f:
        args = pickle.load(f)
    with open(args["datasetPath"], "rb") as f:
        dataset = pickle.load(f)

    n_days = len(dataset["train"])
    model = loadModel(str(model_path), nInputLayers=n_days, device=torch.device(device))
    model.eval()

    eval_dataset = SpeechDataset(dataset[partition])
    loader = DataLoader(
        eval_dataset,
        batch_size=32,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
        collate_fn=padding_collate,
    )

    all_preds: List[str] = []
    all_targets: List[str] = []
    total_chars = 0
    total_edits = 0
    total_words = 0
    total_word_errors = 0

    with torch.no_grad():
        for X, y, X_len, y_len, days in loader:
            X = X.to(device)
            y = y.to(device)
            X_len = X_len.to(device)
            y_len = y_len.to(device)
            days = days.to(device)

            logits = model(X, days)
            adjusted_lens = ((X_len - model.kernelLen) / model.strideLen).to(torch.int32)
            preds = greedy_decode(logits, adjusted_lens)

            for i in range(len(preds)):
                pred_str = numeric_to_string(preds[i])
                true_seq = y[i][: y_len[i]].cpu().numpy().tolist()
                true_str = numeric_to_string(true_seq)

                all_preds.append(pred_str)
                all_targets.append(true_str)

                dist = calculate_edit_distance(pred_str, true_str)
                total_edits += dist
                total_chars += len(true_str)
                total_words += 1
                total_word_errors += int(pred_str != true_str)

    cer = total_edits / total_chars if total_chars > 0 else 0.0
    wer = total_word_errors / total_words if total_words > 0 else 0.0

    result = {
        "partition": partition,
        "cer": cer,
        "wer": wer,
        "n_samples": len(all_preds),
        "total_chars": total_chars,
        "total_edits": total_edits,
        "total_words": total_words,
        "total_word_errors": total_word_errors,
        "model_path": str(model_path),
        "dataset_path": args.get("datasetPath"),
        "param_count": args.get("param_count"),
        "seed": args.get("seed"),
        "split_seed": args.get("split_seed"),  # optional if added upstream
        "predictions": all_preds,
        "targets": all_targets,
    }

    if out_json:
        out_json.parent.mkdir(parents=True, exist_ok=True)
        with open(out_json, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Saved results to {out_json}")

    print(f"Partition: {partition}")
    print(f"CER: {cer:.4f}  WER: {wer:.4f}  Samples: {len(all_preds)}")


def parse_args():
    parser = argparse.ArgumentParser(description="Greedy CTC eval (rebuttal clean).")
    parser.add_argument("--model_path", type=Path, required=True)
    parser.add_argument("--partition", type=str, choices=["test", "competition"], default="test")
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--out_json", type=Path, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    cli_args = parse_args()
    evaluate(
        model_path=cli_args.model_path,
        partition=cli_args.partition,
        device=cli_args.device,
        out_json=cli_args.out_json,
    )

