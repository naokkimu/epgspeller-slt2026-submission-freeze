import torch
import torch.nn.functional as F

class LowPass:
    """Apply moving average filter (lowpass filter)."""
    
    def __init__(self, window=5):
        """
        Args:
            window: Window size for moving average. If 0 or 1, no filtering applied.
        """
        self.window = window
        
        if window > 1:
            # Create uniform kernel for moving average
            kernel = torch.ones(1, 1, window, dtype=torch.float32) / window
            self.register_kernel = kernel
        else:
            self.register_kernel = None
    
    def __call__(self, x):
        """
        Apply moving average filter.
        
        Args:
            x: Input tensor of shape (T, C)
            
        Returns:
            Filtered tensor of shape (T, C)
        """
        if self.window <= 1 or self.register_kernel is None:
            return x
            
        T, C = x.shape
        
        # Process each channel separately
        result = torch.zeros_like(x)
        
        for c in range(C):
            # Extract single channel: (T,) -> (1, 1, T)
            channel_data = x[:, c].unsqueeze(0).unsqueeze(0)
            
            # Apply 1D convolution
            filtered_channel = F.conv1d(channel_data, 
                                       self.register_kernel, 
                                       padding='same')
            
            # Store back: (1, 1, T) -> (T,)
            result[:, c] = filtered_channel.squeeze()
        
        return result

__all__ = ["LowPass"] 