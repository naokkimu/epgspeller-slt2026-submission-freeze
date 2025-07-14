import os
import argparse
import pickle
import optuna
from datetime import datetime
from pathlib import Path
from neural_decoder.neural_decoder_trainer import trainModel


def objective(trial, dataset_path, base_log_dir):
    # Load dataset to get input features dimension
    with open(dataset_path, "rb") as handle:
        dataset = pickle.load(handle)
    n_input_features = dataset['train'][0]['sentenceDat'][0].shape[1]

    # Generate unique log directory for this trial
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dataset_name = Path(dataset_path).stem
    log_dir_name = f"{timestamp}_{dataset_name}_trial_{trial.number}"
    
    # Define hyperparameters to optimize
    model_args = {
        # Hyperparameters to optimize
        'nUnits': trial.suggest_int('nUnits', 16, 128),
        'nLayers': trial.suggest_int('nLayers', 2, 8),
        'dropout': trial.suggest_float('dropout', 0.1, 0.5),
        'strideLen': trial.suggest_int('strideLen', 2, 8),
        'kernelLen': trial.suggest_int('kernelLen', 16, 64),
        
        # Fixed parameters
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
    metrics = trainModel(model_args)
    
    # Return validation CER (Character Error Rate) as the objective to minimize
    return metrics['validation_cer']  # Note: trainModel needs to be modified to return metrics


def main():
    parser = argparse.ArgumentParser(description='Train neural decoder model with Optuna optimization')
    parser.add_argument(
        '--dataset_path',
        type=str,
        required=True,
        help='Path to the dataset'
    )
    parser.add_argument(
        '--n_trials',
        type=int,
        default=100,
        help='Number of optimization trials to run'
    )
    parser.add_argument(
        '--study_name',
        type=str,
        default='silentspeller_optimization',
        help='Name for the Optuna study'
    )
    args = parser.parse_args()

    # Create base log directory for all trials
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_log_dir = os.path.join('./logs', f'optuna_{timestamp}')
    os.makedirs(base_log_dir, exist_ok=True)

    # Create and configure the study
    study = optuna.create_study(
        study_name=args.study_name,
        direction='minimize'  # We want to minimize the CER
    )

    # Run the optimization
    study.optimize(
        lambda trial: objective(trial, args.dataset_path, base_log_dir),
        n_trials=args.n_trials
    )

    # Print results
    print("\nBest trial:")
    trial = study.best_trial
    print(f"  Value (CER): {trial.value:.4f}")
    print("\n  Best hyperparameters:")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")

    # Save study statistics
    optuna.visualization.plot_optimization_history(study).write_image(
        f"{base_log_dir}/optimization_history.png"
    )
    optuna.visualization.plot_param_importances(study).write_image(
        f"{base_log_dir}/param_importances.png"
    )


if __name__ == '__main__':
    main() 