#%%
import os
import pickle
from datetime import datetime
from pathlib import Path
from neural_decoder.neural_decoder_trainer import trainModel

# Set parameters directly
dataset_path = "silentspeller_decoder/data/pca64"  # ここにデータセットのパスを設定
model_name = Path(dataset_path).name  # データセットのディレクトリ名をモデル名として使用

# Load dataset to get input features dimension
with open(dataset_path, "rb") as handle:
    dataset = pickle.load(handle)
n_input_features = dataset['train'][0]['sentenceDat'][0].shape[1]

# データセット名の抽出（パスの最後の部分を使用）
dataset_name = Path(dataset_path).stem

# 日時とデータセット名でログディレクトリ名を生成
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_dir_name = f"{timestamp}_{dataset_name}"
if model_name:  # オプションのモデル名が指定されていれば追加
    log_dir_name += f"_{model_name}"

model_args = {}
model_args['outputDir'] = os.path.join('./logs', log_dir_name)
model_args['datasetPath'] = dataset_path

# 時系列長パラメータ
model_args['seqLen'] = 250        # 平均長に近い値（245.17）を切り上げ
model_args['maxTimeSeriesLen'] = 512  # 最大長（501）を超える2のべき乗

model_args['batchSize'] = 64
model_args['lrStart'] = 0.02
model_args['lrEnd'] = 0.02
model_args['nUnits'] = 128
model_args['nBatch'] = 10000
model_args['nLayers'] = 5
model_args['seed'] = 0
model_args['nClasses'] = 40
model_args['nInputFeatures'] = n_input_features  # データセットから自動的に設定
model_args['dropout'] = 0.4
model_args['whiteNoiseSD'] = 0.8
model_args['constantOffsetSD'] = 0.2
model_args['gaussianSmoothWidth'] = 2.0
model_args['strideLen'] = 4
model_args['kernelLen'] = 32
model_args['bidirectional'] = True
model_args['l2_decay'] = 1e-5

trainModel(model_args)
# %%
