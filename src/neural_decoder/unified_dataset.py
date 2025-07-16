import torch
import numpy as np
from torch.utils.data import Dataset
from neural_decoder.transforms import *

# Simple label mapping for characters
CHAR_TO_ID = {chr(i): i - ord('A') for i in range(ord('A'), ord('Z') + 1)}
CHAR_TO_ID.update({' ': 26, 'SIL': 27})  # Space and silence

def encode_string_label(label_str):
    """Convert string label to character IDs."""
    # Simple approach: use first few characters
    label_str = label_str.upper()[:10]  # Take first 10 chars, uppercase
    char_ids = []
    for char in label_str:
        if char in CHAR_TO_ID:
            char_ids.append(CHAR_TO_ID[char])
        else:
            char_ids.append(26)  # Unknown -> space
    
    # Pad to fixed length
    while len(char_ids) < 10:
        char_ids.append(27)  # SIL padding
    
    return char_ids[:10]

def load_npz(data_path):
    """Load npz dataset and split into train/test."""
    data = np.load(data_path, allow_pickle=True)
    
    # Extract raw data and labels
    all_data = data['data']  # Array of (T, 124) samples
    all_labels = data['label']  # Array of string labels
    
    # Simple 80/20 split for train/test
    n_samples = len(all_data)
    n_train = int(0.8 * n_samples)
    
    indices = np.random.RandomState(42).permutation(n_samples)
    train_indices = indices[:n_train]
    test_indices = indices[n_train:]
    
    return {
        'train_data': all_data[train_indices],
        'train_label': all_labels[train_indices],
        'test_data': all_data[test_indices], 
        'test_label': all_labels[test_indices]
    }

class UnifiedEPGDataset(Dataset):
    """Unified EPG dataset with configurable transforms pipeline."""
    
    def __init__(self, split: str, cfg):
        """
        Args:
            split: 'train' or 'test'
            cfg: Configuration object with transform settings
        """
        # Load data
        data_dict = load_npz(cfg.data.path)
        self.data = data_dict[split + '_data']
        self.label = data_dict[split + '_label']
        self.split = split
        
        # ========== Always-on transforms (deterministic) ==========
        self.pipe = []
        
        if cfg.pca.enable:
            self.pipe.append(PCATransform(cfg.pca.n_components, cfg.pca.model_path))
            
        if cfg.lowpass.enable and cfg.lowpass.window > 1:
            self.pipe.append(LowPass(cfg.lowpass.window))
            
        if cfg.ts2vec.enable:
            self.pipe.append(TS2VecEncoder(cfg.ts2vec))
            
        # ========== Train-only stochastic operations ==========
        self.train_ops = []
        
        if split == "train":
            # SpecAug operations
            if cfg.specaug.time_mask.p > 0:
                self.train_ops.append(TimeMask(**cfg.specaug.time_mask))
            if cfg.specaug.electrode_mask.p > 0:
                self.train_ops.append(ElectrodeMask(**cfg.specaug.electrode_mask))
            if cfg.specaug.time_warp.p > 0:
                self.train_ops.append(TimeWarp(**cfg.specaug.time_warp))
                
            # Noise operations
            if cfg.noise.white_noise.p > 0:
                self.train_ops.append(WhiteNoise(**cfg.noise.white_noise))
            if cfg.noise.drift_noise.p > 0:
                self.train_ops.append(DriftNoise(**cfg.noise.drift_noise))
            if cfg.noise.gaussian_smooth.p > 0:
                self.train_ops.append(GaussianSmooth(**cfg.noise.gaussian_smooth))
        
        print(f"UnifiedEPGDataset {split}: {len(self.data)} samples")
        print(f"  Always-on transforms: {len(self.pipe)}")
        print(f"  Train-only ops: {len(self.train_ops)}")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        # Convert to tensor
        x = torch.tensor(self.data[idx], dtype=torch.float32)  # (T, 124)
        
        # Apply always-on transforms
        for op in self.pipe:
            x = op(x)
            
        # Apply train-only stochastic operations
        if self.split == "train":
            for op in self.train_ops:
                x = op(x)
        
        # Convert label to character sequence
        label_ids = encode_string_label(self.label[idx])
        
        return x, torch.tensor(label_ids, dtype=torch.long)

__all__ = ["UnifiedEPGDataset", "load_npz", "encode_string_label"] 