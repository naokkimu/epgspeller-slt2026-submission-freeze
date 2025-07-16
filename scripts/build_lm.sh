#!/bin/bash
# Build KenLM language model from text corpus

# Check if KenLM is installed
if ! command -v lmplz &> /dev/null; then
    echo "KenLM not found. Installing..."
    
    # Try to install KenLM
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y libkenlm-dev kenlm
    elif command -v yum &> /dev/null; then
        sudo yum install -y kenlm
    else
        echo "Cannot install KenLM automatically. Please install manually."
        echo "See: https://github.com/kpu/kenlm"
        exit 1
    fi
fi

# Parse arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_corpus> <output_model>"
    echo "Example: $0 lm/char_corpus.txt lm/lm_char.bin"
    exit 1
fi

INPUT_CORPUS=$1
OUTPUT_MODEL=$2

# Check if input exists
if [ ! -f "$INPUT_CORPUS" ]; then
    echo "Error: Input corpus file not found: $INPUT_CORPUS"
    exit 1
fi

# Create output directory
mkdir -p $(dirname "$OUTPUT_MODEL")

# Build temporary ARPA model
ARPA_MODEL="${OUTPUT_MODEL%.bin}.arpa"

echo "Building 5-gram character-level language model..."
echo "Input: $INPUT_CORPUS"
echo "Output: $OUTPUT_MODEL"

# Build ARPA model (5-gram) with discount fallback for small datasets
lmplz -o 5 --discount_fallback < "$INPUT_CORPUS" > "$ARPA_MODEL"

if [ $? -ne 0 ]; then
    echo "Error: Failed to build ARPA model"
    exit 1
fi

echo "ARPA model built: $ARPA_MODEL"

# Convert to binary format
build_binary "$ARPA_MODEL" "$OUTPUT_MODEL"

if [ $? -ne 0 ]; then
    echo "Error: Failed to convert to binary format"
    exit 1
fi

echo "Binary model built: $OUTPUT_MODEL"

# Clean up temporary ARPA file
rm -f "$ARPA_MODEL"

echo "Language model build completed successfully!"
echo "Model: $OUTPUT_MODEL"
echo "Size: $(du -h "$OUTPUT_MODEL" | cut -f1)" 