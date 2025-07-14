import re
import csv
import argparse
from pathlib import Path

def extract_pairs(results_file):
    pairs = []
    current_ref = None
    current_pred = None
    
    with open(results_file, 'r') as f:
        for line in f:
            ref_match = re.match(r'Reference: (.*)', line)
            pred_match = re.match(r'Predicted: (.*)', line)
            
            if ref_match:
                current_ref = ref_match.group(1).strip()
            elif pred_match:
                current_pred = pred_match.group(1).strip()
                if current_ref is not None:
                    pairs.append({
                        'reference': current_ref,
                        'predicted': current_pred
                    })
                current_ref = None
                current_pred = None
    
    return pairs

def main():
    parser = argparse.ArgumentParser(description='Extract reference and predicted pairs from detailed results')
    parser.add_argument('results_file', type=str, help='Path to detailed_results.txt')
    
    args = parser.parse_args()
    
    # Get the directory of the input file and create output path
    input_path = Path(args.results_file)
    output_path = input_path.parent / 'prediction_pairs.csv'
    
    pairs = extract_pairs(args.results_file)
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['reference', 'predicted'])
        writer.writeheader()
        writer.writerows(pairs)
    
    print(f"Extracted {len(pairs)} pairs to {output_path}")

if __name__ == '__main__':
    main() 