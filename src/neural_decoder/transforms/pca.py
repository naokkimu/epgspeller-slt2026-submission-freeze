import torch
import numpy as np
import os

class PCATransform:
    """Apply PCA transformation using pre-fitted model."""
    
    def __init__(self, n_components, model_path):
        """
        Args:
            n_components: Number of PCA components to use
            model_path: Path to saved PCA components (.npy file)
        """
        self.n_components = n_components
        self.model_path = model_path
        
        # Load PCA components
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"PCA model not found at {model_path}")
            
        components = np.load(model_path)  # Shape: (n_components_total, n_features)
        
        # Take only the requested number of components
        if n_components > components.shape[0]:
            raise ValueError(f"Requested {n_components} components, but model has only {components.shape[0]}")
            
        self.W = torch.tensor(components[:n_components], dtype=torch.float32)  # (k, 124)
        
    def __call__(self, x):
        """
        Apply PCA transformation.
        
        Args:
            x: Input tensor of shape (T, n_features)
            
        Returns:
            Transformed tensor of shape (T, n_components)
        """
        # x: (T, 124) -> (T, k)
        return x @ self.W.T

__all__ = ["PCATransform"] 