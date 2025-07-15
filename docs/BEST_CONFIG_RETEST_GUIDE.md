# Silent Speller Decoder: 最良条件での追試手続きガイド

このガイドでは、Silent Speller Decoderの最良条件での追試を実行し、結果を取得する手順を説明します。

## 1. 環境準備

### 1.1 必要なパッケージのインストール
```bash
# requirements.txtからパッケージをインストール
pip install -r requirements.txt
```

### 1.2 ディレクトリ構造の確認
```
silentspeller_decoder/
├── data/
│   ├── pca64                    # 64次元PCA特徴量データ
│   ├── pca32                    # 32次元PCA特徴量データ  
│   └── pca16                    # 16次元PCA特徴量データ
├── scripts/
│   ├── best_config_retest.py    # 最良条件での追試スクリプト
│   └── eval_model.py            # モデル評価スクリプト
├── src/
│   └── neural_decoder/          # ニューラルデコーダーパッケージ
└── logs/                        # 学習結果保存ディレクトリ
```

## 2. 最良条件の特定

### 2.1 過去の実験結果に基づく最良条件
Lake Tahoeの実験結果から以下の条件が最良と判明：

**データセット**: pca64 (64次元PCA特徴量)
**モデル構成**:
- nUnits: 128
- nLayers: 5  
- dropout: 0.4
- strideLen: 4
- kernelLen: 32
- bidirectional: True

**学習パラメータ**:
- batchSize: 64
- lrStart: 0.02
- lrEnd: 0.02
- nBatch: 10000

**データ拡張**:
- whiteNoiseSD: 0.8
- constantOffsetSD: 0.2
- gaussianSmoothWidth: 2.0

### 2.2 条件の根拠
- Lake Tahoe実験でCER = 0.123188を達成
- 複数の実験結果の比較により特定

## 3. 追試スクリプトの実行

### 3.1 最良条件での追試実行
```bash
# ログディレクトリの作成
mkdir -p logs

# PYTHONPATHを設定して追試実行
PYTHONPATH=$PYTHONPATH:./src python scripts/best_config_retest.py
```

### 3.2 実行時の出力例
```
=== Best Configuration Retest ===
Dataset: data/pca64
Output directory: ./logs/20250715_074702_pca64_best_config_retest
Model parameters:
  seqLen: 250
  maxTimeSeriesLen: 512
  ...

Starting training with best configuration...
MPS available but using CPU due to CTC loss compatibility
batch 0, ctc loss: 19.243761, cer: 1.000000, time/batch:   0.005
batch 100, ctc loss: 3.063680, cer: 1.000000, time/batch:   0.024
...
```

## 4. 学習結果の確認

### 4.1 結果確認スクリプトの実行
```bash
python check_results.py
```

### 4.2 期待される結果の例
```
=== Training Results ===
Log directory: logs/20250715_074702_pca64_best_config_retest
Dataset: data/pca64
Model configuration:
  nUnits: 128
  nLayers: 5
  dropout: 0.4
  batchSize: 64
  lrStart: 0.02

Final validation loss: 0.550009
Final validation CER: 0.173913
Best validation CER: 0.166667
Best CER achieved at batch: 2700
```

### 4.3 生成されるファイル
```
logs/TIMESTAMP_pca64_best_config_retest/
├── trainingStats        # 学習統計（CER、Loss）
├── modelWeights         # 最良モデルの重み
├── args                 # 学習時の引数
└── training_curves.png  # 学習曲線グラフ
```

## 5. モデル評価の実行

### 5.1 テストデータでの評価
```bash
# テストデータでの評価
PYTHONPATH=$PYTHONPATH:./src python scripts/eval_model.py \
    --model_path logs/TIMESTAMP_pca64_best_config_retest \
    --partition test
```

### 5.2 コンペティションデータでの評価
```bash
# コンペティションデータでの評価
PYTHONPATH=$PYTHONPATH:./src python scripts/eval_model.py \
    --model_path logs/TIMESTAMP_pca64_best_config_retest \
    --partition competition
```

### 5.3 評価結果の確認
```bash
# 評価メトリクスの確認
cat logs/TIMESTAMP_pca64_best_config_retest/evaluation/metrics.txt

# 詳細な結果の確認
head -50 logs/TIMESTAMP_pca64_best_config_retest/evaluation/detailed_results.txt
```

## 6. 期待される最終結果

### 6.1 学習結果
- **Best validation CER**: 0.166667 (batch 2700付近)
- **Final validation CER**: 0.173913
- **Final validation loss**: 0.550009

### 6.2 評価結果
- **Test CER**: 0.2500
- **Test WER**: 0.6000

### 6.3 結果の解釈
- Validation CERが0.16-0.17程度であれば正常
- Test CERはvalidationより若干高くなるのが一般的
- 前回のLake Tahoe実験（CER = 0.123188）との比較

## 7. トラブルシューティング

### 7.1 よくある問題と解決策

**問題**: `ModuleNotFoundError: No module named 'neural_decoder'`
**解決**: PYTHONPATHを設定
```bash
PYTHONPATH=$PYTHONPATH:./src python scripts/best_config_retest.py
```

**問題**: データファイルが見つからない
**解決**: データファイルの存在確認
```bash
ls -la data/pca64
```

**問題**: 学習が途中で止まる
**解決**: メモリ不足の可能性、batchSizeを減らす

### 7.2 実行環境の注意事項
- CPUでの実行（MPS/CUDAは使用しない）
- メモリ使用量: 約2-4GB
- 実行時間: 約30-60分（環境により異なる）

## 8. 結果の再現性について

### 8.1 再現性に影響する要因
- 乱数シード（seed=0で固定）
- 実行環境（CPU/GPU）
- PyTorchバージョン
- 数値計算の精度

### 8.2 期待される変動範囲
- CER: ±0.01程度の変動は正常
- 大きな変動（±0.05以上）がある場合は環境を確認

## 9. 追加の実験

### 9.1 より長時間の学習
```python
# scripts/best_config_retest.pyの修正
model_args['nBatch'] = 20000  # 10000から20000に変更
```

### 9.2 異なるデータセットでの実験
```python
# データセットの変更
dataset_path = "data/pca32"  # pca64からpca32に変更
```

## 10. 参考資料

- `scripts/train_laketahoe.ipynb`: 元のLake Tahoe実験ノートブック
- `scripts/nlayers_n_units_grid_search.py`: グリッドサーチスクリプト
- `scripts/optuna_train.py`: Optunaによる最適化スクリプト
- `src/neural_decoder/neural_decoder_trainer.py`: 学習ロジック
- `src/neural_decoder/model.py`: モデル定義

---

このガイドに従って実行すれば、最良条件での追試結果を再現できます。問題が発生した場合は、トラブルシューティングセクションを参照してください。 