from dataclasses import dataclass
from enum import StrEnum


class ModelPlatforms(StrEnum):
    cloud = "public_cloud"
    network = "private_network"
    local = "local"


class LLMModelKind(StrEnum):
    chat = "chat"
    instruct = "instruct"
    image = "image"
    multimodal = "multimodal"
    audio = "audio"


@dataclass
class LLMGenerationConfig:
    model: str
    platform: ModelPlatforms
    max_new_tokens: int
    temperature: float = 0.0


@dataclass
class LLMModel:
    model_name: str
    kind: LLMModelKind
    platform: ModelPlatforms
    default_config: LLMGenerationConfig
