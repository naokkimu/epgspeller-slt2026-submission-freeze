#!/usr/bin/env python3
"""
CTC decoder with KenLM shallow-fusion for improved decoding.
"""

import numpy as np
import kenlm
from typing import List, Tuple, Optional
import string


class CTCKenLMDecoder:
    """
    CTC decoder with KenLM shallow-fusion support.
    """
    
    def __init__(self, 
                 lm_path: str,
                 alpha: float = 1.0,
                 beta: float = 0.0,
                 beam_width: int = 32,
                 blank_id: int = 0):
        """
        Initialize CTC decoder with KenLM language model.
        
        Args:
            lm_path: Path to KenLM binary model
            alpha: Language model weight
            beta: Length penalty weight
            beam_width: Beam search width
            blank_id: Blank token ID
        """
        self.lm_path = lm_path
        self.alpha = alpha
        self.beta = beta
        self.beam_width = beam_width
        self.blank_id = blank_id
        
        # Load language model
        self.lm = kenlm.Model(lm_path)
        
        # Character set (A-Z)
        self.chars = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.char_to_id = {char: i + 1 for i, char in enumerate(self.chars)}  # +1 for blank
        self.id_to_char = {i + 1: char for i, char in enumerate(self.chars)}
        
        print(f"Loaded KenLM model from {lm_path}")
        print(f"Parameters: alpha={alpha}, beta={beta}, beam_width={beam_width}")
    
    def decode_beam_search(self, logits: np.ndarray, length: int) -> List[Tuple[str, float]]:
        """
        Prefix beam search for CTC with KenLM shallow fusion.
        This implementation correctly handles repeated characters under CTC
        (repeats without blank do not emit a new symbol).
        """
        # Convert logits to log probabilities: [T, C]
        log_probs = logits - np.logaddexp.reduce(logits, axis=-1, keepdims=True)
        T = min(int(length), int(logits.shape[0]))

        # KenLM state tracking per prefix
        init_state = kenlm.State()
        self.lm.BeginSentenceWrite(init_state)

        # Beam: prefix -> dict(p_b, p_nb, lm_state, lm_score)
        beam = {
            "": {
                "p_b": 0.0,  # log(1)
                "p_nb": -np.inf,
                "lm_state": init_state,
                "lm_score": 0.0,
            }
        }

        def logsumexp(a: float, b: float) -> float:
            if a == -np.inf:
                return b
            if b == -np.inf:
                return a
            m = a if a > b else b
            return m + np.log(np.exp(a - m) + np.exp(b - m))

        def total_logp(entry: dict) -> float:
            return logsumexp(entry["p_b"], entry["p_nb"])

        for t in range(T):
            probs = log_probs[t]
            new_beam: dict = {}

            for prefix, entry in beam.items():
                p_b = entry["p_b"]
                p_nb = entry["p_nb"]
                p_total = total_logp(entry)

                # 1) Extend with blank: stays on same prefix
                nb_entry = new_beam.get(prefix)
                if nb_entry is None:
                    new_beam[prefix] = {
                        "p_b": p_total + probs[self.blank_id],
                        "p_nb": -np.inf,
                        "lm_state": entry["lm_state"],
                        "lm_score": entry["lm_score"],
                    }
                else:
                    nb_entry["p_b"] = logsumexp(nb_entry["p_b"], p_total + probs[self.blank_id])

                # 2) Extend with characters
                last_char = prefix[-1] if prefix else None
                for char_id in range(1, len(probs)):
                    if char_id not in self.id_to_char:
                        continue
                    char = self.id_to_char[char_id]

                    # Case A: same as last char
                    if last_char == char:
                        # Repeat without emitting a new symbol (stay on same prefix) from p_nb
                        stay = new_beam.get(prefix)
                        if stay is None:
                            new_beam[prefix] = {
                                "p_b": -np.inf,
                                "p_nb": p_nb + probs[char_id],
                                "lm_state": entry["lm_state"],
                                "lm_score": entry["lm_score"],
                            }
                        else:
                            stay["p_nb"] = logsumexp(stay["p_nb"], p_nb + probs[char_id])

                        # Emit a new symbol (prefix+char) only from p_b
                        new_prefix = prefix + char
                        # LM advances only when a symbol is emitted
                        out_state = kenlm.State()
                        lm_delta = self.lm.BaseScore(entry["lm_state"], char, out_state)
                        lm_score_new = entry["lm_score"] + lm_delta

                        tgt = new_beam.get(new_prefix)
                        if tgt is None:
                            new_beam[new_prefix] = {
                                "p_b": -np.inf,
                                "p_nb": p_b + probs[char_id],
                                "lm_state": out_state,
                                "lm_score": lm_score_new,
                            }
                        else:
                            tgt["p_nb"] = logsumexp(tgt["p_nb"], p_b + probs[char_id])
                            # keep better LM state if scores differ (approx)
                            if lm_score_new > tgt["lm_score"]:
                                tgt["lm_state"] = out_state
                                tgt["lm_score"] = lm_score_new
                        continue

                    # Case B: different char => emit new symbol from (p_b + p_nb)
                    new_prefix = prefix + char
                    out_state = kenlm.State()
                    lm_delta = self.lm.BaseScore(entry["lm_state"], char, out_state)
                    lm_score_new = entry["lm_score"] + lm_delta

                    tgt = new_beam.get(new_prefix)
                    if tgt is None:
                        new_beam[new_prefix] = {
                            "p_b": -np.inf,
                            "p_nb": p_total + probs[char_id],
                            "lm_state": out_state,
                            "lm_score": lm_score_new,
                        }
                    else:
                        tgt["p_nb"] = logsumexp(tgt["p_nb"], p_total + probs[char_id])
                        if lm_score_new > tgt["lm_score"]:
                            tgt["lm_state"] = out_state
                            tgt["lm_score"] = lm_score_new

            # Prune beam by combined score
            def combined(prefix: str, e: dict) -> float:
                return total_logp(e) + self.alpha * e["lm_score"] + self.beta * len(prefix)

            top = sorted(new_beam.items(), key=lambda kv: combined(kv[0], kv[1]), reverse=True)[: self.beam_width]
            beam = {k: v for k, v in top}

        results = []
        for prefix, e in sorted(
            beam.items(),
            key=lambda kv: (total_logp(kv[1]) + self.alpha * kv[1]["lm_score"] + self.beta * len(kv[0])),
            reverse=True,
        ):
            score = total_logp(e) + self.alpha * e["lm_score"] + self.beta * len(prefix)
            results.append((prefix, float(score)))
        return results
    
    def _get_lm_score(self, text: str) -> float:
        """
        Get language model score for text.
        
        Args:
            text: Input text
            
        Returns:
            Language model score
        """
        if not text:
            return 0.0
        
        # Convert to character-level format (space-separated)
        char_text = ' '.join(text)
        
        # Get LM score
        try:
            score = self.lm.score(char_text)
            return score
        except:
            return -10.0  # Fallback for unknown sequences
    
    def _combined_score(self, candidate: dict) -> float:
        """
        Calculate combined score (CTC + LM + length penalty).
        
        Args:
            candidate: Candidate dictionary
            
        Returns:
            Combined score
        """
        ctc_score = candidate['ctc_score']
        lm_score = candidate['lm_score']
        length = len(candidate['text'])
        
        # Combined score with length penalty
        combined = ctc_score + self.alpha * lm_score + self.beta * length
        
        return combined
    
    def decode_greedy(self, logits: np.ndarray, length: int) -> str:
        """
        Greedy decoding (for comparison).
        
        Args:
            logits: Logits of shape (seq_len, vocab_size)
            length: Actual sequence length
            
        Returns:
            Decoded text
        """
        # Convert to probabilities
        probs = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        probs = probs / np.sum(probs, axis=-1, keepdims=True)
        
        decoded = []
        prev_char = None
        
        for t in range(length):
            # Get most probable character
            char_id = np.argmax(probs[t])
            
            if char_id != self.blank_id and char_id in self.id_to_char:
                char = self.id_to_char[char_id]
                
                # Add if different from previous
                if char != prev_char:
                    decoded.append(char)
                    prev_char = char
        
        return ''.join(decoded)


def decode_ctc_kenlm(logits: np.ndarray, 
                     lengths: np.ndarray,
                     lm_path: str,
                     alpha: float = 1.0,
                     beta: float = 0.0,
                     beam_width: int = 32) -> List[str]:
    """
    Decode CTC outputs using KenLM shallow-fusion.
    
    Args:
        logits: Logits array of shape (batch_size, seq_len, vocab_size)
        lengths: Sequence lengths for each batch item
        lm_path: Path to KenLM binary model
        alpha: Language model weight
        beta: Length penalty weight
        beam_width: Beam search width
        
    Returns:
        List of decoded texts
    """
    decoder = CTCKenLMDecoder(lm_path, alpha, beta, beam_width)
    
    results = []
    for i in range(len(logits)):
        # Decode with beam search
        beam_results = decoder.decode_beam_search(logits[i], lengths[i])
        
        # Take best result
        if beam_results:
            best_text, best_score = beam_results[0]
            results.append(best_text)
        else:
            results.append("")
    
    return results 