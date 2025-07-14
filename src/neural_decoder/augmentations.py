import math
import numbers
import torch
from torch import nn
from torch.nn import functional as F
import random


class WhiteNoise(nn.Module):
    def __init__(self, std=0.1):
        super().__init__()
        self.std = std

    def forward(self, x):
        noise = torch.randn_like(x) * self.std
        return x + noise

class MeanDriftNoise(nn.Module):
    def __init__(self, std=0.1):
        super().__init__()
        self.std = std

    def forward(self, x):
        _, C = x.shape
        noise = torch.randn(1, C) * self.std
        return x + noise

class GaussianSmoothing(nn.Module):
    """
    Apply gaussian smoothing on a
    1d, 2d or 3d tensor. Filtering is performed seperately for each channel
    in the input using a depthwise convolution.
    Arguments:
        channels (int, sequence): Number of channels of the input tensors. Output will
            have this number of channels as well.
        kernel_size (int, sequence): Size of the gaussian kernel.
        sigma (float, sequence): Standard deviation of the gaussian kernel.
        dim (int, optional): The number of dimensions of the data.
            Default value is 2 (spatial).
    """

    def __init__(self, channels, kernel_size, sigma, dim=2):
        super(GaussianSmoothing, self).__init__()
        if isinstance(kernel_size, numbers.Number):
            kernel_size = [kernel_size] * dim
        if isinstance(sigma, numbers.Number):
            sigma = [sigma] * dim

        # The gaussian kernel is the product of the
        # gaussian function of each dimension.
        kernel = 1
        meshgrids = torch.meshgrid(
            [torch.arange(size, dtype=torch.float32) for size in kernel_size]
        )
        for size, std, mgrid in zip(kernel_size, sigma, meshgrids):
            mean = (size - 1) / 2
            kernel *= (
                1
                / (std * math.sqrt(2 * math.pi))
                * torch.exp(-(((mgrid - mean) / std) ** 2) / 2)
            )

        # Make sure sum of values in gaussian kernel equals 1.
        kernel = kernel / torch.sum(kernel)

        # Reshape to depthwise convolutional weight
        kernel = kernel.view(1, 1, *kernel.size())
        kernel = kernel.repeat(channels, *[1] * (kernel.dim() - 1))

        self.register_buffer("weight", kernel)
        self.groups = channels

        if dim == 1:
            self.conv = F.conv1d
        elif dim == 2:
            self.conv = F.conv2d
        elif dim == 3:
            self.conv = F.conv3d
        else:
            raise RuntimeError(
                "Only 1, 2 and 3 dimensions are supported. Received {}.".format(dim)
            )

    def forward(self, input):
        """
        Apply gaussian filter to input.
        Arguments:
            input (torch.Tensor): Input to apply gaussian filter on.
        Returns:
            filtered (torch.Tensor): Filtered output.
        """
        return self.conv(input, weight=self.weight, groups=self.groups, padding="same")


# --- New SpecAug++ modules ---------------------------------

class TimeMask:
    """Mask T consecutive frames with prob p."""
    def __init__(self, T=12, p=0.4):
        self.T, self.p = T, p

    def __call__(self, x):
        if random.random() > self.p: return x
        t = random.randint(0, max(0, x.size(0)-self.T-1))
        x[t:t+self.T, :] = 0
        return x

class ElectrodeMask:
    """Mask F random electrodes across the whole sequence."""
    def __init__(self, F=6, p=0.4):
        self.F, self.p = F, p

    def __call__(self, x):
        if random.random() > self.p: return x
        idx = random.sample(range(x.size(1)), self.F)
        x[:, idx] = 0
        return x

class TimeWarp:
    """Spline-warp the time axis by ±W%."""
    def __init__(self, W=0.2, p=0.2):
        self.W, self.p = W, p

    def __call__(self, x):
        if random.random() > self.p: return x
        T = x.size(0)
        factor = 1 + random.uniform(-self.W, self.W)
        idx = torch.linspace(0, T-1, int(T*factor))
        idx = torch.clamp(idx.round().long(), 0, T-1)
        return x[idx]
