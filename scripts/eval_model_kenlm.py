#!/usr/bin/env python3
"""
Evaluate neural decoder model with KenLM shallow-fusion decoding.
"""

import argparse
import pickle
import numpy as np
import torch
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from neural_decoder.dataset import SpeechDataset
from neural_decoder.neural_decoder_trainer import loadModel
from neural_decoder.utils.ctc_decoder_kenlm import CTCKenLMDecoder
import matplotlib.pyplot as plt
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate trained neural decoder model with KenLM")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the trained model directory")
    parser.add_argument("--lm_path", type=str, required=True, help="Path to KenLM binary model")
    parser.add_argument("--alpha", type=float, default=1.0, help="Language model weight")
    parser.add_argument("--beta", type=float, default=0.0, help="Length penalty weight")
    parser.add_argument("--beam_width", type=int, default=32, help="Beam search width")
    parser.add_argument("--partition", type=str, default="test", choices=["test", "competition"],
                      help="Data partition to evaluate on")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for evaluation")
    parser.add_argument("--device", type=str, default="cpu", help="Device to run evaluation on")
    parser.add_argument("--output_dir", type=str, default=None, help="Output directory for results")
    parser.add_argument("--save_predictions", action="store_true", help="Save predictions to file")
    return parser.parse_args()

def load_model_and_args(model_path):
    """Load model and arguments from saved checkpoint."""
    # Load saved arguments
    with open(Path(model_path) / "args", "rb") as f:
        args = pickle.load(f)
    
    # Load dataset to get the number of days
    with open(args["datasetPath"], "rb") as f:
        dataset = pickle.load(f)
    n_days = len(dataset["train"])  # Use the same number of days as in training
    
    # Load model with correct number of days
    model = loadModel(model_path, nInputLayers=n_days)
    
    # Ensure model is on CPU first to avoid device conflicts
    model = model.cpu()
    
    return model, args

def padding_collate(batch):
    """Collate function for padding sequences in a batch"""
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

def calculate_metrics(predictions, targets):
    """Calculate CER and WER metrics."""
    total_chars = 0
    total_char_errors = 0
    total_words = 0
    total_word_errors = 0
    
    for pred, target in zip(predictions, targets):
        # Character-level metrics
        char_errors = calculate_edit_distance(pred, target)
        total_char_errors += char_errors
        total_chars += len(target)
        
        # Word-level metrics (treating each prediction as a single word)
        word_errors = 1 if pred != target else 0
        total_word_errors += word_errors
        total_words += 1
    
    cer = total_char_errors / total_chars if total_chars > 0 else 0
    wer = total_word_errors / total_words if total_words > 0 else 0
    
    return cer, wer

def calculate_edit_distance(s1, s2):
    """Calculate edit distance between two strings."""
    if len(s1) < len(s2):
        return calculate_edit_distance(s2, s1)
    
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

def string_to_numeric(s):
    """Convert string to numeric representation."""
    # A=1, B=2, ..., Z=26
    result = []
    for char in s.upper():
        if 'A' <= char <= 'Z':
            result.append(ord(char) - ord('A') + 1)
    return result

def numeric_to_string(nums):
    """Convert numeric representation to string."""
    result = ""
    for num in nums:
        if 1 <= num <= 26:
            result += chr(ord('A') + num - 1)
    return result

def main():
    args = parse_args()
    
    # Load model and arguments
    print(f"Loading model from {args.model_path}")
    model, model_args = load_model_and_args(args.model_path)
    
    # Set device
    device = torch.device(args.device)
    model = model.to(device)
    model.eval()
    
    # Load dataset
    print(f"Loading dataset from {model_args['datasetPath']}")
    with open(model_args["datasetPath"], "rb") as f:
        dataset = pickle.load(f)
    
    # Get evaluation data
    eval_dataset = SpeechDataset(dataset[args.partition])
    eval_loader = DataLoader(eval_dataset, batch_size=args.batch_size, 
                            shuffle=False, collate_fn=padding_collate)
    
    print(f"Evaluating on {args.partition} set with {len(eval_dataset)} samples")
    print(f"KenLM parameters: alpha={args.alpha}, beta={args.beta}, beam_width={args.beam_width}")

    # Initialize decoder once (avoid re-loading KenLM per batch)
    decoder = CTCKenLMDecoder(
        lm_path=args.lm_path,
        alpha=args.alpha,
        beta=args.beta,
        beam_width=args.beam_width,
        blank_id=0,
    )
    
    # Run evaluation
    all_predictions = []
    all_targets = []
    
    with torch.no_grad():
        for batch_idx, (X, y, X_lens, y_lens, days) in enumerate(eval_loader):
            X = X.to(device)
            y = y.to(device)
            X_lens = X_lens.to(device)
            y_lens = y_lens.to(device)
            days = days.to(device)
            
            # Forward pass
            logits = model(X, days)
            
            # Convert to numpy for KenLM decoding
            logits_np = logits.cpu().numpy()
            lengths_np = X_lens.cpu().numpy()
            
            # Decode with KenLM (beam search per sample)
            predictions = []
            for i in range(logits_np.shape[0]):
                beam_results = decoder.decode_beam_search(logits_np[i], logits_np[i].shape[0])
                predictions.append(beam_results[0][0] if beam_results else "")
            
            # Convert targets to strings
            targets = []
            for i in range(y.size(0)):
                target_seq = y[i][:y_lens[i]].cpu().numpy()
                target_str = numeric_to_string(target_seq)
                targets.append(target_str)
            
            all_predictions.extend(predictions)
            all_targets.extend(targets)
            
            if batch_idx % 10 == 0:
                print(f"Processed {batch_idx * args.batch_size} samples")
    
    # Calculate metrics
    cer, wer = calculate_metrics(all_predictions, all_targets)
    
    print(f"\nEvaluation Results:")
    print(f"Character Error Rate (CER): {cer:.4f}")
    print(f"Word Error Rate (WER): {wer:.4f}")
    
    # Save results
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save metrics
        with open(output_dir / "metrics.txt", "w") as f:
            f.write(f"Character Error Rate (CER): {cer:.4f}\n")
            f.write(f"Word Error Rate (WER): {wer:.4f}\n")
            f.write(f"Alpha: {args.alpha}\n")
            f.write(f"Beta: {args.beta}\n")
            f.write(f"Beam Width: {args.beam_width}\n")
        
        # Save predictions
        if args.save_predictions:
            with open(output_dir / "predictions.txt", "w") as f:
                for i, (pred, target) in enumerate(zip(all_predictions, all_targets)):
                    f.write(f"Sample {i+1}:\n")
                    f.write(f"  Predicted: {pred}\n")
                    f.write(f"  Target:    {target}\n")
                    f.write(f"  Correct:   {pred == target}\n")
                    f.write("\n")
        
        print(f"Results saved to {output_dir}")

if __name__ == "__main__":
    main() 