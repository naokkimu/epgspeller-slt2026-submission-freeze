#!/usr/bin/env python3
"""
Simple PCA model generator for unified pipeline
"""
import numpy as np
from sklearn.decomposition import PCA
import os

def generate_pca_model():
    """
    Generate PCA16 model from existing dataset
    """
    # Load raw dataset
    dataset_path = "data/silentspeller_dataset/p1_2328_old_dataset.npz"
    print(f"Loading dataset from {dataset_path}")
    
    data = np.load(dataset_path, allow_pickle=True)
    
    # Extract training data for PCA fitting
    # Data is stored as array of individual samples (T, 124)
    all_data = data['data']
    print(f"Number of samples: {len(all_data)}")
    print(f"First sample shape: {all_data[0].shape}")
    
    # Concatenate all samples for PCA fitting
    X_flat = np.concatenate([sample for sample in all_data], axis=0)
    N_features = X_flat.shape[1]
    print(f"Flattened data shape: {X_flat.shape}")
    
    # Fit PCA
    print("Fitting PCA with 16 components...")
    pca = PCA(n_components=16)
    pca.fit(X_flat)
    
    # Save PCA components (transformation matrix)
    os.makedirs("models", exist_ok=True)
    np.save("models/pca16.npy", pca.components_)
    
    print(f"PCA model saved to models/pca16.npy")
    print(f"Explained variance ratio: {pca.explained_variance_ratio_.sum():.3f}")
    print(f"Component shape: {pca.components_.shape}")

if __name__ == "__main__":
    generate_pca_model() 