#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import torch
import numpy as np
import random
from neural_decoder.augmentations import TimeMask, ElectrodeMask, TimeWarp


def test_augmentations():
    """Test the SpecAug++ augmentations."""
    print("Testing SpecAug++ augmentations...")
    
    # Create dummy data (time_steps=50, features=128)
    x = torch.randn(50, 128)
    original_shape = x.shape
    
    # Test TimeMask
    print("Testing TimeMask...")
    time_mask = TimeMask(T=12, p=1.0)  # p=1.0 to ensure it's applied
    x_time_masked = time_mask(x.clone())
    assert x_time_masked.shape == original_shape, "TimeMask changed shape"
    print("  ✓ TimeMask works")
    
    # Test ElectrodeMask
    print("Testing ElectrodeMask...")
    electrode_mask = ElectrodeMask(F=6, p=1.0)  # p=1.0 to ensure it's applied
    x_electrode_masked = electrode_mask(x.clone())
    assert x_electrode_masked.shape == original_shape, "ElectrodeMask changed shape"
    print("  ✓ ElectrodeMask works")
    
    # Test TimeWarp
    print("Testing TimeWarp...")
    time_warp = TimeWarp(W=0.2, p=1.0)  # p=1.0 to ensure it's applied
    x_time_warped = time_warp(x.clone())
    assert x_time_warped.shape[1] == original_shape[1], "TimeWarp changed feature dimension"
    print("  ✓ TimeWarp works (shape: {} -> {})".format(original_shape, x_time_warped.shape))
    
    print("All augmentations work correctly!")


def test_probability():
    """Test that augmentations respect probability parameters."""
    print("\nTesting probability parameters...")
    
    x = torch.randn(50, 128)
    
    # Test with p=0.0 (should never apply)
    time_mask = TimeMask(T=12, p=0.0)
    electrode_mask = ElectrodeMask(F=6, p=0.0)
    time_warp = TimeWarp(W=0.2, p=0.0)
    
    # Run multiple times to ensure they're not applied
    for _ in range(10):
        x_time_masked = time_mask(x.clone())
        x_electrode_masked = electrode_mask(x.clone())
        x_time_warped = time_warp(x.clone())
        
        assert torch.equal(x, x_time_masked), "TimeMask applied with p=0.0"
        assert torch.equal(x, x_electrode_masked), "ElectrodeMask applied with p=0.0"
        assert torch.equal(x, x_time_warped), "TimeWarp applied with p=0.0"
    
    print("  ✓ Probability parameters work correctly")


if __name__ == "__main__":
    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)
    
    test_augmentations()
    test_probability()
    print("\n🎉 All tests passed!") 