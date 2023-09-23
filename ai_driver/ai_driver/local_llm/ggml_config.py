from ai_driver.config import server_config
from ai_driver.local_llm.ggml_llm import GGMLConfig


def get_default_ggml_config():
    # Import config vars
    config = GGMLConfig(
        model_path=server_config.LLM_MODEL_BIN_PATH,
        model_type=server_config.MODEL_TYPE,
        max_new_tokens=server_config.MAX_NEW_TOKENS,
        temperature=server_config.TEMPERATURE,
        gpu_layers=server_config.GGML_GPU_LAYERS,
    )
    return config
