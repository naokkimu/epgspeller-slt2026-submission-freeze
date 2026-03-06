#!/usr/bin/env python3
"""Forward sanity check for spatial2d variants on a real EPG NPZ sample.

This script is evidence-only:
- Uses an existing raw NPZ file from raw/silentspeller_dataset/.
- Does not train or evaluate; it only instantiates models and runs forward.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple


def _ensure_src_on_path() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        candidate = p / "src"
        if (candidate / "neural_decoder").is_dir():
            sys.path.insert(0, str(candidate))
            return p
    raise SystemExit("Failed to locate repo root with src/neural_decoder")


def _load_npz_sample(raw_npz: Path, *, idx: int) -> Tuple[Any, Any]:
    import numpy as np

    raw = np.load(raw_npz, allow_pickle=True)
    if "data" not in raw:
        raise SystemExit(f"raw_npz must contain key 'data'. keys={list(raw.keys())}")
    if "label" in raw:
        labels = raw["label"]
    elif "labels" in raw:
        labels = raw["labels"]
    else:
        raise SystemExit(f"raw_npz must contain key 'label' or 'labels'. keys={list(raw.keys())}")

    data = raw["data"]
    if len(data) != len(labels):
        raise SystemExit(f"len(data)!=len(labels): {len(data)} vs {len(labels)}")
    if idx < 0 or idx >= len(data):
        raise SystemExit(f"idx out of range: {idx} (n={len(data)})")

    x = data[idx]
    y = labels[idx]
    return x, y


def _basic_validate_sample(x) -> Dict[str, Any]:
    import numpy as np

    x = np.asarray(x)
    if x.ndim != 2:
        raise SystemExit(f"Expected sample ndim=2, got {x.ndim} shape={x.shape}")
    if x.shape[1] != 124:
        raise SystemExit(f"Expected K=124, got shape={x.shape}")
    if not np.isfinite(x).all():
        raise SystemExit("Sample contains NaN/inf")
    uniq = set(np.unique(x).tolist())
    if not uniq.issubset({0.0, 1.0, 0, 1}):
        raise SystemExit(f"Sample contains values outside {{0,1}}: examples={sorted(list(uniq))[:10]}")
    return {"T": int(x.shape[0]), "K": int(x.shape[1])}


def _run_forward(
    *,
    model_family: str,
    enable_spatial_aug: bool,
    train_mode: bool,
    x_np,
) -> Dict[str, Any]:
    import torch
    from neural_decoder.model import build_model

    x = torch.tensor(x_np, dtype=torch.float32).unsqueeze(0)  # (1,T,124)
    day_idx = torch.zeros((1,), dtype=torch.long)

    model = build_model(
        model_family,
        neural_dim=124,
        n_classes=26,
        hidden_dim=512,
        layer_dim=5,
        nDays=1,
        dropout=0.4,
        device="cpu",
        strideLen=4,
        kernelLen=32,
        gaussianSmoothWidth=2.0,
        bidirectional=False,
        input_proj_dim=64,
        use_day_embed=False,
        selected_channel_indices=None,
        enable_spatial_aug=bool(enable_spatial_aug),
    )

    if train_mode:
        model.train()
    else:
        model.eval()

    with torch.no_grad():
        out = model.forward(x, day_idx)

    isfinite = bool(torch.isfinite(out).all().item())
    param_count = int(sum(p.numel() for p in model.parameters()))

    return {
        "model_family": model_family,
        "enable_spatial_aug": bool(enable_spatial_aug),
        "train_mode": bool(train_mode),
        "param_count": param_count,
        "output_shape": list(out.shape),
        "output_isfinite": isfinite,
    }


def main() -> None:
    repo_root = _ensure_src_on_path()

    ap = argparse.ArgumentParser(description="Forward sanity check for spatial2d variants on a real NPZ sample.")
    ap.add_argument(
        "--raw_npz",
        type=Path,
        default=Path("raw/silentspeller_dataset/p1_2328_old_dataset.npz"),
        help="Raw NPZ path (repo-relative by default).",
    )
    ap.add_argument("--sample_idx", type=int, default=0, help="0-based sample index to test.")
    ap.add_argument(
        "--out_json",
        type=Path,
        default=Path("results/uc20260226/spatial2d_forward_sanity.json"),
        help="Output JSON path.",
    )
    args = ap.parse_args()

    raw_npz = args.raw_npz if args.raw_npz.is_absolute() else (repo_root / args.raw_npz)
    if not raw_npz.is_file():
        raise SystemExit(f"raw_npz not found: {raw_npz}")

    x, y = _load_npz_sample(raw_npz, idx=int(args.sample_idx))
    sample_stats = _basic_validate_sample(x)

    import numpy as np
    import torch

    x_np = np.asarray(x, dtype=np.float32)

    runs = []
    runs.append(
        _run_forward(
            model_family="spatial2d_uni_gru",
            enable_spatial_aug=False,
            train_mode=False,
            x_np=x_np,
        )
    )
    runs.append(
        _run_forward(
            model_family="spatial2d_patchpool_uni_gru",
            enable_spatial_aug=False,
            train_mode=False,
            x_np=x_np,
        )
    )
    # Exercise spatial augmentation code path (train mode).
    runs.append(
        _run_forward(
            model_family="spatial2d_patchpool_uni_gru",
            enable_spatial_aug=True,
            train_mode=True,
            x_np=x_np,
        )
    )

    out = {
        "repo_root": str(repo_root),
        "raw_npz": str(raw_npz),
        "sample_idx": int(args.sample_idx),
        "sample_label_raw": str(y),
        "sample_stats": sample_stats,
        "versions": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "torch": torch.__version__,
        },
        "runs": runs,
    }

    out_json = args.out_json if args.out_json.is_absolute() else (repo_root / args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[OK] wrote: {out_json}")


if __name__ == "__main__":
    main()

