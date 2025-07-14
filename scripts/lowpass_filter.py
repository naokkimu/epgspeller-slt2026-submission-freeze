#%%
#データを読み込む　raw_dataset/p1_2328_old_dataset.npz
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# データを読み込む raw_dataset/p1_2328_old_dataset.npz
DATA_PATH = (Path(__file__).parent.parent / 'raw_dataset'
            / 'p1_2328_old_dataset.npz')


def lowpass_filter(data, window_size=5):
    """Apply a simple moving average lowpass filter to the data.
    
    Args:
        data: Input data to filter (array of 2D arrays)
        window_size: Size of the moving average window
    
    Returns:
        filtered_data: List of filtered data arrays
    """
    filtered_data = []
    for sample in data:
        # 各時間ステップに対して1次元のフィルタリングを適用
        filtered_sample = np.zeros_like(sample)
        for ch in range(sample.shape[1]):
            filtered_sample[:, ch] = np.convolve(
                sample[:, ch], 
                np.ones(window_size) / window_size, 
                mode='same'
            )
        filtered_data.append(filtered_sample)
    return filtered_data


def main():
    # データセットを読み込む
    dataset = np.load(DATA_PATH, allow_pickle=True)

    # データセットのキーを確認
    print(dataset.keys())

    # データの中身を確認
    print("Data shape:", dataset['data'].shape)
    print("Label shape:", dataset['label'].shape)
    print("Data type:", type(dataset['data']))
    print("First sample shape:", dataset['data'][0].shape)
    print("Second sample shape:", dataset['data'][1].shape)

    # 最初のサンプルを抽出
    sample_data = dataset['data'][0]

    # サンプルデータを表示
    plt.figure(figsize=(15, 10))
    
    # 元のデータを表示
    plt.subplot(2, 2, 1)
    plt.title('Original Data')
    plt.imshow(sample_data.T, cmap='gray', aspect='auto')
    plt.colorbar(label='Amplitude')
    plt.xlabel('Time')
    plt.ylabel('Channel')
    
    # 異なる窓サイズでフィルタリングを適用
    window_sizes = [1, 5, 10, 20]
    for i, size in enumerate(window_sizes[1:], 2):
        filtered_data = lowpass_filter([sample_data], window_size=size)[0]
        
        plt.subplot(2, 2, i)
        plt.title(f'Filtered Data (window_size={size})')
        plt.imshow(filtered_data.T, cmap='gray', aspect='auto')
        plt.colorbar(label='Amplitude')
        plt.xlabel('Time')
        plt.ylabel('Channel')
    
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
# %%
