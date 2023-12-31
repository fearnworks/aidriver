#!/bin/bash
source ./model_venv/bin/activate
python3.11 -m pip install -r ./model_worker/requirements.txt
# python3.11 -m pip install git+https://github.com/vllm-project/vllm.git@main 
# Function to display usage information
usage() {
    echo "Usage: $0 [--openai] [-m model_name] [--default (code|small|large)] [additional_args...]"
    exit 1
}

# Initialize variables
OPENAI=false
CODE_DEFAULT="TheBloke/deepseek-coder-33B-instruct-AWQ"
SMALL_MODEL_DEFAULT="TheBloke/Mistral-7B-OpenOrca-AWQ"
LARGE_MODEL_DEFAULT="TheBloke/Dolphin-2.1-70B-AWQ"
MOE_MODEL_DEFAULT=""
MODEL_NAME=$CODE_DEFAULT
EXTRA_ARGS=""

# Parse command line arguments
while [ "$1" != "" ]; do
    case $1 in
        --openai )   OPENAI=true
                    ;;
        -m )         shift
                    MODEL_NAME=$1
                    ;;
        --default )  shift
                    case $1 in
                        code )  MODEL_NAME=$CODE_DEFAULT
                                ;;
                        small ) MODEL_NAME=$SMALL_MODEL_DEFAULT
                                ;;
                        large ) MODEL_NAME=$LARGE_MODEL_DEFAULT
                                ;;
                        * )     usage
                                exit 1
                    esac
                    ;;
        * )          EXTRA_ARGS="$EXTRA_ARGS $1"
    esac
    shift
done

# Auto-detect "awq" or "AWQ" in the model name for quantization flag
QUANTIZATION_FLAG=""
if [[ $MODEL_NAME == *"awq"* || $MODEL_NAME == *"AWQ"* ]]; then
    QUANTIZATION_FLAG="--quantization awq --dtype float16" # awq doesn't yet support bfloat16
fi

# If running in WSL, you might need to use the following:
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/lib/wsl/lib
if [ "$OPENAI" = true ]; then
    # Run OpenAI model
    echo "Model:" $MODEL_NAME
    echo "Quant:" $QUANTIZATION_FLAG
    echo "Extra:" $EXTRA_ARGS
    python3.11 -m vllm.entrypoints.openai.api_server --download-dir /models  --model "$MODEL_NAME" --port 28100 $QUANTIZATION_FLAG $EXTRA_ARGS
else
    # Run Amazon model
    python3.11 -m vllm.entrypoints.api_server --download-dir /models  --model "$MODEL_NAME" --port 28100 $QUANTIZATION_FLAG $EXTRA_ARGS 
fi
