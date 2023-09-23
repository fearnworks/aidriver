import yaml
import os
from dotenv import load_dotenv, find_dotenv
from loguru import logger

load_dotenv(find_dotenv())
from dataclasses import dataclass


@dataclass
class Config:
    RETURN_SOURCE_DOCUMENTS: bool
    VECTOR_COUNT: int
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    DATA_PATH: str
    DB_PATH: str
    MODEL_TYPE: str
    LLM_MODEL_BIN_PATH: str
    CHAT_EMBED_MODEL: str
    INSTRUCT_EMBED_MODEL: str
    MAX_NEW_TOKENS: int
    TEMPERATURE: float
    GGML_GPU_LAYERS: int
    LANGSMITH_LOGGING: bool
    LOG_LEVEL: str

    @classmethod
    def from_yaml(cls, filepath):
        with open(filepath, "r", encoding="utf8") as ymlfile:
            try:
                data = yaml.safe_load(ymlfile)
            except yaml.YAMLError as exc:
                logger.error(f"Error loading config file: {exc}")
                raise exc
            return cls(**data)


def config_langchain():
    if not server_config.LANGSMITH_LOGGING:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"


filename = os.getenv("CONFIG_FILE", "config/config.yaml").lower()
server_config = Config.from_yaml(filename)
config_langchain()
