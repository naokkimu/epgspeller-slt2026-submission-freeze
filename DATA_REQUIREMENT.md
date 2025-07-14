# Silent Speller Neural Decoder - データ要件と整形プロセス

このドキュメントでは、Silent Speller Neural Decoderモデルの入力データ要件と、rawデータから学習可能な形式への整形プロセスについて説明します。

## 1. モデル入力データ要件

### 1.1 神経活動データ（Neural Features）

**基本仕様:**
- **形状**: `(time_steps, n_features)` の2次元配列
- **データ型**: `torch.float32`
- **時間軸**: 可変長（113〜501ステップの範囲）
- **特徴量軸**: 電極数（オリジナル124電極から次元削減可能）

**具体例:**
```python
neural_data.shape  # (272, 16) - 272時間ステップ、16次元特徴量（PCA後）
```

### 1.2 ラベルデータ（Text Labels）

**文字ID変換:**
- `SIL` (Silent) = 0
- `A` = 1, `B` = 2, ..., `Z` = 26
- アルファベットのみサポート（大文字に正規化）

**形式:**
```python
phonemes = [2, 18, 5, 1, 11, 19, 0, 0, ...]  # "BREAKS" → [B, R, E, A, K, S, SIL, SIL, ...]
```

### 1.3 データセット構造

`SpeechDataset`クラスが期待する構造：

```python
session_data = {
    'sentenceDat': [array_1, array_2, ...],     # 神経活動データのリスト
    'transcriptions': ['text1', 'text2', ...],  # 元のテキスト
    'phonemes': [ids_1, ids_2, ...],            # 文字IDの配列
    'timeSeriesLens': [len1, len2, ...],        # 各サンプルの時系列長
    'phoneLens': [plen1, plen2, ...],           # 各サンプルの文字数
    'phonePerTime': [ratio1, ratio2, ...]       # 文字密度（文字数/時間）
}
```

## 2. Raw データから整形するコード

### 2.1 メインスクリプト

**ファイル**: `scripts/prepare_silentspeller_dataset.py`

このスクリプトがrawデータ（`raw_dataset/train_test_competition_split.npz`）から学習可能な形式への変換を担当します。

### 2.2 Raw データ構造

```python
# raw_dataset/train_test_competition_split.npz の内容
{
    'train_data': [array_1, array_2, ...],      # (time_steps, 124) の配列リスト
    'train_label': ['text1', 'text2', ...],     # 対応するテキストラベル
    'test_data': [...],                         # テストデータ
    'test_label': [...],                        # テストラベル
    'competition_data': [...],                  # 競技用データ
    'competition_label': [...]                  # 競技用ラベル
}
```

**統計情報:**
- 訓練サンプル数: 2,128個
- 時系列長の範囲: 113〜501ステップ
- 電極数: 124チャンネル

## 3. 主要な処理ステップ

### 3.1 電極選択（Electrode Selection）

**関数**: `get_selected_electrodes(regions)`

解剖学的領域による電極選択:

```python
ELECTRODE_REGIONS = {
    'anterior': {...},   # 前歯から硬口蓋前部の電極群（1-8行目）
    'middle': {...},     # 硬口蓋中部の電極群（9-12行目）
    'posterior': {...},  # 硬口蓋後部から軟口蓋の電極群（13-16行目）
    'left': {...},       # 左側の電極群（1-8列目）
    'right': {...}       # 右側の電極群（9-16列目）
}
```

### 3.2 前処理（Preprocessing）

#### 標準化とPCA次元削減

```python
def transform_data(data, n_components=16):
    # 1. 全データを1次元に展開
    flattened_data = np.vstack(data)
    
    # 2. 標準化（平均0、分散1）
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(flattened_data)
    
    # 3. PCA次元削減
    if n_components != -1:
        pca = PCA(n_components=n_components)
        transformed_data = pca.fit_transform(scaled_data)
    else:
        transformed_data = scaled_data
    
    # 4. 元の時系列形式に復元
    sequences = restore_sequences(transformed_data, original_shapes)
    return sequences
```

#### ローパスフィルタ（オプション）

```python
def lowpass_filter(data, window_size=5):
    """移動平均による簡単なローパスフィルタ"""
    filtered_data = []
    for sample in data:
        filtered_sample = np.zeros_like(sample)
        for ch in range(sample.shape[1]):
            filtered_sample[:, ch] = np.convolve(
                sample[:, ch], 
                np.ones(window_size) / window_size, 
                mode='same'
            )
        filtered_data.append(filtered_sample)
    return filtered_data
```

### 3.3 テキストラベル変換

**関数**: `text_to_char_ids(text, max_length=500)`

```python
def charToId(c):
    """文字をIDに変換"""
    if c == 'SIL':
        return 0
    return ALPHABET_DEF_SIL.index(c)  # SIL, A, B, C, ...

def text_to_char_ids(text, max_length=500):
    """テキストを文字IDの配列に変換"""
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
```

### 3.4 データ拡張（オプション）

**SpecAugment**: 時間軸と周波数軸のマスキング

```python
def spec_augment(data, time_mask_max_size=50, freq_mask_max_size=30, 
                 n_time_masks_max=2, n_freq_masks_max=2, p_apply=0.8):
    """
    SpecAugmentによるデータ拡張
    - 時間マスク: ランダムな時間区間をゼロに
    - 周波数マスク: ランダムな特徴量をゼロに
    """
    # 実装詳細は scripts/prepare_silentspeller_dataset.py を参照
```

### 3.5 セッションデータ作成

**関数**: `create_session_data(brain_data, labels)`

```python
def create_session_data(brain_data, labels):
    session_data = {
        'sentenceDat': [],
        'transcriptions': [],
        'phonemes': [],
        'timeSeriesLens': [],
        'phoneLens': [],
        'phonePerTime': []
    }
    
    for brain_signal, text in zip(brain_data, labels):
        # 神経データを追加
        session_data['sentenceDat'].append(brain_signal)
        session_data['transcriptions'].append(text)
        
        # 文字ID変換
        char_ids = text_to_char_ids(text)
        session_data['phonemes'].append(char_ids)
        
        # 長さ情報計算
        time_len = len(brain_signal)
        char_len = len([c for c in char_ids if c != charToId('SIL')])
        session_data['timeSeriesLens'].append(time_len)
        session_data['phoneLens'].append(char_len)
        session_data['phonePerTime'].append(char_len / time_len if time_len > 0 else 0)
    
    return session_data
```

## 4. 使用方法

### 4.1 基本的な使用例

```bash
# 基本: PCA16次元に削減
python scripts/prepare_silentspeller_dataset.py --n_components 16

# 全特徴量を使用（PCAなし）
python scripts/prepare_silentspeller_dataset.py --n_components -1

# 異なる次元数での削減
python scripts/prepare_silentspeller_dataset.py --n_components 64
```

### 4.2 前処理オプション

```bash
# ローパスフィルタを適用
python scripts/prepare_silentspeller_dataset.py --n_components 16 \
    --apply_lowpass --lowpass_window_size 5

# 特定の電極領域のみ使用
python scripts/prepare_silentspeller_dataset.py --n_components 16 \
    --electrode_regions anterior left

# 訓練データの一部のみ使用
python scripts/prepare_silentspeller_dataset.py --n_components 16 \
    --train_data_ratio 0.5
```

### 4.3 データ拡張

```bash
# SpecAugmentで3倍に拡張
python scripts/prepare_silentspeller_dataset.py --n_components 16 \
    --apply_spec_augment --augment_multiplier 3
```

### 4.4 出力ファイル命名規則

生成されるファイル名は処理パラメータに基づいて自動生成されます：

```
data/pca16                    # 基本: PCA 16次元
data/pca16_lpf5              # ローパスフィルタ（窓幅5）
data/pca16_aug3x             # 3倍データ拡張
data/pca16_anterior_left     # 特定電極領域
data/train50p_pca16          # 50%訓練データ
```

## 5. データフロー

```
Raw Data (124電極, 可変時間長)
    ↓
電極選択 (anatomical regions)
    ↓
Selected Electrodes
    ↓
ローパスフィルタ (optional)
    ↓
標準化 (StandardScaler)
    ↓
PCA次元削減 (n_components)
    ↓
データ拡張 (SpecAugment, optional)
    ↓
テキストラベル変換 (char IDs)
    ↓
セッション形式変換
    ↓
Final Dataset Format
    ↓
保存 (pickle形式)
```

## 6. モデルでの使用

処理済みデータは以下のように使用されます：

```python
# データセット読み込み
with open('data/pca16', 'rb') as f:
    dataset = pickle.load(f)

# データセットクラスで使用
from neural_decoder.dataset import SpeechDataset
train_dataset = SpeechDataset(dataset['train'])

# データローダー作成
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# モデルへの入力
for neural_feats, phone_seqs, neural_lens, phone_lens, days in train_loader:
    output = model(neural_feats, days)
```

## 7. 重要な注意事項

1. **時系列長の可変性**: 各サンプルの時系列長が異なるため、バッチ処理時にはパディングが必要
2. **CTCロス**: 文字レベルのアライメントが不要なCTC（Connectionist Temporal Classification）を使用
3. **Day Adaptation**: モデルは異なる日（セッション）に対応するday-specific layersを持つ
4. **電極の解剖学的意味**: 電極位置は口腔内の解剖学的構造に対応している

## 8. トラブルシューティング

### よくある問題

1. **メモリ不足**: 大きなデータセットや高次元の特徴量を使用する場合
   - 解決: `n_components`を小さくする、`train_data_ratio`を下げる

2. **PCAの説明分散比が低い**: 重要な情報が失われている可能性
   - 解決: `n_components`を増やす、または`--n_components -1`で全特徴量を使用

3. **処理時間が長い**: データ拡張や大きなデータセットの処理
   - 解決: データ拡張を無効にする、サブサンプリングを使用

### デバッグ用コード

```python
# データの基本統計を確認
def check_data_stats(data_path):
    with open(data_path, 'rb') as f:
        data = pickle.load(f)
    
    train = data['train'][0]
    print(f"Training samples: {len(train['sentenceDat'])}")
    print(f"Feature dimension: {train['sentenceDat'][0].shape[1]}")
    print(f"Time length range: {min(train['timeSeriesLens'])} - {max(train['timeSeriesLens'])}")
    print(f"Text length range: {min(train['phoneLens'])} - {max(train['phoneLens'])}")
```

このレポートは、Silent Speller Neural Decoderプロジェクトにおけるデータ処理の完全なガイドとして機能します。 