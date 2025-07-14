import os
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Train and evaluate neural decoder model')
    parser.add_argument(
        '--dataset_path',
        type=str,
        required=True,
        help='Path to the dataset'
    )
    parser.add_argument(
        '--model_name',
        type=str,
        default='',
        help='Additional name for the model (optional)'
    )
    args = parser.parse_args()

    # まず訓練を実行
    train_cmd = ['python', 'scripts/train.py', '--dataset_path', args.dataset_path]
    if args.model_name:
        train_cmd.extend(['--model_name', args.model_name])
    
    print("Starting training...")
    result = subprocess.run(train_cmd, check=True)
    
    if result.returncode == 0:
        print("Training completed successfully.")
        
        # 最新のログディレクトリを見つける
        log_dirs = sorted(Path('./logs').glob('*'))
        if not log_dirs:
            print("Error: No log directory found")
            return
        latest_log_dir = str(log_dirs[-1])
        
        # 評価を実行
        print("\nStarting evaluation...")
        eval_cmd = [
            'python', 'scripts/eval_model.py',
            '--model_path', latest_log_dir,
            '--partition', 'competition'
        ]
        subprocess.run(eval_cmd, check=True)
        
        print(f"\nAll processes completed. Results are saved in: {latest_log_dir}")
    else:
        print("Training failed.")

if __name__ == '__main__':
    main() 