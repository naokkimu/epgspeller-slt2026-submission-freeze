import argparse
import pickle
import numpy as np
import torch
from neural_decoder.dataset import SpeechDataset
from neural_decoder.neural_decoder_trainer import loadModel
import matplotlib.pyplot as plt
from pathlib import Path
from torch.nn.utils.rnn import pad_sequence

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate trained neural decoder model")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the trained model directory")
    parser.add_argument("--partition", type=str, default="test", choices=["test", "competition"],
                      help="Data partition to evaluate on")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for evaluation")
    parser.add_argument("--device", type=str, default="cpu", help="Device to run evaluation on")
    return parser.parse_args()

def load_model_and_args(model_path):
    # Load saved arguments
    with open(Path(model_path) / "args", "rb") as f:
        args = pickle.load(f)
    
    # Load dataset to get the number of days
    with open(args["datasetPath"], "rb") as f:
        dataset = pickle.load(f)
    n_days = len(dataset["train"])  # Use the same number of days as in training
    
    # Load model with correct number of days
    model = loadModel(model_path, nInputLayers=n_days)
    
    # Ensure model is on CPU first to avoid device conflicts
    model = model.cpu()
    
    return model, args

def padding_collate(batch):
    """Collate function for padding sequences in a batch"""
    X, y, X_lens, y_lens, days = zip(*batch)
    X_padded = pad_sequence(X, batch_first=True, padding_value=0)
    y_padded = pad_sequence(y, batch_first=True, padding_value=0)

    return (
        X_padded,
        y_padded,
        torch.stack(X_lens),
        torch.stack(y_lens),
        torch.stack(days),
    )

def evaluate_model(model, dataset, device, batch_size=32):
    model.eval()
    dataloader = torch.utils.data.DataLoader(
        dataset, batch_size=batch_size, shuffle=False, num_workers=0,
        collate_fn=padding_collate
    )
    
    # データセットの時系列長の分布を確認
    print("\nAnalyzing sequence lengths:")
    all_X_lens = []
    all_y_lens = []
    for X, y, X_len, y_len, day_idx in dataloader:
        all_X_lens.extend(X_len.numpy())
        all_y_lens.extend(y_len.numpy())
    
    print(f"Input sequence lengths:")
    print(f"  Mean: {np.mean(all_X_lens):.2f}")
    print(f"  Min: {np.min(all_X_lens)}")
    print(f"  Max: {np.max(all_X_lens)}")
    print(f"  Median: {np.median(all_X_lens)}")
    
    print(f"\nOutput sequence lengths:")
    print(f"  Mean: {np.mean(all_y_lens):.2f}")
    print(f"  Min: {np.min(all_y_lens)}")
    print(f"  Max: {np.max(all_y_lens)}")
    print(f"  Median: {np.median(all_y_lens)}")
    
    results = {
        "logits": [],
        "true_seqs": [],
        "pred_seqs": [],
        "transcriptions": []
    }
    
    with torch.no_grad():
        for batch_idx, (X, y, X_len, y_len, day_idx) in enumerate(dataloader):
            # Move data to device
            X = X.to(device)
            y = y.to(device)
            X_len = X_len.to(device)
            day_idx = day_idx.to(device)
            
            # Forward pass
            logits = model(X.to(device), day_idx.to(device))
            
            # Calculate adjusted lengths for CTC
            adj_lens = ((X_len - model.kernelLen) / model.strideLen).to(torch.int32)
            
            # Debug output for the first batch
            if batch_idx == 0:
                print("\nDebug output for first batch:")
                print(f"Input shape: {X.shape}")
                print(f"Output logits shape: {logits.shape}")
                print(f"Adjusted lengths: {adj_lens}")
                
                # バッチ内のパディング率を計算
                batch_padding_ratio = []
                for i in range(len(X_len)):
                    total_len = X.shape[1]
                    actual_len = X_len[i].item()
                    padding_ratio = (total_len - actual_len) / total_len * 100
                    batch_padding_ratio.append(padding_ratio)
                
                print(f"\nPadding analysis for first batch:")
                print(f"  Mean padding ratio: {np.mean(batch_padding_ratio):.2f}%")
                print(f"  Min padding ratio: {np.min(batch_padding_ratio):.2f}%")
                print(f"  Max padding ratio: {np.max(batch_padding_ratio):.2f}%")
                
                print(f"\nSample logits distribution:")
                probs = torch.softmax(logits[0, :adj_lens[0]], dim=-1)
                print(f"Max probability per timestep (first sequence):")
                print(probs.max(dim=-1).values[:10])  # Show first 10 timesteps
                print(f"Most probable classes (first sequence):")
                print(probs.argmax(dim=-1)[:10])  # Show first 10 timesteps
            
            # Store results
            results["logits"].extend(logits.cpu().numpy())
            for i in range(len(y)):
                results["true_seqs"].append(y[i][:y_len[i]].cpu().numpy())
            
            # Decode predictions using the same method as in training
            decoded_seqs = []
            for i in range(len(adj_lens)):
                seq = torch.argmax(
                    logits[i, :adj_lens[i]],
                    dim=-1,
                )
                seq = torch.unique_consecutive(seq)
                seq = seq.cpu().numpy()
                seq = np.array([j for j in seq if j != 0])
                decoded_seqs.append(seq)
            
            results["pred_seqs"].extend(decoded_seqs)
    
    return results

def calculate_metrics(results):
    """Calculate Character Error Rate (CER) and Word Error Rate (WER)"""
    total_chars = 0
    total_char_errors = 0
    total_words = 0
    total_word_errors = 0
    
    for true_seq, pred_seq in zip(results["true_seqs"], results["pred_seqs"]):
        # Character level metrics
        total_chars += len(true_seq)
        total_char_errors += sum(1 for i, j in zip(true_seq, pred_seq) if i != j)
        
        # Word level metrics
        true_words = "".join(map(str, true_seq)).split()
        pred_words = "".join(map(str, pred_seq)).split()
        total_words += len(true_words)
        total_word_errors += sum(1 for i, j in zip(true_words, pred_words) if i != j)
    
    cer = total_char_errors / total_chars if total_chars > 0 else 1.0
    wer = total_word_errors / total_words if total_words > 0 else 1.0
    
    return {"cer": cer, "wer": wer}

def plot_results(metrics, save_path):
    """Plot and save evaluation metrics"""
    plt.figure(figsize=(10, 5))
    plt.bar(["CER", "WER"], [metrics["cer"], metrics["wer"]])
    plt.title("Evaluation Metrics")
    plt.ylabel("Error Rate")
    plt.ylim(0, 1)
    plt.savefig(save_path / "evaluation_metrics.png")
    plt.close()

def get_char_mapping(dataset_data):
    """Get character mapping from dataset"""
    # アルファベット定義（format_silentspeller.pyと同じ定義を使用）
    ALPHABET_DEF = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    ALPHABET_DEF_SIL = ALPHABET_DEF + ['SIL']
    
    # 数字からアルファベットへのマッピングを作成
    # 0はSIL（ブランク）トークン、1-26はA-Z
    id2char = {0: 'SIL'}
    for i, char in enumerate(ALPHABET_DEF, start=1):
        id2char[i] = char
    
    return id2char

def ids_to_text(ids, char_map):
    """Convert ID sequence to space-separated text"""
    return ' '.join(char_map[int(idx)] for idx in ids if int(idx) != 0 and int(idx) in char_map)

def calculate_edit_distance(ref: str, hyp: str):
    """
    Calculate Levenshtein distance and count each operation type
    """
    # Create matrix
    d = np.zeros((len(ref) + 1, len(hyp) + 1))
    
    # Initialize first row and column
    for i in range(len(ref) + 1):
        d[i, 0] = i
    for j in range(len(hyp) + 1):
        d[0, j] = j
        
    # Fill the matrix
    for i in range(1, len(ref) + 1):
        for j in range(1, len(hyp) + 1):
            if ref[i-1] == hyp[j-1]:
                d[i, j] = d[i-1, j-1]
            else:
                d[i, j] = min(
                    d[i-1, j] + 1,    # deletion
                    d[i, j-1] + 1,    # insertion
                    d[i-1, j-1] + 1   # substitution
                )
    
    # Backtrack to count operations
    i, j = len(ref), len(hyp)
    insertions = deletions = substitutions = 0
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and ref[i-1] == hyp[j-1]:
            i -= 1
            j -= 1
        else:
            if i > 0 and j > 0 and d[i, j] == d[i-1, j-1] + 1:
                substitutions += 1
                i -= 1
                j -= 1
            elif j > 0 and d[i, j] == d[i, j-1] + 1:
                insertions += 1
                j -= 1
            elif i > 0 and d[i, j] == d[i-1, j] + 1:
                deletions += 1
                i -= 1
    
    return {
        'total': int(d[len(ref), len(hyp)]),
        'insertions': insertions,
        'deletions': deletions,
        'substitutions': substitutions
    }

def save_detailed_results(results, save_path, dataset_data):
    """Save detailed comparison of predictions and references"""
    char_map = get_char_mapping(dataset_data)
    total_stats = {
        'total_chars': 0,
        'total_edits': 0,
        'total_insertions': 0,
        'total_deletions': 0,
        'total_substitutions': 0,
        'correct_predictions': 0
    }
    
    # 文字ごとの統計
    char_stats = {}
    for c in range(1, 27):  # A-Z (1-26)
        char_stats[char_map[c]] = {
            'total': 0,      # 出現回数
            'correct': 0,    # 正しく認識された回数
            'missed': 0,     # 削除された回数
            'wrong': 0       # 誤って認識された回数
        }
    
    # エラーパターンの集計
    error_patterns = {
        'substitutions': {},  # 置換エラー (X→Y)
        'deletions': {},      # 削除エラー (X→)
        'insertions': {}      # 挿入エラー (→X)
    }
    
    with open(save_path / "detailed_results.txt", "w") as f:
        # ヘッダー
        f.write("=== Silent Speller Evaluation Results ===\n\n")
        
        # 各予測の詳細
        for i, (true_seq, pred_seq) in enumerate(zip(results["true_seqs"], results["pred_seqs"])):
            # 文字列に変換
            ref_str = ids_to_text(true_seq, char_map)
            pred_str = ids_to_text(pred_seq, char_map)
            is_correct = ref_str == pred_str
            
            if is_correct:
                total_stats['correct_predictions'] += 1
            
            # 編集距離の計算
            edit_stats = calculate_edit_distance(ref_str, pred_str)
            
            # 統計の更新
            total_stats['total_chars'] += len(ref_str.split())
            total_stats['total_edits'] += edit_stats['total']
            total_stats['total_insertions'] += edit_stats['insertions']
            total_stats['total_deletions'] += edit_stats['deletions']
            total_stats['total_substitutions'] += edit_stats['substitutions']
            
            # 予測結果の出力
            f.write(f"Sample {i+1:03d} {'✓' if is_correct else '✗'}\n")
            f.write(f"Reference: {ref_str}\n")
            f.write(f"Predicted: {pred_str}\n")
            
            # エラーがある場合は詳細を表示
            if not is_correct:
                f.write("Errors:\n")
                if edit_stats['insertions'] > 0:
                    f.write(f"  - Insertions: {edit_stats['insertions']}\n")
                if edit_stats['deletions'] > 0:
                    f.write(f"  - Deletions: {edit_stats['deletions']}\n")
                if edit_stats['substitutions'] > 0:
                    f.write(f"  - Substitutions: {edit_stats['substitutions']}\n")
                
                # 文字ごとの比較を表示
                ref_chars = ref_str.split()
                pred_chars = pred_str.split()
                
                # 文字ごとの統計を更新
                for c in ref_chars:
                    char_stats[c]['total'] += 1
                
                # アライメントと統計の更新
                i, j = 0, 0
                alignment = []
                while i < len(ref_chars) or j < len(pred_chars):
                    if i < len(ref_chars) and j < len(pred_chars):
                        if ref_chars[i] == pred_chars[j]:
                            alignment.append(f" {ref_chars[i]} ")
                            char_stats[ref_chars[i]]['correct'] += 1
                            i += 1
                            j += 1
                        else:
                            alignment.append(f"[{ref_chars[i]}→{pred_chars[j]}]")
                            # 置換エラーを記録
                            error_key = f"{ref_chars[i]}→{pred_chars[j]}"
                            error_patterns['substitutions'][error_key] = error_patterns['substitutions'].get(error_key, 0) + 1
                            char_stats[ref_chars[i]]['wrong'] += 1
                            i += 1
                            j += 1
                    elif i < len(ref_chars):
                        alignment.append(f"[-{ref_chars[i]}]")
                        # 削除エラーを記録
                        error_key = f"{ref_chars[i]}-"
                        error_patterns['deletions'][error_key] = error_patterns['deletions'].get(error_key, 0) + 1
                        char_stats[ref_chars[i]]['missed'] += 1
                        i += 1
                    else:
                        alignment.append(f"[+{pred_chars[j]}]")
                        # 挿入エラーを記録
                        error_key = f"-{pred_chars[j]}"
                        error_patterns['insertions'][error_key] = error_patterns['insertions'].get(error_key, 0) + 1
                        j += 1
                
                f.write("Alignment: " + "".join(alignment) + "\n")
            else:
                # 正解の場合も文字の統計を更新
                for c in ref_str.split():
                    char_stats[c]['total'] += 1
                    char_stats[c]['correct'] += 1
            
            f.write("-" * 50 + "\n\n")
        
        # サマリーの出力
        f.write("\n=== Summary ===\n")
        total_samples = len(results['true_seqs'])
        f.write(f"Total samples: {total_samples}\n")
        f.write(f"Correct predictions: {total_stats['correct_predictions']} ({total_stats['correct_predictions']/total_samples:.1%})\n")
        f.write(f"Total characters: {total_stats['total_chars']}\n")
        f.write(f"Character Error Rate (CER): {total_stats['total_edits']/total_stats['total_chars']:.1%}\n\n")
        
        f.write("Error breakdown:\n")
        f.write(f"  - Insertions: {total_stats['total_insertions']}\n")
        f.write(f"  - Deletions: {total_stats['total_deletions']}\n")
        f.write(f"  - Substitutions: {total_stats['total_substitutions']}\n\n")
        
        # 文字ごとの認識精度
        f.write("=== Character Recognition Accuracy ===\n")
        f.write("Char  Total  Correct  Accuracy  Errors (Sub/Del)\n")
        f.write("-" * 45 + "\n")
        for char in sorted(char_stats.keys()):
            stats = char_stats[char]
            if stats['total'] > 0:
                accuracy = stats['correct'] / stats['total']
                f.write(f"{char:4s} {stats['total']:6d} {stats['correct']:8d} {accuracy:8.1%} {stats['wrong']:4d}/{stats['missed']:4d}\n")
        
        # 頻出エラーパターン
        f.write("\n=== Most Common Error Patterns ===\n")
        
        # 置換エラー
        f.write("\nTop Substitution Errors:\n")
        sorted_subs = sorted(error_patterns['substitutions'].items(), key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_subs[:10]:
            f.write(f"  {pattern}: {count}\n")
        
        # 削除エラー
        f.write("\nTop Deletion Errors:\n")
        sorted_dels = sorted(error_patterns['deletions'].items(), key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_dels[:10]:
            f.write(f"  {pattern}: {count}\n")
        
        # 挿入エラー
        f.write("\nTop Insertion Errors:\n")
        sorted_ins = sorted(error_patterns['insertions'].items(), key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_ins[:10]:
            f.write(f"  {pattern}: {count}\n")

def main():
    args = parse_args()
    
    # Load model and configuration
    model, model_args = load_model_and_args(args.model_path)
    
    # Move model to specified device
    model = model.to(args.device)
    # Ensure all parameters are on the same device
    for param in model.parameters():
        param.data = param.data.to(args.device)
    
    # Load dataset
    with open(model_args["datasetPath"], "rb") as f:
        dataset_data = pickle.load(f)
    dataset = SpeechDataset(dataset_data[args.partition])
    
    # Evaluate model
    results = evaluate_model(model, dataset, args.device, args.batch_size)
    
    # Calculate metrics
    metrics = calculate_metrics(results)
    
    # Save results
    save_path = Path(args.model_path) / "evaluation"
    save_path.mkdir(exist_ok=True)
    
    # Save metrics
    with open(save_path / "metrics.txt", "w") as f:
        f.write(f"Character Error Rate (CER): {metrics['cer']:.4f}\n")
        f.write(f"Word Error Rate (WER): {metrics['wer']:.4f}\n")
    
    # Save detailed results
    save_detailed_results(results, save_path, dataset_data)
    
    # Plot results
    plot_results(metrics, save_path)
    
    print(f"Evaluation completed. Results saved to {save_path}")

if __name__ == "__main__":
    main() 