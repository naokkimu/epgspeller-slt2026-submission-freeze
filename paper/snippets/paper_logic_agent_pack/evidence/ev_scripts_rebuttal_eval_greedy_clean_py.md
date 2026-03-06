# ev_scripts_rebuttal_eval_greedy_clean_py

- kind: `data`
- path: `scripts/rebuttal/eval_greedy_clean.py`
- sha256: `a341ada9fb1e2b0d0a0754edf3e1c122bb9d253c627511256abf39441bfeb0fb`
- size_bytes: 8058
- root_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- abs_path_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/scripts/rebuttal/eval_greedy_clean.py`

## Excerpt

```text
#!/usr/bin/env python3
"""
Greedy CTC evaluation for rebuttal numbers (open-vocab, no LM).
"""

import argparse
import json
import pickle
import time
from pathlib import Path
from typing import List

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


def evaluate(model_path: Path, partition: str, device: str, out_json: Path = None, frame_ms: float = 10.0):
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

                all_preds.append(pred_str)
                all_targets.append(true_str)

                dist = calculate_edit_distance(pred_str, true_str)
                total_edits += dist
                total_chars += len(true_str)
                total_words += 1
                total_word_errors += int(pred_str != true_str)

    cer = total_edits / total_chars if total_chars > 0 else 0.0
    wer = total_word_errors / total_words if total_words > 0 else 0.0
    total_input_seconds = (total_input_frames * frame_ms) / 1000.0
    rtf = (total_infer_seconds / total_input_seconds) if total_input_seconds > 0 else None
    chunk_latency_ms = (
        (total_infer_seconds * 1000.0 / total_output_chunks)
        if total_output_chunks > 0
        else None
    )
    avg_utt_infer_ms = (
        (total_infer_seconds * 1000.0 / len(all_preds)) if len(all_preds) > 0 else 0.0
    )
    first_output_latency_ms = max(0, model.kernelLen - model.strideLen) * frame_ms
    end_to_end_latency_ms = avg_utt_infer_ms + first_output_latency_ms
    model_cfg = args.get("model", {}) if isinstance(args.get("model", {}), dict) else {}
    model_family = model_cfg.get("model_family", "gru")
    # `args["bidirectional"]` isn't reliable for uni-directional families (e.g., uni_gru).
    streaming_ready = model_family in {
        "uni_gru",
        "causal_tcn",
        "mini_transformer",
        "spatial2d_uni_gru",
        "rowcol_uni_gru",
    }

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
        "streaming_metrics": {
            "frame_ms": frame_ms,
            "total_input_frames": total_input_frames,
            "total_input_seconds": total_input_seconds,
            "total_output_chunks": total_output_chunks,
            "total_infer_seconds": total_infer_seconds,
            "rtf": rtf,
            "chunk_latency_ms": chunk_latency_ms,
            "end_to_end_latency_ms": end_to_end_latency_ms,
            "first_output_latency_ms": first_output_latency_ms,
            "model_family": model_family,
            "streaming_ready": streaming_ready,
        },
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
    parser.add_argument("--frame_ms", type=float, default=10.0)
    return parser.parse_args()


if __name__ == "__main__":
    cli_args = parse_args()
    evaluate(
        model_path=cli_args.model_path,
        partition=cli_args.partition,
        device=cli_args.device,
        out_json=cli_args.out_json,
        frame_ms=cli_args.frame_ms,
    )
```
