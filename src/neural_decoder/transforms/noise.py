import random
import torch
import torch.nn.functional as F
import math

class WhiteNoise:
    """Add white noise with probability p."""
    def __init__(self, sd=0.1, p=0.3):
        self.sd, self.p = sd, p

    def __call__(self, x):
        if random.random() > self.p:
            return x
        noise = torch.randn_like(x) * self.sd
        return x + noise

class DriftNoise:
    """Add drift noise (channel-wise constant offset) with probability p."""
    def __init__(self, sd=0.05, p=0.3):
        self.sd, self.p = sd, p

    def __call__(self, x):
        if random.random() > self.p:
            return x
        _, C = x.shape
        noise = torch.randn(1, C) * self.sd
        return x + noise

class GaussianSmooth:
    """Apply Gaussian smoothing with probability p."""
    def __init__(self, width=2.0, p=0.3):
        self.width, self.p = width, p
        # Pre-compute Gaussian kernel
        kernel_size = int(6 * width) + 1  # 6-sigma rule
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        # Create 1D Gaussian kernel
        x = torch.arange(kernel_size, dtype=torch.float32)
        mean = (kernel_size - 1) / 2
        kernel = torch.exp(-((x - mean) / width) ** 2 / 2)
        kernel = kernel / torch.sum(kernel)
        
        self.kernel = kernel.view(1, 1, -1)  # (1, 1, K)

    def __call__(self, x):
        if random.random() > self.p:
            return x
        
        # Apply 1D convolution to each channel
        T, C = x.shape
        result = torch.zeros_like(x)
        
        for c in range(C):
            # Extract single channel: (T,) -> (1, 1, T)
            channel_data = x[:, c].unsqueeze(0).unsqueeze(0)
            
            # Apply 1D convolution
            smoothed_channel = F.conv1d(channel_data, 
                                       self.kernel, 
                                       padding='same')
            
            # Store back: (1, 1, T) -> (T,)
            result[:, c] = smoothed_channel.squeeze()
        
        return result

__all__ = ["WhiteNoise", "DriftNoise", "GaussianSmooth"] 