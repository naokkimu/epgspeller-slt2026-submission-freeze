#!/usr/bin/env python3
"""
Extract labels from dataset to create corpus for KenLM.
"""

import numpy as np
import argparse
from pathlib import Path

def extract_labels(dataset_path, output_path):
    """
    Extract labels from dataset and save as text corpus.
    
    Args:
        dataset_path: Path to the .npz dataset file
        output_path: Path to save the text corpus
    """
    # Load dataset
    data = np.load(dataset_path, allow_pickle=True)
    
    # Extract labels
    if 'label' in data:
        labels = data['label']
    elif 'labels' in data:
        labels = data['labels']
    else:
        # Try to find label-like keys
        available_keys = list(data.keys())
        print(f"Available keys: {available_keys}")
        label_keys = [k for k in available_keys if 'label' in k.lower()]
        if label_keys:
            labels = data[label_keys[0]]
            print(f"Using key: {label_keys[0]}")
        else:
            raise ValueError("No label key found in dataset")
    
    # Convert to text corpus
    corpus_lines = []
    for label in labels:
        # Convert to string if needed
        if isinstance(label, bytes):
            label = label.decode('utf-8')
        elif isinstance(label, np.ndarray):
            label = str(label)
        
        # Add to corpus
        corpus_lines.append(str(label).strip())
    
    # Save corpus
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in corpus_lines:
            f.write(line + '\n')
    
    print(f"Extracted {len(corpus_lines)} labels to {output_path}")
    
    # Print some examples
    print("\nFirst 10 labels:")
    for i, label in enumerate(corpus_lines[:10]):
        print(f"  {i+1}: {label}")

def main():
    parser = argparse.ArgumentParser(description='Extract labels from dataset')
    parser.add_argument('--dataset_path', type=str, default='raw_dataset/p1_2328_old_dataset.npz',
                      help='Path to dataset file')
    parser.add_argument('--output_path', type=str, default='lm/char_corpus.txt',
                      help='Path to output corpus file')
    
    args = parser.parse_args()
    
    extract_labels(args.dataset_path, args.output_path)

if __name__ == '__main__':
    main() 