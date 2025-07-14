#%%
#データを読み込む　raw_dataset/p1_2328_old_dataset.npz
import numpy as np

# データセットを読み込む
dataset = np.load('/Users/naokkimu/lyworks/silentspeller_decoder/raw_dataset/p1_2328_old_dataset.npz',allow_pickle=True)

# データセットのキーを確認
print(dataset.keys())

# データの中身を確認
print(dataset['data'].shape)
print(dataset['label'].shape)

# データを分割する
competition_data = dataset['data'][:50]
competition_label = dataset['label'][:50]
test_data = dataset['data'][50:100]
test_label = dataset['label'][50:100]

# competition と test のラベルを取得
competition_label_set = set(competition_label)
test_label_set = set(test_label)
excluded_labels = competition_label_set | test_label_set

# 訓練データのインデックスを作成（competition と test のラベルを除外）
train_indices = [i for i in range(len(dataset['label'])) 
                if i >= 100 and dataset['label'][i] not in excluded_labels]

train_data = dataset['data'][train_indices]
train_label = dataset['label'][train_indices]

# 分割の確認
print("\n=== データ分割の確認 ===")
print(f"元のデータ総数: {len(dataset['data'])}")
print(f"Competition データ数: {len(competition_data)}")
print(f"テストデータ数: {len(test_data)}")
print(f"訓練データ数: {len(train_data)}")

print("\n=== ラベルの重複チェック ===")
train_label_set = set(train_label)
print(f"Competition データのユニークラベル数: {len(competition_label_set)}")
print(f"テストデータのユニークラベル数: {len(test_label_set)}")
print(f"訓練データのユニークラベル数: {len(train_label_set)}")
print("\nCompetition とテストの重複ラベル:")
print(competition_label_set & test_label_set)
print("\nCompetition と訓練の重複ラベル:")
print(competition_label_set & train_label_set)
print("\nテストと訓練の重複ラベル:")
print(test_label_set & train_label_set)

print("\n=== 各データセットのラベル例 ===")
print(f"Competition の最初の10個のラベル: {competition_label[:10]}")
print(f"テストデータの最初の10個のラベル: {test_label[:10]}")
print(f"訓練データの最初の10個のラベル: {train_label[:10]}")

#%%
# データを保存する
np.savez('/Users/naokkimu/lyworks/silentspeller_decoder/raw_dataset/train_test_competition_split.npz',
         competition_data=competition_data,
         competition_label=competition_label,
         train_data=train_data,
         train_label=train_label,
         test_data=test_data,
         test_label=test_label)

print("\nData saved to data/train_test_competition_split.npz")
# %%
