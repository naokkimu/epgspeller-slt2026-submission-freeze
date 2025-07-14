#%%
#データを読み込む　raw_dataset/p1_2328_old_dataset.npz
import numpy as np

# データセットを読み込む
dataset = np.load('/Users/naokkimu/lyworks/silentspeller_decoder/raw_dataset/p1_2328_old_dataset.npz',allow_pickle=True)

# データセットのキーを確認
print(dataset.keys())

# データの中身を確認
print("Data shape:", dataset['data'].shape)
print("Label shape:", dataset['label'].shape)
print("Data type:", type(dataset['data']))
print("First sample shape:", dataset['data'][0].shape)
print("Second sample shape:", dataset['data'][1].shape)

#最初の３サンプルをvisualize imshowを使って
import matplotlib.pyplot as plt

# 最初の3サンプルを抽出
sample_data = dataset['data'][:3]
sample_labels = dataset['label'][:3]

# サンプルデータを表示
plt.imshow(sample_data[0].T,cmap='gray')
plt.show()
# %%

def spec_augment(data, labels, 
                time_mask_max_size=50,      # 最大時間マスクサイズ
                freq_mask_max_size=30,      # 最大周波数マスクサイズ
                n_time_masks_max=2,         # 最大時間マスク数
                n_freq_masks_max=2,         # 最大周波数マスク数
                p_apply=0.8):              # データ拡張を適用する確率
    """
    Apply SpecAugment to the input data with random parameters.
    
    Args:
        data: List of 2D spectrograms with shape (time_steps, freq_bins)
        labels: Input labels
        time_mask_max_size: Maximum possible length of time mask
        freq_mask_max_size: Maximum possible length of frequency mask
        n_time_masks_max: Maximum number of time masks to apply
        n_freq_masks_max: Maximum number of frequency masks to apply
        p_apply: Probability of applying augmentation to each sample
    
    Returns:
        Augmented data and corresponding labels
    """
    augmented_data = []
    
    for spectrogram in data:
        # p_applyの確率でデータ拡張を適用
        if np.random.random() > p_apply:
            augmented_data.append(spectrogram.copy())
            continue
            
        # 各スペクトログラムをコピー
        aug_spec = spectrogram.copy()
        time_steps, freq_bins = aug_spec.shape
        
        # ランダムなマスクパラメータの生成
        time_mask_size = np.random.randint(time_mask_max_size // 2, time_mask_max_size + 1)
        freq_mask_size = np.random.randint(freq_mask_max_size // 2, freq_mask_max_size + 1)
        n_time_masks = np.random.randint(1, n_time_masks_max + 1)
        n_freq_masks = np.random.randint(1, n_freq_masks_max + 1)
        
        # マスクパラメータの調整（データサイズに応じて）
        time_mask_size = min(time_mask_size, time_steps // 4)  # 最大で1/4までマスク
        freq_mask_size = min(freq_mask_size, freq_bins // 4)   # 最大で1/4までマスク
        
        # Time masking
        for _ in range(n_time_masks):
            t = np.random.randint(0, time_mask_size)
            t0 = np.random.randint(0, time_steps - t)
            aug_spec[t0:t0 + t, :] = 0
            
        # Frequency masking
        for _ in range(n_freq_masks):
            f = np.random.randint(0, freq_mask_size)
            f0 = np.random.randint(0, freq_bins - f)
            aug_spec[:, f0:f0 + f] = 0
            
        augmented_data.append(aug_spec)
    
    return augmented_data, labels

# Apply SpecAugment and display multiple examples
plt.figure(figsize=(15, 10))

# Original spectrograms
for i in range(3):
    plt.subplot(3, 2, 2*i + 1)
    plt.title(f'Original Spectrogram {i+1}')
    plt.imshow(dataset['data'][i], cmap='gray')
    plt.xlabel('Frequency')
    plt.ylabel('Time')

# Generate different augmentations
augmented_data, augmented_labels = spec_augment(dataset['data'][:3], dataset['label'][:3])
for i in range(3):
    plt.subplot(3, 2, 2*i + 2)
    plt.title(f'Augmented Spectrogram {i+1}')
    plt.imshow(augmented_data[i], cmap='gray')
    plt.xlabel('Frequency')
    plt.ylabel('Time')

plt.tight_layout()
plt.show()
# %%
