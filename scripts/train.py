import os
import argparse
import pickle
from datetime import datetime
from pathlib import Path

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

from neural_decoder.neural_decoder_trainer import trainModel
from neural_decoder.model import GRUDecoder


def main():
    parser = argparse.ArgumentParser(description='Train neural decoder model')
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
    parser.add_argument('--n_units', type=int, default=1024)
    parser.add_argument('--n_layers', type=int, default=5)
    parser.add_argument('--n_batch', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--white_noise_sd', type=float, default=0.8)
    parser.add_argument('--constant_offset_sd', type=float, default=0.2)
    parser.add_argument('--gaussian_smooth_width', type=float, default=2.0)
    parser.add_argument('--enable_online_specaug', action='store_true',
                        help='Enable online SpecAugment via aug_conf')
    parser.add_argument('--n_classes', type=int, default=26,
                        help='Number of non-blank classes (blank added internally)')
    parser.add_argument('--val_split', type=str, choices=['test', 'competition'], default='competition',
                        help='Partition used for validation/checkpointing')
    args = parser.parse_args()

    # Load dataset to get input features dimension
    with open(args.dataset_path, "rb") as handle:
        dataset = pickle.load(handle)
    n_input_features = dataset['train'][0]['sentenceDat'][0].shape[1]
    n_days = len(dataset["train"])

    # データセット名の抽出（パスの最後の部分を使用）
    dataset_name = Path(args.dataset_path).stem

    # 日時とデータセット名でログディレクトリ名を生成
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_dir_name = f"{timestamp}_{dataset_name}"
    if args.model_name:  # オプションのモデル名が指定されていれば追加
        log_dir_name += f"_{args.model_name}"

    model_args = {}
    model_args['outputDir'] = os.path.join('./logs', log_dir_name)
    model_args['datasetPath'] = args.dataset_path

    # 時系列長パラメータ
    model_args['seqLen'] = 250        # 平均長に近い値（245.17）を切り上げ
    model_args['maxTimeSeriesLen'] = 512  # 最大長（501）を超える2のべき乗

    model_args['batchSize'] = 64
    model_args['lrStart'] = 0.02
    model_args['lrEnd'] = 0.02
    model_args['nUnits'] = args.n_units
    model_args['nBatch'] = args.n_batch
    model_args['nLayers'] = args.n_layers
    model_args['seed'] = args.seed
    model_args['nClasses'] = args.n_classes
    model_args['nInputFeatures'] = n_input_features  # データセットから自動的に設定
    model_args['dropout'] = 0.4
    model_args['whiteNoiseSD'] = args.white_noise_sd
    model_args['constantOffsetSD'] = args.constant_offset_sd
    model_args['gaussianSmoothWidth'] = args.gaussian_smooth_width
    model_args['strideLen'] = 4
    model_args['kernelLen'] = 32
    model_args['bidirectional'] = True
    model_args['l2_decay'] = 1e-5
    model_args['val_split'] = args.val_split

    # Augmentation configuration
    if args.enable_online_specaug:
        model_args['aug_conf'] = {
            'time_mask': {'T': 12, 'p': 0.4},
            'electrode_mask': {'F': 6, 'p': 0.4},
            'time_warp': {'W': 0.2, 'p': 0.2}
        }
    else:
        model_args['aug_conf'] = None

    # Compute parameter count for logging
    temp_model = GRUDecoder(
        neural_dim=model_args['nInputFeatures'],
        n_classes=model_args['nClasses'],
        hidden_dim=model_args['nUnits'],
        layer_dim=model_args['nLayers'],
        nDays=n_days,
        dropout=model_args['dropout'],
        device='cpu',
        strideLen=model_args['strideLen'],
        kernelLen=model_args['kernelLen'],
        gaussianSmoothWidth=model_args['gaussianSmoothWidth'],
        bidirectional=model_args['bidirectional'],
    )
    model_args['param_count'] = sum(p.numel() for p in temp_model.parameters())

    trainModel(model_args)


if __name__ == '__main__':
    main() 