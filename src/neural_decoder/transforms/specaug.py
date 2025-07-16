import random
import torch
import torch.nn.functional as F

class TimeMask:
    """Mask T consecutive frames with prob p."""
    def __init__(self, T=12, p=0.4):
        self.T, self.p = T, p

    def __call__(self, x):
        if random.random() > self.p: 
            return x
        t = random.randint(0, max(0, x.size(0)-self.T-1))
        x[t:t+self.T, :] = 0
        return x

class ElectrodeMask:
    """Mask F random electrodes across the whole sequence."""
    def __init__(self, F=6, p=0.4):
        self.F, self.p = F, p

    def __call__(self, x):
        if random.random() > self.p: 
            return x
        idx = random.sample(range(x.size(1)), self.F)
        x[:, idx] = 0
        return x

class TimeWarp:
    """Spline-warp the time axis by ±W%."""
    def __init__(self, W=0.05, p=0.2):
        self.W, self.p = W, p

    def __call__(self, x):
        if random.random() > self.p: 
            return x
        T = x.size(0)
        factor = 1 + random.uniform(-self.W, self.W)
        idx = torch.linspace(0, T-1, int(T*factor))
        idx = torch.clamp(idx.round().long(), 0, T-1)
        return x[idx]

__all__ = ["TimeMask", "ElectrodeMask", "TimeWarp"] 