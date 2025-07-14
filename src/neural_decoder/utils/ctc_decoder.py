import numpy as np

def decode_ctc(logits, lengths):
    """
    CTC decoder with improved probability handling.
    
    Args:
        logits: Array of shape (batch_size, sequence_length, num_classes)
        lengths: Array of sequence lengths for each batch item
        
    Returns:
        List of decoded sequences
    """
    # Convert logits to probabilities
    probs = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
    probs = probs / np.sum(probs, axis=-1, keepdims=True)
    
    decoded_sequences = []
    for prob, length in zip(probs, lengths):
        # Only consider predictions up to the sequence length
        sequence = prob[:length]
        
        # Get most probable non-blank characters
        decoded = []
        prev_char = None
        prev_prob = 0
        
        for timestep_prob in sequence:
            # Get top 2 most probable characters and their probabilities
            top2_idx = np.argsort(timestep_prob)[-2:]
            top2_prob = timestep_prob[top2_idx]
            
            # If the most probable character is not blank and probability is high enough
            if top2_idx[-1] != 0 and top2_prob[-1] > 0.1:  # Probability threshold
                curr_char = top2_idx[-1]
                curr_prob = top2_prob[-1]
                
                # Add character if it's different from previous or has higher probability
                if curr_char != prev_char or curr_prob > prev_prob:
                    decoded.append(curr_char)
                    prev_char = curr_char
                    prev_prob = curr_prob
            # If blank is most probable but second most probable is strong
            elif top2_idx[-1] == 0 and len(top2_idx) > 1 and top2_prob[-2] > 0.15:
                curr_char = top2_idx[-2]
                curr_prob = top2_prob[-2]
                
                # Add character if it's different from previous
                if curr_char != prev_char:
                    decoded.append(curr_char)
                    prev_char = curr_char
                    prev_prob = curr_prob
        
        decoded_sequences.append(decoded)
    
    return decoded_sequences 