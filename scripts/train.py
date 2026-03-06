import os
import argparse
import pickle
import json
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
from neural_decoder.model import build_model


def _to_json_safe(obj):
    """Recursively convert numpy/torch scalars into native Python types."""
    if isinstance(obj, dict):
        return {k: _to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_json_safe(v) for v in obj]
    # numpy scalar: has .item()
    if hasattr(obj, "item"):
        try:
            return obj.item()
        except Exception:
            pass
    return obj


def main():
    parser = argparse.ArgumentParser(description='Train neural decoder model')
    parser.add_argument(
        '--dataset_path',
        type=str,
        required=True,
        help='Path to the dataset'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default=None,
        help='If set, write logs/checkpoints to this directory instead of ./logs/<timestamp>_...'
    )
    parser.add_argument(
        '--run_id',
        type=str,
        default=None,
        help='If set (and --output_dir is not set), write logs/checkpoints to ./logs/<run_id> for stable sweep runs'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Allow overwriting an existing output directory. Default: refuse if it already exists.'
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
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--dropout', type=float, default=0.4)
    parser.add_argument('--lr_start', type=float, default=0.02)
    parser.add_argument('--lr_end', type=float, default=0.02)
    parser.add_argument('--l2_decay', type=float, default=1e-5)
    parser.add_argument('--stride_len', type=int, default=4)
    parser.add_argument('--kernel_len', type=int, default=32)
    parser.add_argument('--white_noise_sd', type=float, default=0.8)
    parser.add_argument('--constant_offset_sd', type=float, default=0.2)
    parser.add_argument('--gaussian_smooth_width', type=float, default=2.0)
    parser.add_argument('--enable_online_specaug', action='store_true',
                        help='Enable online SpecAugment via aug_conf')
    parser.add_argument('--n_classes', type=int, default=26,
                        help='Number of non-blank classes (blank added internally)')
    parser.add_argument('--val_split', type=str, choices=['test', 'competition'], default='competition',
                        help='Partition used for validation/checkpointing')
    parser.add_argument('--input_proj_dim', type=int, default=None,
                        help='Optional learnable input projection dimension (e.g., 32/64). None disables projection.')
    parser.add_argument('--disable_day_embed', action='store_true',
                        help='Disable day embedding layers (useful for unified datasets / single-session sweeps).')
    parser.add_argument(
        '--model_family',
        type=str,
        choices=[
            'gru',
            'uni_gru',
            'causal_tcn',
            'mini_transformer',
            'spatial2d_uni_gru',
            'spatial2d_patchpool_uni_gru',
            'rowcol_uni_gru',
        ],
        default='gru',
        help='Decoder family for architecture ablation.',
    )
    parser.add_argument(
        '--enable_spatial_aug',
        action='store_true',
        help='Enable 2D spatial augmentation inside spatial2d_* variants (block dropout + small shift).',
    )
    parser.add_argument('--tcn_layers', type=int, default=4, help='Number of causal TCN blocks.')
    parser.add_argument('--tcn_kernel_size', type=int, default=3, help='Kernel size for causal TCN blocks.')
    parser.add_argument('--transformer_heads', type=int, default=4, help='Attention heads for mini transformer.')
    parser.add_argument('--transformer_layers', type=int, default=2, help='Number of encoder layers for mini transformer.')
    parser.add_argument('--transformer_ff_mult', type=int, default=4, help='FFN expansion ratio for mini transformer.')
    args = parser.parse_args()

    # Load dataset to get input features dimension
    with open(args.dataset_path, "rb") as handle:
        dataset = pickle.load(handle)
    n_input_features = dataset['train'][0]['sentenceDat'][0].shape[1]
    n_days = len(dataset["train"])
    processing_info = dataset.get("processing_info", {}) if isinstance(dataset, dict) else {}
    selected_channel_indices = None
    if isinstance(processing_info, dict):
        selected_channel_indices = processing_info.get("selected_channel_indices")
    if selected_channel_indices is None:
        selected_channel_indices = list(range(int(n_input_features)))
    else:
        selected_channel_indices = [int(x) for x in selected_channel_indices]

    # データセット名の抽出（パスの最後の部分を使用）
    dataset_name = Path(args.dataset_path).stem

    # Resolve output directory
    if args.output_dir:
        output_dir = args.output_dir
    elif args.run_id:
        output_dir = os.path.join("./logs", args.run_id)
    else:
        # 日時とデータセット名でログディレクトリ名を生成
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_dir_name = f"{timestamp}_{dataset_name}"
        if args.model_name:  # オプションのモデル名が指定されていれば追加
            log_dir_name += f"_{args.model_name}"
        output_dir = os.path.join("./logs", log_dir_name)

    out_path = Path(output_dir)
    if out_path.exists() and not args.overwrite:
        raise SystemExit(
            f"Output directory already exists: {out_path}. "
            "Refusing to overwrite. Re-run with --overwrite if you intend to clobber it."
        )
    if out_path.exists() and args.overwrite:
        print(f"[WARN] Overwriting existing output_dir: {out_path}")

    model_args = {}
    model_args['outputDir'] = output_dir
    model_args['datasetPath'] = args.dataset_path

    # 時系列長パラメータ
    model_args['seqLen'] = 250        # 平均長に近い値（245.17）を切り上げ
    model_args['maxTimeSeriesLen'] = 512  # 最大長（501）を超える2のべき乗

    model_args['batchSize'] = args.batch_size
    model_args['lrStart'] = args.lr_start
    model_args['lrEnd'] = args.lr_end
    model_args['nUnits'] = args.n_units
    model_args['nBatch'] = args.n_batch
    model_args['nLayers'] = args.n_layers
    model_args['seed'] = args.seed
    model_args['nClasses'] = args.n_classes
    model_args['nInputFeatures'] = n_input_features  # データセットから自動的に設定
    model_args['dropout'] = args.dropout
    model_args['whiteNoiseSD'] = args.white_noise_sd
    model_args['constantOffsetSD'] = args.constant_offset_sd
    model_args['gaussianSmoothWidth'] = args.gaussian_smooth_width
    model_args['strideLen'] = args.stride_len
    model_args['kernelLen'] = args.kernel_len
    model_args['bidirectional'] = True
    model_args['l2_decay'] = args.l2_decay
    model_args['val_split'] = args.val_split
    model_args['model'] = {
        'input_proj_dim': args.input_proj_dim,
        'use_day_embed': (not args.disable_day_embed),
        'model_family': args.model_family,
        'selected_channel_indices': selected_channel_indices,
        'enable_spatial_aug': bool(args.enable_spatial_aug),
        'tcn_layers': args.tcn_layers,
        'tcn_kernel_size': args.tcn_kernel_size,
        'transformer_heads': args.transformer_heads,
        'transformer_layers': args.transformer_layers,
        'transformer_ff_mult': args.transformer_ff_mult,
    }

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
    temp_n_days = n_days if (not args.disable_day_embed) else 1
    temp_model = build_model(
        args.model_family,
        neural_dim=model_args['nInputFeatures'],
        n_classes=model_args['nClasses'],
        hidden_dim=model_args['nUnits'],
        layer_dim=model_args['nLayers'],
        nDays=temp_n_days,
        dropout=model_args['dropout'],
        device='cpu',
        strideLen=model_args['strideLen'],
        kernelLen=model_args['kernelLen'],
        gaussianSmoothWidth=model_args['gaussianSmoothWidth'],
        bidirectional=model_args['bidirectional'],
        input_proj_dim=args.input_proj_dim,
        use_day_embed=(not args.disable_day_embed),
        tcn_layers=args.tcn_layers,
        tcn_kernel_size=args.tcn_kernel_size,
        transformer_heads=args.transformer_heads,
        transformer_layers=args.transformer_layers,
        transformer_ff_mult=args.transformer_ff_mult,
        selected_channel_indices=selected_channel_indices,
        enable_spatial_aug=bool(args.enable_spatial_aug),
    )
    model_args['param_count'] = sum(p.numel() for p in temp_model.parameters())

    metrics = trainModel(model_args)
    # Persist final/best metrics for sweep aggregation
    metrics_path = Path(model_args['outputDir']) / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(_to_json_safe(metrics), f, indent=2)
    print(f"Wrote metrics to {metrics_path}")


if __name__ == '__main__':
    main() 
