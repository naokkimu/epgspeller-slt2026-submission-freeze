
## Dataset Structure

### Silent Speller Dataset
The dataset (`data/silentspeller_dataset/p1_2328_old_dataset.npz`) contains brain activity data and corresponding labels. The data is organized as follows:

#### Data Format
- Total trials: 2,328
- Components:
  - `data`: Brain activity time series data
    - Shape per trial: (250, 124) - 250 time points × 124 features
  - `label`: Text labels for each trial
    - Unicode strings (max length 13 characters)

## Silent Speller Neural Decoder

脳活動データから文字列を予測するためのニューラルデコーダーの実装です。

## データセット

### Silent Speller Dataset
元のデータセット（`raw_dataset/train_test_competition_split.npz`）の構造：
- 訓練データ、テストデータ、コンペティションデータに分割済み
- 各データの形状: (時系列長, 124)
  - 時系列長: 可変
  - 124: 特徴量（脳波チャンネル）
- ラベル: 英単語（大文字のアルファベットのみ）

## 実行手順

### 1. 環境セットアップ
```bash
# リポジトリのクローン
git clone https://github.com/yourusername/silentspeller_decoder.git
cd silentspeller_decoder

### 2. データの前処理

#### 2.1 基本的な前処理（PCAのみ）
```bash
# 16次元PCAを適用
python scripts/prepare_silentspeller_dataset.py --n_components 16
```

#### 2.2 ノイズ除去を追加（PCA + ローパスフィルタ）
```bash
# 16次元PCA + ウィンドウサイズ5のローパスフィルタを適用
python scripts/prepare_silentspeller_dataset.py --n_components 16 --apply_lowpass --lowpass_window_size 5
```

#### 2.3 データ拡張を含む完全な前処理
```bash
# 16次元PCA + ローパスフィルタ + SpecAugment
python scripts/prepare_silentspeller_dataset.py \
    --n_components 16 \
    --apply_lowpass \
    --lowpass_window_size 5 \
    --apply_spec_augment \
    --random_seed 42
```

#### 2.4 TS2Vecによる特徴量抽出を追加
```bash
# 基本的なTS2Vec特徴量抽出
python scripts/prepare_silentspeller_dataset.py \
    --apply_ts2vec \
    --ts2vec_output_dims 320

# カスタムパラメータでのTS2Vec特徴量抽出
python scripts/prepare_silentspeller_dataset.py \
    --apply_ts2vec \
    --ts2vec_output_dims 256 \
    --ts2vec_hidden_dims 128 \
    --ts2vec_depth 8 \
    --ts2vec_epochs 200 \
    --ts2vec_batch_size 32 \
    --ts2vec_sliding_length 100 \
    --ts2vec_sliding_padding 10
```

TS2Vecのオプション：
- `--apply_ts2vec`: TS2Vec特徴量抽出を適用
- `--ts2vec_output_dims`: 出力特徴量の次元数（デフォルト: 320）
- `--ts2vec_hidden_dims`: 隠れ層の次元数（デフォルト: 64）
- `--ts2vec_depth`: エンコーダーの深さ（デフォルト: 10）
- `--ts2vec_epochs`: 学習エポック数（デフォルト: 100）
- `--ts2vec_batch_size`: バッチサイズ（デフォルト: 16）
- `--ts2vec_sliding_length`: スライディングウィンドウの長さ（デフォルト: None）
- `--ts2vec_sliding_padding`: スライディングウィンドウのパディング（デフォルト: 0）

#### 2.5 複数の前処理を組み合わせる
```bash
# PCA + ローパスフィルタ + TS2Vec
python scripts/prepare_silentspeller_dataset.py \
    --n_components 16 \
    --apply_lowpass \
    --lowpass_window_size 5 \
    --apply_ts2vec \
    --ts2vec_output_dims 320

# すべての前処理を適用
python scripts/prepare_silentspeller_dataset.py \
    --n_components 16 \
    --apply_lowpass \
    --lowpass_window_size 5 \
    --apply_spec_augment \
    --apply_ts2vec \
    --ts2vec_output_dims 320
```

出力ファイル名は適用した処理を反映します：
- `pca16_ts2vec320`: PCA(16次元) + TS2Vec(320次元)
- `pca16_lpf5_ts2vec320`: PCA + ローパスフィルタ + TS2Vec
- `pca16_lpf5_augmented_ts2vec320`: すべての処理を適用

処理の順序：
1. ローパスフィルタ（指定時）
2. データ拡張（指定時、学習データのみ）
3. TS2Vec特徴量抽出（指定時）
4. PCA（指定時）

注意点：
- TS2Vecモデルは学習データで学習され、学習済みモデルは`models/ts2vec_model.pt`に保存
- スライディングウィンドウ推論を使用する場合、出力の時系列長が変更される可能性あり
- GPUが利用可能な場合は自動的に使用（`device`パラメータで制御可能）
- メモリ使用量はTS2Vecの出力次元数とバッチサイズに大きく依存

### 3. モデルの学習

#### 3.1 基本的な学習
```bash
# デフォルトパラメータでの学習
python scripts/train.py \
    --data_path data/pca16_lpf5_augmented \
    --batch_size 64 \
    --learning_rate 0.001 \
    --num_epochs 100
```

#### 3.2 ハイパーパラメータを指定した学習
```bash
# カスタムパラメータでの学習
python scripts/train.py \
    --data_path data/pca16_lpf5_augmented \
    --batch_size 128 \
    --learning_rate 0.002 \
    --num_epochs 200 \
    --hidden_size 256 \
    --num_layers 4 \
    --dropout 0.3 \
    --weight_decay 1e-5
```

利用可能なオプション：
```bash
python scripts/train.py --help
```

### 4. モデルの評価

#### 4.1 テストデータでの評価
```bash
# テストデータでの評価
python scripts/eval_model.py \
    --model_path logs/YYYYMMDD_HHMMSS_pca16_lpf5_augmented \
    --partition test
```

#### 4.2 コンペティションデータでの評価
```bash
# コンペティションデータでの評価
python scripts/eval_model.py \
    --model_path logs/YYYYMMDD_HHMMSS_pca16_lpf5_augmented \
    --partition competition
```

#### 4.3 詳細な評価結果の出力
```bash
# 詳細な評価結果を出力
python scripts/eval_model.py \
    --model_path logs/YYYYMMDD_HHMMSS_pca16_lpf5_augmented \
    --partition test \
    --output_dir evaluation_results \
    --save_predictions \
    --plot_confusion_matrix
```

利用可能なオプション：
```bash
python scripts/eval_model.py --help
```

### 5. 結果の確認

#### 5.1 学習ログの確認
```bash
# TensorBoardでの学習ログ確認
tensorboard --logdir logs/
```

#### 5.2 評価結果の確認
```bash
# 評価結果の確認
cat logs/YYYYMMDD_HHMMSS_pca16_lpf5_augmented/evaluation/detailed_results.txt
```
