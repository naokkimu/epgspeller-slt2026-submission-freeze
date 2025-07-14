import os
import argparse
import pickle
from datetime import datetime
from pathlib import Path
from itertools import product
from neural_decoder.neural_decoder_trainer import trainModel


def grid_search(dataset_path, base_log_dir):
    # Load dataset to get input features dimension
    with open(dataset_path, "rb") as handle:
        dataset = pickle.load(handle)
    n_input_features = dataset['train'][0]['sentenceDat'][0].shape[1]

    # Define grid search parameters
    n_units_values = [16, 32, 48, 64, 80]  # 5 values
    n_layers_values = [2, 3, 4, 5, 6]      # 5 values
    
    # Store results
    results = []

    # Perform grid search
    for n_units, n_layers in product(n_units_values, n_layers_values):
        # Generate unique log directory for this combination
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        dataset_name = Path(dataset_path).stem
        log_dir_name = f"{timestamp}_{dataset_name}_units{n_units}_layers{n_layers}"
        
        # Define model parameters
        model_args = {
            # Grid search parameters
            'nUnits': n_units,
            'nLayers': n_layers,
            
            # Fixed parameters
            'dropout': 0.2,
            'strideLen': 4,
            'kernelLen': 32,
            'lrStart': 1e-3,
            'whiteNoiseSD': 0.5,
            'l2_decay': 1e-5,
            'outputDir': os.path.join(base_log_dir, log_dir_name),
            'datasetPath': dataset_path,
            'seqLen': 250,
            'maxTimeSeriesLen': 512,
            'batchSize': 64,
            'lrEnd': 1e-3,
            'nBatch': 10000,
            'seed': 0,
            'nClasses': 40,
            'nInputFeatures': n_input_features,
            'constantOffsetSD': 0.2,
            'gaussianSmoothWidth': 2.0,
            'bidirectional': True
        }

        # Train model and get metrics
        print(f"\nTraining model with nUnits={n_units}, nLayers={n_layers}")
        metrics = trainModel(model_args)
        
        # Handle case where metrics is None
        if metrics is None:
            print("Warning: Training failed or did not return metrics")
            validation_cer = float('inf')  # Use infinity to mark as worst result
        else:
            validation_cer = metrics.get('validation_cer', float('inf'))
        
        # Store results
        results.append({
            'nUnits': n_units,
            'nLayers': n_layers,
            'validation_cer': validation_cer
        })
        
        # Print current result
        print(f"Validation CER: {validation_cer:.4f}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Train neural decoder model with grid search'
    )
    parser.add_argument(
        '--dataset_path',
        type=str,
        required=True,
        help='Path to the dataset'
    )
    args = parser.parse_args()

    # Create base log directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_log_dir = os.path.join('./logs', f'grid_search_{timestamp}')
    os.makedirs(base_log_dir, exist_ok=True)

    # Run grid search
    results = grid_search(args.dataset_path, base_log_dir)

    # Find and print best result
    best_result = min(results, key=lambda x: x['validation_cer'])
    print("\nBest configuration:")
    print(f"nUnits: {best_result['nUnits']}")
    print(f"nLayers: {best_result['nLayers']}")
    print(f"Validation CER: {best_result['validation_cer']:.4f}")

    # Save results
    results_file = os.path.join(base_log_dir, 'grid_search_results.txt')
    with open(results_file, 'w') as f:
        f.write("nUnits,nLayers,validation_cer\n")
        for result in results:
            f.write(f"{result['nUnits']},{result['nLayers']},"
                   f"{result['validation_cer']:.4f}\n")
    print(f"\nResults saved to {results_file}")


if __name__ == '__main__':
    main() 