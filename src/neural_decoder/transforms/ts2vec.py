import torch
import warnings

class TS2VecEncoder:
    """TS2Vec encoder (stub implementation for future extension)."""
    
    def __init__(self, cfg):
        """
        Args:
            cfg: Configuration object with TS2Vec parameters
        """
        self.cfg = cfg
        self.model = None
        self.fitted = False
        
        # Extract config parameters
        self.output_dims = getattr(cfg, 'output_dims', 320)
        self.hidden_dims = getattr(cfg, 'hidden_dims', 128)
        self.depth = getattr(cfg, 'depth', 8)
        self.epochs = getattr(cfg, 'epochs', 200)
        self.batch_size = getattr(cfg, 'batch_size', 32)
        
        warnings.warn("TS2VecEncoder is currently a stub implementation. "
                     "Returns input unchanged for now.")
    
    def fit(self, x):
        """
        Fit TS2Vec model (placeholder).
        
        Args:
            x: Input tensor of shape (T, C)
        """
        # TODO: Implement actual TS2Vec training
        print(f"TS2Vec fit called with input shape: {x.shape}")
        self.fitted = True
        # For now, just create identity transformation
        self.model = torch.eye(x.size(1))
        
    def __call__(self, x):
        """
        Apply TS2Vec encoding.
        
        Args:
            x: Input tensor of shape (T, C)
            
        Returns:
            Encoded tensor (currently returns input unchanged)
        """
        if not self.fitted:
            self.fit(x)
        
        # TODO: Implement actual TS2Vec encoding
        # For now, return input unchanged
        return x

__all__ = ["TS2VecEncoder"] 