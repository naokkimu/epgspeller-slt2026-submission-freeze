#!/usr/bin/env python3
"""
Silent Speller Decoder: Best Configuration Retest
最良条件での追試を実行するスクリプト
"""
import os
import pickle
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from neural_decoder.neural_decoder_trainer import trainModel

def main():
    print("=== Best Configuration Retest ===")
    
    # Use available dataset (pca16 since pca64 is not available)
    dataset_path = "data/pca16"
    print(f"Dataset: {dataset_path}")
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset {dataset_path} not found")
        return
    
    # Load dataset to get input features dimension
    with open(dataset_path, "rb") as handle:
        dataset = pickle.load(handle)
    n_input_features = dataset['train'][0]['sentenceDat'][0].shape[1]
    
    # Generate log directory name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_dir_name = f"{timestamp}_pca16_best_config_retest"
    output_dir = os.path.join('./logs', log_dir_name)
    
    print(f"Output directory: {output_dir}")
    
    # Best configuration parameters based on Lake Tahoe experiment
    model_args = {
        'outputDir': output_dir,
        'datasetPath': dataset_path,
        
        # Time series parameters
        'seqLen': 250,
        'maxTimeSeriesLen': 512,
        
        # Model architecture (best configuration)
        'nUnits': 128,
        'nLayers': 5,
        'dropout': 0.4,
        'strideLen': 4,
        'kernelLen': 32,
        'bidirectional': True,
        
        # Training parameters
        'batchSize': 64,
        'lrStart': 0.02,
        'lrEnd': 0.02,
        'nBatch': 10000,
        
        # Data augmentation (best configuration)
        'whiteNoiseSD': 0.8,
        'constantOffsetSD': 0.2,
        'gaussianSmoothWidth': 2.0,
        
        # Other parameters
        'seed': 0,
        'nClasses': 40,
        'nInputFeatures': n_input_features,
        'l2_decay': 1e-5
    }
    
    print("Model parameters:")
    for key, value in model_args.items():
        print(f"  {key}: {value}")
    
    print("\nStarting training with best configuration...")
    
    # Train the model
    trainModel(model_args)
    
    print(f"\nTraining completed. Results saved to: {output_dir}")
    print("Run 'python check_results.py' to view the results.")

if __name__ == "__main__":
    main() 