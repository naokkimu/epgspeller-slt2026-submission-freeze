import torch
import pytest
import sys
import os
from omegaconf import OmegaConf

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from neural_decoder.transforms import *
from neural_decoder.unified_dataset import UnifiedEPGDataset

def test_individual_transforms():
    """Test each transform individually."""
    # Create dummy input (T=100, C=124)
    x = torch.randn(100, 124)
    
    # Test PCA transform
    pca = PCATransform(16, "models/pca16.npy")
    x_pca = pca(x.clone())
    assert x_pca.shape == (100, 16), f"PCA output shape: {x_pca.shape}"
    
    # Test LowPass
    lowpass = LowPass(5)
    x_lp = lowpass(x.clone())
    assert x_lp.shape == x.shape, f"LowPass output shape: {x_lp.shape}"
    
    # Test SpecAug
    time_mask = TimeMask(T=12, p=1.0)  # Force application
    x_tm = time_mask(x.clone())
    assert x_tm.shape == x.shape, f"TimeMask output shape: {x_tm.shape}"
    
    electrode_mask = ElectrodeMask(F=6, p=1.0)
    x_em = electrode_mask(x.clone())
    assert x_em.shape == x.shape, f"ElectrodeMask output shape: {x_em.shape}"
    
    time_warp = TimeWarp(W=0.05, p=1.0)
    x_tw = time_warp(x.clone())
    assert x_tw.shape[1] == x.shape[1], f"TimeWarp feature dim: {x_tw.shape[1]}"
    
    # Test Noise
    white_noise = WhiteNoise(sd=0.1, p=1.0)
    x_wn = white_noise(x.clone())
    assert x_wn.shape == x.shape, f"WhiteNoise output shape: {x_wn.shape}"
    
    drift_noise = DriftNoise(sd=0.05, p=1.0)
    x_dn = drift_noise(x.clone())
    assert x_dn.shape == x.shape, f"DriftNoise output shape: {x_dn.shape}"
    
    gaussian_smooth = GaussianSmooth(width=2.0, p=1.0)
    x_gs = gaussian_smooth(x.clone())
    assert x_gs.shape == x.shape, f"GaussianSmooth output shape: {x_gs.shape}"
    
    print("✓ All individual transforms passed")

def test_unified_dataset():
    """Test UnifiedEPGDataset pipeline."""
    # Load config
    cfg_path = "src/neural_decoder/conf/unified_config.yaml"
    cfg = OmegaConf.load(cfg_path)
    
    # Create datasets
    train_ds = UnifiedEPGDataset("train", cfg)
    test_ds = UnifiedEPGDataset("test", cfg)
    
    # Test basic properties
    assert len(train_ds) > 0, "Train dataset is empty"
    assert len(test_ds) > 0, "Test dataset is empty"
    
    # Test data loading
    x, y = train_ds[0]
    print(f"Sample shape: {x.shape}, label: {y}")
    
    # Check PCA reduced dimension
    if cfg.pca.enable:
        assert x.shape[1] == cfg.pca.n_components, f"Expected {cfg.pca.n_components} features, got {x.shape[1]}"
    
    # Test a few samples
    for i in range(min(3, len(train_ds))):
        x, y = train_ds[i]
        assert isinstance(x, torch.Tensor), "Data should be tensor"
        assert isinstance(y, torch.Tensor), "Label should be tensor"
    
    print("✓ UnifiedEPGDataset pipeline test passed")

def test_pipeline_smoke():
    """Full pipeline smoke test."""
    test_individual_transforms()
    test_unified_dataset()
    print("✓ Pipeline smoke-test ✓")

if __name__ == "__main__":
    test_pipeline_smoke() 