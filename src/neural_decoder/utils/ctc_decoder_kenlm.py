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
        Perform beam search decoding with KenLM shallow-fusion.
        
        Args:
            logits: Logits of shape (seq_len, vocab_size)
            length: Actual sequence length
            
        Returns:
            List of (text, score) tuples sorted by score
        """
        # Convert logits to log probabilities
        log_probs = logits - np.logaddexp.reduce(logits, axis=-1, keepdims=True)
        
        # Initialize beam with empty sequence
        beam = [{'text': '', 'ctc_score': 0.0, 'lm_score': 0.0, 'last_char': None}]
        
        # Process each timestep
        for t in range(min(length, logits.shape[0])):
            new_beam = []
            
            for candidate in beam:
                # Get current probabilities
                probs = log_probs[t]
                
                # Extend with blank
                blank_score = candidate['ctc_score'] + probs[self.blank_id]
                new_beam.append({
                    'text': candidate['text'],
                    'ctc_score': blank_score,
                    'lm_score': candidate['lm_score'],
                    'last_char': candidate['last_char']
                })
                
                # Extend with characters
                for char_id in range(1, len(probs)):
                    if char_id in self.id_to_char:
                        char = self.id_to_char[char_id]
                        
                        # Skip if same as last character (CTC property)
                        if char == candidate['last_char']:
                            continue
                        
                        new_text = candidate['text'] + char
                        ctc_score = candidate['ctc_score'] + probs[char_id]
                        
                        # Calculate LM score
                        lm_score = self._get_lm_score(new_text)
                        
                        new_beam.append({
                            'text': new_text,
                            'ctc_score': ctc_score,
                            'lm_score': lm_score,
                            'last_char': char
                        })
            
            # Sort by combined score and keep top beam_width
            beam = sorted(new_beam, key=lambda x: self._combined_score(x), reverse=True)[:self.beam_width]
        
        # Return results
        results = []
        for candidate in beam:
            score = self._combined_score(candidate)
            results.append((candidate['text'], score))
        
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