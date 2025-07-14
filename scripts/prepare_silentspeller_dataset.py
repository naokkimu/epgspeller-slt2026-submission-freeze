#%%
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle
import os
from typing import Optional, Dict, Any, List, Set
import argparse
import torch

# アルファベット定義
ALPHABET_DEF = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
ALPHABET_DEF_SIL = ['SIL'] + ALPHABET_DEF  # SILを先頭に配置

# 電極領域の定義
ELECTRODE_REGIONS = {
    'anterior': {  # 前方部（1-8行目）
        'indices': set([1, 0, 5, 4, 3, 2, 11, 10, 9, 8, 7, 6, 19, 18, 17, 16, 15, 14, 13, 12,
                       27, 26, 25, 24, 23, 22, 21, 20, 35, 34, 33, 32, 31, 30, 29, 28,
                       43, 42, 41, 40, 39, 38, 37, 36, 47, 46, 45, 44]),
        'description': '前歯から硬口蓋前部の電極群'
    },
    'middle': {    # 中央部（9-12行目）
        'indices': set([55, 54, 53, 49, 48, 52, 51, 50, 61, 60, 59, 115, 58, 57, 56,
                       67, 66, 65, 114, 64, 63, 62, 76, 75, 74, 73, 99, 72, 71, 70, 69]),
        'description': '硬口蓋中部の電極群'
    },
    'posterior': { # 後方部（13-16行目）
        'indices': set([90, 89, 88, 87, 86, 95, 94, 83, 82, 81, 80, 79,
                       107, 106, 105, 104, 103, 102, 101, 98, 97, 96, 95, 94, 93, 92, 68,
                       123, 122, 121, 120, 119, 118, 117, 116, 113, 112, 111, 110, 109, 108, 78]),
        'description': '硬口蓋後部から軟口蓋の電極群'
    },
    'left': {      # 左側（1-8列目）
        'indices': set([1, 5, 11, 19, 27, 35, 43, 47, 55, 54, 53, 61, 60, 59, 67, 66, 65,
                       76, 75, 74, 73, 90, 89, 88, 87, 86, 107, 106, 105, 104, 103,
                       123, 122, 121, 120, 119]),
        'description': '左側の電極群'
    },
    'right': {     # 右側（9-16列目）
        'indices': set([0, 4, 3, 2, 8, 7, 6, 16, 15, 14, 13, 12, 24, 23, 22, 21, 20,
                       32, 31, 30, 29, 28, 40, 39, 38, 37, 36, 48, 52, 51, 50, 115, 58, 57, 56,
                       114, 64, 63, 62, 99, 72, 71, 70, 69, 95, 94, 83, 82, 81, 80, 79,
                       98, 97, 96, 95, 94, 93, 92, 68, 116, 113, 112, 111, 110, 109, 108, 78]),
        'description': '右側の電極群'
    }
}

def get_selected_electrodes(regions: List[str]) -> Set[int]:
    """選択された領域の電極インデックスの集合を返す"""
    if 'all' in regions:
        return set(range(124))  # 全電極を返す（0-123）
    
    selected = set()
    for region in regions:
        if region in ELECTRODE_REGIONS:
            selected.update(ELECTRODE_REGIONS[region]['indices'])
    
    return selected if selected else set(range(124))


def charToId(c):
    """文字をIDに変換（SIL=0, A=1, B=2, ...）"""
    if c == 'SIL':
        return 0
    return ALPHABET_DEF_SIL.index(c)


def text_to_spaced_text(text):
    """テキストを空白区切りの文字列に変換"""
    return ' '.join(c for c in text.upper() if c in ALPHABET_DEF)


def text_to_char_ids(text, max_length=500):
    """テキストを文字IDの配列に変換（空白区切り対応）"""
    char_ids = np.ones(max_length, dtype=np.int32) * charToId('SIL')
    
    # 文字を空白で区切る
    spaced_text = text_to_spaced_text(text)
    chars = spaced_text.split()
    
    for i, c in enumerate(chars):
        if i >= max_length:
            break
        if c in ALPHABET_DEF:
            char_ids[i] = ALPHABET_DEF_SIL.index(c)
    
    return char_ids


def create_session_data(brain_data, labels):
    """インデックスのリストからセッションデータを作成"""
    session_data = {
        'sentenceDat': [],
        'transcriptions': [],
        'phonemes': [],
        'timeSeriesLens': [],
        'phoneLens': [],
        'phonePerTime': []
    }
    
    for brain_signal, text in zip(brain_data, labels):
        # 脳活動データ
        session_data['sentenceDat'].append(brain_signal)
        
        # テキストラベル
        session_data['transcriptions'].append(text)
        
        # 文字ID変換
        char_ids = text_to_char_ids(text)
        session_data['phonemes'].append(char_ids)
        
        # 長さ情報
        time_len = len(brain_signal)
        char_len = len([c for c in char_ids if c != charToId('SIL')])
        session_data['timeSeriesLens'].append(time_len)
        session_data['phoneLens'].append(char_len)
        session_data['phonePerTime'].append(
            char_len / time_len if time_len > 0 else 0
        )
    
    # numpy配列に変換
    session_data['timeSeriesLens'] = np.array(session_data['timeSeriesLens'])
    session_data['phoneLens'] = np.array(session_data['phoneLens'])
    session_data['phonePerTime'] = np.array(session_data['phonePerTime'])
    
    return session_data


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


def spec_augment(data, labels, 
                time_mask_max_size=None,      # 最大時間マスクサイズ
                freq_mask_max_size=None,      # 最大周波数マスクサイズ
                n_time_masks_max=2,         # 最大時間マスク数
                n_freq_masks_max=2,         # 最大周波数マスク数
                p_apply=0.8):              # データ拡張を適用する確率
    """
    Apply SpecAugment to the input data with dynamic parameters based on input dimensions.
    
    Args:
        data: List of 2D spectrograms with shape (time_steps, freq_bins)
        labels: Input labels
        time_mask_max_size: Maximum possible length of time mask (if None, calculated dynamically)
        freq_mask_max_size: Maximum possible length of frequency mask (if None, calculated dynamically)
        n_time_masks_max: Maximum number of time masks to apply
        n_freq_masks_max: Maximum number of frequency masks to apply
        p_apply: Probability of applying augmentation to each sample
    
    Returns:
        Augmented data and corresponding labels
    """
    augmented_data = []
    
    # Get dimensions from first sample
    time_steps, freq_bins = data[0].shape
    
    # Dynamically set mask sizes if not provided
    if time_mask_max_size is None:
        time_mask_max_size = min(int(time_steps * 0.2), 50)  # 最大で時間軸の20%まで
    if freq_mask_max_size is None:
        freq_mask_max_size = min(int(freq_bins * 0.2), 30)   # 最大で周波数軸の20%まで
    
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


def prepare_silentspeller_dataset(
    n_components: int = 16,
    train_data_ratio: float = 1.0,
    random_seed: int = 42,
    apply_lowpass: bool = False,
    lowpass_window_size: int = 5,
    apply_spec_augment: bool = False,
    spec_augment_params: Optional[Dict[str, Any]] = None,
    augment_multiplier: int = 1,
    apply_ts2vec: bool = False,
    ts2vec_params: Optional[Dict[str, Any]] = None,
    electrode_regions: List[str] = ['all']
):
    """
    Prepare the Silent Speller dataset with optional data augmentation and filtering.
    
    Args:
        n_components: Number of PCA components
        train_data_ratio: Ratio of training data to use (0.0 to 1.0)
        random_seed: Random seed for reproducibility
        apply_lowpass: Whether to apply lowpass filtering
        lowpass_window_size: Window size for lowpass filter
        apply_spec_augment: Whether to apply SpecAugment
        spec_augment_params: Parameters for SpecAugment
        augment_multiplier: Number of augmented copies to create (1 means double the data)
        apply_ts2vec: Whether to apply TS2Vec
        ts2vec_params: Parameters for TS2Vec
        electrode_regions: List of anatomical regions to use ['anterior', 'middle', 'posterior', 'left', 'right', 'all']
    """
    # Set random seed
    np.random.seed(random_seed)
    
    # Get selected electrodes
    selected_electrodes = get_selected_electrodes(electrode_regions)
    print(f"Using {len(selected_electrodes)} electrodes from regions: {', '.join(electrode_regions)}")
    
    # Default SpecAugment parameters
    default_spec_augment_params = {
        'time_mask_max_size': 50,
        'freq_mask_max_size': 30,
        'n_time_masks_max': 2,
        'n_freq_masks_max': 2,
        'p_apply': 0.8
    }
    
    if spec_augment_params is None:
        spec_augment_params = default_spec_augment_params
    else:
        # Update defaults with provided parameters
        spec_augment_params = {**default_spec_augment_params, **spec_augment_params}

    # Default TS2Vec parameters
    default_ts2vec_params = {
        'output_dims': 320,
        'hidden_dims': 64,
        'depth': 10,
        'device': 'cuda' if torch.cuda.is_available() else 'cpu',
        'batch_size': 16,
        'max_train_length': None,
        'temporal_unit': 0,
        'n_epochs': 100,
        'sliding_length': None,
        'sliding_padding': 0,
        'encoding_window': None
    }
    
    if ts2vec_params is None:
        ts2vec_params = default_ts2vec_params
    else:
        # Update defaults with provided parameters
        ts2vec_params = {**default_ts2vec_params, **ts2vec_params}

    # Load and preprocess data
    print("Loading old dataset...")
    split_path = "raw_dataset/p1_2328_old_dataset.npz"
    split_data = np.load(split_path, allow_pickle=True)
    
    # データの取り出しと電極の選択
    def select_electrodes(data):
        """電極選択を適用"""
        if selected_electrodes == set(range(124)):  # 全電極を使用
            return data
        selected_indices = sorted(list(selected_electrodes))
        return [sample[:, selected_indices] for sample in data]
    
    # データの読み込み（p1_2328_old_dataset.npzの構造に対応）
    all_data = select_electrodes(split_data['data'])
    all_labels = split_data['label']
    
    # データを手動で分割（80% train, 10% test, 10% competition）
    n_total = len(all_data)
    n_train = int(n_total * 0.8)
    n_test = int(n_total * 0.1)
    
    # シャッフル
    indices = np.random.permutation(n_total)
    train_indices = indices[:n_train]
    test_indices = indices[n_train:n_train + n_test]
    competition_indices = indices[n_train + n_test:]
    
    train_data = [all_data[i] for i in train_indices]
    train_labels = [all_labels[i] for i in train_indices]
    test_data = [all_data[i] for i in test_indices]
    test_labels = [all_labels[i] for i in test_indices]
    competition_data = [all_data[i] for i in competition_indices]
    competition_labels = [all_labels[i] for i in competition_indices]

    # Adjust training data size if ratio is less than 1.0
    if train_data_ratio < 1.0:
        print(f"\nReducing training data to {train_data_ratio*100:.1f}% of original size...")
        n_samples = len(train_data)
        n_selected = int(n_samples * train_data_ratio)
        indices = np.random.RandomState(random_seed).permutation(n_samples)[:n_selected]
        train_data = [train_data[i] for i in indices]
        train_labels = [train_labels[i] for i in indices]
        print(f"Selected {n_selected} samples from {n_samples} original samples")

    # Apply lowpass filter if specified
    if apply_lowpass:
        print(f"Applying lowpass filter (window_size={lowpass_window_size})...")
        train_data = lowpass_filter(train_data, window_size=lowpass_window_size)
        test_data = lowpass_filter(test_data, window_size=lowpass_window_size)
        competition_data = lowpass_filter(competition_data, window_size=lowpass_window_size)

    # Standardize and fit PCA using only training data
    print("Fitting PCA and StandardScaler on training data...")
    flattened_train = np.vstack(train_data)
    scaler = StandardScaler()
    scaled_train = scaler.fit_transform(flattened_train)
    
    if n_components != -1:
        pca = PCA(n_components=n_components)
        pca.fit(scaled_train)
        print(f"Original feature dimension: {train_data[0].shape[1]}")
        print(f"Reduced feature dimension: {n_components}")
        print(f"Number of sequences: {len(train_data)}")
        print(f"Explained variance ratio: {pca.explained_variance_ratio_.sum():.4f}")
    else:
        print(f"Using raw features (no PCA)")
        print(f"Feature dimension: {train_data[0].shape[1]}")
        print(f"Number of sequences: {len(train_data)}")

    # Transform data and apply SpecAugment after PCA
    def transform_data(data, labels=None, apply_augment=False, augment_params=None):
        original_shapes = [x.shape for x in data]
        flattened_data = np.vstack(data)
        scaled_data = scaler.transform(flattened_data)
        
        if n_components != -1:
            transformed_data = pca.transform(scaled_data)
        else:
            transformed_data = scaled_data
        
        # Reshape back to original sequence lengths
        start_idx = 0
        sequences = []
        for shape in original_shapes:
            seq_length = shape[0]
            seq_data = transformed_data[start_idx:start_idx + seq_length]
            sequences.append(seq_data)
            start_idx += seq_length
            
        # Apply SpecAugment only after PCA/standardization
        if apply_augment and apply_spec_augment:
            print(f"Applying SpecAugment to create {augment_multiplier}x additional training data...")
            params = augment_params if augment_params is not None else {}
            
            augmented_sequences = []
            for _ in range(augment_multiplier):
                # 各反復で異なるマスクサイズを使用
                time_steps = sequences[0].shape[0]
                freq_bins = sequences[0].shape[1]
                
                # 動的なマスクサイズの設定
                curr_params = params.copy()
                curr_params['time_mask_max_size'] = min(int(time_steps * 0.2), 50)
                curr_params['freq_mask_max_size'] = min(int(freq_bins * 0.2), freq_bins // 2)
                curr_params['p_apply'] = 1.0  # 必ず適用
                
                # 拡張データを生成
                aug_sequences, _ = spec_augment(
                    sequences, 
                    [None] * len(sequences), 
                    **curr_params
                )
                
                augmented_sequences.extend(aug_sequences)
            
            # 元のデータと拡張データを結合
            if labels is not None:
                repeated_labels = np.tile(labels, augment_multiplier + 1)
                return sequences + augmented_sequences, repeated_labels
            else:
                return sequences + augmented_sequences
        
        if labels is not None:
            return sequences, labels
        return sequences

    # Transform all datasets (apply SpecAugment only to training data)
    print("Transforming datasets...")
    train_sequences, train_label = transform_data(
        train_data, 
        train_labels, 
        apply_augment=True,
        augment_params=spec_augment_params
    )
    test_sequences = transform_data(test_data, apply_augment=False)
    competition_sequences = transform_data(competition_data, apply_augment=False)

    print(f"Original training sequences: {len(train_data)}")
    print(f"Augmented training sequences: {len(train_sequences)}")

    # Create session data
    print("Creating training session...")
    train_data = [
        create_session_data(
            train_sequences,
            train_label
        )
    ]
    
    print("Creating test session...")
    test_data = [
        create_session_data(
            test_sequences,
            test_labels
        )
    ]
    
    print("Creating competition session...")
    competition_data = [
        create_session_data(
            competition_sequences,
            competition_labels
        )
    ]
    
    # データの保存
    print("Saving formatted data...")
    formatted_data = {
        'train': train_data,
        'test': test_data,
        'competition': competition_data
    }
    
    # Add processing information to the formatted data
    processing_info = {
        'train_data_ratio': train_data_ratio,
        'n_components': n_components,
        'random_seed': random_seed,
        'apply_lowpass': apply_lowpass,
        'lowpass_window_size': lowpass_window_size if apply_lowpass else None,
        'apply_spec_augment': apply_spec_augment,
        'spec_augment_params': spec_augment_params if apply_spec_augment else None,
        'augment_multiplier': augment_multiplier if apply_spec_augment else 0,
        'apply_ts2vec': apply_ts2vec,
        'ts2vec_params': ts2vec_params if apply_ts2vec else None,
        'electrode_regions': electrode_regions
    }
    formatted_data['processing_info'] = processing_info
    
    # Generate output path with processing information
    output_name = []
    if train_data_ratio < 1.0:
        output_name.append(f"train{int(train_data_ratio*100)}p")
    if n_components != -1:
        output_name.append(f"pca{n_components}")
    if 'all' not in electrode_regions:
        output_name.append('_'.join(sorted(electrode_regions)))  # 領域名をソートして一貫性を保つ
    if apply_lowpass:
        output_name.append(f"lpf{lowpass_window_size}")
    if apply_spec_augment:
        output_name.append(f"aug{augment_multiplier+1}x")
    if apply_ts2vec:
        output_name.append(f"ts2vec{ts2vec_params['output_dims']}")
    
    formatted_output_path = f"data/{'_'.join(output_name)}"
    
    os.makedirs(os.path.dirname(formatted_output_path), exist_ok=True)
    with open(formatted_output_path, 'wb') as f:
        pickle.dump(formatted_data, f)
    
    print(f"Done! Dataset preparation completed successfully. Saved to {formatted_output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare Silent Speller dataset with different configurations')
    parser.add_argument('--n_components', type=int, required=True,
                      help='Number of PCA components')
    parser.add_argument('--train_data_ratio', type=float, default=1.0,
                      help='Ratio of training data to use (0.0 to 1.0)')
    parser.add_argument('--random_seed', type=int, default=42,
                      help='Random seed for reproducibility')
    parser.add_argument('--apply_lowpass', action='store_true',
                      help='Apply lowpass filter')
    parser.add_argument('--lowpass_window_size', type=int, default=5,
                      help='Window size for lowpass filter')
    parser.add_argument('--apply_spec_augment', action='store_true',
                      help='Apply SpecAugment data augmentation')
    parser.add_argument('--apply_ts2vec', action='store_true',
                      help='Apply TS2Vec feature extraction')
    parser.add_argument('--ts2vec_output_dims', type=int, default=320,
                      help='Output dimension for TS2Vec')
    parser.add_argument('--ts2vec_hidden_dims', type=int, default=64,
                      help='Hidden dimension for TS2Vec')
    parser.add_argument('--ts2vec_depth', type=int, default=10,
                      help='Depth of TS2Vec encoder')
    parser.add_argument('--ts2vec_epochs', type=int, default=100,
                      help='Number of epochs for TS2Vec training')
    parser.add_argument('--ts2vec_batch_size', type=int, default=16,
                      help='Batch size for TS2Vec')
    parser.add_argument('--ts2vec_sliding_length', type=int, default=None,
                      help='Sliding window length for TS2Vec inference')
    parser.add_argument('--ts2vec_sliding_padding', type=int, default=0,
                      help='Sliding window padding for TS2Vec inference')
    parser.add_argument('--augment_multiplier', type=int, default=1,
                      help='Number of augmented copies to create (1 means double the data)')
    parser.add_argument('--electrode_regions', nargs='+', 
                      choices=['anterior', 'middle', 'posterior', 'left', 'right', 'all'],
                      default=['all'],
                      help='Anatomical regions of electrodes to use. Multiple regions can be specified.')
    
    args = parser.parse_args()
    
    # Prepare TS2Vec parameters if needed
    ts2vec_params = None
    if args.apply_ts2vec:
        ts2vec_params = {
            'output_dims': args.ts2vec_output_dims,
            'hidden_dims': args.ts2vec_hidden_dims,
            'depth': args.ts2vec_depth,
            'batch_size': args.ts2vec_batch_size,
            'n_epochs': args.ts2vec_epochs,
            'sliding_length': args.ts2vec_sliding_length,
            'sliding_padding': args.ts2vec_sliding_padding
        }
    
    prepare_silentspeller_dataset(
        n_components=args.n_components,
        train_data_ratio=args.train_data_ratio,
        random_seed=args.random_seed,
        apply_lowpass=args.apply_lowpass,
        lowpass_window_size=args.lowpass_window_size,
        apply_spec_augment=args.apply_spec_augment,
        augment_multiplier=args.augment_multiplier,
        apply_ts2vec=args.apply_ts2vec,
        ts2vec_params=ts2vec_params,
        electrode_regions=args.electrode_regions
    )

# %%
