#!/usr/bin/env python3
"""
Convert word-level corpus to character-level corpus for KenLM.
"""

import argparse
from pathlib import Path

def word_to_char_corpus(input_path, output_path):
    """
    Convert word-level corpus to character-level corpus.
    
    Args:
        input_path: Path to word-level corpus file
        output_path: Path to save character-level corpus file
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    
    # Convert to character-level
    char_lines = []
    for word in words:
        # Add spaces between characters
        char_word = ' '.join(word.upper())
        char_lines.append(char_word)
    
    # Save character-level corpus
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in char_lines:
            f.write(line + '\n')
    
    print(f"Converted {len(words)} words to character-level corpus: {output_path}")
    
    # Print some examples
    print("\nFirst 10 character-level entries:")
    for i, line in enumerate(char_lines[:10]):
        print(f"  {i+1}: {line}")

def main():
    parser = argparse.ArgumentParser(description='Convert word-level corpus to character-level')
    parser.add_argument('--input_path', type=str, default='lm/char_corpus.txt',
                      help='Path to input word-level corpus file')
    parser.add_argument('--output_path', type=str, default='lm/char_corpus_converted.txt',
                      help='Path to output character-level corpus file')
    
    args = parser.parse_args()
    
    word_to_char_corpus(args.input_path, args.output_path)

if __name__ == '__main__':
    main() 