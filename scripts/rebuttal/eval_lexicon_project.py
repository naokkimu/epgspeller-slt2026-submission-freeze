#!/usr/bin/env python3
"""
Lexicon projection baseline: project greedy CTC outputs to nearest lexicon word.
"""

import argparse
import json
import pickle
from pathlib import Path
from typing import List, Tuple, Dict

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


def greedy_preds_targets(model_path: Path, partition: str, device: str) -> Tuple[List[str], List[str], Dict]:
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

    preds: List[str] = []
    targets: List[str] = []

    with torch.no_grad():
        for X, y, X_len, y_len, days in loader:
            X = X.to(device)
            y = y.to(device)
            X_len = X_len.to(device)
            y_len = y_len.to(device)
            days = days.to(device)

            logits = model(X, days)
            adjusted_lens = ((X_len - model.kernelLen) / model.strideLen).to(torch.int32)
            for i in range(logits.size(0)):
                seq_logits = logits[i, : adjusted_lens[i]]
                decoded = torch.argmax(seq_logits, dim=-1)
                decoded = torch.unique_consecutive(decoded, dim=-1)
                decoded = decoded[decoded != 0]
                preds.append(numeric_to_string(decoded.cpu().tolist()))

                true_seq = y[i][: y_len[i]].cpu().numpy().tolist()
                targets.append(numeric_to_string(true_seq))

    meta = {
        "dataset_path": args.get("datasetPath"),
        "param_count": args.get("param_count"),
        "seed": args.get("seed"),
        "split_seed": args.get("split_seed"),
    }
    return preds, targets, meta


def build_lexicon(dataset_path: Path, source: str, lexicon_path: Path = None) -> List[str]:
    with open(dataset_path, "rb") as f:
        dataset = pickle.load(f)

    def collect_from(split_key: str) -> List[str]:
        words = []
        for day in dataset[split_key]:
            # Normalize to uppercase to match greedy-decoded predictions/targets.
            words.extend(str(w).upper().strip() for w in day["transcriptions"])
        return words

    if source == "file":
        if not lexicon_path:
            raise ValueError("lexicon_path is required when lexicon_source=file")
        with open(lexicon_path, "r") as f:
            return [line.strip().upper() for line in f if line.strip()]

    if source == "all":
        words = collect_from("train") + collect_from("test") + collect_from("competition")
    elif source == "train":
        words = collect_from("train")
    else:
        raise ValueError(f"Unsupported lexicon source: {source}")

    return sorted(set(words))


def project_predictions(preds: List[str], lexicon: List[str]) -> List[str]:
    projected: List[str] = []
    for p in preds:
        best_word = ""
        best_dist = 1e9
        for w in lexicon:
            dist = calculate_edit_distance(p, w)
            if dist < best_dist:
                best_dist = dist
                best_word = w
        projected.append(best_word)
    return projected


def compute_metrics(preds: List[str], targets: List[str]) -> Dict:
    total_chars = 0
    total_edits = 0
    total_words = len(preds)
    total_word_errors = 0
    for p, t in zip(preds, targets):
        total_edits += calculate_edit_distance(p, t)
        total_chars += len(t)
        total_word_errors += int(p != t)
    cer = total_edits / total_chars if total_chars > 0 else 0.0
    wer = total_word_errors / total_words if total_words > 0 else 0.0
    return {
        "cer": cer,
        "wer": wer,
        "total_chars": total_chars,
        "total_edits": total_edits,
        "total_words": total_words,
        "total_word_errors": total_word_errors,
    }


def main():
    parser = argparse.ArgumentParser(description="Lexicon projection baseline.")
    parser.add_argument("--pred_json", type=Path, default=None,
                        help="Greedy eval JSON containing predictions/targets.")
    parser.add_argument("--model_path", type=Path, default=None,
                        help="If pred_json not given, run greedy from this model.")
    parser.add_argument("--partition", type=str, choices=["test", "competition"], default="test")
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--lexicon_source", type=str, choices=["all", "train", "file"], default="all")
    parser.add_argument("--lexicon_path", type=Path, default=None,
                        help="Required when lexicon_source=file")
    parser.add_argument("--out_json", type=Path, default=None)
    args = parser.parse_args()

    if args.pred_json is None and args.model_path is None:
        raise ValueError("Either --pred_json or --model_path must be provided.")

    # Load predictions/targets and dataset path metadata
    if args.pred_json:
        with open(args.pred_json, "r") as f:
            pred_payload = json.load(f)
        preds = pred_payload["predictions"]
        targets = pred_payload["targets"]
        dataset_path = Path(pred_payload["dataset_path"])
        meta = {
            "param_count": pred_payload.get("param_count"),
            "seed": pred_payload.get("seed"),
            "split_seed": pred_payload.get("split_seed"),
            "model_path": pred_payload.get("model_path"),
            "streaming_metrics": pred_payload.get("streaming_metrics"),
        }
    else:
        preds, targets, meta = greedy_preds_targets(args.model_path, args.partition, args.device)
        dataset_path = Path(meta["dataset_path"])
        meta["model_path"] = str(args.model_path)
        meta["streaming_metrics"] = None

    lexicon = build_lexicon(dataset_path, args.lexicon_source, args.lexicon_path)
    projected_preds = project_predictions(preds, lexicon)
    metrics = compute_metrics(projected_preds, targets)

    result = {
        "partition": args.partition,
        "lexicon_source": args.lexicon_source,
        "lexicon_size": len(lexicon),
        "cer": metrics["cer"],
        "wer": metrics["wer"],
        "total_chars": metrics["total_chars"],
        "total_edits": metrics["total_edits"],
        "total_words": metrics["total_words"],
        "total_word_errors": metrics["total_word_errors"],
        "dataset_path": str(dataset_path),
        "model_path": meta.get("model_path"),
        "param_count": meta.get("param_count"),
        "seed": meta.get("seed"),
        "split_seed": meta.get("split_seed"),
        "streaming_metrics": meta.get("streaming_metrics"),
    }

    if args.out_json:
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        with open(args.out_json, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Saved results to {args.out_json}")

    print(f"Partition: {args.partition}")
    print(f"Lexicon size: {len(lexicon)}")
    print(f"CER: {metrics['cer']:.4f}  WER: {metrics['wer']:.4f}  Samples: {metrics['total_words']}")


if __name__ == "__main__":
    main()

