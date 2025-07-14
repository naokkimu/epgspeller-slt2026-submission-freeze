import csv
from pathlib import Path
import argparse
from typing import List, Dict, Tuple
import Levenshtein
import nltk
from nltk.corpus import words


# 音素的に似ている文字のグループと重み
PHONETIC_GROUPS = [
    ({'B', 'P'}, 0.9),    # 両唇音（最も混同されやすい）
    ({'D', 'T'}, 0.85),   # 歯茎音
    ({'V', 'F'}, 0.85),   # 唇歯音
    ({'G', 'K'}, 0.8),    # 軟口蓋音
    ({'M', 'N'}, 0.7),    # 鼻音（比較的区別しやすい）
    ({'S', 'Z'}, 0.75),   # 歯擦音
]

# 母音グループ
VOWELS = {'A', 'E', 'I', 'O', 'U', 'Y'}


def preprocess_word(word: str) -> str:
    """スペースを除去して単語を前処理"""
    return ''.join(word.split())


def load_dictionary() -> set:
    """NLTKの辞書をロードし、必要な前処理を行う"""
    try:
        nltk.data.find('corpora/words')
    except LookupError:
        nltk.download('words')
    
    # 辞書の単語を全て大文字に変換
    word_set = {word.upper() for word in words.words()}
    # 長さによるフィルタリング（1-10文字）
    word_set = {word for word in word_set if 1 <= len(word) <= 10}
    return word_set


def get_phonetic_similarity(char1: str, char2: str) -> float:
    """2つの文字の音素的類似度を計算"""
    if char1 == char2:
        return 1.0
    
    # 音素グループ内で一致する場合
    for group, weight in PHONETIC_GROUPS:
        if char1 in group and char2 in group:
            return weight
    
    # 両方とも母音の場合は若干の類似性を認める
    if char1 in VOWELS and char2 in VOWELS:
        return 0.3
    
    return 0.0


def get_max_distance(word_len: int) -> int:
    """単語の長さに応じて許容する最大編集距離を決定"""
    if word_len <= 3:
        return 1
    elif word_len <= 6:
        return 2
    else:
        return min(3, word_len // 3)


def calculate_word_similarity(pred: str, cand: str) -> float:
    """予測単語と候補単語の類似度を計算"""
    # スペースを除去
    pred_clean = preprocess_word(pred)
    cand_clean = preprocess_word(cand)
    
    # 長さの差が大きすぎる場合はペナルティ
    len_diff = abs(len(pred_clean) - len(cand_clean))
    if len_diff > min(len(pred_clean), len(cand_clean)) / 2:
        return 0.0
    
    # 基本スコアは編集距離の逆数
    edit_dist = Levenshtein.distance(pred_clean, cand_clean)
    if edit_dist == 0:
        return 1.0
    
    # 編集距離が大きすぎる場合は低いスコア
    max_allowed_dist = get_max_distance(len(pred_clean))
    if edit_dist > max_allowed_dist:
        return 0.1
    
    base_score = 1.0 / (1 + edit_dist)
    
    # 音素的類似性を考慮（先頭と末尾を重視）
    phonetic_score = 0.0
    min_len = min(len(pred_clean), len(cand_clean))
    
    # 先頭の文字の一致を重視
    if min_len > 0:
        head_similarity = get_phonetic_similarity(pred_clean[0], cand_clean[0])
        phonetic_score += head_similarity * 1.5  # 先頭は1.5倍の重み
    
    # 末尾の文字の一致を重視
    if min_len > 1:
        tail_similarity = get_phonetic_similarity(pred_clean[-1], cand_clean[-1])
        phonetic_score += tail_similarity * 1.2  # 末尾は1.2倍の重み
    
    # 中間の文字
    for i in range(1, min_len - 1):
        sim = get_phonetic_similarity(pred_clean[i], cand_clean[i])
        # 子音の一致をより重視
        if pred_clean[i] not in VOWELS and cand_clean[i] not in VOWELS:
            sim *= 1.2
        phonetic_score += sim
    
    # 正規化
    max_possible_score = 1.5 + 1.2 + (max(len(pred_clean), len(cand_clean)) - 2) * 1.2
    phonetic_score /= max_possible_score
    
    # 最終スコアは編集距離と音素的類似性の重み付き平均
    final_score = 0.6 * base_score + 0.4 * phonetic_score
    
    # 長さの差に応じてペナルティを適用
    length_penalty = 1.0 - (len_diff / (max(len(pred_clean), len(cand_clean)) + 1))
    final_score *= length_penalty
    
    return final_score


def format_word(word: str, spaces: bool = True) -> str:
    """単語をスペース区切りまたは連続した形式に変換"""
    if spaces:
        return ' '.join(word)
    return word


def correct_word(pred: str, dictionary: set) -> Tuple[str, float]:
    """単語を修正して最適な候補を返す"""
    pred_clean = preprocess_word(pred)
    if not pred_clean:
        return pred, 0.0
    
    # すでに辞書に存在する場合
    if pred_clean in dictionary:
        return format_word(pred_clean, spaces=(' ' in pred)), 1.0
    
    # 短すぎる予測は修正しない
    if len(pred_clean) < 2:
        return pred, 0.0
    
    candidates = []
    max_distance = get_max_distance(len(pred_clean))
    
    for word in dictionary:
        if abs(len(word) - len(pred_clean)) <= max_distance + 1:
            similarity = calculate_word_similarity(pred_clean, word)
            if similarity > 0.3:  # 最小類似度閾値
                candidates.append((word, similarity))
    
    # スコアで並び替えて最適な候補を選択
    candidates.sort(key=lambda x: x[1], reverse=True)
    
    if not candidates:
        return pred, 0.0
    
    best_candidate, best_score = candidates[0]
    
    # スコアが閾値を超える場合のみ修正を適用
    if best_score > 0.5:
        return format_word(best_candidate, spaces=(' ' in pred)), best_score
    return pred, 0.0


def correct_prediction(pred: str, dictionary: set) -> Tuple[str, float]:
    """スペース区切りの予測文字列全体を修正"""
    words = pred.split()
    if not words:
        return pred, 0.0
    
    # 単語が1つの場合は直接修正
    if len(words) == 1 or ' ' not in pred:
        return correct_word(pred, dictionary)
    
    # 複数単語の場合は個別に修正
    corrected_words = []
    total_score = 0.0
    word_count = 0
    
    # 連続した文字をグループ化
    current_word = []
    for word in words:
        if len(word) == 1:
            current_word.append(word)
        else:
            if current_word:
                joined_word = ''.join(current_word)
                corrected, score = correct_word(joined_word, dictionary)
                corrected_words.append(corrected)
                total_score += score
                word_count += 1
                current_word = []
            corrected, score = correct_word(word, dictionary)
            corrected_words.append(corrected)
            total_score += score
            word_count += 1
    
    # 残りの文字があれば処理
    if current_word:
        joined_word = ''.join(current_word)
        corrected, score = correct_word(joined_word, dictionary)
        corrected_words.append(corrected)
        total_score += score
        word_count += 1
    
    return ' '.join(corrected_words), total_score / word_count if word_count > 0 else 0.0


def main():
    parser = argparse.ArgumentParser(
        description='Apply dictionary-based spell correction'
    )
    parser.add_argument(
        'prediction_file',
        type=str,
        help='Path to prediction_pairs.csv'
    )
    
    args = parser.parse_args()
    input_path = Path(args.prediction_file)
    output_path = input_path.parent / 'corrected_predictions.csv'
    
    # 辞書のロード
    print("Loading dictionary...")
    dictionary = load_dictionary()
    print(f"Loaded {len(dictionary)} words")
    
    # 予測の読み込みと修正
    pairs = []
    corrected_count = 0
    total_count = 0
    
    with open(input_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_count += 1
            reference = row['reference']
            predicted = row['predicted']
            corrected, score = correct_prediction(predicted, dictionary)
            
            if corrected != predicted:
                corrected_count += 1
            
            pairs.append({
                'reference': reference,
                'predicted': predicted,
                'corrected': corrected,
                'confidence': f"{score:.3f}"
            })
    
    # 結果の保存
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['reference', 'predicted', 'corrected', 'confidence']
        )
        writer.writeheader()
        writer.writerows(pairs)
    
    print(f"Processed {total_count} predictions")
    print(f"Applied corrections to {corrected_count} predictions")
    print(f"Results saved to {output_path}")


if __name__ == '__main__':
    main() 