#!/usr/bin/env python3
"""
Training results checker
学習結果を確認するスクリプト
"""
import os
import pickle
import glob
import numpy as np
from pathlib import Path

def find_latest_log_dir():
    """最新のログディレクトリを探す"""
    log_dirs = glob.glob("logs/*_pca16_best_config_retest")
    if not log_dirs:
        log_dirs = glob.glob("logs/*")
    
    if not log_dirs:
        return None
    
    # 最新のディレクトリを取得
    latest_dir = max(log_dirs, key=os.path.getmtime)
    return latest_dir

def check_training_results():
    """学習結果をチェックする"""
    log_dir = find_latest_log_dir()
    
    if not log_dir:
        print("No training logs found in ./logs directory")
        return
    
    print("=== Training Results ===")
    print(f"Log directory: {log_dir}")
    
    # Dataset path check
    args_path = os.path.join(log_dir, "args")
    if os.path.exists(args_path):
        with open(args_path, "rb") as f:
            args = pickle.load(f)
        print(f"Dataset: {args.get('datasetPath', 'Unknown')}")
        
        print("Model configuration:")
        config_keys = ['nUnits', 'nLayers', 'dropout', 'batchSize', 'lrStart', 
                      'strideLen', 'kernelLen', 'bidirectional']
        for key in config_keys:
            if key in args:
                print(f"  {key}: {args[key]}")
    
    # Training stats check
    stats_path = os.path.join(log_dir, "trainingStats")
    if os.path.exists(stats_path):
        with open(stats_path, "rb") as f:
            stats = pickle.load(f)
        
        if 'validationLoss' in stats and len(stats['validationLoss']) > 0:
            final_val_loss = stats['validationLoss'][-1]
            print(f"\nFinal validation loss: {final_val_loss:.6f}")
        
        if 'validationCER' in stats and len(stats['validationCER']) > 0:
            final_val_cer = stats['validationCER'][-1]
            best_val_cer = min(stats['validationCER'])
            best_cer_batch = np.argmin(stats['validationCER']) * 100  # Assuming validation every 100 batches
            
            print(f"Final validation CER: {final_val_cer:.6f}")
            print(f"Best validation CER: {best_val_cer:.6f}")
            print(f"Best CER achieved at batch: {best_cer_batch}")
    
    # Check if model weights exist
    weights_path = os.path.join(log_dir, "modelWeights")
    if os.path.exists(weights_path):
        print(f"\nModel weights saved: {weights_path}")
    else:
        print("\nWarning: Model weights not found")
    
    # Check if training curves exist
    curves_path = os.path.join(log_dir, "training_curves.png")
    if os.path.exists(curves_path):
        print(f"Training curves saved: {curves_path}")
    
    print(f"\nFor model evaluation, run:")
    print(f"PYTHONPATH=$PYTHONPATH:./src python scripts/eval_model.py --model_path {log_dir} --partition test")

if __name__ == "__main__":
    check_training_results() 