#!/bin/bash
# Grid search for optimal alpha and beta parameters in KenLM decoding

# Parse arguments
if [ $# -ne 3 ]; then
    echo "Usage: $0 <model_path> <lm_path> <beam_width>"
    echo "Example: $0 logs/20250715_115950_pca16_best_config_retest/modelWeights lm/lm_char.bin 32"
    exit 1
fi

MODEL_PATH=$1
LM_PATH=$2
BEAM_WIDTH=$3

# Check if files exist
if [ ! -d "$MODEL_PATH" ]; then
    echo "Error: Model directory not found: $MODEL_PATH"
    exit 1
fi

if [ ! -f "$LM_PATH" ]; then
    echo "Error: Language model file not found: $LM_PATH"
    exit 1
fi

# Create output directory
OUTPUT_DIR="grid_search_results"
mkdir -p "$OUTPUT_DIR"

# Define parameter ranges
ALPHA_VALUES=(0.8 1.0 1.2)
BETA_VALUES=(-0.3 0.0 0.3)

echo "Starting KenLM grid search..."
echo "Model: $MODEL_PATH"
echo "Language Model: $LM_PATH"
echo "Beam Width: $BEAM_WIDTH"
echo "Alpha values: ${ALPHA_VALUES[@]}"
echo "Beta values: ${BETA_VALUES[@]}"
echo "Output directory: $OUTPUT_DIR"

# Create results file
RESULTS_FILE="$OUTPUT_DIR/grid_search_results.txt"
echo "Alpha,Beta,CER,WER" > "$RESULTS_FILE"

# Run grid search
for alpha in "${ALPHA_VALUES[@]}"; do
    for beta in "${BETA_VALUES[@]}"; do
        echo "Testing alpha=$alpha, beta=$beta..."
        
        # Run evaluation with KenLM
        python scripts/eval_model_kenlm.py \
            --model_path "$MODEL_PATH" \
            --lm_path "$LM_PATH" \
            --alpha "$alpha" \
            --beta "$beta" \
            --beam_width "$BEAM_WIDTH" \
            --partition test \
            --output_dir "$OUTPUT_DIR/alpha${alpha}_beta${beta}" \
            2>&1 | tee "$OUTPUT_DIR/alpha${alpha}_beta${beta}.log"
        
        # Extract CER and WER from log (assuming they're printed)
        CER=$(grep "Character Error Rate" "$OUTPUT_DIR/alpha${alpha}_beta${beta}.log" | tail -1 | grep -o '[0-9.]*')
        WER=$(grep "Word Error Rate" "$OUTPUT_DIR/alpha${alpha}_beta${beta}.log" | tail -1 | grep -o '[0-9.]*')
        
        if [ -z "$CER" ]; then
            CER="N/A"
        fi
        if [ -z "$WER" ]; then
            WER="N/A"
        fi
        
        echo "$alpha,$beta,$CER,$WER" >> "$RESULTS_FILE"
        echo "Results: CER=$CER, WER=$WER"
        echo "---"
    done
done

# Find best parameters
echo "Grid search completed!"
echo "Results saved to: $RESULTS_FILE"
echo ""
echo "Best results:"
if [ -f "$RESULTS_FILE" ]; then
    echo "Full results:"
    cat "$RESULTS_FILE"
    echo ""
    
    # Find best CER (assuming column 3 contains CER)
    BEST_LINE=$(tail -n +2 "$RESULTS_FILE" | grep -v "N/A" | sort -t, -k3 -n | head -1)
    if [ ! -z "$BEST_LINE" ]; then
        BEST_ALPHA=$(echo "$BEST_LINE" | cut -d, -f1)
        BEST_BETA=$(echo "$BEST_LINE" | cut -d, -f2)
        BEST_CER=$(echo "$BEST_LINE" | cut -d, -f3)
        
        echo "Best configuration:"
        echo "Alpha: $BEST_ALPHA"
        echo "Beta: $BEST_BETA"
        echo "CER: $BEST_CER"
        
        # Save best config
        echo "alpha=$BEST_ALPHA" > "$OUTPUT_DIR/best_config.txt"
        echo "beta=$BEST_BETA" >> "$OUTPUT_DIR/best_config.txt"
        echo "cer=$BEST_CER" >> "$OUTPUT_DIR/best_config.txt"
        
        echo "Best configuration saved to: $OUTPUT_DIR/best_config.txt"
    fi
fi

echo "Grid search completed!" 